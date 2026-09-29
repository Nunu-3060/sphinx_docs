"""ポアソン円盤サンプリング(Bridsonのアルゴリズム)による点配置。

:doc:`../spirals` のフィロタキシスは規則正しすぎるほど整然とした
点配置、一様乱数による点配置（:doc:`../shapes` のボロノイ図で使った
種点など）は逆に粒がまだらに固まったり隙間ができたりする配置だった。
**ポアソン円盤サンプリング** は、その中間に位置する「どの2点も
最小距離 ``min_dist`` 以上離れているが、全体としては隙間なく
埋め尽くされている」という、いわゆる **ブルーノイズ** 特性を持つ
点配置を作る手法である。網膜の視細胞の並びや、砂粒の分布など、
自然界の「均一だがランダムに見える」配置の多くがこの性質を持つ。
"""

import math

import numpy as np
from PIL import Image, ImageDraw

from voronoi import render_mosaic, voronoi_regions


def poisson_disk_sampling(
    width: float,
    height: float,
    min_dist: float,
    rng: np.random.Generator,
    k: int = 30,
) -> np.ndarray:
    """Bridson (2007) のアルゴリズムで、最小距離 ``min_dist`` を
    保った点群を生成する。

    手順は次の通り。

    1. 最初の点を1つランダムに置き、「アクティブリスト」に入れる。
    2. アクティブリストから点を1つ選び、その周囲の環状領域
       (``min_dist`` 〜 ``2 * min_dist``) から候補点を ``k`` 回まで
       試す。既存のどの点とも ``min_dist`` 以上離れている候補が
       見つかれば採用し、新たにアクティブリストへ加える。
    3. ``k`` 回試しても候補が見つからなければ、その点をアクティブ
       リストから外す(これ以上その点の周りには新しい点を置けない
       ということ)。
    4. アクティブリストが空になるまで2-3を繰り返す。

    全画素を総当たりで距離チェックすると低速になるため、
    ``min_dist / sqrt(2)`` を1辺とする格子(1マスに点は高々1つしか
    入らない大きさ)にあらかじめ点を登録しておき、候補点の周囲
    5x5マス程度だけを調べれば十分になる、という高速化を行っている。
    """
    cell_size: float = min_dist / math.sqrt(2)
    grid_w: int = int(math.ceil(width / cell_size))
    grid_h: int = int(math.ceil(height / cell_size))
    grid: np.ndarray = np.full((grid_h, grid_w), -1, dtype=np.int64)

    points: list[np.ndarray] = []
    active: list[int] = []

    def cell_of(p: np.ndarray) -> tuple[int, int]:
        return int(p[1] / cell_size), int(p[0] / cell_size)

    first: np.ndarray = rng.uniform([0.0, 0.0], [width, height])
    points.append(first)
    gy, gx = cell_of(first)
    grid[gy, gx] = 0
    active.append(0)

    while active:
        source_idx: int = active[rng.integers(len(active))]
        base: np.ndarray = points[source_idx]
        accepted: bool = False

        for _ in range(k):
            angle: float = rng.uniform(0.0, 2.0 * math.pi)
            radius: float = rng.uniform(min_dist, 2.0 * min_dist)
            candidate: np.ndarray = base + radius * np.array(
                [math.cos(angle), math.sin(angle)]
            )
            in_bounds: bool = (
                0.0 <= candidate[0] < width and 0.0 <= candidate[1] < height
            )
            if not in_bounds:
                continue

            gy, gx = cell_of(candidate)
            too_close: bool = False
            for yy in range(max(0, gy - 2), min(grid_h, gy + 3)):
                for xx in range(max(0, gx - 2), min(grid_w, gx + 3)):
                    neighbor_idx = grid[yy, xx]
                    if neighbor_idx == -1:
                        continue
                    gap: float = float(
                        np.hypot(*(points[neighbor_idx] - candidate))
                    )
                    if gap < min_dist:
                        too_close = True
                        break
                if too_close:
                    break

            if not too_close:
                points.append(candidate)
                grid[gy, gx] = len(points) - 1
                active.append(len(points) - 1)
                accepted = True
                break

        if not accepted:
            active.remove(source_idx)

    return np.array(points)


def render_points(
    points: np.ndarray,
    width: int,
    height: int,
    radius: float = 3.0,
    color: tuple[int, int, int] = (40, 70, 160),
) -> Image.Image:
    """点群を単純な塗りつぶし円として描画する。"""
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    for x, y in points:
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius], fill=color
        )
    return img


def main() -> None:
    width: int = 480
    height: int = 480
    min_dist: float = 16.0

    rng: np.random.Generator = np.random.default_rng(seed=0)
    poisson_points: np.ndarray = poisson_disk_sampling(
        width, height, min_dist, rng
    )
    render_points(poisson_points, width, height).save("poisson_disk.png")

    # 同じ点数を一様乱数で配置すると、粒の密集と隙間が目立つ。
    rng = np.random.default_rng(seed=0)
    random_points: np.ndarray = rng.uniform(
        low=[0.0, 0.0], high=[width, height], size=(len(poisson_points), 2)
    )
    render_points(random_points, width, height).save("uniform_random.png")

    # 種点の配置だけを差し替えて、ボロノイ図の見え方を比較する。
    region_id: np.ndarray = voronoi_regions(poisson_points, width, height)
    render_mosaic(region_id, len(poisson_points), rng).save(
        "voronoi_poisson.png"
    )


if __name__ == "__main__":
    main()
