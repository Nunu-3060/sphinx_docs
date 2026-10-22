"""主な酒類の純アルコール量を計算して棒グラフに描く。

純アルコール量 [g] = 飲む量 [mL] × アルコール度数 [%] / 100 × 0.8 (アルコールの比重)

基準線の出典:
    厚生労働省「健康日本21 (第三次)」
    生活習慣病のリスクを高める飲酒量は、1 日当たりの純アルコール量で
    男性 40 g 以上、女性 20 g 以上とされる。
"""

import matplotlib.pyplot as plt

from figure_style import save_figure, setup_style

ALCOHOL_DENSITY: float = 0.8

# (酒類と量, 量 [mL], 度数 [%])
DRINKS: list[tuple[str, float, float]] = [
    ("ビール\n中瓶 1 本 500 mL", 500.0, 5.0),
    ("チューハイ\n1 缶 350 mL", 350.0, 7.0),
    ("日本酒\n1 合 180 mL", 180.0, 15.0),
    ("ワイン\nグラス 1 杯 120 mL", 120.0, 12.0),
    ("焼酎\n100 mL", 100.0, 25.0),
    ("ウイスキー\nシングル 30 mL", 30.0, 43.0),
]


def pure_alcohol_grams(volume_ml: float, percent: float) -> float:
    """飲む量とアルコール度数から純アルコール量 [g] を求める。"""
    return volume_ml * percent / 100.0 * ALCOHOL_DENSITY


def main() -> None:
    """図を作成して保存する。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.4))

    labels = [name for name, _, _ in DRINKS]
    grams = [pure_alcohol_grams(volume, percent) for _, volume, percent in DRINKS]
    bars = ax.bar(labels, grams, color="#6baed6")
    for bar, value in zip(bars, grams):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.5, f"{value:.1f} g",
                ha="center", va="bottom", fontsize=9)

    ax.axhline(20.0, color="#e6550d", linestyle="--", linewidth=1)
    ax.text(5.45, 25.0, "女性の生活習慣病のリスクを\n高める量 (1 日 20 g 以上)", ha="right", fontsize=9,
            color="#e6550d")
    ax.set_ylabel("純アルコール量 [g]")
    ax.set_ylim(0.0, 30.0)
    ax.tick_params(axis="x", labelsize=9)
    save_figure(fig, "pure_alcohol.png")


if __name__ == "__main__":
    main()
