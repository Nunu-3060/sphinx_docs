"""経験累積分布関数（ECDF）: 分布を階級なしで比較する.

架空の Web API の改修前と改修後の応答時間を ECDF で比較する。
縦軸の値が 0.95 となる横軸の値が、95 パーセンタイルである。

使い方: python ch04_ecdf.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def create_figure() -> Figure:
    """改修前と改修後の応答時間の ECDF を描く."""
    rng = np.random.default_rng(4)
    before = rng.lognormal(np.log(120), 0.5, 1000)
    after = rng.lognormal(np.log(100), 0.35, 1000)

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.ecdf(before, label="改修前")
    ax.ecdf(after, label="改修後")
    ax.axhline(0.95, color="gray", linestyle="--", linewidth=1)
    ax.text(490, 0.93, "累積割合 0.95", ha="right", va="top", color="gray")
    ax.set_xlim(0, 500)
    ax.set_xlabel("応答時間（ミリ秒）")
    ax.set_ylabel("累積割合")
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
