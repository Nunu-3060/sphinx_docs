"""差分成長（differential growth）。

点をつないだ閉じた曲線を用意し、次の 3 つの規則で点を動かし続ける。

1. 引き寄せ: 曲線上で隣り合う点どうしは、決まった間隔に近づこうとする。
2. 整列: 各点は、両隣の点の中点に少し近づき、曲線をなめらかにする。
3. 反発: 曲線上で離れていても、空間的に近い点どうしは押し合う。

さらに、長くなった辺の中点に新しい点を挿入して曲線を伸ばす。
曲線は伸び続けるのに、反発のために自分自身とは交わりにくいので、
限られた範囲に押し込められて、脳のしわや珊瑚のように折りたたまれる。

反発の計算には、近くにある点の組を全て求める近傍探索が必要になる。
ここでは ``neighbor_search.py`` の格子による探索を使う。
"""

import numpy as np
from PIL import Image, ImageDraw

from neighbor_search import grid_pairs


def initial_circle(num_points: int, radius: float, center: float) -> np.ndarray:
    """中心 (center, center)・半径 ``radius`` の円周上に点を並べる。"""
    angles: np.ndarray = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    unit: np.ndarray = np.stack([np.cos(angles), np.sin(angles)], axis=1)
    result: np.ndarray = center + radius * unit
    return result


def growth_step(
    points: np.ndarray,
    rest_length: float,
    repulsion_radius: float,
    attraction: float = 0.1,
    alignment: float = 0.3,
    repulsion: float = 0.5,
) -> np.ndarray:
    """3 つの規則で点を 1 ステップ動かした位置を返す。

    ``points`` は閉じた曲線上の点を順に並べた形状 (N, 2) の配列で、
    最後の点と最初の点も隣り合うものとする。
    """
    prev_points: np.ndarray = np.roll(points, 1, axis=0)
    next_points: np.ndarray = np.roll(points, -1, axis=0)
    move: np.ndarray = np.zeros_like(points)

    # 1. 引き寄せ: 隣の点との距離を rest_length に近づける。
    for neighbor in (prev_points, next_points):
        delta: np.ndarray = neighbor - points
        length: np.ndarray = np.linalg.norm(delta, axis=1, keepdims=True)
        move += attraction * delta * (1.0 - rest_length / np.maximum(length, 1e-9))

    # 2. 整列: 両隣の中点に近づく。
    move += alignment * ((prev_points + next_points) / 2 - points)

    # 3. 反発: 半径 repulsion_radius 以内の点の組を押し離す。近いほど強く押す。
    pairs: np.ndarray = grid_pairs(points, repulsion_radius)
    if len(pairs) > 0:
        i: np.ndarray = pairs[:, 0]
        j: np.ndarray = pairs[:, 1]
        delta_ij: np.ndarray = points[i] - points[j]
        dist: np.ndarray = np.linalg.norm(delta_ij, axis=1, keepdims=True)
        strength: np.ndarray = repulsion * (1.0 - dist / repulsion_radius)
        push: np.ndarray = delta_ij / np.maximum(dist, 1e-9) * strength
        # 同じ点が複数の組に現れるため、np.add.at で足し込む。
        np.add.at(move, i, push)
        np.add.at(move, j, -push)

    result: np.ndarray = points + move
    return result


def split_edges(
    points: np.ndarray, max_length: float, probability: float, rng: np.random.Generator
) -> np.ndarray:
    """長さが ``max_length`` を超える辺の中点に、新しい点を挿入する。

    条件を満たす辺を全て分割すると、曲線が急に伸びて形が整う暇が
    なくなる。そこで、各辺を確率 ``probability`` でだけ分割し、
    成長をゆっくりにする。
    """
    next_points: np.ndarray = np.roll(points, -1, axis=0)
    long_edge: np.ndarray = (np.linalg.norm(next_points - points, axis=1) > max_length) & (
        rng.random(len(points)) < probability
    )
    if not long_edge.any():
        return points
    midpoints: np.ndarray = (points[long_edge] + next_points[long_edge]) / 2
    # 各辺の始点の直後に中点を入れる。np.insert の挿入位置は、
    # 元の配列での位置（始点の番号 + 1）で指定する。
    result: np.ndarray = np.insert(points, np.flatnonzero(long_edge) + 1, midpoints, axis=0)
    return result


def grow(max_points: int = 4000, size: int = 800, seed: int = 0) -> np.ndarray:
    """小さな円から曲線を育て、点の数が ``max_points`` に達したら返す。

    最初の円の点の位置に小さな乱数を加え、成長のきっかけを作る。
    隣り合う点の間隔の目標は 4 ピクセル、反発が働く距離はその 4 倍、
    分割する辺の長さは目標の 1.05 倍を超えるものとする。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    rest_length: float = 4.0
    points: np.ndarray = initial_circle(60, 40.0, size / 2)
    points += rng.normal(0.0, 1.0, points.shape)

    while len(points) < max_points:
        points = growth_step(points, rest_length, repulsion_radius=4 * rest_length)
        points = split_edges(points, 1.05 * rest_length, probability=0.02, rng=rng)
    return points


def render_curve(points: np.ndarray, size: int) -> Image.Image:
    """閉じた曲線を描いた画像を返す。"""
    image: Image.Image = Image.new("RGB", (size, size), (245, 241, 232))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    closed: list[tuple[float, float]] = [(float(x), float(y)) for x, y in points]
    closed.append(closed[0])
    draw.line(closed, fill=(30, 50, 80), width=2, joint="curve")
    return image


def main() -> None:
    size: int = 800
    points: np.ndarray = grow(size=size)
    print(f"points: {len(points)}")
    render_curve(points, size).save("differential_growth.png")


if __name__ == "__main__":
    main()
