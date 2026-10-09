"""ケーススタディ 1: 応答時間の時間変化を見る.

server_log.py のアクセスログを 1 時間ごとに集計し、応答時間の中央値と
95 パーセンタイルを折れ線グラフで描く。

使い方: python ch15_case_timeseries.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from server_log import HOURS, INCIDENT_START, make_log


def hourly_percentiles(times: np.ndarray, response: np.ndarray,
                       q: float) -> np.ndarray:
    """1 時間ごとの応答時間の q パーセンタイルを返す."""
    hours = times.astype(int)
    return np.array([np.percentile(response[hours == h], q)
                     for h in range(HOURS)])


def create_figure() -> Figure:
    """1 時間ごとの中央値と 95 パーセンタイルの折れ線グラフを描く."""
    times, _, response = make_log()
    hours = np.arange(HOURS)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.plot(hours, hourly_percentiles(times, response, 95), color="C1",
            label="95 パーセンタイル")
    ax.plot(hours, hourly_percentiles(times, response, 50), color="C0",
            label="中央値")
    ax.annotate("障害", xy=(INCIDENT_START + 2, 1300),
                xytext=(INCIDENT_START + 15, 1300),
                arrowprops={"arrowstyle": "->"}, va="center")
    ax.set_yscale("log")
    ticks = [20, 50, 100, 200, 500, 1000, 2000]
    ax.set_yticks(ticks, [str(tick) for tick in ticks])
    ax.set_ylim(20, 3000)
    ax.set_xticks(range(0, HOURS + 1, 24),
                  [f"{day + 1} 日目" for day in range(8)])
    ax.set_xlim(0, HOURS)
    ax.set_ylabel("応答時間（ミリ秒、対数軸）")
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper right")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
