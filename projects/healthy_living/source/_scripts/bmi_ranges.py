"""BMI の判定区分と、年齢別の目標とする BMI の範囲を描く。

出典:
    日本肥満学会「肥満症診療ガイドライン」(肥満度分類)
    厚生労働省「日本人の食事摂取基準 (2025年版)」(目標とする BMI の範囲)
"""

import matplotlib.pyplot as plt

from figure_style import save_figure, setup_style

# (下限, 上限, ラベル, 色)
CATEGORIES: list[tuple[float, float, str, str]] = [
    (15.0, 18.5, "低体重\n18.5 未満", "#9ecae1"),
    (18.5, 25.0, "普通体重\n18.5 以上 25 未満", "#a1d99b"),
    (25.0, 30.0, "肥満 (1 度)\n25 以上 30 未満", "#fdd0a2"),
    (30.0, 35.0, "肥満 (2 度)\n30 以上 35 未満", "#fdae6b"),
    (35.0, 40.0, "肥満 (3 度)\n35 以上 40 未満", "#fd8d3c"),
]

# (年齢区分, 下限, 上限)
TARGETS: list[tuple[str, float, float]] = [
    ("18〜49 歳", 18.5, 24.9),
    ("50〜64 歳", 20.0, 24.9),
    ("65 歳以上", 21.5, 24.9),
]


def main() -> None:
    """図を作成して保存する。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.2))

    # 上段: 判定区分
    for low, high, label, color in CATEGORIES:
        ax.barh(3.4, high - low, left=low, height=0.9, color=color, edgecolor="white")
        ax.text((low + high) / 2, 3.4, label, ha="center", va="center", fontsize=9)

    # 下段: 年齢別の目標とする範囲
    for i, (age, low, high) in enumerate(TARGETS):
        y = 2.0 - i * 0.8
        ax.barh(y, high - low, left=low, height=0.5, color="#4292c6")
        ax.text(low - 0.3, y, age, ha="right", va="center", fontsize=10)
        ax.text(high + 0.3, y, f"{low}〜{high}", ha="left", va="center", fontsize=9)

    ax.text(15.0, 4.15, "判定区分 (日本肥満学会、40 以上は肥満 4 度)", fontsize=10, fontweight="bold")
    ax.text(11.6, 2.55, "目標とする BMI の範囲 (食事摂取基準 2025年版)", fontsize=10, fontweight="bold")
    ax.set_xlim(11.5, 40.0)
    ax.set_ylim(0.0, 4.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("BMI")
    save_figure(fig, "bmi_ranges.png")


if __name__ == "__main__":
    main()
