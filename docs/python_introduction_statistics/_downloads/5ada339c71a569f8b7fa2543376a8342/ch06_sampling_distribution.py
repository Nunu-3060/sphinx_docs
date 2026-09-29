"""第 6 章: 標本分布と中心極限定理。

乱数を使ったシミュレーションで、大数の法則と中心極限定理を確かめる。
標本平均の分布のグラフを保存する。保存先のフォルダーは --outdir で
指定する（既定値は output）。
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面に表示せず、ファイルに保存するだけにする

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import numpy.typing as npt  # noqa: E402

SEED = 1
REPETITIONS = 10_000  # 標本を取り出す回数
SAMPLE_SIZES = (2, 10, 30)

FloatArray = npt.NDArray[np.float64]


def show_law_of_large_numbers(rng: np.random.Generator) -> None:
    """サイコロを振る回数を増やすと、出た目の平均値が 3.5 に近づくことを示す。

    Args:
        rng: 乱数生成器
    """
    rolls = rng.integers(1, 7, size=100_000)
    print("--- 大数の法則（サイコロの目の平均値） ---")
    for n in (10, 100, 1_000, 10_000, 100_000):
        print(f"{n:>7} 回: {rolls[:n].mean():.4f}")


def sample_means(rng: np.random.Generator, sample_size: int) -> FloatArray:
    """指数分布（平均値 1、標準偏差 1）から標本を繰り返し取り出し、
    標本平均を計算する。

    Args:
        rng: 乱数生成器
        sample_size: 1 回に取り出す標本の大きさ

    Returns:
        REPETITIONS 個の標本平均
    """
    samples = rng.exponential(scale=1.0, size=(REPETITIONS, sample_size))
    means: FloatArray = samples.mean(axis=1)
    return means


def show_central_limit_theorem(rng: np.random.Generator,
                               path: Path) -> None:
    """標本の大きさごとに標本平均の分布を調べ、ヒストグラムを保存する。

    Args:
        rng: 乱数生成器
        path: 保存先のファイル
    """
    print("--- 標本平均の平均値と標準偏差 ---")
    fig, axes = plt.subplots(1, len(SAMPLE_SIZES), figsize=(12, 4))
    for ax, n in zip(axes, SAMPLE_SIZES):
        means = sample_means(rng, n)
        theory_se = 1.0 / np.sqrt(n)  # 標準誤差の理論値
        print(f"n = {n:>2}: 平均値 {means.mean():.4f}、"
              f"標準偏差 {means.std():.4f}（理論値 {theory_se:.4f}）")
        ax.hist(means, bins=50, density=True, edgecolor="black")
        ax.set_title(f"Sample mean (n = {n})")
        ax.set_xlabel("Sample mean")
    axes[0].set_ylabel("Density")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    """第 6 章のサンプルをすべて実行する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("output"),
                        help="グラフの保存先のフォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(SEED)
    show_law_of_large_numbers(rng)
    print()
    show_central_limit_theorem(rng, outdir / "ch06_sample_means.png")


if __name__ == "__main__":
    main()
