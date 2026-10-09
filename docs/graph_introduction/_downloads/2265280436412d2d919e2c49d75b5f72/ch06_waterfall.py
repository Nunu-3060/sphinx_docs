"""ウォーターフォールチャート: 増減の内訳を示す.

架空の事業の売上から営業利益までの内訳を、増減の棒を階段状に
つなげて描く。

使い方: python ch06_waterfall.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

STEPS = [  # (項目名, 増減額（百万円）)
    ("売上", 500),
    ("売上原価", -220),
    ("人件費", -130),
    ("広告費", -45),
    ("その他の経費", -35),
]


def create_figure() -> Figure:
    """売上から営業利益までのウォーターフォールチャートを描く."""
    fig, ax = plt.subplots(figsize=(7.5, 4))
    level = 0
    names = []
    for index, (name, amount) in enumerate(STEPS):
        # 棒の下端は、増加なら現在の水準、減少なら減少後の水準
        bottom = level if amount >= 0 else level + amount
        color = "C0" if amount >= 0 else "C3"
        ax.bar(index, abs(amount), bottom=bottom, color=color)
        ax.text(index, level + max(amount, 0) + 8, f"{amount:+d}",
                ha="center")
        level += amount
        names.append(name)
        # 次の棒とつなぐ点線
        ax.plot([index + 0.4, index + 0.6], [level, level], color="gray",
                linestyle=":")
    # 最後に合計（営業利益）の棒を置く
    total_index = len(STEPS)
    ax.bar(total_index, level, color="C2")
    ax.text(total_index, level + 8, f"{level}", ha="center")
    names.append("営業利益")
    ax.set_xticks(range(len(names)), names)
    ax.set_ylabel("金額（百万円）")
    ax.set_ylim(0, 560)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
