"""符号付き距離関数 (SDF: Signed Distance Function) による形状表現。

各図形を「その点から図形の境界までの符号付き距離」を返す関数として
定義する。内側では負、外側では正、境界でちょうど0になるようにする
のが約束事で、この符号だけで内外判定ができる。複数の図形は距離値
どうしの min/max といった単純な演算で合成でき、距離場そのものを
可視化すれば、境界のアンチエイリアスや等高線表現も自然に扱える。
"""

import numpy as np
from PIL import Image


def sdf_circle(
    x: np.ndarray, y: np.ndarray, cx: float, cy: float, radius: float
) -> np.ndarray:
    """中心 (cx, cy)、半径 radius の円までの符号付き距離。"""
    return np.hypot(x - cx, y - cy) - radius


def sdf_box(
    x: np.ndarray,
    y: np.ndarray,
    cx: float,
    cy: float,
    half_width: float,
    half_height: float,
) -> np.ndarray:
    """中心 (cx, cy)、半径 (half_width, half_height) の矩形までの距離。"""
    qx: np.ndarray = np.abs(x - cx) - half_width
    qy: np.ndarray = np.abs(y - cy) - half_height
    outside: np.ndarray = np.hypot(np.maximum(qx, 0.0), np.maximum(qy, 0.0))
    inside: np.ndarray = np.minimum(np.maximum(qx, qy), 0.0)
    return outside + inside


def sdf_segment(
    x: np.ndarray,
    y: np.ndarray,
    ax: float,
    ay: float,
    bx: float,
    by: float,
    thickness: float = 0.0,
) -> np.ndarray:
    """端点 (ax, ay)-(bx, by) を結ぶ線分(太さ thickness)までの距離。"""
    pax: np.ndarray = x - ax
    pay: np.ndarray = y - ay
    bax: float = bx - ax
    bay: float = by - ay
    h: np.ndarray = np.clip(
        (pax * bax + pay * bay) / (bax * bax + bay * bay), 0.0, 1.0
    )
    dx: np.ndarray = pax - h * bax
    dy: np.ndarray = pay - h * bay
    return np.hypot(dx, dy) - thickness


def union(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    """2つの図形の和集合(どちらかの内側なら内側)。"""
    return np.minimum(d1, d2)


def intersection(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    """2つの図形の積集合(両方の内側なら内側)。"""
    return np.maximum(d1, d2)


def subtraction(d1: np.ndarray, d2: np.ndarray) -> np.ndarray:
    """d1 から d2 の領域を取り除いた差集合。"""
    return np.maximum(d1, -d2)


def smooth_union(d1: np.ndarray, d2: np.ndarray, k: float) -> np.ndarray:
    """継ぎ目を滑らかに繋いだ和集合(k は滑らかさの半径)。"""
    h: np.ndarray = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0)
    return d2 * (1.0 - h) + d1 * h - k * h * (1.0 - h)


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    """``x`` が ``edge0`` から ``edge1`` へ進むにつれ、0から1へなめらかに変化する値。"""
    t: np.ndarray = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def render_fill(
    d: np.ndarray,
    inside_color: tuple[int, int, int] = (240, 90, 60),
    outside_color: tuple[int, int, int] = (255, 255, 255),
    aa_width: float = 1.5,
) -> Image.Image:
    """符号付き距離を、境界をアンチエイリアスした塗りつぶし画像にする。

    ``aa_width`` 幅の帯を d=0 の周りに取り、その中だけ内側色と外側色を
    smoothstep で滑らかに混ぜることで、超解像なしでも滑らかな境界に
    なる。
    """
    t: np.ndarray = _smoothstep(aa_width / 2, -aa_width / 2, d)
    inside: np.ndarray = np.array(inside_color, dtype=float)
    outside: np.ndarray = np.array(outside_color, dtype=float)
    pixels: np.ndarray = outside + (inside - outside) * t[..., np.newaxis]
    return Image.fromarray(pixels.round().astype(np.uint8))


def render_isolines(
    d: np.ndarray, spacing: float = 12.0, line_width: float = 1.2
) -> Image.Image:
    """距離場を等高線状の縞模様として可視化する。

    内側・外側で背景の濃淡を変え、距離が ``spacing`` の倍数になる
    位置に線を引くことで、図形の境界からの距離を視覚化する。
    """
    background: np.ndarray = np.where(d < 0.0, 210.0, 245.0)
    distance_to_line: np.ndarray = np.abs(
        np.mod(d + spacing / 2.0, spacing) - spacing / 2.0
    )
    line_strength: np.ndarray = _smoothstep(
        line_width, 0.0, distance_to_line
    )
    gray: np.ndarray = background * (1.0 - line_strength)
    rgb: np.ndarray = np.stack([gray, gray, gray], axis=-1)
    return Image.fromarray(rgb.round().astype(np.uint8))


def main() -> None:
    from perlin_noise import fbm2d, make_permutation

    width: int = 480
    height: int = 480
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )

    circle: np.ndarray = sdf_circle(xs, ys, 190.0, 240.0, 110.0)
    box: np.ndarray = sdf_box(xs, ys, 300.0, 240.0, 90.0, 90.0)

    sharp: np.ndarray = union(circle, box)
    smooth: np.ndarray = smooth_union(circle, box, k=40.0)

    render_fill(sharp).save("sdf_boolean_sharp.png")
    render_fill(smooth).save("sdf_boolean_smooth.png")
    render_isolines(smooth).save("sdf_isolines.png")

    perm: np.ndarray = make_permutation(seed=3)
    scale: float = 0.01
    warp_strength: float = 40.0
    warp_x: np.ndarray = xs + warp_strength * fbm2d(
        xs * scale, ys * scale, perm, octaves=4
    )
    # x方向と同じ座標のまま perm を再利用すると2軸の歪みが強く相関
    # してしまうため、適当に離れた座標オフセット (5.2, 1.3) を加えて
    # 評価し、実質的に無相関な別のノイズ場として扱う
    # (noise章の domain_warp2d と同じ考え方)。
    warp_y: np.ndarray = ys + warp_strength * fbm2d(
        xs * scale + 5.2, ys * scale + 1.3, perm, octaves=4
    )
    organic: np.ndarray = sdf_circle(warp_x, warp_y, 240.0, 240.0, 150.0)
    render_fill(organic, inside_color=(60, 140, 210)).save(
        "sdf_organic_blob.png"
    )


if __name__ == "__main__":
    main()
