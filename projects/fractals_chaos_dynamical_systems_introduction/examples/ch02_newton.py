"""ニュートン法を写像の反復として見る（2 の平方根を求める）.

使い方: python ch02_newton.py [--save DIR]
"""

from decimal import Decimal, getcontext

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util
from ch02_cobweb import cobweb


def newton_map(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """g(x) = x^2 - 2 に対するニュートン法の写像 N(x) = x - g(x) / g'(x) = (x + 2 / x) / 2."""
    return (x + 2.0 / x) / 2.0


def create_figures() -> dict[str, Figure]:
    """ニュートン法の写像のクモの巣図（cobweb）を作る."""
    fig, ax = plt.subplots(figsize=(5.0, 5.0))
    cobweb(ax, newton_map, 3.2, 5, 0.5, 3.5)
    ax.set_title("$N(x) = (x + 2/x)/2$")
    fig.tight_layout()
    return {"cobweb": fig}


def report() -> None:
    """50 桁の精度で反復し、各ステップで正しい桁数がどう増えるかを表示する."""
    getcontext().prec = 60
    exact = Decimal(2).sqrt()
    x = Decimal(1)
    print(" n  x_n                                                    誤差")
    for n in range(7):
        error = abs(x - exact)
        print(f"{n:2d}  {x:.50f}  {float(error):.1e}")
        x = (x + 2 / x) / 2


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
