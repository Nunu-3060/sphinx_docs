"""第 3 章: 過学習を確かめ、交差検証でモデルの複雑さを選ぶ。

真の関係が y = sin(2πx) で、測定に雑音が乗った模擬データに、
次数の異なる多項式を当てはめます。

* 訓練データでの誤差は、次数を上げるほど小さくなる
* 訓練に使っていない検証データでの誤差は、ある次数を超えると
  大きくなる (過学習)
* 5 分割交差検証で、適切な次数を選ぶ

図は ch03_overfitting.png として保存します。

実行例::

    python ch03_overfitting.py --outdir output
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
NOISE = 0.25  # 雑音の標準偏差
DEGREES = range(0, 10)  # 試す多項式の次数


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def make_data(n: int, rng: np.random.Generator) -> tuple[Array, Array]:
    """区間 [0, 1] の一様乱数の x と、雑音を含む y を作る。"""
    x = rng.uniform(0.0, 1.0, size=n)
    y = np.sin(2 * np.pi * x) + rng.normal(0.0, NOISE, size=n)
    return x, y


def rmse(coefficients: Array, x: Array, y: Array) -> float:
    """多項式の予測値と y の差の二乗平均平方根を返す。"""
    residuals = np.polyval(coefficients, x) - y
    return float(np.sqrt(np.mean(residuals ** 2)))


def cross_validation(x: Array, y: Array, degree: int, folds: int,
                     rng: np.random.Generator) -> float:
    """k 分割交差検証で、検証誤差の平均を返す。

    データを folds 個のグループに分け、1 つを検証用、残りを訓練用に
    して当てはめることを、検証用のグループを替えながら繰り返します。
    """
    order = rng.permutation(x.size)
    errors = []
    for part in np.array_split(order, folds):
        train = np.setdiff1d(order, part)
        coefficients = np.polyfit(x[train], y[train], degree)
        errors.append(rmse(coefficients, x[part], y[part]))
    return float(np.mean(errors))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(3)
    x_train, y_train = make_data(15, rng)
    x_valid, y_valid = make_data(200, rng)

    print("次数  訓練誤差  検証誤差  5 分割交差検証")
    train_errors, valid_errors, cv_errors = [], [], []
    for degree in DEGREES:
        coefficients = np.polyfit(x_train, y_train, degree)
        train_errors.append(rmse(coefficients, x_train, y_train))
        valid_errors.append(rmse(coefficients, x_valid, y_valid))
        cv_errors.append(cross_validation(x_train, y_train, degree, 5,
                                          np.random.default_rng(0)))
        print(f"{degree:4d}  {train_errors[-1]:8.3f}  "
              f"{valid_errors[-1]:8.3f}  {cv_errors[-1]:14.3f}")
    best = int(np.argmin(cv_errors))
    print(f"交差検証で選んだ次数: {DEGREES[best]}")

    setup_font()
    fig = Figure(figsize=(10, 4), layout="constrained")
    ax_fit, ax_err = fig.subplots(1, 2)
    grid = np.linspace(0.0, 1.0, 200)
    ax_fit.plot(grid, np.sin(2 * np.pi * grid), color="gray",
                linestyle=":", label="真の関係")
    ax_fit.plot(x_train, y_train, "ko", label="訓練データ")
    for degree in (1, 3, 9):
        coefficients = np.polyfit(x_train, y_train, degree)
        ax_fit.plot(grid, np.polyval(coefficients, grid),
                    label=f"{degree} 次式")
    ax_fit.set_ylim(-2.0, 2.0)
    ax_fit.set_xlabel("x")
    ax_fit.set_ylabel("y")
    ax_fit.set_title("次数の異なる多項式の当てはめ")
    ax_fit.grid(alpha=0.3)
    ax_fit.legend(loc="lower left", fontsize=8)

    ax_err.plot(list(DEGREES), train_errors, "o-", label="訓練誤差")
    ax_err.plot(list(DEGREES), valid_errors, "s-", label="検証誤差")
    ax_err.set_yscale("log")
    ax_err.set_xlabel("多項式の次数")
    ax_err.set_ylabel("誤差 (RMSE)")
    ax_err.set_title("次数と誤差の関係")
    ax_err.grid(alpha=0.3, which="both")
    ax_err.legend(loc="upper left")
    fig.savefig(outdir / "ch03_overfitting.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
