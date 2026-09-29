"""ロイド緩和(Lloyd relaxation)による種点の均等化。

種点からボロノイ図を作り、各種点をその領域の重心へ移動させる、
という操作を繰り返す。領域が大きい(周りに隙間がある)種点ほど
大きく動くため、繰り返すうちに種点の間隔がそろい、領域の大きさと
形が均一なボロノイ図(重心ボロノイ分割)に近づいていく。
重心を求めるときに画素ごとの重み(密度)を掛けると、重みの大きい
場所に種点が集まる配置になる。
"""

import numpy as np
from PIL import Image, ImageDraw

from voronoi import render_mosaic


def nearest_seed(
    points: np.ndarray, width: int, height: int, rows_per_chunk: int = 32
) -> np.ndarray:
    """各画素にもっとも近い種点の番号を、形状 (height, width) で返す。

    :doc:`../shapes` の ``voronoi_regions`` と同じ結果になるが、種点が
    数千個あっても扱えるように、画素を数行ずつに分けて計算する。
    距離の 2 乗 ``|q - p|^2 = |q|^2 - 2 q・p + |p|^2`` のうち、画素 q
    だけで決まる ``|q|^2`` は最小値の比較に影響しないため省き、
    残りを行列積で一度に求めている。
    """
    xs: np.ndarray = np.arange(width, dtype=float)
    squared_norm: np.ndarray = (points**2).sum(axis=1)
    region_id: np.ndarray = np.empty((height, width), dtype=np.int64)
    for top in range(0, height, rows_per_chunk):
        ys: np.ndarray = np.arange(
            top, min(top + rows_per_chunk, height), dtype=float
        )
        gx: np.ndarray
        gy: np.ndarray
        gx, gy = np.meshgrid(xs, ys)
        pixels: np.ndarray = np.stack([gx.ravel(), gy.ravel()], axis=1)
        scores: np.ndarray = squared_norm - 2.0 * pixels @ points.T
        region_id[top:top + len(ys)] = scores.argmin(axis=1).reshape(
            len(ys), width
        )
    return region_id


def weighted_centroids(
    region_id: np.ndarray, points: np.ndarray, density: np.ndarray
) -> np.ndarray:
    """各ボロノイ領域の、密度 ``density`` で重み付けした重心を返す。

    領域内の重みの合計が 0 の種点(画素を持たない、または密度が 0 の
    領域だけを持つ種点)は、元の位置のまま動かさない。
    """
    height: int
    width: int
    height, width = region_id.shape
    ys: np.ndarray
    xs: np.ndarray
    ys, xs = np.mgrid[0:height, 0:width]
    labels: np.ndarray = region_id.ravel()
    weight: np.ndarray = density.ravel()
    count: int = len(points)

    total: np.ndarray = np.bincount(labels, weights=weight, minlength=count)
    sum_x: np.ndarray = np.bincount(
        labels, weights=weight * xs.ravel(), minlength=count
    )
    sum_y: np.ndarray = np.bincount(
        labels, weights=weight * ys.ravel(), minlength=count
    )

    centroids: np.ndarray = points.copy()
    has_weight: np.ndarray = total > 0
    centroids[has_weight, 0] = sum_x[has_weight] / total[has_weight]
    centroids[has_weight, 1] = sum_y[has_weight] / total[has_weight]
    return centroids


def lloyd_relaxation(
    points: np.ndarray,
    width: int,
    height: int,
    iterations: int,
    density: np.ndarray | None = None,
) -> np.ndarray:
    """ボロノイ図の作成と重心への移動を ``iterations`` 回繰り返す。

    ``density`` を省略すると全ての画素の重みが等しい通常のロイド緩和、
    形状 (height, width) の配列を渡すと重み付きのロイド緩和になる。
    """
    weights: np.ndarray = (
        np.ones((height, width)) if density is None else density
    )
    current: np.ndarray = points.astype(float)
    for _ in range(iterations):
        region_id: np.ndarray = nearest_seed(current, width, height)
        current = weighted_centroids(region_id, current, weights)
    return current


def render_regions_with_seeds(
    points: np.ndarray, width: int, height: int, seed: int
) -> Image.Image:
    """種点ごとに色分けしたボロノイ図に、種点を黒い点で重ねて描く。"""
    region_id: np.ndarray = nearest_seed(points, width, height)
    rng: np.random.Generator = np.random.default_rng(seed)
    image: Image.Image = render_mosaic(region_id, len(points), rng)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    radius: float = 3.0
    for x, y in points:
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius], fill=(20, 20, 20)
        )
    return image


def main() -> None:
    size: int = 400
    rng: np.random.Generator = np.random.default_rng(seed=1)
    points: np.ndarray = rng.uniform(0.0, float(size), size=(60, 2))

    render_regions_with_seeds(points, size, size, seed=9).save(
        "lloyd_before.png"
    )
    relaxed: np.ndarray = lloyd_relaxation(points, size, size, iterations=30)
    render_regions_with_seeds(relaxed, size, size, seed=9).save(
        "lloyd_after.png"
    )


if __name__ == "__main__":
    main()
