"""ケーススタディ 3: エンドポイントの応答時間を比較する.

server_log.py のアクセスログから障害の時間帯を除き、エンドポイントごとの
応答時間の中央値、95 パーセンタイル、99 パーセンタイルを
ドットプロットで比較する。目標値（SLO）を縦線で示す。

使い方: python ch15_case_comparison.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from server_log import (ENDPOINTS, INCIDENT_HOURS, INCIDENT_START,
                        make_log)

PERCENTILES = [(50, "中央値", "o"), (95, "95 パーセンタイル", "s"),
               (99, "99 パーセンタイル", "^")]
SLO = 500  # 95 パーセンタイルの目標値（ミリ秒）


def create_figure() -> Figure:
    """エンドポイントごとのパーセンタイルのドットプロットを描く."""
    times, endpoints, response = make_log()
    normal = ((times < INCIDENT_START)
              | (times >= INCIDENT_START + INCIDENT_HOURS))
    fig, ax = plt.subplots(figsize=(8, 3))
    for row, name in enumerate(ENDPOINTS):
        values = response[normal & (endpoints == row)]
        points = [np.percentile(values, q) for q, _, _ in PERCENTILES]
        ax.plot([points[0], points[-1]], [row, row], color="lightgray",
                zorder=1)
        for (_, label, marker), point in zip(PERCENTILES, points):
            ax.scatter(point, row, marker=marker, color="C0", zorder=2,
                       label=label if row == 0 else None)
    ax.axvline(SLO, color="C3", linestyle="--")
    ax.text(SLO + 10, -0.5, "目標値（95 パーセンタイル）", color="C3",
            va="center", fontsize=9)
    ax.set_yticks(range(len(ENDPOINTS)), ENDPOINTS)
    ax.set_ylim(len(ENDPOINTS) - 0.5, -0.8)  # 1 つ目を上に置き、上に余白を取る
    ax.set_xlim(0, 800)
    ax.set_xlabel("応答時間（ミリ秒）")
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=9)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
