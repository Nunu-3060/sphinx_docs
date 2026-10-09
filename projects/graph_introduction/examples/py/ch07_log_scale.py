"""対数軸: 指数的に増える量を描く.

架空のサービスの登録ユーザー数を、通常の軸と対数軸で描く。
対数軸では、一定の割合で増える期間が直線になり、増え方の変化が分かる。

使い方: python ch07_log_scale.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def make_users() -> tuple[np.ndarray, np.ndarray]:
    """月数と登録ユーザー数を作る.

    12 か月目までは毎月 40%、それ以降は毎月 10% ずつ増える。
    """
    months = np.arange(0, 25)
    rates = np.where(months <= 12, 1.4, 1.1)
    rates[0] = 1.0  # 0 か月目は増加なし
    users = 100 * np.cumprod(rates)
    return months, users


def create_figure() -> Figure:
    """同じデータを通常の軸と対数軸で描く."""
    months, users = make_users()
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.6))
    ax_left.plot(months, users, marker=".")
    ax_left.set_title("通常の軸")
    ax_right.plot(months, users, marker=".")
    ax_right.set_yscale("log")
    ax_right.set_title("対数軸")
    for ax in (ax_left, ax_right):
        ax.axvline(12, color="gray", linestyle="--", linewidth=1)
        ax.set_xlabel("サービス開始からの月数")
        ax.set_ylabel("登録ユーザー数（人）")
        ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
