"""グレイ＝スコット・モデル: 反応と拡散だけで、斑点や縞の模様が自然に生まれる.

2 種類の物質の濃度 u, v が、次の反応拡散方程式に従って変化する。

  du/dt = Du ∇²u - u v^2 + F (1 - u)
  dv/dt = Dv ∇²v + u v^2 - (F + k) v

供給率 F と除去率 k の組み合わせによって、できる模様が変わる。

使い方: python ch11_reaction_diffusion.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Array = NDArray[np.float64]
DU, DV = 0.16, 0.08


def laplacian(a: Array) -> Array:
    """5 点差分によるラプラシアン（上下左右の値の和 - 4 × 中心の値）。端は反対側とつなぐ（周期境界）."""
    result: Array = np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1) - 4.0 * a
    return result


def gray_scott(f: float, k: float, n: int = 128, steps: int = 6000, seed: int = 0) -> Array:
    """一様な状態の中央に小さな乱れを置き、steps ステップ（時間刻み 1）後の v の濃度を返す."""
    rng = np.random.default_rng(seed)
    u = np.ones((n, n))
    v = np.zeros((n, n))
    center = slice(n // 2 - 8, n // 2 + 8)
    u[center, center] = 0.5
    v[center, center] = 0.25
    u += 0.02 * rng.random((n, n))
    v += 0.02 * rng.random((n, n))
    for _ in range(steps):
        uvv = u * v * v
        u += DU * laplacian(u) - uvv + f * (1.0 - u)
        v += DV * laplacian(v) + uvv - (f + k) * v
    return v


EXAMPLES = [
    (0.035, 0.065, "斑点"),
    (0.022, 0.051, "縞"),
    (0.040, 0.060, "迷路"),
    (0.030, 0.062, "広がる輪と斑点"),
]


def create_figures() -> dict[str, Figure]:
    """4 組の (F, k) で生まれる模様を並べる（patterns）."""
    fig, axes = plt.subplots(1, 4, figsize=(14.0, 3.9))
    for ax, (f, k, name) in zip(axes, EXAMPLES):
        ax.imshow(gray_scott(f, k), cmap="magma", interpolation="bilinear")
        ax.set_title(f"$F = {f}$, $k = {k}$\n{name}", fontsize=10)
        ax.axis("off")
    fig.tight_layout()
    return {"patterns": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
