"""第 15 章: 同じデータでも、示し方によって結論が伝わるかどうかが変わる。

ゴム製のシール部品について、試験時の温度と、シールの不具合の件数を
24 回の試験で記録した、という想定の模擬データを使います。この部品を
-2 ℃ で使う計画があるとします。

* 悪い例: 不具合が起きた試験だけを描き、温度の範囲も試験の範囲に
  限っている。傾向が見えず、「温度とは関係がない」と誤解しやすい
* 良い例: 不具合のなかった試験も含めてすべて描き、使う予定の温度
  まで横軸を広げ、結論をタイトルにしている

図は ch15_chart_makeover.png として保存します。

実行例::

    python ch15_chart_makeover.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
from matplotlib import font_manager
from matplotlib.figure import Figure

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

PLANNED_TEMPERATURE = -2.0  # 使う予定の温度 [℃]

# (試験時の温度 [℃], 不具合の件数) の模擬データ
TESTS: list[tuple[float, int]] = [
    (12, 2), (13, 1), (14, 1), (15, 0), (16, 1), (17, 0),
    (18, 0), (19, 1), (19, 0), (20, 0), (21, 0), (21, 0),
    (22, 0), (22, 0), (23, 0), (24, 1), (24, 0), (25, 0),
    (26, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0),
]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def summarize() -> None:
    """温度帯ごとの不具合の発生率を表示する。"""
    for low, high in ((10, 18), (18, 31)):
        group = [count for temp, count in TESTS if low <= temp < high]
        with_failure = sum(1 for count in group if count > 0)
        print(f"{low}〜{high - 1} ℃: 試験 {len(group):2d} 回のうち "
              f"{with_failure} 回で不具合 ({with_failure / len(group):.0%})")
    lowest = min(temp for temp, _ in TESTS)
    print(f"試験した最低温度: {lowest} ℃、"
          f"使う予定の温度: {PLANNED_TEMPERATURE} ℃")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    summarize()
    setup_font()
    fig = Figure(figsize=(10, 4), layout="constrained")
    ax_bad, ax_good = fig.subplots(1, 2)

    # 悪い例: 不具合のあった試験だけ
    failed = [(t, c) for t, c in TESTS if c > 0]
    ax_bad.plot([t for t, _ in failed], [c for _, c in failed], "o",
                color="gray")
    ax_bad.set_title("悪い例: シール不具合の記録")
    ax_bad.set_xlabel("温度 [℃]")
    ax_bad.set_ylabel("不具合の件数")
    ax_bad.set_ylim(0, 3)
    ax_bad.set_yticks([0, 1, 2, 3])
    ax_bad.grid(alpha=0.3)

    # 良い例: すべての試験と、使う予定の温度
    ax_good.plot([t for t, _ in TESTS], [c for _, c in TESTS], "o",
                 color="tab:blue", alpha=0.7, label="試験結果 (24 回)")
    ax_good.axvspan(-5, min(t for t, _ in TESTS), color="tab:red",
                    alpha=0.1, label="試験していない温度")
    ax_good.axvline(PLANNED_TEMPERATURE, color="tab:red", linestyle="--",
                    label=f"使う予定の温度 {PLANNED_TEMPERATURE:.0f} ℃")
    ax_good.set_title("良い例: 低温ほど不具合が多く、\n"
                      "予定の温度では試験していない")
    ax_good.set_xlabel("温度 [℃]")
    ax_good.set_ylabel("不具合の件数")
    ax_good.set_xlim(-5, 32)
    ax_good.set_ylim(-0.2, 3)
    ax_good.set_yticks([0, 1, 2, 3])
    ax_good.grid(alpha=0.3)
    ax_good.legend(loc="upper right", fontsize=8)
    fig.savefig(outdir / "ch15_chart_makeover.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
