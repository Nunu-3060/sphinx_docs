"""BSP（二分空間分割）でダンジョンの部屋と通路を生成する（Pillow）。

1. マップ全体の矩形を、縦または横に再帰的に 2 分割する。
2. 分割しきった矩形（葉）の中に、ひとまわり小さい部屋を置く。
3. 分割したときの兄弟同士を通路でつなぐ。兄弟は必ずつながるので、全体も 1 つにつながる。
4. スタートから幅優先探索（BFS）を行い、最も遠い床をゴールにする。

実行例:
    python procgen_bsp.py                       # 生成して画像を表示する
    python procgen_bsp.py --seed 5              # 別のダンジョンを生成する
    python procgen_bsp.py --output bsp.png      # 画像を保存する
"""

from __future__ import annotations

import argparse
import random
from collections import deque
from dataclasses import dataclass

from PIL import Image, ImageDraw

WIDTH = 60
HEIGHT = 36
CELL = 8
MIN_LEAF = 9  # これより小さい矩形は分割しない

WALL_COLOR = (52, 46, 60)
FLOOR_COLOR = (222, 205, 170)
SPLIT_COLOR = (110, 170, 230)
START_COLOR = (90, 190, 110)
GOAL_COLOR = (220, 80, 70)


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2


@dataclass
class Node:
    """BSP 木のノード。葉なら room を持ち、そうでなければ子を 2 つ持つ。"""

    area: Rect
    left: Node | None = None
    right: Node | None = None
    room: Rect | None = None

    def rooms(self) -> list[Rect]:
        if self.room is not None:
            return [self.room]
        assert self.left is not None and self.right is not None
        return self.left.rooms() + self.right.rooms()


def split(node: Node, rng: random.Random) -> None:
    """node を再帰的に分割する。"""
    a = node.area
    can_vertical = a.w >= MIN_LEAF * 2
    can_horizontal = a.h >= MIN_LEAF * 2
    if not (can_vertical or can_horizontal):
        return
    if can_vertical and can_horizontal:
        # 細長い矩形は長い方向に切る。縦と横の長さが近いときはランダムに選ぶ。
        if a.w > a.h * 1.25:
            vertical = True
        elif a.h > a.w * 1.25:
            vertical = False
        else:
            vertical = rng.random() < 0.5
    else:
        vertical = can_vertical
    if vertical:
        cut = rng.randint(MIN_LEAF, a.w - MIN_LEAF)
        node.left = Node(Rect(a.x, a.y, cut, a.h))
        node.right = Node(Rect(a.x + cut, a.y, a.w - cut, a.h))
    else:
        cut = rng.randint(MIN_LEAF, a.h - MIN_LEAF)
        node.left = Node(Rect(a.x, a.y, a.w, cut))
        node.right = Node(Rect(a.x, a.y + cut, a.w, a.h - cut))
    split(node.left, rng)
    split(node.right, rng)


def place_rooms(node: Node, rng: random.Random) -> None:
    """葉の矩形の内側に、周囲に 1 マス以上の余白を取って部屋を置く。"""
    if node.left is None or node.right is None:
        a = node.area
        w = rng.randint(4, a.w - 2)
        h = rng.randint(4, a.h - 2)
        x = rng.randint(a.x + 1, a.x + a.w - w - 1)
        y = rng.randint(a.y + 1, a.y + a.h - h - 1)
        node.room = Rect(x, y, w, h)
        return
    place_rooms(node.left, rng)
    place_rooms(node.right, rng)


def carve_corridors(node: Node, grid: list[list[bool]], rng: random.Random) -> None:
    """兄弟の部分木から部屋を 1 つずつ選び、L 字の通路でつなぐ。"""
    if node.left is None or node.right is None:
        return
    carve_corridors(node.left, grid, rng)
    carve_corridors(node.right, grid, rng)
    (x1, y1) = rng.choice(node.left.rooms()).center()
    (x2, y2) = rng.choice(node.right.rooms()).center()
    for x in range(min(x1, x2), max(x1, x2) + 1):
        grid[y1][x] = False
    for y in range(min(y1, y2), max(y1, y2) + 1):
        grid[y][x2] = False


def leaves(node: Node) -> list[Node]:
    if node.left is None or node.right is None:
        return [node]
    return leaves(node.left) + leaves(node.right)


def distances(grid: list[list[bool]], start: tuple[int, int]) -> dict[tuple[int, int], int]:
    """start から各床マスまでの歩数を BFS で求める。"""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not grid[ny][nx] and (nx, ny) not in dist:
                dist[(nx, ny)] = dist[(x, y)] + 1
                queue.append((nx, ny))
    return dist


def fill_cell(pen: ImageDraw.ImageDraw, x: int, y: int, color: tuple[int, int, int]) -> None:
    pen.rectangle((x * CELL, y * CELL, (x + 1) * CELL - 1, (y + 1) * CELL - 1), fill=color)


def draw_stage(root: Node, grid: list[list[bool]] | None, show_split: bool,
               marks: dict[tuple[int, int], tuple[int, int, int]] | None = None) -> Image.Image:
    image = Image.new("RGB", (WIDTH * CELL, HEIGHT * CELL), WALL_COLOR)
    pen = ImageDraw.Draw(image)
    if grid is not None:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if not grid[y][x]:
                    fill_cell(pen, x, y, FLOOR_COLOR)
    for (x, y), color in (marks or {}).items():
        fill_cell(pen, x, y, color)
    if show_split:
        for leaf in leaves(root):
            a = leaf.area
            pen.rectangle((a.x * CELL, a.y * CELL, (a.x + a.w) * CELL - 1, (a.y + a.h) * CELL - 1),
                          outline=SPLIT_COLOR, width=2)
    return image


def side_by_side(images: list[Image.Image], gap: int = 12) -> Image.Image:
    width = sum(img.width for img in images) + gap * (len(images) - 1)
    result = Image.new("RGB", (width, images[0].height), (255, 255, 255))
    x = 0
    for img in images:
        result.paste(img, (x, 0))
        x += img.width + gap
    return result


def generate(rng: random.Random) -> Image.Image:
    root = Node(Rect(0, 0, WIDTH, HEIGHT))
    split(root, rng)
    place_rooms(root, rng)

    rooms_only = [[True] * WIDTH for _ in range(HEIGHT)]
    for room in root.rooms():
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                rooms_only[y][x] = False
    grid = [row[:] for row in rooms_only]
    carve_corridors(root, grid, rng)

    start = root.rooms()[0].center()
    dist = distances(grid, start)
    goal = max(dist, key=lambda cell: dist[cell])
    floor_count = sum(not cell for row in grid for cell in row)
    print(f"部屋の数 {len(root.rooms())}, 床のマス {floor_count}, BFS で到達できた床 {len(dist)}")
    print(f"スタート {start} からゴール {goal} までの最短歩数: {dist[goal]}")

    marks = {start: START_COLOR, goal: GOAL_COLOR}
    return side_by_side([
        draw_stage(root, None, show_split=True),
        draw_stage(root, rooms_only, show_split=True),
        draw_stage(root, grid, show_split=False, marks=marks),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seed", type=int, default=4, help="乱数のシード（同じ値なら同じダンジョンになる）")
    parser.add_argument("--output", help="画像を保存するファイル名（省略時は画面に表示する）")
    args = parser.parse_args()

    image = generate(random.Random(args.seed))
    if args.output:
        image.save(args.output)
    else:
        image.show()


if __name__ == "__main__":
    main()
