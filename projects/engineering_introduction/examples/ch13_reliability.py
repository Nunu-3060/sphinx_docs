"""第 13 章: システムの信頼度とアベイラビリティを計算する。

1. 直列系・並列系・k-out-of-n 系の信頼度
2. MTBF と MTTR からアベイラビリティを求め、年間の停止時間に換算する
3. 故障率の時間変化 (バスタブ曲線) を図にする (ch13_bathtub.png)

実行例::

    python ch13_reliability.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

HOURS_PER_YEAR = 365 * 24

Array = NDArray[np.float64]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def series(reliabilities: list[float]) -> float:
    """直列系の信頼度 (すべてが動作して初めて系が動作する)。"""
    return math.prod(reliabilities)


def parallel(reliabilities: list[float]) -> float:
    """並列系の信頼度 (1 つでも動作すれば系が動作する)。"""
    return 1 - math.prod(1 - r for r in reliabilities)


def k_out_of_n(k: int, n: int, r: float) -> float:
    """同じ信頼度 r の要素 n 個のうち、k 個以上が動作する確率。"""
    return sum(math.comb(n, i) * r ** i * (1 - r) ** (n - i)
               for i in range(k, n + 1))


def availability(mtbf: float, mttr: float) -> float:
    """アベイラビリティ (稼働率) MTBF / (MTBF + MTTR)。"""
    return mtbf / (mtbf + mttr)


def plot_bathtub(path: Path) -> None:
    """3 つのワイブル分布の故障率を足し合わせてバスタブ曲線を描く。"""

    def weibull_hazard(t: Array, shape: float, scale: float) -> Array:
        result: Array = (shape / scale) * (t / scale) ** (shape - 1)
        return result

    t = np.linspace(0.05, 10.0, 500)
    early = weibull_hazard(t, 0.5, 20.0)  # 初期故障 (形状パラメーター < 1)
    random_ = np.full_like(t, 0.1)  # 偶発故障 (一定)
    wear = weibull_hazard(t, 5.0, 9.0)  # 摩耗故障 (形状パラメーター > 1)

    fig = Figure(figsize=(7, 4), layout="constrained")
    ax = fig.add_subplot()
    ax.plot(t, early + random_ + wear, linewidth=2.5, label="故障率の合計")
    ax.plot(t, early, "--", label="初期故障")
    ax.plot(t, random_, "--", label="偶発故障")
    ax.plot(t, wear, "--", label="摩耗故障")
    ax.set_ylim(0, 0.8)
    ax.set_xlabel("使用時間 (相対値)")
    ax.set_ylabel("故障率 (相対値)")
    ax.set_title("バスタブ曲線")
    ax.text(0.4, 0.62, "初期故障期")
    ax.text(4.0, 0.62, "偶発故障期")
    ax.text(8.2, 0.62, "摩耗故障期")
    ax.grid(alpha=0.3)
    ax.legend(loc="center", bbox_to_anchor=(0.45, 0.47), ncols=2)
    fig.savefig(path, dpi=120)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("1. 信頼度 (各要素の信頼度 0.95)")
    print(f"   直列 3 個      : {series([0.95] * 3):.4f}")
    print(f"   並列 2 個      : {parallel([0.95] * 2):.4f}")
    print(f"   2-out-of-3     : {k_out_of_n(2, 3, 0.95):.4f}")

    print("2. アベイラビリティと年間の停止時間")
    a = availability(mtbf=2000.0, mttr=4.0)
    print(f"   MTBF 2000 h, MTTR 4 h -> {a:.5f} "
          f"(年間 {(1 - a) * HOURS_PER_YEAR:.1f} 時間停止)")
    for nines in (2, 3, 4, 5):
        a = 1 - 10 ** -nines
        downtime_min = (1 - a) * HOURS_PER_YEAR * 60
        print(f"   {a * 100:.{max(nines - 2, 0)}f} % -> "
              f"年間 {downtime_min:8.1f} 分停止")

    setup_font()
    plot_bathtub(outdir / "ch13_bathtub.png")
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
