"""第 10 章: 片持ち梁の設計で、パレート最適解を求める。

長さ 1 m の鋼製の片持ち梁の先端に 1000 N の荷重をかけます。
断面は幅 b、高さ h の長方形です。

* 目的 1: 質量を小さくしたい (材料費・重量の削減)
* 目的 2: 先端のたわみを小さくしたい (剛性の確保)
* 制約: 根元の曲げ応力が許容応力 150 MPa 以下

2 つの目的は両立しないため、ランダムに作った設計案の中から、
どちらの目的でも他の案に負けていない案 (パレート最適解) を選びます。
図は ch10_pareto.png として保存します。

実行例::

    python ch10_pareto.py --outdir output
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

LENGTH = 1.0  # 梁の長さ [m]
FORCE = 1000.0  # 先端の荷重 [N]
YOUNG = 206e9  # 鋼のヤング率 [Pa]
DENSITY = 7850.0  # 鋼の密度 [kg/m^3]
ALLOWABLE_STRESS = 150e6  # 許容応力 [Pa]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def evaluate(b: Array, h: Array) -> tuple[Array, Array, Array]:
    """幅 b [m] と高さ h [m] から、質量・たわみ・最大応力を計算する。"""
    mass = DENSITY * b * h * LENGTH
    second_moment = b * h ** 3 / 12  # 断面二次モーメント
    deflection = FORCE * LENGTH ** 3 / (3 * YOUNG * second_moment)
    stress = FORCE * LENGTH / (b * h ** 2 / 6)  # 曲げモーメント / 断面係数
    return mass, deflection, stress


def pareto_mask(f1: Array, f2: Array) -> NDArray[np.bool_]:
    """2 つの目的 (どちらも小さいほど良い) のパレート最適解の印を返す。"""
    order = np.argsort(f1)
    mask = np.zeros(f1.size, dtype=np.bool_)
    best_f2 = np.inf
    # f1 の小さい順に見ていき、それまでより f2 が小さい案だけが残る
    for index in order:
        if f2[index] < best_f2:
            mask[index] = True
            best_f2 = f2[index]
    return mask


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--seed", type=int, default=0,
                        help="設計案を作る乱数のシード")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    b = rng.uniform(0.010, 0.050, size=3000)  # 幅 10〜50 mm
    h = rng.uniform(0.010, 0.100, size=3000)  # 高さ 10〜100 mm
    mass, deflection, stress = evaluate(b, h)

    feasible = stress <= ALLOWABLE_STRESS
    print(f"設計案 {b.size} 個のうち、応力の制約を満たす案: "
          f"{int(np.sum(feasible))} 個")

    fb, fh = b[feasible], h[feasible]
    fm, fd = mass[feasible], deflection[feasible]
    front = pareto_mask(fm, fd)
    print(f"パレート最適解: {int(np.sum(front))} 個")
    print("  質量[kg]  たわみ[mm]  幅[mm]  高さ[mm]")
    indices = np.nonzero(front)[0]
    for index in indices[np.argsort(fm[indices])][::8]:
        print(f"  {fm[index]:8.2f}  {fd[index] * 1000:10.2f}  "
              f"{fb[index] * 1000:6.1f}  {fh[index] * 1000:8.1f}")

    setup_font()
    fig = Figure(figsize=(7, 4.5), layout="constrained")
    ax = fig.add_subplot()
    ax.scatter(mass[~feasible], deflection[~feasible] * 1000, s=4,
               color="lightgray", label="応力の制約を満たさない案")
    ax.scatter(fm, fd * 1000, s=4, color="tab:blue", alpha=0.4,
               label="制約を満たす案")
    order = np.argsort(fm[front])
    ax.plot(fm[front][order], fd[front][order] * 1000, "o-",
            color="tab:red", markersize=3, label="パレート最適解")
    ax.set_yscale("log")
    ax.set_xlabel("質量 [kg]")
    ax.set_ylabel("先端のたわみ [mm]")
    ax.set_title("質量とたわみのトレードオフ")
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper right")
    fig.savefig(outdir / "ch10_pareto.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
