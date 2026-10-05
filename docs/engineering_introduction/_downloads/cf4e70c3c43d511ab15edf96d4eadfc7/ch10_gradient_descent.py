"""第 10 章: 最急降下法で関数の最小値を探し、学習率の影響を確かめる。

目的関数 f(x, y) = x^2 + 10 y^2 は、y 方向にだけ急な「細長い谷」の
形をしています。最急降下法の学習率 (1 回に進む幅の係数) を変えて、

* 小さすぎると収束が遅い
* 大きいとジグザグに進む
* 大きすぎると発散する (この関数では 0.1 が境目)

ことを確かめます。図は ch10_gradient_descent.png として保存します。

実行例::

    python ch10_gradient_descent.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

Array = NDArray[np.float64]
START = np.array([-9.0, 2.0])  # 探索の開始点


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def objective(p: Array) -> float:
    """目的関数 f(x, y) = x^2 + 10 y^2。"""
    return float(p[0] ** 2 + 10 * p[1] ** 2)


def gradient(p: Array) -> Array:
    """目的関数の勾配 (2x, 20y)。"""
    return np.array([2 * p[0], 20 * p[1]])


def gradient_descent(rate: float, max_iter: int = 1000,
                     tol: float = 1e-6) -> tuple[Array, str]:
    """最急降下法で探索し、通った点の列と結果の説明を返す。

    勾配の大きさが tol 未満になったら収束、目的関数が 1e6 を超えたら
    発散とみなします。
    """
    p = START.copy()
    path = [p.copy()]
    for i in range(1, max_iter + 1):
        p = p - rate * gradient(p)
        path.append(p.copy())
        if np.linalg.norm(gradient(p)) < tol:
            return np.array(path), f"{i} 回で収束"
        if objective(p) > 1e6:
            return np.array(path), f"{i} 回で発散 (f = {objective(p):.3g})"
    return np.array(path), f"{max_iter} 回で収束せず"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    setup_font()
    fig = Figure(figsize=(8, 4.2), layout="constrained")
    ax = fig.add_subplot()
    xs = np.linspace(-10, 10, 200)
    ys = np.linspace(-3.5, 3.5, 200)
    grid_x, grid_y = np.meshgrid(xs, ys)
    ax.contour(grid_x, grid_y, grid_x ** 2 + 10 * grid_y ** 2,
               levels=[1, 5, 15, 30, 60, 100, 150], colors="lightgray")

    for rate, color in ((0.02, "tab:blue"), (0.09, "tab:orange"),
                        (0.105, "tab:red")):
        path, result = gradient_descent(rate)
        print(f"学習率 {rate:5.3f}: {result}")
        shown = path[:15]
        ax.plot(shown[:, 0], shown[:, 1], "o-", markersize=3, color=color,
                label=f"学習率 {rate}")
    ax.plot(0, 0, "k*", markersize=12, label="最小点")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("最急降下法の軌跡 (最初の 15 回)")
    ax.legend(loc="lower right", fontsize=8)
    fig.savefig(outdir / "ch10_gradient_descent.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
