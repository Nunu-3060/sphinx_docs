"""第 9 章: 3 点見積もりとモンテカルロ法で、開発期間の分布を求める。

順番に行う 5 つの作業のそれぞれについて、楽観値・最頻値・悲観値の
3 つの日数を見積もり、作業日数が三角分布に従うと仮定して、全体の
期間の分布を乱数で求めます。

* 最頻値を足しただけの計画は、半分以上の確率で遅れる
* 「80 % の確率で間に合う日数」を示すと、計画の確からしさが伝わる

図は ch09_schedule.png として保存します。

実行例::

    python ch09_schedule.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

# 作業名: (楽観値, 最頻値, 悲観値) [日]
TASKS: dict[str, tuple[float, float, float]] = {
    "要求定義": (3, 5, 10),
    "回路・機構の設計": (8, 10, 20),
    "ソフトウェアの実装": (10, 15, 30),
    "結合試験": (4, 5, 15),
    "環境試験と修正": (3, 5, 12),
}


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def pert_mean(low: float, mode: float, high: float) -> float:
    """PERT の期待値 (楽観値 + 4 × 最頻値 + 悲観値) / 6 を返す。"""
    return (low + 4 * mode + high) / 6


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--samples", type=int, default=100_000,
                        help="モンテカルロ法の試行回数")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    most_likely = sum(mode for _, mode, _ in TASKS.values())
    pert_total = sum(pert_mean(*estimate) for estimate in TASKS.values())
    print(f"最頻値の合計      : {most_likely:5.1f} 日")
    print(f"PERT の期待値の合計: {pert_total:5.1f} 日")

    rng = np.random.default_rng(0)
    total = np.zeros(args.samples)
    for low, mode, high in TASKS.values():
        total += rng.triangular(low, mode, high, size=args.samples)

    on_time = float(np.mean(total <= most_likely))
    print(f"最頻値の合計 ({most_likely:.0f} 日) 以内に終わる確率: "
          f"{on_time:.0%}")
    percentiles = {p: float(np.percentile(total, p)) for p in (50, 80, 95)}
    for p, days in percentiles.items():
        print(f"{p:3d} % の確率で終わる日数: {days:5.1f} 日")

    setup_font()
    fig = Figure(figsize=(7, 4), layout="constrained")
    ax = fig.add_subplot()
    ax.hist(total, bins=80, color="tab:blue", alpha=0.7)
    ax.axvline(most_likely, color="black", linestyle="-",
               label=f"最頻値の合計 {most_likely:.0f} 日")
    for (p, days), style in zip(percentiles.items(), [":", "--", "-."]):
        ax.axvline(days, color="tab:red", linestyle=style,
                   label=f"{p} % 点 {days:.0f} 日")
    ax.set_xlabel("全体の期間 [日]")
    ax.set_ylabel("度数")
    ax.set_title("開発期間の分布 (モンテカルロ法)")
    ax.legend(loc="upper right")
    fig.savefig(outdir / "ch09_schedule.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
