"""ラングトンのアリのサンプル.

白いセルの上ではアリが右に 90 度向きを変え, 黒いセルの上では左に 90 度向きを変える.
その後, いま居るセルの色を反転させてから, 向いている方向へ 1 セル進む.
何もない盤面から始めると, 約 1 万ステップの不規則な動きの後に「ハイウェイ」と
呼ばれる周期的な構造を作りながら一方向へ進み続ける.

使い方の例::

    python langtons_ant.py
    python langtons_ant.py --steps 500 --size 40
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

Grid = npt.NDArray[np.uint8]

# 向きは 0: 上, 1: 右, 2: 下, 3: 左 とする. 配列の行番号は下に行くほど大きい.
DIRECTIONS: tuple[tuple[int, int], ...] = ((-1, 0), (0, 1), (1, 0), (0, -1))


@dataclass
class Ant:
    """アリの位置 (行, 列) と向き."""

    row: int
    col: int
    direction: int = 0


def step(grid: Grid, ant: Ant) -> None:
    """アリを 1 ステップ動かす. grid と ant をその場で書き換える."""
    if grid[ant.row, ant.col] == 0:   # 白いセル: 右に曲がる
        ant.direction = (ant.direction + 1) % 4
    else:                             # 黒いセル: 左に曲がる
        ant.direction = (ant.direction - 1) % 4
    grid[ant.row, ant.col] ^= 1       # セルの色を反転する
    d_row, d_col = DIRECTIONS[ant.direction]
    rows, cols = grid.shape
    ant.row = (ant.row + d_row) % rows  # 周期境界条件
    ant.col = (ant.col + d_col) % cols


def run(size: int, steps: int) -> tuple[Grid, Ant]:
    """size × size の白い盤面の中央からアリを steps ステップ動かす."""
    grid = np.zeros((size, size), dtype=np.uint8)
    ant = Ant(size // 2, size // 2)
    for _ in range(steps):
        step(grid, ant)
    return grid, ant


def main() -> None:
    parser = argparse.ArgumentParser(description="ラングトンのアリを動かして結果を表示する")
    parser.add_argument("--size", type=int, default=160, help="盤面の一辺のセル数")
    parser.add_argument("--steps", type=int, default=11000, help="ステップ数")
    parser.add_argument("--output", default=None, help="画像の保存先 (省略時は画面に表示)")
    args = parser.parse_args()

    grid, ant = run(args.size, args.steps)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap="binary", interpolation="nearest")
    ax.plot(ant.col, ant.row, "r.", markersize=8)
    ax.set_title(f"Langton's ant after {args.steps} steps")
    ax.set_xticks([])
    ax.set_yticks([])
    if args.output:
        fig.savefig(args.output, dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
