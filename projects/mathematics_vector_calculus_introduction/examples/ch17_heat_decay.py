"""1 次元の熱伝導方程式の厳密解で、温度の山がならされていく様子を描く.

使い方: python ch17_heat_decay.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

ALPHA = 0.01  # 温度拡散率 [m^2/s]
LENGTH = 1.0  # 棒の長さ [m]


def temperature(x: NDArray[np.float64], t: float) -> NDArray[np.float64]:
    """両端を 0 に保った棒の温度. 2 つの正弦波（モード）の重ね合わせ.

    sin(n pi x / L) exp(-alpha (n pi / L)^2 t) は、どの n でも熱伝導方程式を満たす。
    """
    result = np.zeros_like(x)
    for n, amplitude in ((1, 1.0), (3, 0.5)):
        kn = n * np.pi / LENGTH
        result += amplitude * np.sin(kn * x) * np.exp(-ALPHA * kn**2 * t)
    return result


def create_figure() -> Figure:
    """いくつかの時刻での温度分布を重ねて描く."""
    x = np.linspace(0.0, LENGTH, 201)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    for i, t in enumerate((0.0, 1.0, 3.0, 10.0, 30.0)):
        ax.plot(x, temperature(x, t), color=f"C{i}", label=f"$t = {t:g}$ s")
    ax.set_xlabel("位置 $x$ [m]")
    ax.set_ylabel("温度 $T$（基準からの差）")
    ax.set_title("熱伝導による温度分布の変化")
    ax.grid(True, color="0.9")
    ax.legend()
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
