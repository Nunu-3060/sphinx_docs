"""距離場を使った円充填(サークルパッキング)。

平面の空いている場所に、既存の円と重ならない円を1つずつ置いていく。
ある点を中心に置ける円の最大半径は、その点から「既存の円の縁」
「キャンバスの端」のうち、もっとも近いものまでの距離に等しい。
これは、既存の円を全て合わせた図形(和集合)の符号付き距離関数
そのものであり、:doc:`../shapes` の ``sdf_circle`` と ``union`` だけで
計算できる。円を置くたびにその円の距離関数を ``union`` で重ねて
いけば、次に置ける半径の分布(空き距離の場)がいつでも手に入る。
"""

import numpy as np
from PIL import Image, ImageDraw

from sdf import sdf_box, sdf_circle, union


def pack_circles(
    free_distance: np.ndarray,
    rng: np.random.Generator,
    max_count: int = 1000,
    min_radius: float = 2.0,
    max_radius: float = 40.0,
    padding: float = 1.5,
) -> list[tuple[float, float, float]]:
    """空き距離の場 ``free_distance`` の中に、重ならない円を詰める。

    ``free_distance`` は画素ごとに「その画素を中心に置ける円の最大
    半径」を表す配列で、円を置いてはいけない場所では 0 以下にしておく。
    毎回、半径 ``min_radius`` 以上の円を置ける画素の中から中心を
    一様にランダムに選び、半径を空き距離(から隙間 ``padding`` を
    引いた値)と ``max_radius`` の小さいほうに決める。置いた円の
    距離関数を ``union`` で空き距離の場に重ねてから、次の円に進む。

    戻り値は、置いた円の (中心 x, 中心 y, 半径) のリスト。
    """
    height: int
    width: int
    height, width = free_distance.shape
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    distance: np.ndarray = free_distance.astype(float)
    circles: list[tuple[float, float, float]] = []

    for _ in range(max_count):
        candidates: np.ndarray = np.flatnonzero(
            distance >= min_radius + padding
        )
        if candidates.size == 0:
            break  # これ以上、最小半径の円を置ける場所がない。

        index: int = int(rng.choice(candidates))
        cy: int
        cx: int
        cy, cx = divmod(index, width)
        radius: float = min(float(distance[cy, cx]) - padding, max_radius)
        circles.append((float(cx), float(cy), radius))

        distance = union(distance, sdf_circle(xs, ys, cx, cy, radius))

    return circles


def canvas_distance(width: int, height: int, margin: float) -> np.ndarray:
    """キャンバスの内側(周囲に ``margin`` の余白を残す)での空き距離。

    矩形の距離関数は内側で負になるため、符号を反転して「矩形の端まで
    の距離」として使う。
    """
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    return -sdf_box(
        xs,
        ys,
        (width - 1) / 2,
        (height - 1) / 2,
        width / 2 - margin,
        height / 2 - margin,
    )


def draw_circles(
    image: Image.Image,
    circles: list[tuple[float, float, float]],
    palette: list[tuple[int, int, int]],
    rng: np.random.Generator,
) -> None:
    """円のリストを、パレットからランダムに選んだ色で塗りつぶして描く。"""
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for cx, cy, radius in circles:
        color: tuple[int, int, int] = palette[int(rng.integers(len(palette)))]
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius], fill=color
        )


def main() -> None:
    width: int = 480
    height: int = 480
    margin: float = 12.0
    background: tuple[int, int, int] = (250, 246, 238)

    # 1. キャンバス全体に円を詰める。
    rng: np.random.Generator = np.random.default_rng(seed=7)
    free: np.ndarray = canvas_distance(width, height, margin)
    circles: list[tuple[float, float, float]] = pack_circles(free, rng)
    image: Image.Image = Image.new("RGB", (width, height), background)
    draw_circles(
        image,
        circles,
        [(38, 70, 83), (42, 157, 143), (233, 196, 106), (244, 162, 97),
         (231, 111, 81)],
        rng,
    )
    image.save("circle_packing.png")

    # 2. 図形の距離関数で、円を置ける場所を内側と外側に分ける。
    #    内側の空き距離は距離関数の符号を反転した値、外側の空き距離は
    #    距離関数そのものになる(どちらもキャンバスの端までの距離と
    #    union で合わせる)。
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    shape: np.ndarray = union(
        sdf_circle(xs, ys, 190.0, 240.0, 110.0),
        sdf_box(xs, ys, 300.0, 240.0, 90.0, 90.0),
    )
    rng = np.random.default_rng(seed=3)
    inside: list[tuple[float, float, float]] = pack_circles(
        union(-shape, free), rng, max_radius=14.0
    )
    outside: list[tuple[float, float, float]] = pack_circles(
        union(shape, free), rng, max_radius=14.0
    )
    image = Image.new("RGB", (width, height), background)
    draw_circles(
        image, inside, [(231, 111, 81), (244, 162, 97), (214, 79, 60)], rng
    )
    draw_circles(
        image, outside, [(160, 170, 175), (190, 196, 198), (130, 142, 150)],
        rng,
    )
    image.save("circle_packing_shape.png")


if __name__ == "__main__":
    main()
