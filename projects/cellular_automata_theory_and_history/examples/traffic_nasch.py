"""ナーゲル・シュレッケンベルク・モデルによる交通流シミュレーション.

周回道路 (周期境界条件) を L 個のセルに区切り, 各セルに車が高々 1 台入る.
各車の速度は 0〜v_max の整数で, 毎ステップ次の 4 つの規則を全車に同時に適用する.

1. 加速: v ← min(v + 1, v_max)
2. 減速: v ← min(v, 前の車までの空きセル数)
3. ランダムな減速: 確率 p で v ← max(v - 1, 0)
4. 移動: 位置 ← 位置 + v

使い方の例::

    python traffic_nasch.py                       # 時空図を表示する
    python traffic_nasch.py --density 0.1 --p 0.3
    python traffic_nasch.py --diagram             # 基本図 (密度と流量の関係) を表示する
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

IntArray = npt.NDArray[np.int64]

EMPTY = -1  # 時空図で車が居ないセルを表す値


@dataclass
class Road:
    """周回道路の状態. positions と velocities の i 番目が i 台目の車を表す."""

    length: int
    positions: IntArray
    velocities: IntArray


def make_road(length: int, n_cars: int, rng: np.random.Generator) -> Road:
    """車をランダムな位置に速度 0 で配置した道路を作る."""
    positions = np.sort(rng.choice(length, size=n_cars, replace=False)).astype(np.int64)
    velocities = np.zeros(n_cars, dtype=np.int64)
    return Road(length, positions, velocities)


def step(road: Road, v_max: int, p: float, rng: np.random.Generator) -> None:
    """全車に 4 つの規則を同時に適用する. road をその場で書き換える.

    車は追い越しをしないので, 配列上の並び順は周回方向の並び順のまま保たれる.
    """
    pos = road.positions
    vel = road.velocities
    # 前の車 (配列上で次の要素, 最後の車にとっては先頭の車) までの空きセル数
    gaps = (np.roll(pos, -1) - pos - 1) % road.length
    if pos.size == 1:
        gaps[:] = road.length - 1
    vel = np.minimum(vel + 1, v_max)              # 1. 加速
    vel = np.minimum(vel, gaps)                   # 2. 減速
    slow = rng.random(vel.size) < p
    vel = np.where(slow, np.maximum(vel - 1, 0), vel)  # 3. ランダムな減速
    road.positions = (pos + vel) % road.length    # 4. 移動
    road.velocities = vel


def snapshot(road: Road) -> IntArray:
    """道路の各セルについて, 車が居れば速度を, 居なければ EMPTY を入れた配列を返す."""
    cells = np.full(road.length, EMPTY, dtype=np.int64)
    cells[road.positions] = road.velocities
    return cells


def simulate(length: int, density: float, v_max: int, p: float, steps: int, seed: int | None = None) -> IntArray:
    """時空図 (形は (steps + 1, length)) を計算する."""
    rng = np.random.default_rng(seed)
    road = make_road(length, max(1, round(density * length)), rng)
    history = np.empty((steps + 1, length), dtype=np.int64)
    history[0] = snapshot(road)
    for t in range(steps):
        step(road, v_max, p, rng)
        history[t + 1] = snapshot(road)
    return history


def mean_flow(length: int, density: float, v_max: int, p: float,
              transient: int = 500, measure: int = 500, seed: int | None = None) -> float:
    """十分に時間が経った後の流量 (1 ステップに 1 セルあたりを通過する車の台数) を求める.

    流量は 密度 × 平均速度 = (全車の速度の和) / 道路のセル数 で計算できる.
    """
    rng = np.random.default_rng(seed)
    n_cars = round(density * length)
    if n_cars == 0:
        return 0.0
    road = make_road(length, n_cars, rng)
    for _ in range(transient):
        step(road, v_max, p, rng)
    total = 0.0
    for _ in range(measure):
        step(road, v_max, p, rng)
        total += float(road.velocities.sum()) / length
    return total / measure


def main() -> None:
    parser = argparse.ArgumentParser(description="ナーゲル・シュレッケンベルク・モデルの交通流シミュレーション")
    parser.add_argument("--length", type=int, default=200, help="道路のセル数")
    parser.add_argument("--density", type=float, default=0.2, help="車の密度 (0〜1)")
    parser.add_argument("--vmax", type=int, default=5, help="最高速度")
    parser.add_argument("--p", type=float, default=0.25, help="ランダムな減速の確率")
    parser.add_argument("--steps", type=int, default=200, help="ステップ数")
    parser.add_argument("--diagram", action="store_true", help="基本図 (密度と流量の関係) を描く")
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 6))
    if args.diagram:
        densities = np.linspace(0.02, 0.9, 30)
        flows = [mean_flow(args.length, float(rho), args.vmax, args.p) for rho in densities]
        ax.plot(densities, flows, "o-")
        ax.set_xlabel("density")
        ax.set_ylabel("flow")
        ax.set_title(f"fundamental diagram (v_max={args.vmax}, p={args.p})")
    else:
        history = simulate(args.length, args.density, args.vmax, args.p, args.steps)
        ax.imshow(history != EMPTY, cmap="binary", interpolation="nearest", aspect="auto")
        ax.set_xlabel("position")
        ax.set_ylabel("time")
        ax.set_title(f"density={args.density}, v_max={args.vmax}, p={args.p}")
    plt.show()


if __name__ == "__main__":
    main()
