"""本文で使う模式図を matplotlib で描く。conf.py からビルド時に呼び出される。"""

import math
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Arc, Polygon, Wedge  # noqa: E402

ARROW = {"arrowstyle": "-|>", "lw": 1.6, "mutation_scale": 14}


def _arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], color: str = "black") -> None:
    ax.annotate("", xy=end, xytext=start, arrowprops={**ARROW, "color": color})


def _unit(angle_deg: float) -> tuple[float, float]:
    """鉛直上向きから時計回りに angle_deg 度回した単位ベクトル。"""
    a = math.radians(angle_deg)
    return math.sin(a), math.cos(a)


def _finish(fig: Figure, output: Path) -> None:
    fig.tight_layout()
    fig.savefig(output, dpi=120)
    plt.close(fig)


def plot_solid_angle(output: Path) -> None:
    """立体角（左）と投影面積（右）の模式図。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 3.6))

    # 左：単位球（の断面）と、球面上の微小面積が張る立体角
    ax1.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=180, color="gray", lw=1.2))
    ax1.add_patch(Wedge((0, 0), 1.0, 55, 75, color="tab:orange", alpha=0.35))
    ax1.add_patch(Arc((0, 0), 2, 2, theta1=55, theta2=75, color="tab:orange", lw=4))
    for angle in (55, 75):
        x, y = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ax1.plot([0, 1.35 * x], [0, 1.35 * y], color="tab:orange", lw=1, linestyle="--")
    ax1.plot([-1.2, 1.2], [0, 0], color="black", lw=1)
    ax1.plot(0, 0, "ko", ms=4)
    ax1.text(0.05, -0.15, "center", fontsize=9)
    ax1.text(0.72, 0.62, "$dA$ on\nunit sphere", fontsize=10, color="tab:orange")
    ax1.text(0.1, 0.45, r"$d\omega$", fontsize=13, color="tab:orange")
    ax1.text(-1.15, 0.85, "unit sphere\n(radius 1)", fontsize=9, color="gray")
    ax1.set_title(r"Solid angle $d\omega$ = area on the unit sphere", fontsize=10)
    ax1.set_xlim(-1.3, 1.4)
    ax1.set_ylim(-0.3, 1.45)

    # 右：面に斜めから当たる光束と投影面積 dA cosθ
    ax2.plot([-1.2, 1.2], [0, 0], color="black", lw=1)
    ax2.plot([-0.5, 0.5], [0, 0], color="tab:blue", lw=5)
    ax2.text(-0.12, -0.2, r"$dA$", fontsize=12, color="tab:blue")
    _arrow(ax2, (0, 0), (0, 1.0))
    ax2.text(0.04, 1.02, r"$\mathbf{n}$", fontsize=12)
    theta = 50.0
    dx, dy = _unit(-theta)
    for offset in (-0.5, 0.5):
        ax2.plot([offset, offset + 1.9 * dx], [0, 1.9 * dy], color="tab:red", lw=1, linestyle="--")
    # 光束に垂直な断面（投影面積）
    px, py = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    c0 = (-0.5 + 0.9 * dx, 0.9 * dy)
    ax2.plot([c0[0], c0[0] + px * math.cos(math.radians(theta))],
             [c0[1], c0[1] + py * math.cos(math.radians(theta))], color="tab:red", lw=4)
    ax2.text(-1.45, 1.4, r"projected area $dA\cos\theta$", fontsize=10, color="tab:red")
    _arrow(ax2, (0.0 + 1.25 * dx, 1.25 * dy), (0.15 * dx, 0.15 * dy), color="tab:red")
    ax2.add_patch(Arc((0, 0), 0.7, 0.7, theta1=90, theta2=90 + theta, color="black"))
    ax2.text(-0.2, 0.42, r"$\theta$", fontsize=12)
    ax2.set_title("Light arriving at an angle spreads over a larger area", fontsize=10)
    ax2.set_xlim(-1.5, 1.3)
    ax2.set_ylim(-0.3, 1.6)

    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")
    _finish(fig, output)


def plot_snell(output: Path) -> None:
    """反射と屈折の模式図。"""
    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.add_patch(Polygon([(-1.5, 0), (1.5, 0), (1.5, -1.3), (-1.5, -1.3)], color="tab:blue", alpha=0.12))
    ax.plot([-1.5, 1.5], [0, 0], color="black", lw=1)
    ax.plot([0, 0], [-1.25, 1.25], color="gray", lw=1, linestyle="--")
    theta1, n1, n2 = 50.0, 1.0, 1.5
    theta2 = math.degrees(math.asin(n1 * math.sin(math.radians(theta1)) / n2))
    ix, iy = _unit(-theta1)
    _arrow(ax, (1.2 * ix, 1.2 * iy), (0, 0))
    rx, ry = _unit(theta1)
    _arrow(ax, (0, 0), (1.2 * rx, 1.2 * ry), color="tab:orange")
    tx, ty = _unit(180 - theta2)
    _arrow(ax, (0, 0), (1.2 * tx, 1.2 * ty), color="tab:green")
    ax.add_patch(Arc((0, 0), 0.8, 0.8, theta1=90, theta2=90 + theta1))
    ax.add_patch(Arc((0, 0), 0.8, 0.8, theta1=90 - theta1, theta2=90))
    ax.add_patch(Arc((0, 0), 0.8, 0.8, theta1=270, theta2=270 + theta2))
    ax.text(-0.3, 0.5, r"$\theta_1$", fontsize=12)
    ax.text(0.17, 0.5, r"$\theta_1$", fontsize=12)
    ax.text(0.1, -0.6, r"$\theta_2$", fontsize=12)
    ax.text(-1.25, 1.0, "incident", fontsize=10)
    ax.text(0.75, 1.0, "reflected", fontsize=10, color="tab:orange")
    ax.text(0.5, -1.15, "refracted", fontsize=10, color="tab:green")
    ax.text(-1.45, 0.08, r"medium 1 ($n_1$ = 1.0, air)", fontsize=9)
    ax.text(-1.45, -0.2, r"medium 2 ($n_2$ = 1.5, glass)", fontsize=9)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    _finish(fig, output)


def plot_microfacets(output: Path) -> None:
    """マイクロファセットの模式図。ハーフベクトルと同じ向きの微小面だけが光を観測者へ反射する。"""
    rng = np.random.default_rng(3)
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    xs = np.linspace(-3.0, 3.0, 25)
    ys = rng.uniform(-0.18, 0.18, len(xs))
    ys[0] = ys[-1] = 0.0
    ax.add_patch(Polygon(np.column_stack([np.r_[xs, 3.0, -3.0], np.r_[ys, -0.6, -0.6]]),
                         color="tab:gray", alpha=0.25))
    ax.plot(xs, ys, color="black", lw=1.2)

    view = np.array(_unit(35.0))
    light = np.array(_unit(-50.0))
    half = (view + light) / np.linalg.norm(view + light)
    for k in range(len(xs) - 1):
        p0 = np.array([xs[k], ys[k]])
        p1 = np.array([xs[k + 1], ys[k + 1]])
        tangent = (p1 - p0) / np.linalg.norm(p1 - p0)
        normal = np.array([-tangent[1], tangent[0]])
        mid = (p0 + p1) / 2.0
        aligned = float(normal @ half) > 0.995
        color = "tab:red" if aligned else "tab:blue"
        if aligned:
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="tab:red", lw=3)
        _arrow(ax, (mid[0], mid[1]), (mid[0] + 0.45 * normal[0], mid[1] + 0.45 * normal[1]), color=color)

    origin = (0.0, 1.0)
    _arrow(ax, (origin[0] + 1.0 * light[0], origin[1] + 1.0 * light[1]), origin, color="black")
    _arrow(ax, origin, (origin[0] + 1.0 * view[0], origin[1] + 1.0 * view[1]), color="black")
    _arrow(ax, origin, (origin[0] + 0.9 * half[0], origin[1] + 0.9 * half[1]), color="tab:red")
    ax.text(origin[0] + 1.05 * light[0] - 0.4, origin[1] + 1.05 * light[1], r"$\omega_i$ (to light)", fontsize=11)
    ax.text(origin[0] + 1.05 * view[0], origin[1] + 1.05 * view[1], r"$\omega_o$ (to eye)", fontsize=11)
    ax.text(origin[0] + 0.95 * half[0] - 0.1, origin[1] + 0.95 * half[1] + 0.05, r"$\mathbf{h}$",
            fontsize=12, color="tab:red")
    ax.text(-3.0, -0.5, "red: microfacets whose normal equals the half vector h", fontsize=9, color="tab:red")
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-0.65, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _finish(fig, output)


def plot_rendering_equation(output: Path) -> None:
    """レンダリング方程式の各量を示す模式図。"""
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.add_patch(Polygon([(-2.0, 0), (2.0, 0), (2.0, -0.4), (-2.0, -0.4)], color="tab:gray", alpha=0.25))
    ax.plot([-2.0, 2.0], [0, 0], color="black", lw=1)
    ax.add_patch(Arc((0, 0), 2.6, 2.6, theta1=0, theta2=180, color="gray", lw=1, linestyle="--"))
    ax.plot(0, 0, "ko", ms=4)
    ax.text(0.06, -0.25, r"$\mathbf{x}$", fontsize=12)
    _arrow(ax, (0, 0), (0, 1.0))
    ax.text(0.05, 1.02, r"$\mathbf{n}$", fontsize=12)

    for angle in (-70.0, -20.0, 15.0, 60.0):
        dx, dy = _unit(angle)
        _arrow(ax, (1.3 * dx, 1.3 * dy), (0.12 * dx, 0.12 * dy), color="tab:blue")
    dx, dy = _unit(-45.0)
    _arrow(ax, (1.3 * dx, 1.3 * dy), (0.12 * dx, 0.12 * dy), color="tab:red")
    ax.text(1.4 * dx - 0.35, 1.4 * dy, r"$L_i(\mathbf{x}, \omega_i)$", fontsize=11, color="tab:red")
    ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=90, theta2=135))
    ax.text(-0.33, 0.55, r"$\theta_i$", fontsize=11)

    ox, oy = _unit(45.0)
    _arrow(ax, (0, 0), (1.6 * ox, 1.6 * oy), color="tab:green")
    ax.text(1.6 * ox + 0.05, 1.6 * oy, r"$L_o(\mathbf{x}, \omega_o)$", fontsize=11, color="tab:green")
    ax.text(-1.95, 1.25, "incoming light from all directions\n" r"over the hemisphere $\Omega$",
            fontsize=9, color="tab:blue")
    ax.set_xlim(-2.0, 2.4)
    ax.set_ylim(-0.4, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")
    _finish(fig, output)


def main() -> None:
    out = Path(".")
    plot_solid_angle(out / "solid_angle.png")
    plot_snell(out / "snell.png")
    plot_microfacets(out / "microfacets.png")
    plot_rendering_equation(out / "rendering_equation.png")


if __name__ == "__main__":
    main()
