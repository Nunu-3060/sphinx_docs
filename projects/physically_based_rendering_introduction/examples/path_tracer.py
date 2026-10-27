"""NumPy だけで書いた教育用のミニパストレーサー。

コーネルボックス風のシーン（赤と緑の壁、白い球、金の球、天井の面光源）を描画し、
PNG 画像として保存する。速度よりも読みやすさを優先しているが、
全画素のレイを NumPy 配列でまとめて処理することで、Python のループを最小限にしている。

実装している主な要素は次のとおり。

* ピンホールカメラによるレイの生成
* レイと球・長方形の交差判定
* ランバート BRDF（拡散反射）と GGX マイクロファセット BRDF（金属）
* BRDF に基づく重点サンプリング
* 次イベント推定（光源サンプリング）と多重重点サンプリング
* ロシアンルーレットによるパスの打ち切り

実行例::

    python path_tracer.py --width 256 --height 256 --spp 64 --output cornell_box.png
"""

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
from PIL import Image

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.intp]
BoolArray = npt.NDArray[np.bool_]
Vec3 = tuple[float, float, float]

# 交差位置から次のレイを出すときに、同じ面と再び交差しないようにずらす量
EPSILON = 1e-4


# ---------------------------------------------------------------------------
# シーンの定義
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Material:
    """表面の材質。

    albedo は拡散反射面では反射率、金属では垂直入射時のフレネル反射率 F0 として使う。
    roughness は金属のみで使う知覚的ラフネスで、GGX の α は roughness の 2 乗とする。
    """

    albedo: Vec3 = (0.8, 0.8, 0.8)
    emission: Vec3 = (0.0, 0.0, 0.0)
    metal: bool = False
    roughness: float = 0.5


@dataclass(frozen=True)
class Sphere:
    """球。"""

    center: Vec3
    radius: float
    material: Material


@dataclass(frozen=True)
class Rectangle:
    """corner を 1 つの頂点とし、互いに直交する 2 辺 edge_u, edge_v で張られる長方形。

    表側の法線は cross(edge_u, edge_v) の向きとする。
    光源として使う場合は表側だけが光を放つ。
    """

    corner: Vec3
    edge_u: Vec3
    edge_v: Vec3
    material: Material


Shape = Sphere | Rectangle


@dataclass(frozen=True)
class Camera:
    """ピンホールカメラ。fov_degrees は縦方向の画角。"""

    position: Vec3
    look_at: Vec3
    up: Vec3 = (0.0, 1.0, 0.0)
    fov_degrees: float = 40.0


@dataclass(frozen=True)
class Scene:
    """描画するシーン。shapes[light_index] は光源となる長方形でなければならない。"""

    shapes: tuple[Shape, ...]
    light_index: int
    camera: Camera


@dataclass(frozen=True)
class MaterialTable:
    """材質を物体番号で引けるように配列にまとめたもの。"""

    albedo: FloatArray      # (物体数, 3)
    emission: FloatArray    # (物体数, 3)
    metal: BoolArray        # (物体数,)
    roughness: FloatArray   # (物体数,)


def cornell_box_scene() -> Scene:
    """1 × 1 × 1 の箱の中に球を 2 つ置いたシーンを作る。手前（z = 1）は開いている。"""
    white = Material(albedo=(0.725, 0.71, 0.68))
    red = Material(albedo=(0.63, 0.065, 0.05))
    green = Material(albedo=(0.14, 0.45, 0.091))
    gold = Material(albedo=(1.0, 0.782, 0.344), metal=True, roughness=0.3)
    light = Material(albedo=(0.0, 0.0, 0.0), emission=(10.0, 10.0, 10.0))

    shapes: tuple[Shape, ...] = (
        Rectangle((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), white),   # 床
        Rectangle((0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), white),   # 天井
        Rectangle((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), white),   # 奥の壁
        Rectangle((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), red),     # 左の壁
        Rectangle((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), green),   # 右の壁
        Rectangle((0.35, 0.999, 0.35), (0.3, 0.0, 0.0), (0.0, 0.0, 0.3), light),  # 光源（下向き）
        Sphere((0.3, 0.2, 0.4), 0.2, white),
        Sphere((0.72, 0.18, 0.62), 0.18, gold),
    )
    camera = Camera(position=(0.5, 0.5, 2.2), look_at=(0.5, 0.5, 0.0))
    return Scene(shapes=shapes, light_index=5, camera=camera)


def build_material_table(scene: Scene) -> MaterialTable:
    """シーン中の材質を配列にまとめる。"""
    materials = [shape.material for shape in scene.shapes]
    return MaterialTable(
        albedo=np.array([m.albedo for m in materials], dtype=np.float64),
        emission=np.array([m.emission for m in materials], dtype=np.float64),
        metal=np.array([m.metal for m in materials], dtype=np.bool_),
        roughness=np.array([m.roughness for m in materials], dtype=np.float64),
    )


# ---------------------------------------------------------------------------
# ベクトル演算の補助関数（いずれも (N, 3) の配列を行ごとに処理する）
# ---------------------------------------------------------------------------

def dot(a: FloatArray, b: FloatArray) -> FloatArray:
    """行ごとの内積を返す。"""
    result: FloatArray = np.einsum("ij,ij->i", a, b)
    return result


def normalize(v: FloatArray) -> FloatArray:
    """行ごとに長さ 1 に正規化する。"""
    result: FloatArray = v / np.linalg.norm(v, axis=-1, keepdims=True)
    return result


def orthonormal_basis(normals: FloatArray) -> tuple[FloatArray, FloatArray]:
    """法線から、法線と直交する 2 本の単位ベクトル（接線と従接線）を作る。

    Duff らの方法（"Building an Orthonormal Basis, Revisited", 2017）による。
    """
    nx, ny, nz = normals[:, 0], normals[:, 1], normals[:, 2]
    sign = np.where(nz >= 0.0, 1.0, -1.0)
    a = -1.0 / (sign + nz)
    b = nx * ny * a
    tangent = np.stack([1.0 + sign * nx * nx * a, sign * b, -sign * nx], axis=1)
    bitangent = np.stack([b, sign + ny * ny * a, -ny], axis=1)
    return tangent, bitangent


def to_world(local: FloatArray, normals: FloatArray) -> FloatArray:
    """法線を z 軸とする局所座標系のベクトルをワールド座標系に変換する。"""
    tangent, bitangent = orthonormal_basis(normals)
    result: FloatArray = local[:, 0:1] * tangent + local[:, 1:2] * bitangent + local[:, 2:3] * normals
    return result


def rectangle_normal(rect: Rectangle) -> FloatArray:
    """長方形の表側の単位法線を返す。"""
    normal = np.cross(np.array(rect.edge_u), np.array(rect.edge_v))
    result: FloatArray = normal / np.linalg.norm(normal)
    return result


# ---------------------------------------------------------------------------
# 交差判定
# ---------------------------------------------------------------------------

def intersect_sphere(sphere: Sphere, origins: FloatArray, directions: FloatArray) -> FloatArray:
    """各レイが球と最初に交わる距離 t を返す。交わらない場合は inf とする。"""
    oc = origins - np.array(sphere.center)
    b = dot(oc, directions)
    c = dot(oc, oc) - sphere.radius ** 2
    discriminant = b * b - c
    sqrt_d = np.sqrt(np.maximum(discriminant, 0.0))
    t_near = -b - sqrt_d
    t_far = -b + sqrt_d
    t = np.where(t_near > EPSILON, t_near, t_far)
    hit = (discriminant > 0.0) & (t > EPSILON)
    result: FloatArray = np.where(hit, t, np.inf)
    return result


def intersect_rectangle(rect: Rectangle, origins: FloatArray, directions: FloatArray) -> FloatArray:
    """各レイが長方形と交わる距離 t を返す。交わらない場合は inf とする。"""
    corner = np.array(rect.corner)
    edge_u = np.array(rect.edge_u)
    edge_v = np.array(rect.edge_v)
    normal = rectangle_normal(rect)
    with np.errstate(divide="ignore", invalid="ignore"):
        denom = directions @ normal
        t = ((corner - origins) @ normal) / denom
        rel = origins + t[:, None] * directions - corner
        u = rel @ edge_u / (edge_u @ edge_u)
        v = rel @ edge_v / (edge_v @ edge_v)
        hit = (np.abs(denom) > 1e-12) & (t > EPSILON) & (u >= 0.0) & (u <= 1.0) & (v >= 0.0) & (v <= 1.0)
    result: FloatArray = np.where(hit, t, np.inf)
    return result


def intersect_scene(scene: Scene, origins: FloatArray, directions: FloatArray) -> tuple[FloatArray, IntArray]:
    """最も近い交差点までの距離と、交差した物体の番号（交差なしは -1）を返す。"""
    nearest_t = np.full(len(origins), np.inf)
    shape_ids = np.full(len(origins), -1, dtype=np.intp)
    for index, shape in enumerate(scene.shapes):
        if isinstance(shape, Sphere):
            t = intersect_sphere(shape, origins, directions)
        else:
            t = intersect_rectangle(shape, origins, directions)
        closer = t < nearest_t
        nearest_t[closer] = t[closer]
        shape_ids[closer] = index
    return nearest_t, shape_ids


def normals_at(scene: Scene, shape_ids: IntArray, points: FloatArray) -> FloatArray:
    """交差点における物体の幾何法線（表側）を返す。"""
    normals = np.zeros_like(points)
    for index, shape in enumerate(scene.shapes):
        mask = shape_ids == index
        if not np.any(mask):
            continue
        if isinstance(shape, Sphere):
            normals[mask] = (points[mask] - np.array(shape.center)) / shape.radius
        else:
            normals[mask] = rectangle_normal(shape)
    return normals


# ---------------------------------------------------------------------------
# BRDF
# ---------------------------------------------------------------------------

def ggx_distribution(cos_h: FloatArray, alpha: FloatArray) -> FloatArray:
    """GGX（Trowbridge-Reitz）法線分布関数 D。"""
    a2 = alpha * alpha
    denom = cos_h * cos_h * (a2 - 1.0) + 1.0
    result: FloatArray = a2 / (math.pi * denom * denom)
    return result


def smith_g1(cos_v: FloatArray, alpha: FloatArray) -> FloatArray:
    """GGX に対する Smith のマスキング関数 G1。"""
    a2 = alpha * alpha
    result: FloatArray = 2.0 * cos_v / (cos_v + np.sqrt(a2 + (1.0 - a2) * cos_v * cos_v))
    return result


def fresnel_schlick(cos_theta: FloatArray, f0: FloatArray) -> FloatArray:
    """フレネル反射率の Schlick 近似。f0 は (N, 3) の RGB 値。"""
    result: FloatArray = f0 + (1.0 - f0) * ((1.0 - cos_theta) ** 5)[:, None]
    return result


def evaluate_brdf(table: MaterialTable, ids: IntArray, normals: FloatArray,
                  wo: FloatArray, wi: FloatArray) -> FloatArray:
    """BRDF の値 f_r(wi, wo) を RGB で返す。wi は表側を向いていることを前提とする。"""
    albedo = table.albedo[ids]
    result: FloatArray = albedo / math.pi  # ランバート BRDF
    metal = table.metal[ids]
    if np.any(metal):
        n, o, i = normals[metal], wo[metal], wi[metal]
        alpha = np.maximum(table.roughness[ids][metal] ** 2, 1e-3)
        h = normalize(o + i)
        cos_o = np.maximum(dot(n, o), 1e-6)
        cos_i = np.maximum(dot(n, i), 1e-6)
        cos_h = np.clip(dot(n, h), 0.0, 1.0)
        cos_oh = np.clip(dot(o, h), 0.0, 1.0)
        d = ggx_distribution(cos_h, alpha)
        g = smith_g1(cos_o, alpha) * smith_g1(cos_i, alpha)
        f = fresnel_schlick(cos_oh, albedo[metal])
        result[metal] = f * (d * g / (4.0 * cos_o * cos_i))[:, None]
    return result


def brdf_pdf(table: MaterialTable, ids: IntArray, normals: FloatArray,
             wo: FloatArray, wi: FloatArray) -> FloatArray:
    """sample_brdf が方向 wi を選ぶ確率密度（立体角に関する密度）を返す。"""
    cos_i = dot(normals, wi)
    result: FloatArray = np.maximum(cos_i, 0.0) / math.pi  # コサイン重み付きサンプリング
    metal = table.metal[ids]
    if np.any(metal):
        n, o, i = normals[metal], wo[metal], wi[metal]
        alpha = np.maximum(table.roughness[ids][metal] ** 2, 1e-3)
        h = normalize(o + i)
        cos_h = np.clip(dot(n, h), 0.0, 1.0)
        cos_oh = np.maximum(dot(o, h), 1e-6)
        # ハーフベクトルの確率密度 D(h) cosθ_h を、反射方向の確率密度に変換する
        pdf = ggx_distribution(cos_h, alpha) * cos_h / (4.0 * cos_oh)
        result[metal] = np.where(cos_i[metal] > 0.0, pdf, 0.0)
    return result


def sample_cosine_hemisphere(normals: FloatArray, rng: np.random.Generator) -> FloatArray:
    """法線まわりの半球から、確率密度 cosθ / π で方向をサンプリングする。"""
    xi = rng.random((len(normals), 2))
    r = np.sqrt(xi[:, 0])
    phi = 2.0 * math.pi * xi[:, 1]
    local = np.stack([r * np.cos(phi), r * np.sin(phi), np.sqrt(1.0 - xi[:, 0])], axis=1)
    return to_world(local, normals)


def sample_ggx_half_vector(normals: FloatArray, alpha: FloatArray, rng: np.random.Generator) -> FloatArray:
    """確率密度 D(h) cosθ_h でハーフベクトル h をサンプリングする。"""
    xi = rng.random((len(normals), 2))
    cos_theta = np.sqrt((1.0 - xi[:, 0]) / (1.0 + (alpha * alpha - 1.0) * xi[:, 0]))
    sin_theta = np.sqrt(np.maximum(0.0, 1.0 - cos_theta * cos_theta))
    phi = 2.0 * math.pi * xi[:, 1]
    local = np.stack([sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta], axis=1)
    return to_world(local, normals)


def sample_brdf(table: MaterialTable, ids: IntArray, normals: FloatArray, wo: FloatArray,
                rng: np.random.Generator) -> tuple[FloatArray, FloatArray, FloatArray]:
    """次の方向 wi、重み f_r cosθ_i / pdf、確率密度 pdf を返す。無効なサンプルの重みは 0 とする。"""
    albedo = table.albedo[ids]
    metal = table.metal[ids]
    diffuse = ~metal
    wi = np.empty_like(wo)
    weight = np.zeros_like(wo)

    if np.any(diffuse):
        # ランバート BRDF では f_r cosθ / pdf = (ρ / π) cosθ / (cosθ / π) = ρ となる
        wi[diffuse] = sample_cosine_hemisphere(normals[diffuse], rng)
        weight[diffuse] = albedo[diffuse]

    if np.any(metal):
        n, o = normals[metal], wo[metal]
        alpha = np.maximum(table.roughness[ids][metal] ** 2, 1e-3)
        h = sample_ggx_half_vector(n, alpha, rng)
        cos_oh = dot(o, h)
        i = 2.0 * cos_oh[:, None] * h - o  # wo を h に関して反射させる
        cos_o = dot(n, o)
        cos_i = dot(n, i)
        cos_h = dot(n, h)
        valid = (cos_oh > 0.0) & (cos_i > 0.0) & (cos_o > 0.0)
        # f_r cosθ_i / pdf = F G (wo・h) / ((n・wo)(n・h))
        g = smith_g1(np.maximum(cos_o, 1e-6), alpha) * smith_g1(np.maximum(cos_i, 1e-6), alpha)
        f = fresnel_schlick(np.clip(cos_oh, 0.0, 1.0), albedo[metal])
        w = f * (g * cos_oh / (np.maximum(cos_o, 1e-6) * np.maximum(cos_h, 1e-6)))[:, None]
        wi[metal] = i
        weight[metal] = np.where(valid[:, None], w, 0.0)

    return wi, weight, brdf_pdf(table, ids, normals, wo, wi)


# ---------------------------------------------------------------------------
# 光の輸送
# ---------------------------------------------------------------------------

def light_pdf(scene: Scene, dist2: FloatArray, cos_light: FloatArray) -> FloatArray:
    """光源上の点を一様に選んだときの、立体角に関する確率密度 r^2 / (cosθ_l A) を返す。"""
    light = scene.shapes[scene.light_index]
    assert isinstance(light, Rectangle)
    area = float(np.linalg.norm(np.cross(light.edge_u, light.edge_v)))
    result: FloatArray = dist2 / (np.maximum(cos_light, 1e-6) * area)
    return result


def mis_weight(pdf_a: FloatArray, pdf_b: FloatArray) -> FloatArray:
    """多重重点サンプリングのバランスヒューリスティック p_a / (p_a + p_b)。"""
    total = pdf_a + pdf_b
    result: FloatArray = np.where(total > 0.0, pdf_a / np.maximum(total, 1e-300), 0.0)
    return result


def direct_lighting(scene: Scene, table: MaterialTable, ids: IntArray, points: FloatArray,
                    normals: FloatArray, wo: FloatArray, rng: np.random.Generator) -> FloatArray:
    """次イベント推定：光源上の点を 1 つ選び、そこから直接届く光の寄与を求める。

    BRDF のサンプリングで光源に当たる場合の寄与と、多重重点サンプリングで組み合わせる。
    """
    light = scene.shapes[scene.light_index]
    assert isinstance(light, Rectangle)
    corner = np.array(light.corner)
    edge_u = np.array(light.edge_u)
    edge_v = np.array(light.edge_v)
    light_normal = rectangle_normal(light)
    area = float(np.linalg.norm(np.cross(edge_u, edge_v)))

    # 光源上の点を一様に選ぶ（面積に関する確率密度は 1 / area）
    xi = rng.random((len(points), 2))
    light_points = corner + xi[:, 0:1] * edge_u + xi[:, 1:2] * edge_v
    to_light = light_points - points
    dist2 = dot(to_light, to_light)
    wi = to_light / np.sqrt(dist2)[:, None]
    cos_surface = dot(normals, wi)
    cos_light = -(wi @ light_normal)

    # 遮蔽判定（シャドウレイ）：最初に当たる物体が光源なら見えている
    _, hit_ids = intersect_scene(scene, points + normals * EPSILON, wi)
    visible = (cos_surface > 0.0) & (cos_light > 0.0) & (hit_ids == scene.light_index)

    brdf = evaluate_brdf(table, ids, normals, wo, wi)
    emission = table.emission[scene.light_index]
    geometry = np.where(visible, cos_surface * cos_light * area / dist2, 0.0)
    weight = mis_weight(light_pdf(scene, dist2, cos_light), brdf_pdf(table, ids, normals, wo, wi))
    result: FloatArray = brdf * emission * (geometry * weight)[:, None]
    return result


def trace_paths(scene: Scene, table: MaterialTable, origins: FloatArray, directions: FloatArray,
                max_depth: int, use_nee: bool, rng: np.random.Generator) -> FloatArray:
    """各カメラレイについてパスを 1 本ずつ追跡し、運ばれてきた放射輝度を返す。"""
    radiance = np.zeros_like(origins)
    throughput = np.ones_like(origins)       # ここまでのパスの重み（BRDF × cos / pdf の積）
    pixel = np.arange(len(origins))           # 各パスがどの画素に属するか
    previous_pdf = np.zeros(len(origins))     # 直前の反射で方向を選んだときの確率密度

    for depth in range(max_depth):
        t, ids = intersect_scene(scene, origins, directions)
        hit = ids >= 0                        # 何にも当たらなかったパスは終了
        pixel, throughput, origins, directions = pixel[hit], throughput[hit], origins[hit], directions[hit]
        t, ids, previous_pdf = t[hit], ids[hit], previous_pdf[hit]
        if len(pixel) == 0:
            break

        points = origins + t[:, None] * directions
        geometric_normals = normals_at(scene, ids, points)
        front = dot(geometric_normals, directions) < 0.0
        normals = np.where(front[:, None], geometric_normals, -geometric_normals)
        wo = -directions

        # 光源に当たった場合の寄与
        emitted = throughput * table.emission[ids] * front[:, None]
        if depth == 0 or not use_nee:
            radiance[pixel] += emitted
        else:
            # 次イベント推定でも同じ経路を数えているので、多重重点サンプリングの重みを掛けて加える
            pdf_light = light_pdf(scene, t * t, dot(geometric_normals, wo))
            radiance[pixel] += emitted * mis_weight(previous_pdf, pdf_light)[:, None]

        # 光源は光を反射しないものとし、光源に当たったパスはここで終了する
        alive = ids != scene.light_index
        pixel, throughput, ids = pixel[alive], throughput[alive], ids[alive]
        points, normals, wo = points[alive], normals[alive], wo[alive]

        if use_nee:
            radiance[pixel] += throughput * direct_lighting(scene, table, ids, points, normals, wo, rng)

        new_directions, weight, previous_pdf = sample_brdf(table, ids, normals, wo, rng)
        throughput = throughput * weight

        # ロシアンルーレット：重みの小さいパスほど高い確率で打ち切り、生き残ったパスの重みを増やす
        survive = throughput.max(axis=1) > 0.0
        if depth >= 3:
            q = np.clip(throughput.max(axis=1), 0.05, 0.95)
            survive &= rng.random(len(q)) < q
            throughput = throughput / q[:, None]

        pixel, throughput, previous_pdf = pixel[survive], throughput[survive], previous_pdf[survive]
        origins = points[survive] + normals[survive] * EPSILON
        directions = new_directions[survive]

    return radiance


def generate_camera_rays(camera: Camera, width: int, height: int,
                         rng: np.random.Generator) -> tuple[FloatArray, FloatArray]:
    """画素ごとに 1 本ずつカメラレイを生成する。画素内の位置はランダムにずらす。"""
    position = np.array(camera.position)
    forward = np.array(camera.look_at) - position
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, np.array(camera.up))
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)

    rows, cols = np.mgrid[0:height, 0:width]
    rows, cols = rows.ravel(), cols.ravel()
    jitter = rng.random((len(rows), 2))
    tan_half = math.tan(math.radians(camera.fov_degrees) / 2.0)
    x = (2.0 * (cols + jitter[:, 0]) / width - 1.0) * tan_half * width / height
    y = (1.0 - 2.0 * (rows + jitter[:, 1]) / height) * tan_half

    directions = normalize(forward + x[:, None] * right + y[:, None] * up)
    origins = np.tile(position, (len(rows), 1))
    return origins, directions


def render(scene: Scene, width: int, height: int, spp: int, max_depth: int = 8,
           use_nee: bool = True, seed: int = 0) -> FloatArray:
    """シーンを描画し、線形な放射輝度の画像（高さ × 幅 × 3）を返す。"""
    rng = np.random.default_rng(seed)
    table = build_material_table(scene)
    accumulated = np.zeros((width * height, 3))
    for _ in range(spp):
        origins, directions = generate_camera_rays(scene.camera, width, height, rng)
        accumulated += trace_paths(scene, table, origins, directions, max_depth, use_nee, rng)
    result: FloatArray = (accumulated / spp).reshape(height, width, 3)
    return result


# ---------------------------------------------------------------------------
# 画像の保存
# ---------------------------------------------------------------------------

def linear_to_srgb(linear: FloatArray) -> FloatArray:
    """線形な値を sRGB の符号化値に変換する（入力は 0〜1 に切り詰める）。"""
    c = np.clip(linear, 0.0, 1.0)
    result: FloatArray = np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1.0 / 2.4) - 0.055)
    return result


def save_image(linear: FloatArray, path: Path) -> None:
    """線形な放射輝度の画像を sRGB の 8 ビット PNG として保存する。"""
    pixels = np.round(linear_to_srgb(linear) * 255.0).astype(np.uint8)
    Image.fromarray(pixels).save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="NumPy によるミニパストレーサー")
    parser.add_argument("--width", type=int, default=256, help="画像の幅（画素）")
    parser.add_argument("--height", type=int, default=256, help="画像の高さ（画素）")
    parser.add_argument("--spp", type=int, default=64, help="1 画素あたりのサンプル数")
    parser.add_argument("--max-depth", type=int, default=8, help="反射回数の上限")
    parser.add_argument("--no-nee", action="store_true", help="次イベント推定を使わない")
    parser.add_argument("--seed", type=int, default=0, help="乱数の種")
    parser.add_argument("--output", type=Path, default=Path("cornell_box.png"), help="出力ファイル名")
    args = parser.parse_args()

    image = render(cornell_box_scene(), args.width, args.height, args.spp,
                   max_depth=args.max_depth, use_nee=not args.no_nee, seed=args.seed)
    save_image(image, args.output)
    print(f"{args.output} を保存した")


if __name__ == "__main__":
    main()
