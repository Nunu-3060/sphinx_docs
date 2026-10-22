"""最小二乗法で、測定データに直線と 2 次式を当てはめる.

データは、真の関係に正規分布の誤差を加えて作った架空のものである。
係数は、正規方程式 a^T a c = a^T y を解いて求める。

使い方: python ch09_least_squares.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

Vector = NDArray[np.float64]


def make_data() -> tuple[Vector, Vector, Vector, Vector]:
    """直線用と 2 次式用の架空の測定データを作る."""
    rng = np.random.default_rng(seed=1)
    x1 = np.linspace(0.0, 10.0, 15)
    y1 = 1.5 + 0.8 * x1 + rng.normal(0.0, 0.8, x1.size)
    x2 = np.linspace(-1.0, 5.0, 20)
    y2 = 0.5 * x2**2 - 2.0 * x2 + 3.0 + rng.normal(0.0, 0.5, x2.size)
    return x1, y1, x2, y2


def fit_polynomial(x: Vector, y: Vector, degree: int) -> Vector:
    """degree 次の多項式を当てはめ、係数を次数の低い順に返す."""
    a = np.vander(x, degree + 1, increasing=True)  # 列が 1, x, x^2, ... の行列
    return np.linalg.solve(a.T @ a, a.T @ y)  # 正規方程式を解く


def report() -> None:
    """正規方程式と np.linalg.lstsq で求めた係数を表示する."""
    x1, y1, x2, y2 = make_data()
    with np.printoptions(precision=4, suppress=True):
        print("直線 c0 + c1 x の係数（正規方程式）:", fit_polynomial(x1, y1, 1))
        a = np.vander(x1, 2, increasing=True)
        print("直線 c0 + c1 x の係数（lstsq）:    ", np.linalg.lstsq(a, y1)[0])
        print("2 次式 c0 + c1 x + c2 x^2 の係数:  ", fit_polynomial(x2, y2, 2))


def create_figure() -> Figure:
    """データと、当てはめた直線、2 次式を描く."""
    x1, y1, x2, y2 = make_data()
    fig, (ax_line, ax_quad) = plt.subplots(1, 2, figsize=(10, 4))

    c = fit_polynomial(x1, y1, 1)
    fitted = c[0] + c[1] * x1
    ax_line.vlines(x1, y1, fitted, color="C3", linewidth=1, label="残差")
    ax_line.plot(x1, y1, "o", color="C0", label="データ")
    ax_line.plot(x1, fitted, color="C1", label=f"y = {c[0]:.2f} + {c[1]:.2f} x")
    ax_line.set_title("直線の当てはめ")
    ax_line.legend()

    c = fit_polynomial(x2, y2, 2)
    xs = np.linspace(-1.0, 5.0, 100)
    ax_quad.plot(x2, y2, "o", color="C0", label="データ")
    sign1 = "+" if c[1] >= 0 else "-"
    sign2 = "+" if c[2] >= 0 else "-"
    label = f"y = {c[0]:.2f} {sign1} {abs(c[1]):.2f} x {sign2} {abs(c[2]):.2f} x²"
    ax_quad.plot(xs, c[0] + c[1] * xs + c[2] * xs**2, color="C1", label=label)
    ax_quad.set_title("2 次式の当てはめ")
    ax_quad.legend()

    for ax in (ax_line, ax_quad):
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, color="0.9")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
