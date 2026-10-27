"""洞窟型のマップを手続き型生成し、到達可能性を検証する（Pillow）。

2 つの方法で生成できる。

* walk : ランダムウォーク（酔歩）で床を掘り進める
* cave : セル・オートマトンでノイズを滑らかにし、洞窟らしい形にする

cave では、生成後に幅優先探索（BFS）で床をつながった領域に分け、最も大きい領域だけを残す。
こうすると「どこからも行けない小部屋」が無くなる。

実行例:
    python procgen_cave.py                                  # cave で生成し、画像を表示する
    python procgen_cave.py --method walk --seed 3           # ランダムウォークで生成する
    python procgen_cave.py --output cave.png                # 画像を保存する
"""

from __future__ import annotations

import argparse
import random
from collections import deque

from PIL import Image, ImageDraw

WIDTH = 60
HEIGHT = 36
CELL = 8  # 画像にするときの 1 マスの大きさ（ピクセル）

WALL = True
FLOOR = False
Grid = list[list[bool]]  # grid[y][x] が True なら壁

WALL_COLOR = (52, 46, 60)
FLOOR_COLOR = (222, 205, 170)
REMOVED_COLOR = (200, 90, 80)  # 最大の領域以外として埋めた床


def random_walk(rng: random.Random, floor_ratio: float = 0.3) -> Grid:
    """中央から 1 歩ずつランダムに歩き、通った場所を床にする。"""
    grid = [[WALL] * WIDTH for _ in range(HEIGHT)]
    x, y = WIDTH // 2, HEIGHT // 2
    target = int(WIDTH * HEIGHT * floor_ratio)
    dug = 0
    while dug < target:
        if grid[y][x] == WALL:
            grid[y][x] = FLOOR
            dug += 1
        dx, dy = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        # 外周の 1 マスは壁のまま残す。
        x = min(max(x + dx, 1), WIDTH - 2)
        y = min(max(y + dy, 1), HEIGHT - 2)
    return grid


def random_noise(rng: random.Random, wall_probability: float = 0.45) -> Grid:
    """各マスを確率 wall_probability で壁にする。外周は必ず壁にする。"""
    grid: Grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            border = x in (0, WIDTH - 1) or y in (0, HEIGHT - 1)
            row.append(border or rng.random() < wall_probability)
        grid.append(row)
    return grid


def count_wall_neighbors(grid: Grid, x: int, y: int) -> int:
    """周囲 8 マスのうち壁の数を数える。マップの外は壁とみなす。"""
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT) or grid[ny][nx] == WALL:
                count += 1
    return count


def smooth(grid: Grid) -> Grid:
    """セル・オートマトンを 1 回適用する。

    壁は周囲の壁が 4 以上なら壁のまま、床は周囲の壁が 5 以上なら壁になる。
    """
    new: Grid = []
    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            n = count_wall_neighbors(grid, x, y)
            row.append(n >= 4 if grid[y][x] == WALL else n >= 5)
        new.append(row)
    return new


def find_regions(grid: Grid) -> list[list[tuple[int, int]]]:
    """上下左右でつながった床の領域を、大きい順に返す。"""
    seen: set[tuple[int, int]] = set()
    regions: list[list[tuple[int, int]]] = []
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == WALL or (x, y) in seen:
                continue
            region = []
            queue = deque([(x, y)])
            seen.add((x, y))
            while queue:
                cx, cy = queue.popleft()
                region.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if grid[ny][nx] == FLOOR and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            regions.append(region)
    return sorted(regions, key=len, reverse=True)


def keep_largest_region(grid: Grid) -> tuple[Grid, list[tuple[int, int]]]:
    """最も大きい床の領域だけを残し、新しいグリッドと、埋めたマスの一覧を返す。"""
    regions = find_regions(grid)
    new = [row[:] for row in grid]
    removed = [cell for region in regions[1:] for cell in region]
    for x, y in removed:
        new[y][x] = WALL
    return new, removed


def floor_ratio(grid: Grid) -> float:
    return sum(cell == FLOOR for row in grid for cell in row) / (WIDTH * HEIGHT)


def draw(grid: Grid, removed: list[tuple[int, int]] | None = None) -> Image.Image:
    image = Image.new("RGB", (WIDTH * CELL, HEIGHT * CELL), WALL_COLOR)
    pen = ImageDraw.Draw(image)
    marked = set(removed or [])
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == FLOOR:
                color = FLOOR_COLOR
            elif (x, y) in marked:
                color = REMOVED_COLOR
            else:
                continue
            pen.rectangle((x * CELL, y * CELL, (x + 1) * CELL - 1, (y + 1) * CELL - 1), fill=color)
    return image


def side_by_side(images: list[Image.Image], gap: int = 12) -> Image.Image:
    width = sum(img.width for img in images) + gap * (len(images) - 1)
    result = Image.new("RGB", (width, images[0].height), (255, 255, 255))
    x = 0
    for img in images:
        result.paste(img, (x, 0))
        x += img.width + gap
    return result


def generate_cave(rng: random.Random) -> Image.Image:
    """初期状態、1 回後、4 回後、最大の領域だけを残した結果の 4 枚を横に並べる。"""
    grid = random_noise(rng)
    stages = [draw(grid)]
    for step in range(1, 5):
        grid = smooth(grid)
        if step in (1, 4):
            stages.append(draw(grid))
    print(f"平滑化 4 回後: 床の割合 {floor_ratio(grid):.0%}, 領域の数 {len(find_regions(grid))}")
    final, removed = keep_largest_region(grid)
    print(f"最大の領域だけを残した後: 床の割合 {floor_ratio(final):.0%}, 埋めたマス {len(removed)}")
    stages.append(draw(final, removed))
    return side_by_side(stages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--method", choices=["walk", "cave"], default="cave", help="生成方法")
    parser.add_argument("--seed", type=int, default=7, help="乱数のシード（同じ値なら同じマップになる）")
    parser.add_argument("--output", help="画像を保存するファイル名（省略時は画面に表示する）")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    if args.method == "walk":
        grid = random_walk(rng)
        print(f"ランダムウォーク: 床の割合 {floor_ratio(grid):.0%}, 領域の数 {len(find_regions(grid))}")
        image = draw(grid)
    else:
        image = generate_cave(rng)

    if args.output:
        image.save(args.output)
    else:
        image.show()


if __name__ == "__main__":
    main()
