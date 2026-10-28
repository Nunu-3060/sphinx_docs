"""2 次元の連続時間の力学系の相図（相平面上の流れの様子）を描く.

* 線形系 x' = A x の平衡点（原点）を、行列 A の固有値で 4 種類に分類する
* 非線形系の例として、減衰のない振り子 θ'' = -sin θ の相図を描く

使い方: python ch03_phase_portrait.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

# 平衡点の種類と、その例になる行列 A
LINEAR_EXAMPLES: list[tuple[str, NDArray[np.float64]]] = [
    ("安定結節点", np.array([[-1.0, 0.0], [0.0, -3.0]])),
    ("鞍点", np.array([[1.0, 0.0], [0.0, -1.0]])),
    ("安定渦状点", np.array([[-0.3, -1.0], [1.0, -0.3]])),
    ("中心", np.array([[0.0, -1.0], [1.0, 0.0]])),
]


def format_eigenvalues(a: NDArray[np.float64]) -> str:
    """行列 a の固有値を、図の見出しに使う文字列にする."""
    values = np.linalg.eigvals(a)
    if abs(values[0].imag) > 1e-12:
        # 複素共役の組は「実部 ± 虚部 i」の形にまとめる
        re, im = values[0].real, abs(values[0].imag)
        imag = "i" if im == 1.0 else f"{im:g}i"
        return f"固有値 ±{imag}" if re == 0.0 else f"固有値 {re:g} ± {imag}"
    parts = [f"{v.real:g}" for v in values]
    return "固有値 " + ", ".join(parts)


def create_figures() -> dict[str, Figure]:
    """線形系の 4 種類の相図（linear）と、振り子の相図（pendulum）を作る."""
    grid = np.linspace(-2.0, 2.0, 41)
    x, y = np.meshgrid(grid, grid)
    fig1, axes = plt.subplots(1, 4, figsize=(14.0, 3.9))
    for ax, (name, a) in zip(axes, LINEAR_EXAMPLES):
        u = a[0, 0] * x + a[0, 1] * y
        v = a[1, 0] * x + a[1, 1] * y
        ax.streamplot(x, y, u, v, density=0.9, color="C0", linewidth=0.8, arrowsize=0.8)
        ax.plot(0.0, 0.0, "o", color="C3")
        ax.set_title(f"{name}\n{format_eigenvalues(a)}", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-2.0, 2.0)
        ax.set_ylim(-2.0, 2.0)
        ax.set_xticks([])
        ax.set_yticks([])
    fig1.tight_layout()

    theta = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 81)
    omega = np.linspace(-3.0, 3.0, 61)
    th, om = np.meshgrid(theta, omega)
    fig2, ax2 = plt.subplots(figsize=(9.0, 4.4))
    ax2.streamplot(th, om, om, -np.sin(th), density=1.2, color="0.55", linewidth=0.7, arrowsize=0.7)
    # エネルギー E = ω^2 / 2 - cos θ が 1 になる曲線（セパラトリクス）は、揺れと回転の境目になる
    t = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 400)
    separatrix = 2.0 * np.abs(np.cos(t / 2.0))
    ax2.plot(t, separatrix, color="C3", linewidth=1.8, label="セパラトリクス")
    ax2.plot(t, -separatrix, color="C3", linewidth=1.8)
    ax2.plot([-2.0 * np.pi, 0.0, 2.0 * np.pi], [0.0, 0.0, 0.0], "o", color="C0", label="中心（真下に静止）")
    ax2.plot([-np.pi, np.pi], [0.0, 0.0], "x", color="k", markersize=9, mew=2, label="鞍点（真上に静止）")
    ax2.set_xlim(-2.0 * np.pi, 2.0 * np.pi)
    ax2.set_ylim(-3.0, 3.0)
    ax2.set_xticks(np.arange(-2, 3) * np.pi, ["$-2\\pi$", "$-\\pi$", "$0$", "$\\pi$", "$2\\pi$"])
    ax2.set_xlabel("角度 $\\theta$")
    ax2.set_ylabel("角速度 $\\omega$")
    ax2.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig2.tight_layout()
    return {"linear": fig1, "pendulum": fig2}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
