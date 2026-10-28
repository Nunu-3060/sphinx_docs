"""結合写像格子（CML）: 1 次元に並べたカオス写像を隣どうしで結合した系の時空パターン.

各格子点 i の値 x(i) を、次の規則で同時に更新する（両端は反対側とつなぐ）。

  x_{n+1}(i) = (1 - ε) f(x_n(i)) + (ε / 2) [f(x_n(i - 1)) + f(x_n(i + 1))]
  f(x) = 1 - a x^2

a は各点のカオスの強さ、ε は隣との結合の強さを表す。

使い方: python ch11_coupled_map_lattice.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util


def coupled_map_lattice(a: float, eps: float, size: int = 128, steps: int = 400, transient: int = 2000,
                        seed: int = 0) -> NDArray[np.float64]:
    """時空図（行が時刻、列が格子点の位置）を返す.

    多くの格子点は周期 2 で振動するので、そのまま描くと縞模様が目立つ。
    そこで 1 ステップおきの値を記録して、振動の位相がそろった領域が同じ色になるようにする。
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.0, 1.0, size)
    rows = []
    for n in range(transient + steps):
        fx = 1.0 - a * x * x
        x = (1.0 - eps) * fx + 0.5 * eps * (np.roll(fx, 1) + np.roll(fx, -1))
        if n >= transient and (n - transient) % 2 == 0:
            rows.append(x.copy())
    return np.array(rows)


EXAMPLES = [
    (1.44, 0.1, "領域が凍結したパターン"),
    (1.71, 0.4, "規則的な部分と乱れの混在"),
    (1.9, 0.1, "乱れの広がり"),
    (2.0, 0.3, "全体が乱れた状態"),
]


def create_figures() -> dict[str, Figure]:
    """4 組の (a, ε) の時空図を並べる（spacetime）."""
    fig, axes = plt.subplots(1, 4, figsize=(14.0, 4.6), sharey=True)
    for ax, (a, eps, name) in zip(axes, EXAMPLES):
        ax.imshow(coupled_map_lattice(a, eps), cmap="coolwarm", aspect="auto", interpolation="nearest",
                  vmin=-1.0, vmax=1.0)
        ax.set_title(f"$a = {a}$, $\\varepsilon = {eps}$\n{name}", fontsize=10)
        ax.set_xlabel("格子点の位置 $i$")
    axes[0].set_ylabel("時刻（2 ステップごと）")
    fig.tight_layout()
    return {"spacetime": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
