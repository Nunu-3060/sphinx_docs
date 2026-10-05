"""第 11 章: 寸法公差の積み上げを 3 つの方法で見積もる。

内寸 50.6 mm のケースに、4 つの部品を一列に並べて収める、という
想定です。部品とケースの寸法にはそれぞれ公差があり、残る隙間が
0.2 mm 未満になると組み立てられないものとします。

* ワーストケース法: すべての寸法が最悪の側に外れたと仮定する
* RSS 法 (二乗和平方根法): 公差を 2 乗して足し、平方根をとる
* モンテカルロ法: 各寸法を正規分布 (公差 = 3σ) とみなして乱数で試す

図は ch11_tolerance.png として保存します。

実行例::

    python ch11_tolerance.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

HOUSING = (50.6, 0.10)  # ケースの内寸と公差 [mm]
PARTS = [(10.0, 0.10), (20.0, 0.20), (15.0, 0.15), (5.0, 0.05)]
MIN_GAP = 0.2  # 組み立てに必要な最小の隙間 [mm]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--samples", type=int, default=1_000_000,
                        help="モンテカルロ法の試行回数")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    nominal_gap = HOUSING[0] - sum(size for size, _ in PARTS)
    tolerances = [HOUSING[1]] + [tol for _, tol in PARTS]
    worst = sum(tolerances)
    rss = math.sqrt(sum(tol ** 2 for tol in tolerances))
    print(f"隙間の公称値: {nominal_gap:.3f} mm")
    print(f"ワーストケース法: {nominal_gap:.3f} ± {worst:.3f} mm "
          f"(最小 {nominal_gap - worst:.3f} mm)")
    print(f"RSS 法          : {nominal_gap:.3f} ± {rss:.3f} mm "
          f"(最小 {nominal_gap - rss:.3f} mm)")

    rng = np.random.default_rng(0)
    gap = rng.normal(HOUSING[0], HOUSING[1] / 3, args.samples)
    for size, tol in PARTS:
        gap -= rng.normal(size, tol / 3, args.samples)
    defect_rate = float(np.mean(gap < MIN_GAP))
    print(f"モンテカルロ法  : 平均 {gap.mean():.3f} mm, "
          f"標準偏差 {gap.std():.4f} mm")
    print(f"  隙間が {MIN_GAP} mm 未満になる割合: {defect_rate:.4%}")

    setup_font()
    fig = Figure(figsize=(7, 4), layout="constrained")
    ax = fig.add_subplot()
    ax.hist(gap, bins=100, color="tab:blue", alpha=0.7)
    for value, label, style in (
            (nominal_gap - worst, "ワーストケースの下限", "--"),
            (nominal_gap - rss, "RSS の下限", ":"),
            (MIN_GAP, "必要な隙間", "-")):
        ax.axvline(value, color="black", linestyle=style, label=label)
    ax.set_xlabel("隙間 [mm]")
    ax.set_ylabel("度数")
    ax.set_title("隙間の分布 (モンテカルロ法)")
    ax.legend(loc="upper right")
    fig.savefig(outdir / "ch11_tolerance.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
