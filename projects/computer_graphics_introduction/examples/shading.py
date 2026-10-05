"""「ライティングとシェーディング」の章の照明の計算と、その章の図を作る。

照明の計算は、光の強さに比例する線形な値で行う。関数は全て NumPy の
配列をまとめて受け取り、画素ごと(または頂点ごと)の結果を返す。
raytracer.py からも使う。

次の図を作る。

* shading_terms.png: 環境光、拡散反射、鏡面反射の成分と、その合計
* shading_models.png: フラット、グーロー、フォンの各シェーディング
* shininess.png: 光沢度による鏡面反射のハイライトの違い
"""

from dataclasses import dataclass

import numpy as np

from cg_utils import (FloatArray, hstack, linear_to_srgb, normalize,
                      output_dir, save_image, srgb_to_linear)
from renderer import (FrameBuffer, Mesh, draw_mesh, flatten, make_sphere,
                      transform_normals, transform_positions)
from transform import look_at, perspective

# ---------------------------------------------------------------------------
# 照明モデル
# ---------------------------------------------------------------------------


@dataclass
class Material:
    """物体の表面の性質。色は sRGB の値で指定する。"""

    color: tuple[float, float, float]
    ambient: float = 0.08     # 環境光の強さ
    specular: float = 0.5     # 鏡面反射の強さ
    shininess: float = 32.0   # 光沢度(大きいほどハイライトが小さく鋭い)


def dot(a: FloatArray, b: FloatArray) -> FloatArray:
    """末尾の軸をベクトルとみなした内積。"""
    return np.asarray(np.sum(a * b, axis=-1, keepdims=True))


def lambert(normal: FloatArray, light_dir: FloatArray) -> FloatArray:
    """ランバートの拡散反射の係数 max(N・L, 0) を返す。

    normal と light_dir(表面から光源へ向かう向き)は長さ 1 とする。
    """
    return np.maximum(dot(normal, light_dir), 0.0)


def blinn_phong(normal: FloatArray, light_dir: FloatArray,
                view_dir: FloatArray, shininess: float) -> FloatArray:
    """ブリン-フォンの鏡面反射の係数 max(N・H, 0) ** shininess を返す。

    view_dir は表面から視点へ向かう長さ 1 のベクトル、H は light_dir と
    view_dir の中間の向き(ハーフベクトル)である。光が裏から当たる場合は
    0 とする。
    """
    half = normalize(light_dir + view_dir)
    facing = dot(normal, light_dir) > 0.0
    return np.where(facing, np.maximum(dot(normal, half), 0.0) ** shininess,
                    0.0)


def shade(position: FloatArray, normal: FloatArray, eye: FloatArray,
          light_dir: FloatArray, material: Material,
          terms: tuple[str, ...] = ("ambient", "diffuse", "specular")
          ) -> FloatArray:
    """平行光源で照らした表面の色(線形な値)を求める。

    terms で、合計に含める成分を選べる。光源の色は白とする。
    """
    base = srgb_to_linear(np.array(material.color))
    n = normalize(normal)
    v = normalize(eye - position)
    color = np.zeros(position.shape[:-1] + (3,))
    if "ambient" in terms:
        color = color + material.ambient * base
    if "diffuse" in terms:
        color = color + lambert(n, light_dir) * base
    if "specular" in terms:
        color = color + material.specular * blinn_phong(
            n, light_dir, v, material.shininess)
    return color


# ---------------------------------------------------------------------------
# 球を描く
# ---------------------------------------------------------------------------

SIZE = 200
EYE: FloatArray = np.array([0.0, 0.0, 3.6])
LIGHT_DIR: FloatArray = normalize(np.array([-0.6, 0.7, 0.8]))
BACKGROUND: FloatArray = np.array([1.0, 1.0, 1.0])


def view_projection() -> FloatArray:
    """全ての図で共通のビュー変換と投影の行列を掛け合わせたもの。"""
    view = look_at(EYE, np.zeros(3), np.array([0.0, 1.0, 0.0]))
    return perspective(40.0, 1.0, 0.5, 10.0) @ view


def render_phong(mesh: Mesh, material: Material,
                 terms: tuple[str, ...] = ("ambient", "diffuse", "specular")
                 ) -> FloatArray:
    """位置と法線を画素ごとに補間し、画素ごとに照明を計算して描く。

    フラットシェーディングもこの関数で描く(flatten() で法線を面ごとに
    そろえたメッシュを渡す)。
    """
    model = np.eye(4)
    fb = FrameBuffer(SIZE, SIZE, {"position": 3, "normal": 3})
    draw_mesh(fb, view_projection() @ model, mesh, {
        "position": transform_positions(model, mesh.positions),
        "normal": transform_normals(model, mesh.normals),
    })
    color = shade(fb.attributes["position"], fb.attributes["normal"], EYE,
                  LIGHT_DIR, material, terms)
    image = linear_to_srgb(color)
    return np.where(fb.covered[..., None], image, BACKGROUND)


def render_gouraud(mesh: Mesh, material: Material) -> FloatArray:
    """頂点ごとに照明を計算し、その色を画素ごとに補間して描く。"""
    model = np.eye(4)
    positions = transform_positions(model, mesh.positions)
    normals = transform_normals(model, mesh.normals)
    vertex_colors = shade(positions, normals, EYE, LIGHT_DIR, material)
    fb = FrameBuffer(SIZE, SIZE, {"color": 3})
    draw_mesh(fb, view_projection() @ model, mesh, {"color": vertex_colors})
    image = linear_to_srgb(fb.attributes["color"])
    return np.where(fb.covered[..., None], image, BACKGROUND)


# ---------------------------------------------------------------------------
# 図の作成
# ---------------------------------------------------------------------------

BLUE = Material(color=(0.25, 0.45, 0.8))


def terms_figure() -> FloatArray:
    """環境光、拡散反射、鏡面反射の成分と、その合計を並べる。"""
    sphere = make_sphere()
    panels = [render_phong(sphere, BLUE, (term,))
              for term in ("ambient", "diffuse", "specular")]
    panels.append(render_phong(sphere, BLUE))
    return hstack(panels)


def models_figure() -> FloatArray:
    """頂点の少ない球を、フラット、グーロー、フォンの各方法で描く。"""
    sphere = make_sphere(16, 8)
    material = Material(color=(0.25, 0.45, 0.8), shininess=24.0)
    return hstack([
        render_phong(flatten(sphere), material),
        render_gouraud(sphere, material),
        render_phong(sphere, material),
    ])


def shininess_figure() -> FloatArray:
    """光沢度を 8、32、128 に変えた球を並べる。"""
    sphere = make_sphere()
    panels = []
    for shininess in (8.0, 32.0, 128.0):
        material = Material(color=(0.8, 0.3, 0.25), shininess=shininess)
        panels.append(render_phong(sphere, material))
    return hstack(panels)


def main() -> None:
    out = output_dir()
    save_image(terms_figure(), out / "shading_terms.png")
    save_image(models_figure(), out / "shading_models.png")
    save_image(shininess_figure(), out / "shininess.png")


if __name__ == "__main__":
    main()
