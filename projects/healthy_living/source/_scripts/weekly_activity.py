"""1 週間の身体活動量 (メッツ・時) の積み上げ例を描く。

推奨値の出典:
    厚生労働省「健康づくりのための身体活動・運動ガイド2023」
    成人の身体活動は週 23 メッツ・時以上を目安とする。
"""

import matplotlib.pyplot as plt

from figure_style import save_figure, setup_style

DAYS: list[str] = ["月", "火", "水", "木", "金", "土", "日"]

# (活動名, メッツ, 曜日ごとの時間 [時間], 色)
ACTIVITIES: list[tuple[str, float, list[float], str]] = [
    ("通勤・買い物の歩行 (3.0 メッツ)", 3.0, [0.7, 0.7, 0.7, 0.7, 0.7, 0.5, 0.5], "#9ecae1"),
    ("階段・掃除など (3.5 メッツ)", 3.5, [0.2, 0.2, 0.2, 0.2, 0.2, 0.5, 0.5], "#a1d99b"),
    ("速歩 (4.3 メッツ)", 4.3, [0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0], "#fdae6b"),
    ("筋力トレーニング (3.5 メッツ)", 3.5, [0.0, 0.0, 0.3, 0.0, 0.0, 0.3, 0.0], "#bcbddc"),
]

WEEKLY_TARGET: float = 23.0


def main() -> None:
    """図を作成して保存する。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(8.0, 4.4))

    bottoms = [0.0] * len(DAYS)
    for name, mets, hours, color in ACTIVITIES:
        values = [mets * h for h in hours]
        ax.bar(DAYS, values, bottom=bottoms, color=color, label=name, edgecolor="white")
        bottoms = [b + v for b, v in zip(bottoms, values)]

    for i, total in enumerate(bottoms):
        ax.text(i, total + 0.1, f"{total:.1f}", ha="center", va="bottom", fontsize=9)

    weekly_total = sum(bottoms)
    ax.set_ylabel("身体活動量 [メッツ・時]")
    ax.set_title(f"1 週間の合計: {weekly_total:.1f} メッツ・時 (目安: {WEEKLY_TARGET:.0f} メッツ・時以上)")
    ax.set_ylim(0.0, max(bottoms) * 1.45)
    ax.legend(loc="upper left", fontsize=9, ncol=2, frameon=False)
    save_figure(fig, "weekly_activity.png")


if __name__ == "__main__":
    main()
