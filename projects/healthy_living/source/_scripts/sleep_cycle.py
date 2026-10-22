"""一晩の睡眠段階の推移 (模式図) を描く。

実際の推移は個人差や日による差が大きい。ここでは、
「深いノンレム睡眠は前半に多く、レム睡眠は後半に長くなる」
という一般的な傾向を示すための模式図とする。
"""

import matplotlib.pyplot as plt

from figure_style import save_figure, setup_style

# 段階: 0 = 覚醒, 1 = レム睡眠, 2 = 浅いノンレム睡眠, 3 = 中程度のノンレム睡眠, 4 = 深いノンレム睡眠
STAGE_LABELS: list[str] = ["覚醒", "レム睡眠", "浅いノンレム", "中程度のノンレム", "深いノンレム"]

# (開始時刻 [時間], 段階)
SCHEDULE: list[tuple[float, int]] = [
    (0.0, 0), (0.15, 2), (0.35, 3), (0.6, 4), (1.1, 3), (1.3, 2), (1.4, 1),
    (1.6, 2), (1.8, 3), (2.1, 4), (2.5, 3), (2.7, 2), (2.9, 1),
    (3.2, 2), (3.5, 3), (3.9, 2), (4.3, 1),
    (4.8, 2), (5.3, 3), (5.5, 2), (5.9, 1),
    (6.5, 2), (6.9, 1), (7.6, 0), (8.0, 0),
]


def main() -> None:
    """図を作成して保存する。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 3.8))

    times = [t for t, _ in SCHEDULE]
    stages = [s for _, s in SCHEDULE]
    ax.step(times, stages, where="post", color="#2171b5", linewidth=2)

    # レム睡眠の区間を強調する
    for (start, stage), (end, _) in zip(SCHEDULE, SCHEDULE[1:]):
        if stage == 1:
            ax.axvspan(start, end, color="#fdae6b", alpha=0.4, linewidth=0)

    ax.set_yticks(range(len(STAGE_LABELS)))
    ax.set_yticklabels(STAGE_LABELS)
    ax.invert_yaxis()
    ax.set_xlim(0.0, 8.0)
    ax.set_xticks(range(9))
    ax.set_xlabel("入眠からの経過時間 [時間]")
    ax.set_title("一晩の睡眠段階の推移 (模式図、橙色はレム睡眠)")
    save_figure(fig, "sleep_cycle.png")


if __name__ == "__main__":
    main()
