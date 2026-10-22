"""2 次元のベクトル場を、渦なしの成分と発散のない成分の和として組み立てて描く.

使い方: python ch16_helmholtz.py
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

Array = NDArray[np.float64]


def potential(x: Array, y: Array) -> Array:
    """スカラーポテンシャル φ = -exp(-((x - 1)^2 + y^2))（点 (1, 0) の周りの湧き出し）."""
    return -np.exp(-((x - 1) ** 2 + y**2))


def stream(x: Array, y: Array) -> Array:
    """ベクトルポテンシャルの z 成分 ψ = exp(-((x + 1)^2 + y^2))（点 (-1, 0) の周りの渦）."""
    return np.exp(-((x + 1) ** 2 + y**2))


def components(x: Array, y: Array) -> tuple[Array, Array, Array, Array]:
    """渦なしの成分 ∇φ と、発散のない成分 ∇×(ψ e_z) = (∂ψ/∂y, -∂ψ/∂x) を返す."""
    phi = potential(x, y)
    psi = stream(x, y)
    gx, gy = -2 * (x - 1) * phi, -2 * y * phi  # ∇φ
    sx, sy = -2 * y * psi, 2 * (x + 1) * psi  # (∂ψ/∂y, -∂ψ/∂x)
    return gx, gy, sx, sy


def create_figure() -> Figure:
    """渦なしの成分、発散のない成分、その和の 3 つを並べて描く."""
    xx, yy = vc_plot.mesh((-2.5, 2.5), (-2.0, 2.0), 17)
    gx, gy, sx, sy = components(xx, yy)
    panels = [
        (gx, gy, r"渦なしの成分 $\nabla\phi$"),
        (sx, sy, r"発散のない成分 $\nabla\times(\psi\,\mathbf{e}_z)$"),
        (gx + sx, gy + sy, r"和 $\mathbf{F}$"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8))
    for ax, (u, v, title) in zip(axes, panels):
        vc_plot.setup_plane(ax, (-2.5, 2.5), (-2.0, 2.0))
        ax.quiver(xx, yy, u, v, color="C0", scale=12, width=0.005)
        ax.set_title(title)
    fig.tight_layout()
    return fig


def report() -> None:
    """各成分の発散と回転を SymPy で求め、分解の性質を確かめる."""
    x, y = sp.symbols("x y", real=True)
    phi = -sp.exp(-((x - 1) ** 2 + y**2))
    psi = sp.exp(-((x + 1) ** 2 + y**2))
    gx, gy = sp.diff(phi, x), sp.diff(phi, y)
    sx, sy = sp.diff(psi, y), -sp.diff(psi, x)

    def div(fx: sp.Expr, fy: sp.Expr) -> sp.Expr:
        return sp.simplify(sp.diff(fx, x) + sp.diff(fy, y))

    def rot_z(fx: sp.Expr, fy: sp.Expr) -> sp.Expr:
        return sp.simplify(sp.diff(fy, x) - sp.diff(fx, y))

    laplacian_phi = sp.diff(phi, x, 2) + sp.diff(phi, y, 2)
    laplacian_psi = sp.diff(psi, x, 2) + sp.diff(psi, y, 2)
    print(f"渦なしの成分の回転     : {rot_z(gx, gy)}")
    print(f"発散のない成分の発散   : {div(sx, sy)}")
    print(f"和の発散 - ∇²φ         : {sp.simplify(div(gx + sx, gy + sy) - laplacian_phi)}")
    print(f"和の回転の z 成分 + ∇²ψ : {sp.simplify(rot_z(gx + sx, gy + sy) + laplacian_psi)}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
