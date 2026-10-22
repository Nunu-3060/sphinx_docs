"""空間植民アルゴリズム（space colonization algorithm）による樹木の生成。

木を育てたい範囲（樹冠）に、枝が伸びていく目標となる点（誘引点）を
たくさん散らしておく。幹の根元から始めて、次の手順を繰り返す。

1. 各誘引点について、影響距離以内にある最も近い枝の節を探す。
2. 1 つ以上の誘引点から選ばれた節は、それらの誘引点へ向かう向きの
   平均の方向に、新しい節を 1 つ伸ばす。
3. 枝の節が消去距離以内に近づいた誘引点は、取り除く。

誘引点が残っている間、枝は空いた空間を奪い合うように伸びていく。
枝どうしが同じ誘引点を取り合うため、枝は自然に間隔を空けて広がる。
"""

import numpy as np
from PIL import Image, ImageDraw


def crown_attractors(rng: np.random.Generator, count: int, size: int) -> np.ndarray:
    """樹冠の形（横長の楕円）の中に、誘引点を一様に散らす。"""
    center: np.ndarray = np.array([size * 0.5, size * 0.38])
    semi_axes: np.ndarray = np.array([size * 0.42, size * 0.3])
    points: list[np.ndarray] = []
    total: int = 0
    while total < count:
        candidates: np.ndarray = rng.uniform(-1.0, 1.0, size=(count, 2))
        inside: np.ndarray = candidates[(candidates**2).sum(axis=1) < 1.0]
        points.append(center + inside * semi_axes)
        total += len(inside)
    result: np.ndarray = np.concatenate(points)[:count]
    return result


def _key(point: np.ndarray) -> tuple[int, int]:
    """点の位置を 0.1 ピクセル単位に丸めた、重複判定用のキーを返す。"""
    return int(round(float(point[0]) * 10)), int(round(float(point[1]) * 10))


def grow_tree(
    attractors: np.ndarray,
    root: np.ndarray,
    step: float = 4.0,
    influence: float = 60.0,
    kill: float = 8.0,
    max_iterations: int = 500,
) -> tuple[np.ndarray, np.ndarray]:
    """空間植民アルゴリズムで枝を伸ばし、節の位置と親の番号を返す。

    戻り値は、形状 (N, 2) の節の位置と、形状 (N,) の各節の親の節の
    番号（根は -1）。根から誘引点までは離れているため、根から上へ
    幹を伸ばし、どれかの誘引点が影響距離に入るまで続ける。
    """
    nodes: list[np.ndarray] = [root]
    parents: list[int] = [-1]

    # 幹: 誘引点のどれかが影響距離に入るまで、真上へ伸ばす。
    while np.linalg.norm(attractors - nodes[-1], axis=1).min() > influence:
        nodes.append(nodes[-1] + np.array([0.0, -step]))
        parents.append(len(nodes) - 2)

    # 既にある節の位置（0.1 ピクセル単位に丸めたもの）。同じ節から毎回
    # 同じ向きに伸ばして、同じ位置に節が重なるのを防ぐために使う。
    occupied: set[tuple[int, int]] = {_key(node) for node in nodes}

    remaining: np.ndarray = attractors
    for _ in range(max_iterations):
        if len(remaining) == 0:
            break
        node_array: np.ndarray = np.array(nodes)

        # 1. 各誘引点に最も近い節と、その距離を求める（誘引点 x 節の表）。
        diff: np.ndarray = remaining[:, np.newaxis, :] - node_array[np.newaxis, :, :]
        dist: np.ndarray = np.linalg.norm(diff, axis=2)
        nearest: np.ndarray = dist.argmin(axis=1)
        nearest_dist: np.ndarray = dist[np.arange(len(remaining)), nearest]

        # 3. 節が消去距離以内に来た誘引点を取り除く。
        alive: np.ndarray = nearest_dist > kill
        remaining = remaining[alive]
        nearest = nearest[alive]
        nearest_dist = nearest_dist[alive]

        # 2. 影響距離以内の誘引点から選ばれた節を、向きの平均の方向に伸ばす。
        active: np.ndarray = nearest_dist < influence
        if not active.any():
            break
        directions: np.ndarray = remaining[active] - node_array[nearest[active]]
        directions /= np.linalg.norm(directions, axis=1, keepdims=True)
        summed: np.ndarray = np.zeros_like(node_array)
        np.add.at(summed, nearest[active], directions)

        for index in np.unique(nearest[active]):
            length: float = float(np.linalg.norm(summed[index]))
            if length < 1e-9:
                continue  # 向きが打ち消し合った節は伸ばさない
            new_node: np.ndarray = node_array[index] + summed[index] / length * step
            key: tuple[int, int] = _key(new_node)
            if key in occupied:
                continue
            occupied.add(key)
            nodes.append(new_node)
            parents.append(int(index))

    return np.array(nodes), np.array(parents)


def branch_thickness(parents: np.ndarray) -> np.ndarray:
    """各節より先にある節の数から、枝の太さを決める。

    先に多くの枝が付いている節ほど太くする。太さは先の節の数の
    平方根に比例させる（太い枝の断面積が、その先の細い枝の断面積の
    合計に等しいとみなす考え方に相当する）。節は親より後に追加される
    ため、番号の大きい節から順に、自分の数を親へ足していけばよい。
    """
    counts: np.ndarray = np.ones(len(parents))
    for index in range(len(parents) - 1, 0, -1):
        counts[parents[index]] += counts[index]
    result: np.ndarray = np.sqrt(counts)
    return result


def render_tree(
    nodes: np.ndarray, parents: np.ndarray, attractors: np.ndarray, size: int
) -> Image.Image:
    """枝を太さ付きの線分として描き、誘引点の初期配置を薄く重ねる。"""
    image: Image.Image = Image.new("RGB", (size, size), (245, 241, 232))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for x, y in attractors:
        draw.point((float(x), float(y)), fill=(200, 190, 170))

    thickness: np.ndarray = branch_thickness(parents)
    scale: float = 14.0 / float(thickness.max())  # 根元の太さを 14 ピクセルにする
    for index in range(1, len(nodes)):
        parent: int = int(parents[index])
        width: int = max(1, int(round(thickness[index] * scale)))
        start: tuple[float, float] = (float(nodes[parent, 0]), float(nodes[parent, 1]))
        end: tuple[float, float] = (float(nodes[index, 0]), float(nodes[index, 1]))
        draw.line([start, end], fill=(60, 45, 35), width=width)
        # 太い線分の継ぎ目に隙間ができないよう、節に円を描いて埋める。
        r: float = width / 2
        draw.ellipse([end[0] - r, end[1] - r, end[0] + r, end[1] + r], fill=(60, 45, 35))
    return image


def main() -> None:
    size: int = 600
    rng: np.random.Generator = np.random.default_rng(seed=2)
    attractors: np.ndarray = crown_attractors(rng, 1500, size)
    root: np.ndarray = np.array([size * 0.5, size * 0.97])
    nodes: np.ndarray
    parents: np.ndarray
    nodes, parents = grow_tree(attractors, root)
    print(f"nodes: {len(nodes)}")
    render_tree(nodes, parents, attractors, size).save("space_colonization.png")


if __name__ == "__main__":
    main()
