"""ケーススタディ 2: 応答時間の分布を見る.

server_log.py のアクセスログから障害の時間帯を除き、エンドポイントごとの
応答時間の分布をヒストグラムで描く。応答時間は右に長い裾を持つため、
横軸を対数にし、階級も対数で等間隔に取る。

使い方: python ch15_case_distribution.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from server_log import (ENDPOINTS, INCIDENT_HOURS, INCIDENT_START,
                        make_log)


def create_figure() -> Figure:
    """エンドポイントごとの応答時間のヒストグラムを縦に並べて描く."""
    times, endpoints, response = make_log()
    normal = ((times < INCIDENT_START)
              | (times >= INCIDENT_START + INCIDENT_HOURS))
    bins = np.logspace(np.log10(5), np.log10(2000), 60)
    fig, axes = plt.subplots(len(ENDPOINTS), 1, figsize=(7, 5),
                             sharex=True)
    for index, (ax, name) in enumerate(zip(axes, ENDPOINTS)):
        values = response[normal & (endpoints == index)]
        ax.hist(values, bins=bins, color=f"C{index}")
        ax.axvline(np.median(values), color="black", linestyle="--",
                   linewidth=1)
        ax.set_title(f"{name}（破線は中央値）", loc="left", fontsize=10)
        ax.set_ylabel("件数")
    axes[-1].set_xscale("log")
    axes[-1].set_xlabel("応答時間（ミリ秒、対数軸）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
