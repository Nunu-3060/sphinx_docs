"""マルコフ連鎖: 天気の移り変わりの確率と、定常分布.

状態は「晴れ」「曇り」「雨」の 3 つである。推移行列 P の j 列目は、
今日の天気が j のときの、明日の天気の確率である（各列の和は 1）。
確率分布 x_k は x_{k+1} = P x_k で変化し、固有値 1 の固有ベクトル
（定常分布）に近づく。

使い方: python ch10_markov.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

STATES = ["晴れ", "曇り", "雨"]
P = np.array([[0.7, 0.3, 0.2],
              [0.2, 0.4, 0.3],
              [0.1, 0.3, 0.5]])


def steady_state() -> NDArray[np.float64]:
    """固有値 1 の固有ベクトルを、成分の和が 1 になるように正規化して返す."""
    values, vectors = np.linalg.eig(P)
    k = int(np.argmin(np.abs(values - 1.0)))
    v: NDArray[np.float64] = np.real(vectors[:, k])
    return v / v.sum()


def report() -> None:
    """分布の変化と定常分布を表示する."""
    with np.printoptions(precision=4, suppress=True):
        print("P の固有値 =", np.real_if_close(np.linalg.eigvals(P)))
        x = np.array([1.0, 0.0, 0.0])  # 今日は晴れ
        for k in range(1, 11):
            x = P @ x
            if k in (1, 2, 5, 10):
                print(f"{k} 日後の分布 =", x)
        print("定常分布 =", steady_state())


def create_figure() -> Figure:
    """晴れから始めた場合と雨から始めた場合の、分布の変化を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    pi = steady_state()
    for ax, start in zip(axes, (0, 2)):
        x = np.zeros(3)
        x[start] = 1.0
        history = [x]
        for _ in range(12):
            x = P @ x
            history.append(x)
        h = np.array(history)
        for i, name in enumerate(STATES):
            ax.plot(h[:, i], "o-", color=f"C{i}", label=name)
            ax.axhline(pi[i], color=f"C{i}", linestyle=":")
        ax.set_title(f"今日が{STATES[start]}の場合")
        ax.set_xlabel("日数")
        ax.grid(True, color="0.9")
    axes[0].set_ylabel("確率")
    axes[0].legend()
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
