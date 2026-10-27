"""HPP モデル (格子ガス・オートマトン) の簡易実装.

正方格子の各ノードには, 東・北・西・南の 4 方向へ動く粒子が方向ごとに高々 1 個ずつ存在できる.
1 ステップは次の 2 段階からなる.

1. 衝突: 正面衝突する 2 粒子 (東と西のみ, または北と南のみ) を 90 度回転させる.
2. 移動: 各粒子を向いている方向の隣のノードへ移す.

衝突の前後で粒子数と運動量が保存される. 境界条件は周期境界とする.

使い方の例::

    python lattice_gas_hpp.py
    python lattice_gas_hpp.py --size 256 --steps 60
"""

from __future__ import annotations

import argparse

import numpy as np
import numpy.typing as npt

BoolGrid = npt.NDArray[np.bool_]
FloatGrid = npt.NDArray[np.float64]

# 4 方向の粒子の有無を形 (4, 行数, 列数) の真偽値配列で表す. 配列の行番号は下に行くほど大きい.
EAST, NORTH, WEST, SOUTH = 0, 1, 2, 3


def collide(state: BoolGrid) -> BoolGrid:
    """正面衝突する粒子の組を 90 度回転させた状態を返す."""
    e, n, w, s = state
    horizontal = e & w & ~n & ~s  # 東西からの正面衝突
    vertical = n & s & ~e & ~w    # 南北からの正面衝突
    flip = horizontal | vertical  # 該当するノードでは 4 方向すべての有無を反転すればよい
    result: BoolGrid = state ^ flip
    return result


def propagate(state: BoolGrid) -> BoolGrid:
    """各粒子を隣のノードへ移動させた状態を返す."""
    moved = np.empty_like(state)
    moved[EAST] = np.roll(state[EAST], 1, axis=1)
    moved[WEST] = np.roll(state[WEST], -1, axis=1)
    moved[NORTH] = np.roll(state[NORTH], -1, axis=0)
    moved[SOUTH] = np.roll(state[SOUTH], 1, axis=0)
    return moved


def step(state: BoolGrid) -> BoolGrid:
    """衝突と移動をこの順に行う."""
    return propagate(collide(state))


def initial_state(size: int, background: float, bump: float, radius: int, seed: int | None = None) -> BoolGrid:
    """一様な背景の中央に, 粒子の密度が高い円形の領域を置いた初期状態を作る."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size]
    inside = (y - size / 2) ** 2 + (x - size / 2) ** 2 < radius ** 2
    probability = np.where(inside, bump, background)
    state: BoolGrid = rng.random((4, size, size)) < probability
    return state


def coarse_density(state: BoolGrid, block: int) -> FloatGrid:
    """block × block のノードごとに平均した粒子密度を返す. 微視的なゆらぎをならして見るために使う."""
    counts = state.sum(axis=0).astype(np.float64)
    rows, cols = counts.shape
    reshaped = counts[:rows - rows % block, :cols - cols % block].reshape(rows // block, block, cols // block, block)
    result: FloatGrid = reshaped.mean(axis=(1, 3))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="HPP モデルで密度の波が広がる様子を表示する")
    parser.add_argument("--size", type=int, default=256, help="格子の一辺のノード数")
    parser.add_argument("--steps", type=int, default=60, help="ステップ数")
    parser.add_argument("--block", type=int, default=4, help="密度を平均するブロックの一辺")
    args = parser.parse_args()

    state = initial_state(args.size, background=0.2, bump=0.7, radius=args.size // 16, seed=1)
    for _ in range(args.steps):
        state = step(state)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(coarse_density(state, args.block), cmap="viridis", interpolation="nearest")
    ax.set_title(f"HPP lattice gas, step {args.steps}")
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()


if __name__ == "__main__":
    main()
