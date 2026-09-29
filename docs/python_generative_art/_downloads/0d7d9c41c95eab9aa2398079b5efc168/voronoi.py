"""ボロノイ図とドロネー三角形分割。

複数の「種点」を平面上に散らし、各点を最も近い種点で塗り分けると
**ボロノイ図** になる。:doc:`../shapes` で扱った距離関数を、1つの
図形ではなく多数の点に対して同時に評価し、最小値を与えた種点の
番号で塗り分ける、という一般化として捉えられる。隣り合う領域どうし
の種点を線で結ぶと、ボロノイ図の双対グラフである **ドロネー三角形
分割** が得られる。
"""

import numpy as np
from PIL import Image, ImageDraw


def minkowski_distance(dx: np.ndarray, dy: np.ndarray, p: float) -> np.ndarray:
    """ミンコフスキー距離 ``(|dx|^p + |dy|^p)^(1/p)``。

    ``p=1`` で **マンハッタン距離** （軸方向にしか移動できない距離、
    碁盤の目状の道を歩く距離）、``p=2`` で通常の **ユークリッド距離**
    になる。``p`` を無限大に近づけた極限は、``dx``・``dy`` のうち
    絶対値が大きい方だけで決まる **チェビシェフ距離** （将棋の王が
    1手で動ける距離、といったイメージ）に収束するため、``p`` が
    有限でない場合はこの極限の式を直接使う。
    """
    if np.isinf(p):
        return np.maximum(np.abs(dx), np.abs(dy))
    return (np.abs(dx) ** p + np.abs(dy) ** p) ** (1.0 / p)


def voronoi_regions(
    points: np.ndarray, width: int, height: int, p: float = 2.0
) -> np.ndarray:
    """各画素について、最も近い種点の番号(領域ID)を求める。

    ``points`` は形状 ``(N, 2)`` の座標配列。距離の測り方は ``p``
    （ミンコフスキー距離の次数）で切り替えられ、既定のユークリッド
    距離 (``p=2``) 以外に、マンハッタン距離 (``p=1``) やチェビシェフ
    距離 (``p=numpy.inf``) も指定できる。戻り値は形状
    ``(height, width)`` の整数配列で、値は0からN-1の領域ID。
    """
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    px: np.ndarray = points[:, 0, np.newaxis, np.newaxis]
    py: np.ndarray = points[:, 1, np.newaxis, np.newaxis]
    dx: np.ndarray = xs[np.newaxis, :, :] - px
    dy: np.ndarray = ys[np.newaxis, :, :] - py
    distances: np.ndarray = minkowski_distance(dx, dy, p)
    return np.argmin(distances, axis=0)


def render_mosaic(
    region_id: np.ndarray, num_points: int, rng: np.random.Generator
) -> Image.Image:
    """各領域を種点ごとに割り当てたランダムな色で塗り分ける。"""
    colors: np.ndarray = rng.integers(60, 230, size=(num_points, 3))
    pixels: np.ndarray = colors[region_id]
    return Image.fromarray(pixels.astype(np.uint8))


def render_edges(
    region_id: np.ndarray,
    background: tuple[int, int, int] = (255, 255, 255),
    line_color: tuple[int, int, int] = (30, 30, 30),
) -> Image.Image:
    """隣接する画素の領域番号が変わる境界を線として描画する。"""
    height: int
    width: int
    height, width = region_id.shape
    boundary: np.ndarray = np.zeros((height, width), dtype=bool)
    boundary[:, :-1] |= region_id[:, :-1] != region_id[:, 1:]
    boundary[:-1, :] |= region_id[:-1, :] != region_id[1:, :]

    pixels: np.ndarray = np.full(
        (height, width, 3), background, dtype=np.uint8
    )
    pixels[boundary] = line_color
    return Image.fromarray(pixels)


def adjacent_pairs(region_id: np.ndarray) -> set[tuple[int, int]]:
    """ラスタ上で隣接している領域番号の組を、ドロネーの辺として集める。

    2つの領域が画素単位で隣接している(=ボロノイ図で境界を共有する)
    なら、その2つの種点はドロネー三角形分割でも辺で結ばれる、という
    性質を利用して、明示的な三角形分割アルゴリズムを使わずに辺を
    求めている。
    """
    horiz: np.ndarray = np.stack(
        [region_id[:, :-1], region_id[:, 1:]], axis=-1
    ).reshape(-1, 2)
    vert: np.ndarray = np.stack(
        [region_id[:-1, :], region_id[1:, :]], axis=-1
    ).reshape(-1, 2)
    all_pairs: np.ndarray = np.concatenate([horiz, vert], axis=0)
    differing: np.ndarray = all_pairs[all_pairs[:, 0] != all_pairs[:, 1]]
    sorted_pairs: np.ndarray = np.sort(differing, axis=1)
    unique_pairs: np.ndarray = np.unique(sorted_pairs, axis=0)
    return {(int(a), int(b)) for a, b in unique_pairs}


def render_delaunay(
    points: np.ndarray,
    pairs: set[tuple[int, int]],
    width: int,
    height: int,
    line_color: tuple[int, int, int] = (60, 90, 160),
    point_color: tuple[int, int, int] = (200, 60, 60),
) -> Image.Image:
    """種点と、隣接ペアを結ぶ線分から成るドロネー三角形分割を描く。"""
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for i, j in pairs:
        x0, y0 = points[i]
        x1, y1 = points[j]
        draw.line([(x0, y0), (x1, y1)], fill=line_color, width=1)

    radius: float = 3.0
    for x, y in points:
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=point_color,
        )

    return img


def main() -> None:
    width: int = 500
    height: int = 500
    rng: np.random.Generator = np.random.default_rng(seed=1)

    num_points: int = 40
    points: np.ndarray = rng.uniform(
        low=[0.0, 0.0],
        high=[float(width), float(height)],
        size=(num_points, 2),
    )

    region_id: np.ndarray = voronoi_regions(points, width, height)

    render_mosaic(region_id, num_points, rng).save("voronoi_mosaic.png")
    render_edges(region_id).save("voronoi_edges.png")

    pairs: set[tuple[int, int]] = adjacent_pairs(region_id)
    render_delaunay(points, pairs, width, height).save("delaunay.png")

    # 同じ種点でも距離の測り方(p)を変えると、領域の形が大きく変わる。
    metrics: dict[str, float] = {
        "manhattan": 1.0,
        "euclidean": 2.0,
        "chebyshev": float("inf"),
    }
    for name, p in metrics.items():
        metric_region_id: np.ndarray = voronoi_regions(
            points, width, height, p=p
        )
        render_edges(metric_region_id).save(f"voronoi_{name}.png")


if __name__ == "__main__":
    main()
