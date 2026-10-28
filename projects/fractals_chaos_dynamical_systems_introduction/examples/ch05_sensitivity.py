"""初期値鋭敏性: わずかに異なる 2 つの初期値から出た軌道が離れていく様子を見る.

ロジスティック写像 x_{n+1} = 4 x_n (1 - x_n) で、初期値の差を 1e-10 にする。

使い方: python ch05_sensitivity.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import plot_util
from ch04_logistic import orbit


def create_figures() -> dict[str, Figure]:
    """2 本の軌道の時系列（上）と、差の絶対値の対数グラフ（下）を描く（divergence）."""
    n = 60
    delta = 1e-10
    a = orbit(4.0, 0.2, n)
    b = orbit(4.0, 0.2 + delta, n)
    steps = np.arange(n + 1)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.0, 6.0), sharex=True)
    ax1.plot(steps, a, "o-", markersize=3, linewidth=0.8, label="$x_n$（$x_0 = 0.2$）")
    ax1.plot(steps, b, "s--", markersize=3, linewidth=0.8, label="$y_n$（$y_0 = 0.2 + 10^{-10}$）")
    ax1.set_ylabel("$x_n$, $y_n$")
    ax1.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax2.semilogy(steps, np.abs(a - b) + 1e-17, "o-", markersize=3, linewidth=0.8, color="C3", label="2 本の軌道の差")
    ax2.semilogy(steps[:35], delta * 2.0**steps[:35], color="0.4", linestyle=":", label="$10^{-10} \\times 2^n$")
    ax2.set_xlabel("$n$")
    ax2.set_ylabel("$|x_n - y_n|$")
    ax2.set_ylim(1e-11, 10.0)
    ax2.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax2.grid(True, color="0.9")
    fig.tight_layout()
    return {"divergence": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
