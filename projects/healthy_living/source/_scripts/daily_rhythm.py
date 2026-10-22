"""体内時計を整える 1 日の過ごし方の例を時間軸で描く。

時刻は 7 時起床、23 時就寝の場合の一例である。
"""

import matplotlib.pyplot as plt

from figure_style import save_figure, setup_style

# (開始時刻, 終了時刻, ラベル, 色)
BLOCKS: list[tuple[float, float, str, str]] = [
    (0.0, 7.0, "睡眠", "#6baed6"),
    (7.0, 7.5, "", "#fec44f"),
    (7.5, 8.0, "", "#a1d99b"),
    (8.0, 12.0, "日中の活動", "#fee391"),
    (12.0, 13.0, "昼食", "#a1d99b"),
    (13.0, 19.0, "日中の活動", "#fee391"),
    (19.0, 20.0, "夕食", "#a1d99b"),
    (20.0, 21.5, "くつろぐ", "#dadaeb"),
    (21.5, 22.0, "", "#fc9272"),
    (22.0, 23.0, "", "#bcbddc"),
    (23.0, 24.0, "睡眠", "#6baed6"),
]

# (矢印の先の時刻, 注記, 注記の高さ, 注記の横位置)
NOTES: list[tuple[float, str, float, float]] = [
    (7.25, "起床後に朝の光を浴び\n朝食をとる", 0.75, 7.25),
    (14.0, "カフェインは午後の\n早い時間までにする", 0.75, 14.0),
    (19.5, "夕食は就寝の\n3 時間前までに", 1.35, 19.5),
    (21.75, "入浴は就寝の\n1〜2 時間前", 0.75, 21.2),
    (22.5, "就寝前は\n照明を落とす", 1.35, 23.0),
]


def main() -> None:
    """図を作成して保存する。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(10.0, 3.6))

    for start, end, label, color in BLOCKS:
        ax.barh(0.0, end - start, left=start, height=0.6, color=color, edgecolor="white")
        if label:
            ax.text((start + end) / 2, 0.0, label, ha="center", va="center", fontsize=9)

    for time, note, y, text_x in NOTES:
        ax.annotate(note, xy=(time, 0.3), xytext=(text_x, y), ha="center", va="bottom", fontsize=9,
                    arrowprops={"arrowstyle": "->", "color": "gray"})

    ax.set_xlim(0.0, 24.0)
    ax.set_ylim(-0.5, 2.0)
    ax.set_xticks(range(0, 25, 2))
    ax.set_xticklabels([f"{h}:00" for h in range(0, 25, 2)])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("時刻")
    save_figure(fig, "daily_rhythm.png")


if __name__ == "__main__":
    main()
