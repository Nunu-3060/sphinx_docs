"""ライフゲーム (および Life-like セル・オートマトン) のサンプル.

B/S 表記で規則を指定できる. 既定値の B3/S23 がコンウェイのライフゲームである.
境界条件は周期境界 (上端と下端, 左端と右端がつながっている) とする.

使い方の例::

    python game_of_life.py --pattern glider
    python game_of_life.py --pattern gosper_gun --size 60 80
    python game_of_life.py --random 0.3 --rule B36/S23
"""

from __future__ import annotations

import argparse

import numpy as np
import numpy.typing as npt

Grid = npt.NDArray[np.uint8]

# パターンは文字列で表す. "O" が生きているセル, "." が死んでいるセルである.
PATTERNS: dict[str, list[str]] = {
    "block": [
        "OO",
        "OO",
    ],
    "beehive": [
        ".OO.",
        "O..O",
        ".OO.",
    ],
    "blinker": [
        "OOO",
    ],
    "toad": [
        ".OOO",
        "OOO.",
    ],
    "glider": [
        ".O.",
        "..O",
        "OOO",
    ],
    "lwss": [
        ".O..O",
        "O....",
        "O...O",
        "OOOO.",
    ],
    "r_pentomino": [
        ".OO",
        "OO.",
        ".O.",
    ],
    "gosper_gun": [
        "........................O...........",
        "......................O.O...........",
        "............OO......OO............OO",
        "...........O...O....OO............OO",
        "OO........O.....O...OO..............",
        "OO........O...O.OO....O.O...........",
        "..........O.....O.......O...........",
        "...........O...O....................",
        "............OO......................",
    ],
}


def parse_rule(rule: str) -> tuple[frozenset[int], frozenset[int]]:
    """"B3/S23" のような B/S 表記を (誕生の条件, 生存の条件) に変換する."""
    birth_part, survive_part = rule.upper().split("/")
    if not (birth_part.startswith("B") and survive_part.startswith("S")):
        raise ValueError(f"B/S 表記ではない: {rule}")
    birth = frozenset(int(ch) for ch in birth_part[1:])
    survive = frozenset(int(ch) for ch in survive_part[1:])
    return birth, survive


def pattern_to_array(pattern: list[str]) -> Grid:
    """文字列で表したパターンを 0/1 の配列に変換する."""
    return np.array([[1 if ch == "O" else 0 for ch in row] for row in pattern], dtype=np.uint8)


def place(pattern: list[str], shape: tuple[int, int], top: int | None = None, left: int | None = None) -> Grid:
    """指定した大きさの盤面にパターンを置く. 位置を省略すると中央に置く."""
    grid = np.zeros(shape, dtype=np.uint8)
    cells = pattern_to_array(pattern)
    h, w = cells.shape
    if top is None:
        top = (shape[0] - h) // 2
    if left is None:
        left = (shape[1] - w) // 2
    grid[top:top + h, left:left + w] = cells
    return grid


def count_neighbors(grid: Grid) -> Grid:
    """各セルの周囲 8 セル (ムーア近傍から中心を除いたもの) にある生きたセルの数を数える."""
    total = np.zeros_like(grid)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            total += np.roll(grid, (dy, dx), axis=(0, 1))
    return total


def step(grid: Grid,
         birth: frozenset[int] = frozenset({3}),
         survive: frozenset[int] = frozenset({2, 3})) -> Grid:
    """1 世代だけ時間発展させる."""
    n = count_neighbors(grid)
    born = (grid == 0) & np.isin(n, list(birth))
    stays = (grid == 1) & np.isin(n, list(survive))
    result: Grid = (born | stays).astype(np.uint8)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="ライフゲームをアニメーション表示する")
    parser.add_argument("--rule", default="B3/S23", help="B/S 表記の規則 (既定値は B3/S23)")
    parser.add_argument("--pattern", choices=sorted(PATTERNS), default="glider", help="初期パターン")
    parser.add_argument("--random", type=float, default=None, metavar="DENSITY",
                        help="指定すると, この密度のランダムな初期配置を使う")
    parser.add_argument("--size", type=int, nargs=2, default=(40, 40), metavar=("ROWS", "COLS"), help="盤面の大きさ")
    parser.add_argument("--steps", type=int, default=200, help="表示する世代数")
    parser.add_argument("--interval", type=int, default=100, help="1 世代あたりの表示時間 [ms]")
    args = parser.parse_args()

    birth, survive = parse_rule(args.rule)
    shape = (args.size[0], args.size[1])
    if args.random is not None:
        rng = np.random.default_rng()
        grid = (rng.random(shape) < args.random).astype(np.uint8)
    else:
        grid = place(PATTERNS[args.pattern], shape)

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.artist import Artist

    fig, ax = plt.subplots()
    image = ax.imshow(grid, cmap="binary", vmin=0, vmax=1, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])

    state = {"grid": grid}

    def update(frame: int) -> list[Artist]:
        state["grid"] = step(state["grid"], birth, survive)
        image.set_data(state["grid"])
        ax.set_title(f"{args.rule}  generation {frame + 1}")
        return [image]

    # アニメーションのオブジェクトは表示が終わるまで変数に保持しておく必要がある.
    animation = FuncAnimation(fig, update, frames=args.steps, interval=args.interval, repeat=False)
    plt.show()
    del animation


if __name__ == "__main__":
    main()
