"""基本セル・オートマトン (ECA) の時空図を描くサンプル.

ルール番号 (0〜255) を指定すると, その規則で時間発展させた結果を
時空図 (横軸がセルの位置, 縦軸が時刻で, 下に行くほど新しい) として表示する.

使い方の例::

    python elementary_ca.py 30
    python elementary_ca.py 110 --width 301 --steps 150 --random
    python elementary_ca.py 90 --output rule90.png
"""

from __future__ import annotations

import argparse

import numpy as np
import numpy.typing as npt

Cells = npt.NDArray[np.uint8]


def rule_table(rule: int) -> Cells:
    """ルール番号から局所規則の表を作る.

    戻り値の k 番目の要素は, 近傍 (左, 中央, 右) を 2 進数 4 * 左 + 2 * 中央 + 右 と
    みなしたときの値が k である場合の次の状態を表す.
    """
    if not 0 <= rule <= 255:
        raise ValueError(f"ルール番号は 0〜255 で指定する: {rule}")
    return np.array([(rule >> k) & 1 for k in range(8)], dtype=np.uint8)


def step(cells: Cells, table: Cells) -> Cells:
    """周期境界条件のもとで 1 ステップだけ時間発展させる."""
    left = np.roll(cells, 1)    # 各セルの左隣の状態
    right = np.roll(cells, -1)  # 各セルの右隣の状態
    index = 4 * left + 2 * cells + right
    result: Cells = table[index]
    return result


def evolve(rule: int, initial: Cells, steps: int) -> Cells:
    """初期配置から steps ステップ分を計算し, 時空図を 2 次元配列で返す.

    戻り値の形は (steps + 1, セル数) で, 0 行目が初期配置である.
    """
    table = rule_table(rule)
    history = np.zeros((steps + 1, initial.size), dtype=np.uint8)
    history[0] = initial
    for t in range(steps):
        history[t + 1] = step(history[t], table)
    return history


def single_seed(width: int) -> Cells:
    """中央の 1 セルだけが 1 で, 残りが 0 の初期配置を作る."""
    cells = np.zeros(width, dtype=np.uint8)
    cells[width // 2] = 1
    return cells


def random_cells(width: int, density: float = 0.5, seed: int | None = None) -> Cells:
    """各セルが確率 density で 1 になるランダムな初期配置を作る."""
    rng = np.random.default_rng(seed)
    return (rng.random(width) < density).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="基本セル・オートマトンの時空図を描く")
    parser.add_argument("rule", type=int, help="ルール番号 (0〜255)")
    parser.add_argument("--width", type=int, default=201, help="セルの数")
    parser.add_argument("--steps", type=int, default=100, help="計算するステップ数")
    parser.add_argument("--random", action="store_true", help="ランダムな初期配置を使う")
    parser.add_argument("--seed", type=int, default=None, help="乱数のシード")
    parser.add_argument("--output", default=None, help="画像の保存先 (省略時は画面に表示)")
    args = parser.parse_args()

    if args.random:
        initial = random_cells(args.width, seed=args.seed)
    else:
        initial = single_seed(args.width)
    history = evolve(args.rule, initial, args.steps)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 8 * history.shape[0] / history.shape[1]))
    ax.imshow(history, cmap="binary", interpolation="nearest")
    ax.set_title(f"Rule {args.rule}")
    ax.set_xlabel("position")
    ax.set_ylabel("time")
    if args.output:
        fig.savefig(args.output, dpi=150, bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    main()
