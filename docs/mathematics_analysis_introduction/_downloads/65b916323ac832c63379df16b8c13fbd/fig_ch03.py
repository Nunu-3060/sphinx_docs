"""第 3 章「級数」の図を生成する。

生成する図（source/images に保存する）:

* ch03_partial_sums.png    : 調和級数と交代調和級数の部分和の推移
* ch03_rearrangement.png   : 交代調和級数の並べ替えによる部分和の変化
* ch03_integral_test.png   : 積分判定法の考え方（長方形の面積と積分の比較）

実行方法::

    python fig_ch03.py
"""

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from plot_style import save, setup_style


def alternating_terms(n: int) -> npt.NDArray[np.float64]:
    """交代調和級数の項 (-1)^(k+1) / k (k = 1, ..., n) を返す。"""
    k = np.arange(1, n + 1, dtype=np.float64)
    return np.where(k % 2 == 1, 1.0, -1.0) / k


def rearranged_terms(n: int, positives: int, negatives: int) -> npt.NDArray[np.float64]:
    """交代調和級数を「正の項 positives 個、負の項 negatives 個」の順に並べ替えた項を n 個返す。"""
    terms: list[float] = []
    next_odd, next_even = 1, 2
    while len(terms) < n:
        for _ in range(positives):
            terms.append(1.0 / next_odd)
            next_odd += 2
        for _ in range(negatives):
            terms.append(-1.0 / next_even)
            next_even += 2
    return np.array(terms[:n], dtype=np.float64)


def plot_partial_sums() -> None:
    """調和級数と交代調和級数の部分和を並べて描く。"""
    n = 200
    k = np.arange(1, n + 1)
    harmonic = np.cumsum(1.0 / k)
    alternating = np.cumsum(alternating_terms(n))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(k, harmonic, ".", markersize=3, label=r"部分和 $H_n$")
    ax1.plot(k, np.log(k), label=r"$\log n$")
    ax1.set_xlabel(r"$n$")
    ax1.set_title("調和級数（発散する）")
    ax1.legend()

    m = 40
    ax2.plot(k[:m], alternating[:m], "o-", markersize=3, label=r"部分和 $A_n$")
    ax2.axhline(np.log(2.0), color="tab:red", linestyle="--", label=r"$\log 2$")
    ax2.set_xlabel(r"$n$")
    ax2.set_title(r"交代調和級数（$\log 2$ に収束する）")
    ax2.legend()
    save(fig, "ch03_partial_sums.png")


def plot_rearrangement() -> None:
    """交代調和級数の並べ替えで部分和の極限が変わる様子を描く。"""
    n = 300
    k = np.arange(1, n + 1)
    original = np.cumsum(alternating_terms(n))
    two_one = np.cumsum(rearranged_terms(n, 2, 1))
    one_two = np.cumsum(rearranged_terms(n, 1, 2))

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(k, two_one, color="tab:orange", label="正 2 個・負 1 個の順")
    ax.plot(k, original, color="tab:blue", label="元の順序")
    ax.plot(k, one_two, color="tab:green", label="正 1 個・負 2 個の順")
    for value, text in [(1.5, r"$\frac{3}{2}\log 2$"), (1.0, r"$\log 2$"), (0.5, r"$\frac{1}{2}\log 2$")]:
        ax.axhline(value * np.log(2.0), color="gray", linestyle="--", linewidth=0.8)
        ax.text(n * 1.01, value * np.log(2.0), text, va="center")
    ax.set_xlabel("足した項の数")
    ax.set_ylabel("部分和")
    ax.set_ylim(0.0, 1.6)
    ax.legend(loc="upper right")
    save(fig, "ch03_rearrangement.png")


def plot_integral_test() -> None:
    """1/k の長方形と曲線 y = 1/x を比べて積分判定法の考え方を示す。"""
    x = np.linspace(1.0, 8.0, 400)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, left in [(ax1, True), (ax2, False)]:
        ax.plot(x, 1.0 / x, color="black", label=r"$y = 1/x$")
        for k in range(1, 8):
            height = 1.0 / k if left else 1.0 / (k + 1)
            ax.bar(k, height, width=1.0, align="edge", alpha=0.35, edgecolor="tab:blue", color="tab:blue")
        ax.set_xlim(0.8, 8.2)
        ax.set_ylim(0.0, 1.1)
        ax.set_xlabel(r"$x$")
        ax.legend()
    ax1.set_title(r"$\sum_{k=1}^{n} \frac{1}{k} \geq \int_1^{n+1} \frac{dx}{x}$")
    ax2.set_title(r"$\sum_{k=2}^{n} \frac{1}{k} \leq \int_1^{n} \frac{dx}{x}$")
    save(fig, "ch03_integral_test.png")


def main() -> None:
    """第 3 章の図をすべて生成する。"""
    setup_style()
    plot_partial_sums()
    plot_rearrangement()
    plot_integral_test()


if __name__ == "__main__":
    main()
