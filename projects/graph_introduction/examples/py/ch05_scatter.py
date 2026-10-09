"""散布図と回帰直線: 2 つの量の関係を見る.

架空の Web サーバーの、1 分あたりのリクエスト数と CPU 使用率の関係を
散布図で描き、最小二乗法で求めた回帰直線を重ねる。

使い方: python ch05_scatter.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def make_data() -> tuple[np.ndarray, np.ndarray]:
    """リクエスト数と CPU 使用率のデータを作る."""
    rng = np.random.default_rng(5)
    requests = rng.uniform(100, 1000, 150)
    cpu = 10 + 0.06 * requests + rng.normal(0, 5, 150)
    # バッチ処理が動いていた時間帯の外れ値
    requests = np.append(requests, [200, 260, 310])
    cpu = np.append(cpu, [78, 82, 75])
    return requests, cpu


def create_figure() -> Figure:
    """散布図に回帰直線を重ねて描く."""
    requests, cpu = make_data()
    slope, intercept = np.polyfit(requests, cpu, 1)
    r = np.corrcoef(requests, cpu)[0, 1]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.scatter(requests, cpu, color="C0", alpha=0.7, label="測定値")
    line_x = np.array([100.0, 1000.0])
    ax.plot(line_x, slope * line_x + intercept, color="C1",
            label=f"回帰直線（r = {r:.2f}）")
    ax.annotate("外れ値", xy=(260, 80), xytext=(450, 88),
                arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("リクエスト数（件/分）")
    ax.set_ylabel("CPU 使用率（%）")
    ax.set_ylim(0, 100)
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
