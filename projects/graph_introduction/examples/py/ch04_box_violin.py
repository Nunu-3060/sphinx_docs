"""箱ひげ図とバイオリンプロット.

架空の 3 チームのタスク完了時間を、箱ひげ図とバイオリンプロットで描く。
チーム C の分布は 2 つの山を持つが、箱ひげ図では分からない。

使い方: python ch04_box_violin.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

TEAMS = ["チーム A", "チーム B", "チーム C"]


def make_durations() -> list[np.ndarray]:
    """チームごとのタスク完了時間（時間）を作る."""
    rng = np.random.default_rng(2)
    team_a = rng.normal(8, 1.5, 200)
    team_b = rng.gamma(4, 2.2, 200)  # 右に裾を引く分布
    team_c = np.concatenate([rng.normal(5, 1, 100), rng.normal(11, 1, 100)])
    return [team_a, team_b, team_c]


def create_figure() -> Figure:
    """同じデータの箱ひげ図とバイオリンプロットを並べて描く."""
    durations = make_durations()
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(9, 3.6),
                                            sharey=True)
    ax_left.boxplot(durations, tick_labels=TEAMS)
    ax_left.set_title("箱ひげ図")
    ax_left.set_ylabel("完了時間（時間）")

    ax_right.violinplot(durations, showmedians=True)
    ax_right.set_xticks([1, 2, 3], TEAMS)
    ax_right.set_title("バイオリンプロット")

    for ax in (ax_left, ax_right):
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
