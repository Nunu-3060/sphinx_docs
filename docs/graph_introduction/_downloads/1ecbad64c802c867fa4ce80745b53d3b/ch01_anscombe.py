"""アンスコムの例: 要約統計量が同じでも、グラフにすると違いが分かる.

4 組のデータは、平均、分散、相関係数、回帰直線がほぼ同じである。
実行すると要約統計量を表示し、4 組の散布図を描く。

使い方: python ch01_anscombe.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

# Anscombe (1973) のデータ。1 組目から 3 組目は x が共通である。
X_COMMON = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
DATASETS = {
    "I": (X_COMMON,
          [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82,
           5.68]),
    "II": (X_COMMON,
           [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26,
            4.74]),
    "III": (X_COMMON,
            [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42,
             5.73]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
           [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91,
            6.89]),
}


def print_statistics() -> None:
    """4 組のデータの要約統計量を表示する."""
    print("組   x平均  x分散  y平均  y分散  相関係数")
    for name, (x_values, y_values) in DATASETS.items():
        x = np.array(x_values, dtype=float)
        y = np.array(y_values, dtype=float)
        r = np.corrcoef(x, y)[0, 1]
        print(f"{name:4} {x.mean():6.2f} {x.var(ddof=1):6.2f} "
              f"{y.mean():6.2f} {y.var(ddof=1):6.2f} {r:8.3f}")


def create_figure() -> Figure:
    """4 組のデータの散布図に回帰直線を重ねて描く."""
    fig, axes = plt.subplots(2, 2, figsize=(7, 5.5), sharex=True,
                             sharey=True)
    line_x = np.array([3.0, 20.0])
    for ax, (name, (x_values, y_values)) in zip(axes.flat, DATASETS.items()):
        x = np.array(x_values, dtype=float)
        y = np.array(y_values, dtype=float)
        slope, intercept = np.polyfit(x, y, 1)
        ax.plot(line_x, slope * line_x + intercept, color="C1", zorder=1)
        ax.scatter(x, y, color="C0", zorder=2)
        ax.set_title(f"データ {name}")
        ax.grid(alpha=0.3)
    for ax in axes[1]:
        ax.set_xlabel("x")
    for ax in axes[:, 0]:
        ax.set_ylabel("y")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    print_statistics()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
