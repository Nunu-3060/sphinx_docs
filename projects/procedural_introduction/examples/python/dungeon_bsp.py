"""第 11 章「レベルとダンジョン」: 二分空間分割（BSP）で部屋と通路を作る。

* bsp_steps.png: 分割を 1 段ずつ進める様子と、部屋・通路を置いた結果
* bsp_map.png: できあがったダンジョンの地図（部屋の番号付き）
* bsp_tree.dot: 分割の木（Graphviz の形式。本文の graphviz ディレクティブで読み込む）

ここで作る関数は、lock_and_key.py でも使う。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from common import IntArray, output_dir, save_figure, setup_matplotlib

WALL, ROOM, CORRIDOR = 0, 1, 2
MAP_WIDTH, MAP_HEIGHT = 64, 40


@dataclass
class Rect:
    """格子上の長方形。左上が (x, y)、幅 w、高さ h（単位はマス）。"""

    x: int
    y: int
    w: int
    h: int

    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2


@dataclass
class Node:
    """BSP の木の節。葉（子を持たない節）にだけ部屋を置く。"""

    area: Rect
    depth: int
    children: list[Node] = field(default_factory=list)
    vertical: bool = False  # 縦の線で左右に分けたなら True
    room: Rect | None = None
    room_id: int = -1


def split(node: Node, rng: np.random.Generator, min_size: int = 10, max_depth: int = 4) -> None:
    """節の領域を 2 つに分け、子についても繰り返す（再帰的な二分空間分割）。

    横長の領域は縦の線で、縦長の領域は横の線で分ける（細長い部屋を避けるため）。
    分ける位置は、両側に min_size 以上残り、偏りすぎない範囲から無作為に選ぶ。
    """
    area = node.area
    if node.depth >= max_depth:
        return
    if area.w > area.h * 1.25:
        vertical = True
    elif area.h > area.w * 1.25:
        vertical = False
    else:
        vertical = bool(rng.random() < 0.5)
    length = area.w if vertical else area.h
    if length < 2 * min_size:
        return  # これ以上分けると小さすぎる
    # 極端に偏った分割を避けるため、切る位置を全体の 30〜70 % の範囲に限る。
    low = max(min_size, int(length * 0.3))
    high = min(length - min_size, int(length * 0.7))
    cut = int(rng.integers(low, high + 1))
    if vertical:
        first = Rect(area.x, area.y, cut, area.h)
        second = Rect(area.x + cut, area.y, area.w - cut, area.h)
    else:
        first = Rect(area.x, area.y, area.w, cut)
        second = Rect(area.x, area.y + cut, area.w, area.h - cut)
    node.vertical = vertical
    node.children = [Node(first, node.depth + 1), Node(second, node.depth + 1)]
    for child in node.children:
        split(child, rng, min_size, max_depth)


def leaves(node: Node) -> list[Node]:
    """木の葉を左から順に返す。"""
    if not node.children:
        return [node]
    return [leaf for child in node.children for leaf in leaves(child)]


def place_rooms(root: Node, rng: np.random.Generator, min_room: int = 4) -> list[Rect]:
    """各葉の領域の中に、壁 1 マス分の余白を残して、無作為な大きさ・位置の部屋を置く。"""
    rooms = []
    for index, leaf in enumerate(leaves(root)):
        area = leaf.area
        w = int(rng.integers(min_room, area.w - 2 + 1))
        h = int(rng.integers(min_room, area.h - 2 + 1))
        x = area.x + 1 + int(rng.integers(0, area.w - 2 - w + 1))
        y = area.y + 1 + int(rng.integers(0, area.h - 2 - h + 1))
        leaf.room = Rect(x, y, w, h)
        leaf.room_id = index
        rooms.append(leaf.room)
    return rooms


def connect(node: Node) -> list[tuple[int, int]]:
    """木を下から順にたどり、各節の 2 つの子の部屋どうしを通路で結ぶ。結んだ部屋の番号の組を返す。

    2 つの子の側からそれぞれ部屋を 1 つ選ぶ。互いに最も近い組を選ぶと、通路が短くなる。
    すべての節で 2 つの子を結ぶので、全部屋が 1 つにつながる（部屋と通路は木の形になる）。
    """
    if not node.children:
        return []
    links = connect(node.children[0]) + connect(node.children[1])
    first = leaves(node.children[0])
    second = leaves(node.children[1])
    pairs = [(a, b) for a in first for b in second]
    a, b = min(pairs, key=lambda pair: distance(pair[0], pair[1]))
    links.append((a.room_id, b.room_id))
    return links


def distance(a: Node, b: Node) -> float:
    """2 つの葉の部屋の中心の間の距離。"""
    assert a.room is not None and b.room is not None
    (ax, ay), (bx, by) = a.room.center(), b.room.center()
    return float(np.hypot(ax - bx, ay - by))


def carve_corridor(grid: IntArray, start: tuple[int, int], end: tuple[int, int], horizontal_first: bool) -> None:
    """2 点の間に L 字形の通路を掘る（先に横へ進むか、先に縦へ進むかを選べる）。"""
    (x0, y0), (x1, y1) = start, end
    corner = (x1, y0) if horizontal_first else (x0, y1)
    for (ax, ay), (bx, by) in [(start, corner), (corner, end)]:
        xs = slice(min(ax, bx), max(ax, bx) + 1)
        ys = slice(min(ay, by), max(ay, by) + 1)
        segment = grid[ys, xs]
        segment[segment == WALL] = CORRIDOR


def generate(seed: int) -> tuple[Node, list[Rect], list[tuple[int, int]], IntArray]:
    """BSP のダンジョンを作る。木の根、部屋、通路で結んだ部屋の組、地図（WALL / ROOM / CORRIDOR）を返す。"""
    rng = np.random.default_rng(seed)
    root = Node(Rect(0, 0, MAP_WIDTH, MAP_HEIGHT), 0)
    split(root, rng)
    rooms = place_rooms(root, rng)
    links = connect(root)
    grid = np.full((MAP_HEIGHT, MAP_WIDTH), WALL, dtype=np.int64)
    for room in rooms:
        grid[room.y:room.y + room.h, room.x:room.x + room.w] = ROOM
    for a, b in links:
        carve_corridor(grid, rooms[a].center(), rooms[b].center(), bool(rng.random() < 0.5))
    return root, rooms, links, grid


MAP_COLORS = {WALL: (0.18, 0.18, 0.22), ROOM: (0.92, 0.88, 0.78), CORRIDOR: (0.75, 0.68, 0.55)}


def map_image(grid: IntArray) -> Any:
    image = np.zeros(grid.shape + (3,))
    for value, color in MAP_COLORS.items():
        image[grid == value] = color
    return image


def draw_areas(ax: Any, node: Node, max_depth: int) -> None:
    """深さ max_depth までの分割線を描く。"""
    if not node.children or node.depth >= max_depth:
        return
    a = node.children[1].area
    if node.vertical:
        ax.plot([a.x, a.x], [a.y, a.y + a.h], color="#c44e52", linewidth=2.2 - 0.4 * node.depth)
    else:
        ax.plot([a.x, a.x + a.w], [a.y, a.y], color="#c44e52", linewidth=2.2 - 0.4 * node.depth)
    for child in node.children:
        draw_areas(ax, child, max_depth)


def setup_map_axes(ax: Any) -> None:
    ax.set_xlim(0, MAP_WIDTH)
    ax.set_ylim(MAP_HEIGHT, 0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def draw_steps(file_name: str, root: Node, grid: IntArray) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    figure, axes = plt.subplots(1, 4, figsize=(14, 2.9))
    for column, depth in enumerate([1, 2, 4]):
        ax = axes[column]
        ax.add_patch(Rectangle((0, 0), MAP_WIDTH, MAP_HEIGHT, color="#f4f1ea"))
        draw_areas(ax, root, depth)
        setup_map_axes(ax)
        ax.set_title(f"深さ {depth} までの分割", fontsize=10)
    ax = axes[3]
    ax.imshow(map_image(grid), extent=(0, MAP_WIDTH, MAP_HEIGHT, 0), interpolation="nearest")
    draw_areas(ax, root, 9)
    setup_map_axes(ax)
    ax.set_title("葉に部屋を置き、兄弟どうしを通路で結ぶ", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_map(file_name: str, rooms: list[Rect], grid: IntArray) -> None:
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(figsize=(8, 5.2))
    ax.imshow(map_image(grid), extent=(0, MAP_WIDTH, MAP_HEIGHT, 0), interpolation="nearest")
    for index, room in enumerate(rooms):
        cx, cy = room.x + room.w / 2.0, room.y + room.h / 2.0
        ax.text(cx, cy, f"R{index}", ha="center", va="center", fontsize=10, color="#333333")
    setup_map_axes(ax)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def tree_dot(root: Node) -> str:
    """分割の木を Graphviz の dot 形式の文字列にする。葉には部屋の番号を書く。"""
    lines = [
        "digraph G {",
        '    node [shape=box, style="rounded,filled", fillcolor="#eef3fb", color="#4c72b0", fontsize=11];',
        '    edge [color="#777777"];',
    ]
    counter = 0

    def visit(node: Node) -> str:
        nonlocal counter
        name = f"n{counter}"
        counter += 1
        a = node.area
        if node.children:
            direction = "縦に分割" if node.vertical else "横に分割"
            lines.append(f'    {name} [label="{direction}\\n{a.w}×{a.h}"];')
            for child in node.children:
                lines.append(f"    {name} -> {visit(child)};")
        else:
            lines.append(f'    {name} [label="R{node.room_id}", shape=ellipse, fillcolor="#fdf0e6", color="#dd8452"];')
        return name

    visit(root)
    lines.append("}")
    return "\n".join(lines) + "\n"


SEED = 7


def main() -> None:
    setup_matplotlib()
    root, rooms, _, grid = generate(SEED)
    draw_steps("bsp_steps.png", root, grid)
    draw_map("bsp_map.png", rooms, grid)
    Path(output_dir(__file__) / "bsp_tree.dot").write_text(tree_dot(root), encoding="utf-8")


if __name__ == "__main__":
    main()
