"""本文で使う図を matplotlib で生成する。conf.py から呼び出される。"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.patches import Circle, Rectangle  # noqa: E402

FILL = "#5b9bd5"
EDGE = "#1f3b57"


def make_venn(path: Path) -> None:
    """和・積・差・対称差・補集合のベン図を 1 枚にまとめて出力する。"""
    ca, cb, r = (-0.45, 0.0), (0.45, 0.0), 0.8
    xs, ys = np.meshgrid(np.linspace(-2.0, 2.0, 801), np.linspace(-1.25, 1.25, 501))
    in_a = (xs - ca[0]) ** 2 + (ys - ca[1]) ** 2 <= r**2
    in_b = (xs - cb[0]) ** 2 + (ys - cb[1]) ** 2 <= r**2

    panels: list[tuple[str, np.ndarray]] = [
        (r"$A \cup B$", in_a | in_b),
        (r"$A \cap B$", in_a & in_b),
        (r"$A \setminus B$", in_a & ~in_b),
        (r"$A \triangle B$", in_a ^ in_b),
        (r"$A^{c}$", ~in_a),
    ]

    fig, axes = plt.subplots(1, len(panels), figsize=(15, 3.2))
    for ax, (title, mask) in zip(axes, panels):
        image = np.where(mask, 1.0, 0.0)
        ax.imshow(image, extent=(-2.0, 2.0, -1.25, 1.25), origin="lower",
                  cmap=ListedColormap(["white", FILL]), vmin=0, vmax=1)
        ax.add_patch(Rectangle((-2.0, -1.25), 4.0, 2.5, fill=False, edgecolor=EDGE, linewidth=2))
        ax.add_patch(Circle(ca, r, fill=False, edgecolor=EDGE, linewidth=1.5))
        ax.add_patch(Circle(cb, r, fill=False, edgecolor=EDGE, linewidth=1.5))
        ax.text(-1.25, 0.95, "$A$", fontsize=16, ha="center", va="center")
        ax.text(1.25, 0.95, "$B$", fontsize=16, ha="center", va="center")
        ax.text(-1.8, 1.0, "$U$", fontsize=14, ha="center", va="center")
        ax.set_title(title, fontsize=18)
        ax.set_xlim(-2.05, 2.05)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)


def make_diagonal(path: Path) -> None:
    """対角線論法の表を出力する。"""
    rows = [
        [0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]
    n = len(rows)
    d = [1 - rows[i][i] for i in range(n)]

    fig, ax = plt.subplots(figsize=(6.4, 5.0))
    for i, row in enumerate(rows):
        y = n - i
        ax.text(-0.6, y, f"$s_{i}$", fontsize=16, ha="center", va="center")
        for j, bit in enumerate(row):
            if i == j:
                ax.add_patch(Rectangle((j - 0.4, y - 0.4), 0.8, 0.8, color=FILL, alpha=0.5))
            ax.text(j, y, str(bit), fontsize=16, ha="center", va="center")
        ax.text(n - 0.2, y, r"$\cdots$", fontsize=16, ha="center", va="center")
    ax.text((n - 1) / 2, 0.45, r"$\vdots$", fontsize=16, ha="center", va="center")
    y = -0.6
    ax.text(-0.6, y, "$d$", fontsize=16, ha="center", va="center", color="#c00000")
    for j, bit in enumerate(d):
        ax.add_patch(Rectangle((j - 0.4, y - 0.4), 0.8, 0.8, fill=False, edgecolor="#c00000", linewidth=1.5))
        ax.text(j, y, str(bit), fontsize=16, ha="center", va="center", color="#c00000")
    ax.text(n - 0.2, y, r"$\cdots$", fontsize=16, ha="center", va="center", color="#c00000")
    for j in range(n):
        ax.text(j, n + 0.8, f"${j}$", fontsize=13, ha="center", va="center", color="gray")
    ax.set_xlim(-1.1, n + 0.3)
    ax.set_ylim(-1.2, n + 1.2)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=100, bbox_inches="tight")
    plt.close(fig)


def make_all(out_dir: Path) -> None:
    """すべての図を out_dir に出力する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    make_venn(out_dir / "venn.png")
    make_diagonal(out_dir / "diagonal.png")


if __name__ == "__main__":
    make_all(Path(__file__).resolve().parent.parent / "_figures")
