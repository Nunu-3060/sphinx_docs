"""迷路生成アルゴリズム(再帰的バックトラッキング法)。

:doc:`../tiling` の **ワン・タイル** は、隣り合うタイルの辺のラベルが
一致するように配置する、制約充足によるタイリングだった。迷路もまた
「隣り合うセルの間に壁があるか通路があるかを、行き止まりなく全体が
1つにつながるように決める」という、セル間の関係を無視できない
タイリングの一種として捉えられる。ここでは **再帰的バックトラッキング
法** で迷路を生成する。

1. すべてのセルを「未訪問」、すべての壁を「あり」とする。
2. 適当なセルから出発し、隣接する未訪問セルへランダムに移動しながら、
   通った壁を取り除く。今いるセルをスタックに積んでおく。
3. 未訪問の隣接セルがなくなったら、スタックを1つ戻って続きを探す。
4. スタックが空になったら(最初のセルまで戻ったら)終了。

深さ優先探索で穴を掘り進めるこの手順は、必ず「行き止まりのない
1本道が張り巡らされた、閉路のない迷路」(木構造の迷路)を作る。
"""

from collections import deque

import numpy as np
from PIL import Image, ImageDraw

# 壁の向き。0:北 1:東 2:南 3:西 の順に固定し、反対向きの壁を
# ``(d + 2) % 4`` で求められるようにする。
_DR: tuple[int, int, int, int] = (-1, 0, 1, 0)
_DC: tuple[int, int, int, int] = (0, 1, 0, -1)


def generate_maze(
    cols: int, rows: int, rng: np.random.Generator
) -> np.ndarray:
    """再帰的バックトラッキング法で迷路を生成する。

    戻り値は ``(rows, cols, 4)`` の真偽値配列で、``walls[r, c, d]`` が
    真ならセル ``(r, c)`` の向き ``d`` (北・東・南・西) に壁がある
    ことを表す。再帰呼び出しではなく明示的なスタックを使うことで、
    セル数が多い場合でも Python の再帰上限に引っかからないようにして
    いる。
    """
    walls: np.ndarray = np.ones((rows, cols, 4), dtype=bool)
    visited: np.ndarray = np.zeros((rows, cols), dtype=bool)

    stack: list[tuple[int, int]] = [(0, 0)]
    visited[0, 0] = True

    while stack:
        r, c = stack[-1]
        candidates: list[tuple[int, int, int]] = []
        for d in range(4):
            nr, nc = r + _DR[d], c + _DC[d]
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr, nc]:
                candidates.append((d, nr, nc))

        if not candidates:
            stack.pop()
            continue

        d, nr, nc = candidates[rng.integers(len(candidates))]
        walls[r, c, d] = False
        walls[nr, nc, (d + 2) % 4] = False
        visited[nr, nc] = True
        stack.append((nr, nc))

    return walls


def solve_maze(
    walls: np.ndarray, start: tuple[int, int], goal: tuple[int, int]
) -> list[tuple[int, int]]:
    """幅優先探索で ``start`` から ``goal`` までの最短経路を求める。

    再帰的バックトラッキング法で作った迷路は閉路を持たない木構造なので、
    2点を結ぶ経路はそもそも1本しかない。幅優先探索はその唯一の経路を
    最短距離として見つけ出す。
    """
    rows, cols, _ = walls.shape
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    visited: set[tuple[int, int]] = {start}
    queue: deque[tuple[int, int]] = deque([start])

    while queue:
        r, c = queue.popleft()
        if (r, c) == goal:
            break
        for d in range(4):
            if walls[r, c, d]:
                continue
            nr, nc = r + _DR[d], c + _DC[d]
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                came_from[(nr, nc)] = (r, c)
                queue.append((nr, nc))

    path: list[tuple[int, int]] = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path


def render_maze(
    walls: np.ndarray,
    cell_size: int,
    path: list[tuple[int, int]] | None = None,
    wall_color: tuple[int, int, int] = (30, 30, 30),
    path_color: tuple[int, int, int] = (200, 60, 60),
) -> Image.Image:
    """迷路を格子状の壁として描画する。``path`` を渡すと経路を重ねる。"""
    rows, cols, _ = walls.shape
    width: int = cols * cell_size
    height: int = rows * cell_size
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for r in range(rows):
        for c in range(cols):
            x0, y0 = c * cell_size, r * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            if walls[r, c, 0]:
                draw.line([(x0, y0), (x1, y0)], fill=wall_color, width=3)
            if walls[r, c, 1]:
                draw.line([(x1, y0), (x1, y1)], fill=wall_color, width=3)
            if walls[r, c, 2]:
                draw.line([(x0, y1), (x1, y1)], fill=wall_color, width=3)
            if walls[r, c, 3]:
                draw.line([(x0, y0), (x0, y1)], fill=wall_color, width=3)

    if path is not None:
        centers = [
            (c * cell_size + cell_size / 2, r * cell_size + cell_size / 2)
            for r, c in path
        ]
        draw.line(centers, fill=path_color, width=cell_size // 3)

    return img


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=3)
    cols, rows = 30, 30
    walls: np.ndarray = generate_maze(cols, rows, rng)

    render_maze(walls, cell_size=16).save("maze_backtracker.png")

    path: list[tuple[int, int]] = solve_maze(
        walls, start=(0, 0), goal=(rows - 1, cols - 1)
    )
    render_maze(walls, cell_size=16, path=path).save("maze_solution.png")


if __name__ == "__main__":
    main()
