"""折れ線グラフと移動平均: 時間変化の傾向を見る.

架空の Web サイトの 1 日あたりの訪問者数（半年分）を折れ線グラフで描き、
7 日間の移動平均を重ねる。曜日による上下が平らになり、傾向が見やすくなる。

使い方: python ch07_line.py
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

WINDOW = 7  # 移動平均を計算する日数


def make_visitors() -> tuple[np.ndarray, np.ndarray]:
    """日付と訪問者数のデータを作る."""
    dates = np.arange("2025-01-01", "2025-07-01", dtype="datetime64[D]")
    rng = np.random.default_rng(8)
    days = np.arange(len(dates))
    trend = 1000 + 3 * days
    # 1970-01-01 は木曜日なので、日数に 3 を足して 7 で割った余りが
    # 曜日になる（0 が月曜日、5 と 6 が土曜日と日曜日）
    weekday = (dates.astype(int) + 3) % 7
    weekly = np.where(weekday >= 5, -250, 50)
    visitors = trend + weekly + rng.normal(0, 60, len(dates))
    return dates, visitors


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    """直前の window 個の値の平均を返す。最初の window - 1 個は NaN."""
    result = np.full(len(values), np.nan)
    sums = np.convolve(values, np.ones(window), mode="valid")
    result[window - 1:] = sums / window
    return result


def create_figure() -> Figure:
    """訪問者数と移動平均の折れ線グラフを描く."""
    dates, visitors = make_visitors()
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(dates, visitors, color="C0", alpha=0.4, linewidth=1,
            label="日ごとの値")
    ax.plot(dates, moving_average(visitors, WINDOW), color="C0",
            linewidth=2, label=f"{WINDOW} 日間の移動平均")
    # 目盛りの日付を「1 月」の形式で表示する
    ax.xaxis.set_major_formatter(
        lambda value, _: f"{mdates.num2date(value).month} 月")
    ax.set_ylabel("訪問者数（人/日）")
    ax.set_ylim(0, 1800)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
