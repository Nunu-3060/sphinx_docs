"""「レイトレーシング」の章のレイトレーサーと、その章の図を作るスクリプト。

全ての画素のレイを NumPy の配列にまとめ、交差判定と照明の計算を一度に
行う。レイの始点と向きは (レイの数, 3) の配列で表す。

次の図を作る。

* raytrace.png: 影と反射を順に加えたレイトレーシングの結果
* pathtrace.png: 1 画素あたりのサンプル数を変えたパストレーシングの結果
"""

from dataclasses import dataclass, field

import numpy as np

from cg_utils import (BoolArray, FloatArray, hstack, linear_to_srgb,
                      normalize, output_dir, save_image, srgb_to_linear)
from shading import blinn_phong, dot, lambert

# 交点からレイを飛ばすとき、その面自身と再び交差しないようにずらす距離。
EPSILON = 1e-4


# ---------------------------------------------------------------------------
# 物体
# ---------------------------------------------------------------------------

@dataclass
class Surface:
    """物体の表面の性質。色は sRGB の値で指定する。"""

    color: tuple[float, float, float]
    reflectivity: float = 0.0   # 鏡面反射で映り込む割合
    checker: bool = False       # True なら市松模様にする


@dataclass
class Sphere:
    """球。"""

    center: FloatArray
    radius: float
    surface: Surface

    def intersect(self, origins: FloatArray, dirs: FloatArray) -> FloatArray:
        """各レイが球と最初に交わる距離 t を返す。交わらなければ無限大。

        レイ上の点 o + t d を球の式 |p - c|^2 = r^2 に代入した、t の 2 次
        方程式を解く。d は長さ 1 なので、t^2 の係数は 1 になる。
        """
        oc = origins - self.center
        b = np.sum(oc * dirs, axis=-1)
        c = np.sum(oc * oc, axis=-1) - self.radius ** 2
        disc = b * b - c
        sqrt_disc = np.sqrt(np.maximum(disc, 0.0))
        t_near = -b - sqrt_disc
        t_far = -b + sqrt_disc
        t = np.where(t_near > EPSILON, t_near, t_far)
        return np.where((disc >= 0.0) & (t > EPSILON), t, np.inf)

    def normal_at(self, points: FloatArray) -> FloatArray:
        """球の表面の点 points での法線を返す。"""
        return normalize(points - self.center)


@dataclass
class Plane:
    """点 point を通り、法線が normal の無限に広い平面。"""

    point: FloatArray
    normal: FloatArray
    surface: Surface

    def intersect(self, origins: FloatArray, dirs: FloatArray) -> FloatArray:
        """各レイが平面と交わる距離 t を返す。交わらなければ無限大。"""
        denom = dirs @ self.normal
        with np.errstate(divide="ignore", invalid="ignore"):
            t = ((self.point - origins) @ self.normal) / denom
        return np.where((np.abs(denom) > 1e-9) & (t > EPSILON), t, np.inf)

    def normal_at(self, points: FloatArray) -> FloatArray:
        """平面の法線を、点の数だけ並べて返す。"""
        return np.asarray(np.broadcast_to(self.normal, points.shape))


@dataclass
class Triangle:
    """三角形。頂点は外側から見て反時計回りに並べる。"""

    v0: FloatArray
    v1: FloatArray
    v2: FloatArray
    surface: Surface
    normal: FloatArray = field(init=False)

    def __post_init__(self) -> None:
        self.normal = normalize(np.cross(self.v1 - self.v0,
                                         self.v2 - self.v0))

    def intersect(self, origins: FloatArray, dirs: FloatArray) -> FloatArray:
        """メラー-トランボアの方法で、三角形と交わる距離 t を返す。

        交点を o + t d = v0 + u (v1 - v0) + v (v2 - v0) と表し、t、u、v の
        連立 1 次方程式をクラメルの公式で解く。u >= 0、v >= 0、u + v <= 1
        なら交点は三角形の内側にある。
        """
        e1 = self.v1 - self.v0
        e2 = self.v2 - self.v0
        p = np.cross(dirs, e2)
        det = p @ e1
        with np.errstate(divide="ignore", invalid="ignore"):
            inv_det = 1.0 / det
            s = origins - self.v0
            u = np.sum(s * p, axis=-1) * inv_det
            q = np.cross(s, e1)
            v = np.sum(dirs * q, axis=-1) * inv_det
            t = (q @ e2) * inv_det
        hit = ((np.abs(det) > 1e-9) & (u >= 0.0) & (v >= 0.0)
               & (u + v <= 1.0) & (t > EPSILON))
        return np.where(hit, t, np.inf)

    def normal_at(self, points: FloatArray) -> FloatArray:
        """三角形の法線を、点の数だけ並べて返す。"""
        return np.asarray(np.broadcast_to(self.normal, points.shape))


Shape = Sphere | Plane | Triangle


def base_color(shape: Shape, points: FloatArray) -> FloatArray:
    """物体の表面の色(線形な値)を、点の数だけ並べて返す。"""
    color = srgb_to_linear(np.array(shape.surface.color))
    colors = np.broadcast_to(color, points.shape).copy()
    if shape.surface.checker:
        cell = np.floor(points[:, 0]) + np.floor(points[:, 2])
        colors[cell % 2 == 1] *= 0.3
    return colors


# ---------------------------------------------------------------------------
# レイの生成と交差判定
# ---------------------------------------------------------------------------

def camera_rays(width: int, height: int, eye: FloatArray,
                target: FloatArray, fovy_degrees: float,
                jitter: FloatArray | None = None
                ) -> tuple[FloatArray, FloatArray]:
    """カメラから各画素の中心を通るレイの始点と向きを作る。

    jitter に (高さ × 幅, 2) の 0 から 1 の値を渡すと、画素の中心ではなく
    画素の中のその位置を通るレイを作る。
    """
    forward = normalize(target - eye)
    right = normalize(np.cross(forward, np.array([0.0, 1.0, 0.0])))
    up = np.cross(right, forward)
    half_h = np.tan(np.radians(fovy_degrees) / 2.0)
    half_w = half_h * width / height

    ys, xs = np.mgrid[0:height, 0:width]
    offset = np.full((height * width, 2), 0.5) if jitter is None else jitter
    px = xs.ravel() + offset[:, 0]
    py = ys.ravel() + offset[:, 1]
    # 画素の座標を、カメラの前方 1 の距離にあるスクリーン上の座標に変換する。
    sx = (2.0 * px / width - 1.0) * half_w
    sy = (1.0 - 2.0 * py / height) * half_h
    dirs = normalize(forward + sx[:, None] * right + sy[:, None] * up)
    origins = np.broadcast_to(eye, dirs.shape).copy()
    return origins, dirs


def closest_hit(scene: list[Shape], origins: FloatArray,
                dirs: FloatArray) -> tuple[FloatArray, FloatArray]:
    """各レイが最初に当たる物体の番号と距離を返す。

    どの物体にも当たらないレイは、番号が -1、距離が無限大になる。
    """
    distances = np.stack([shape.intersect(origins, dirs) for shape in scene])
    index = np.argmin(distances, axis=0)
    t = distances[index, np.arange(len(dirs))]
    return np.where(np.isfinite(t), index, -1), t


def in_shadow(scene: list[Shape], points: FloatArray,
              light_dir: FloatArray) -> BoolArray:
    """各点から光源の方向へ飛ばしたレイが、物体にさえぎられるかを返す。"""
    dirs = np.broadcast_to(light_dir, points.shape)
    _, t = closest_hit(scene, points, dirs)
    return np.asarray(np.isfinite(t))


def reflect(d: FloatArray, n: FloatArray) -> FloatArray:
    """向き d を、法線 n の面で鏡のように反射させた向きを返す。"""
    return np.asarray(d - 2.0 * dot(d, n) * n)


# ---------------------------------------------------------------------------
# レイトレーシング
# ---------------------------------------------------------------------------

LIGHT_DIR: FloatArray = normalize(np.array([-0.5, 1.0, 0.6]))


def sky(dirs: FloatArray) -> FloatArray:
    """レイがどの物体にも当たらなかったときの色(空の色、線形な値)。"""
    t = np.clip(dirs[:, 1], 0.0, 1.0)[:, None]
    return np.asarray((1 - t) * np.array([0.75, 0.85, 1.0])
                      + t * np.array([0.3, 0.5, 0.9]))


def trace(scene: list[Shape], origins: FloatArray, dirs: FloatArray,
          depth: int, shadows: bool) -> FloatArray:
    """レイの色(線形な値)を求める。

    鏡面反射する物体に当たったレイは、depth が 0 になるまで反射の向きに
    レイを飛ばし直し、その色を混ぜる(再帰的なレイトレーシング)。
    """
    color = sky(dirs)
    index, t = closest_hit(scene, origins, dirs)
    for k, shape in enumerate(scene):
        hit = index == k
        if not hit.any():
            continue
        o, d = origins[hit], dirs[hit]
        points = o + t[hit, None] * d
        normals = shape.normal_at(points)
        albedo = base_color(shape, points)

        # 影: 光源の方向がさえぎられていれば、直接光を当てない。
        light = np.ones((len(points), 1))
        if shadows:
            light[in_shadow(scene, points, LIGHT_DIR)] = 0.0
        diffuse = lambert(normals, LIGHT_DIR)
        specular = blinn_phong(normals, LIGHT_DIR, -d, 64.0)
        local = (albedo * (0.12 + 0.88 * diffuse * light)
                 + 0.4 * specular * light)

        r = shape.surface.reflectivity
        if r > 0.0 and depth > 0:
            reflected = trace(scene, points, reflect(d, normals),
                              depth - 1, shadows)
            local = (1.0 - r) * local + r * reflected
        color[hit] = local
    return color


def demo_scene() -> list[Shape]:
    """市松模様の床、3 つの球、三角形でできた四角錐を並べた場面。"""
    scene: list[Shape] = [
        Plane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]),
              Surface((0.9, 0.9, 0.9), reflectivity=0.15, checker=True)),
        Sphere(np.array([0.0, 1.0, 0.0]), 1.0,
               Surface((0.85, 0.85, 0.85), reflectivity=0.7)),
        Sphere(np.array([-2.1, 0.7, 0.6]), 0.7, Surface((0.85, 0.25, 0.2))),
        Sphere(np.array([1.9, 0.6, 1.0]), 0.6, Surface((0.25, 0.45, 0.85))),
    ]
    # 四角錐の側面の 4 枚の三角形(底面は床に接するので省く)。
    apex = np.array([2.2, 1.6, -1.6])
    base = [np.array([2.2 + x, 0.0, -1.6 + z])
            for x, z in ((-0.8, 0.8), (0.8, 0.8), (0.8, -0.8), (-0.8, -0.8))]
    for i in range(4):
        scene.append(Triangle(base[i], base[(i + 1) % 4], apex,
                              Surface((0.3, 0.7, 0.35))))
    return scene


def raytrace_figure() -> FloatArray:
    """影も反射もないもの、影を加えたもの、反射も加えたものを並べる。"""
    width, height = 320, 240
    scene = demo_scene()
    origins, dirs = camera_rays(width, height, np.array([0.0, 2.2, 6.5]),
                                np.array([0.0, 0.8, 0.0]), 40.0)
    panels = []
    for depth, shadows in ((0, False), (0, True), (3, True)):
        color = trace(scene, origins, dirs, depth, shadows)
        panels.append(linear_to_srgb(color.reshape(height, width, 3)))
    return hstack(panels)


# ---------------------------------------------------------------------------
# パストレーシング
# ---------------------------------------------------------------------------

def cosine_sample(normals: FloatArray, rng: np.random.Generator) -> FloatArray:
    """法線のまわりの半球から、cos に比例する確率で向きを選ぶ。

    単位円板上に一様に点を取り、半球に持ち上げる方法を使う。
    """
    n = len(normals)
    r = np.sqrt(rng.random(n))
    phi = 2.0 * np.pi * rng.random(n)
    x, y = r * np.cos(phi), r * np.sin(phi)
    z = np.sqrt(np.maximum(0.0, 1.0 - x * x - y * y))
    # 法線を z 軸とする正規直交基底を作り、(x, y, z) を変換する。
    helper = np.where(np.abs(normals[:, :1]) > 0.9,
                      np.array([0.0, 1.0, 0.0]), np.array([1.0, 0.0, 0.0]))
    tangent = normalize(np.cross(helper, normals))
    bitangent = np.cross(normals, tangent)
    return np.asarray(x[:, None] * tangent + y[:, None] * bitangent
                      + z[:, None] * normals)


def dome(dirs: FloatArray) -> FloatArray:
    """パストレーシングで光源として使う、空の明るさ(線形な値)。

    真上ほど明るく、地平線に近いほど暗い。
    """
    t = np.clip(dirs[:, 1], 0.0, 1.0)[:, None]
    return np.asarray(0.3 + 0.9 * t * np.array([0.95, 0.97, 1.0]))


def path_trace(scene: list[Shape], origins: FloatArray, dirs: FloatArray,
               rng: np.random.Generator, bounces: int = 4) -> FloatArray:
    """拡散反射する物体だけの場面で、空を光源としてレイの色を推定する。

    物体に当たるたびに、反射する向きを乱数で 1 つ選んでレイを続ける。
    cos に比例する確率で向きを選ぶと、ランバート反射では「これまでの
    反射率の積(throughput)」を掛けていくだけで済む。
    """
    color = np.zeros_like(dirs)
    throughput = np.ones_like(dirs)
    alive = np.arange(len(dirs))
    for _ in range(bounces + 1):
        index, t = closest_hit(scene, origins, dirs)
        missed = index < 0
        # 空に抜けたレイは、空の明るさを持ち帰って終わる。
        color[alive[missed]] = throughput[missed] * dome(dirs[missed])
        keep = ~missed
        alive, index, t = alive[keep], index[keep], t[keep]
        origins, dirs = origins[keep], dirs[keep]
        throughput = throughput[keep]
        if len(alive) == 0:
            break
        points = origins + t[:, None] * dirs
        normals = np.zeros_like(points)
        albedo = np.zeros_like(points)
        for k, shape in enumerate(scene):
            hit = index == k
            if hit.any():
                normals[hit] = shape.normal_at(points[hit])
                albedo[hit] = base_color(shape, points[hit])
        # 裏側から当たった場合は、法線を反転して表側として扱う。
        normals = np.where(dot(normals, dirs) > 0.0, -normals, normals)
        throughput = throughput * albedo
        origins = points
        dirs = cosine_sample(normals, rng)
    return color


def diffuse_scene() -> list[Shape]:
    """パストレーシング用の、拡散反射だけの物体を並べた場面。"""
    return [
        Plane(np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]),
              Surface((0.8, 0.8, 0.8))),
        Sphere(np.array([-0.55, 0.5, 0.0]), 0.5, Surface((0.9, 0.2, 0.15))),
        Sphere(np.array([0.55, 0.5, -0.2]), 0.5, Surface((0.85, 0.85, 0.85))),
    ]


def pathtrace_figure() -> FloatArray:
    """1 画素あたり 1、16、128 本のレイで推定した画像を並べる。"""
    width, height = 240, 180
    scene = diffuse_scene()
    eye = np.array([0.0, 1.5, 3.0])
    target = np.array([0.0, 0.35, 0.0])
    rng = np.random.default_rng(1)
    panels = []
    for samples in (1, 16, 128):
        total = np.zeros((width * height, 3))
        for _ in range(samples):
            jitter = rng.random((width * height, 2))
            origins, dirs = camera_rays(width, height, eye, target, 40.0,
                                        jitter)
            total += path_trace(scene, origins, dirs, rng)
        image = (total / samples).reshape(height, width, 3)
        panels.append(linear_to_srgb(image))
    return hstack(panels)


def main() -> None:
    out = output_dir()
    save_image(raytrace_figure(), out / "raytrace.png")
    save_image(pathtrace_figure(), out / "pathtrace.png")


if __name__ == "__main__":
    main()
