"""第 5 章: 確率分布。

scipy.stats を使い、二項分布・ポアソン分布・正規分布の確率を計算する。
また、二項分布の確率質量関数と正規分布の確率密度関数のグラフを保存する。
保存先のフォルダーは --outdir で指定する（既定値は output）。
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面に表示せず、ファイルに保存するだけにする

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402


def show_binomial() -> None:
    """コインを 10 回投げたときに表が出る回数（二項分布）を調べる。"""
    n, p = 10, 0.5
    dist = stats.binom(n, p)
    print("--- 二項分布 B(10, 0.5) ---")
    print(f"表がちょうど 5 回出る確率: {dist.pmf(5):.4f}")
    print(f"表が 3 回以下になる確率: {dist.cdf(3):.4f}")
    print(f"期待値: {dist.mean():.2f}、分散: {dist.var():.2f}")


def show_poisson() -> None:
    """1 時間に平均 3 件届く問い合わせの件数（ポアソン分布）を調べる。"""
    dist = stats.poisson(3)
    print("--- ポアソン分布 Po(3) ---")
    for k in range(6):
        print(f"{k} 件の確率: {dist.pmf(k):.4f}")
    print(f"6 件以上の確率: {dist.sf(5):.4f}")
    print(f"期待値: {dist.mean():.2f}、分散: {dist.var():.2f}")


def show_normal() -> None:
    """平均値 50、標準偏差 10 の正規分布の確率を調べる。"""
    mu, sigma = 50.0, 10.0
    dist = stats.norm(loc=mu, scale=sigma)
    print("--- 正規分布 N(50, 10^2) ---")
    print(f"60 以下になる確率: {dist.cdf(60):.4f}")
    print(f"40 以上 60 以下になる確率: {dist.cdf(60) - dist.cdf(40):.4f}")
    print(f"下側の確率が 0.975 になる値: {dist.ppf(0.975):.2f}")
    for k in (1, 2, 3):
        prob = dist.cdf(mu + k * sigma) - dist.cdf(mu - k * sigma)
        print(f"平均値 ± {k} 標準偏差の範囲に入る確率: {prob:.4f}")


def plot_distributions(path: Path) -> None:
    """二項分布の確率質量関数と正規分布の確率密度関数を保存する。

    Args:
        path: 保存先のファイル
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    k = np.arange(0, 11)
    ax1.bar(k, stats.binom.pmf(k, 10, 0.5))
    ax1.set_xlabel("k")
    ax1.set_ylabel("P(X = k)")
    ax1.set_title("Binomial distribution B(10, 0.5)")

    x = np.linspace(10, 90, 400)
    ax2.plot(x, stats.norm.pdf(x, loc=50, scale=10))
    ax2.set_xlabel("x")
    ax2.set_ylabel("f(x)")
    ax2.set_title("Normal distribution N(50, 10^2)")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    """第 5 章のサンプルをすべて実行する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("output"),
                        help="グラフの保存先のフォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    show_binomial()
    print()
    show_poisson()
    print()
    show_normal()
    plot_distributions(outdir / "ch05_distributions.png")


if __name__ == "__main__":
    main()
