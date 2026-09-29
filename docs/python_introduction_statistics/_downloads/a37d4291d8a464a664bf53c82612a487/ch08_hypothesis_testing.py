"""第 8 章: 仮説検定の考え方。

コイン投げの例で p 値を計算する。また、シミュレーションで第一種の過誤と
検出力、検定を繰り返すことの問題（多重比較）を確かめる。
"""

import numpy as np
from scipy import stats

SEED = 8
REPETITIONS = 10_000
ALPHA = 0.05


def show_coin_test() -> None:
    """コインを 100 回投げて表が 60 回出たとき、コインが公正かを検定する。"""
    heads, trials = 60, 100
    two_sided = stats.binomtest(heads, trials, p=0.5,
                                alternative="two-sided")
    greater = stats.binomtest(heads, trials, p=0.5, alternative="greater")
    print("--- コイン投げの検定（100 回中 60 回表） ---")
    print(f"両側検定の p 値: {two_sided.pvalue:.4f}")
    print(f"片側検定（表が出やすい）の p 値: {greater.pvalue:.4f}")


def rejection_rate(rng: np.random.Generator, true_mean: float,
                   sample_size: int = 20) -> float:
    """母平均が true_mean の正規母集団から標本を取り出し、
    「母平均は 50」という帰無仮説を 1 標本 t 検定で検定する。
    これを繰り返し、帰無仮説が棄却された割合を返す。

    Args:
        rng: 乱数生成器
        true_mean: 母集団の本当の平均値
        sample_size: 標本の大きさ

    Returns:
        有意水準 ALPHA で帰無仮説が棄却された割合
    """
    samples = rng.normal(true_mean, 10.0, size=(REPETITIONS, sample_size))
    result = stats.ttest_1samp(samples, popmean=50.0, axis=1)
    return float(np.mean(result.pvalue < ALPHA))


def show_multiple_testing(rng: np.random.Generator,
                          n_tests: int = 20) -> None:
    """帰無仮説が正しい検定を n_tests 回行い、少なくとも 1 回は
    誤って棄却してしまう確率を調べる。

    Args:
        rng: 乱数生成器
        n_tests: 1 セットあたりの検定の回数
    """
    samples = rng.normal(50.0, 10.0, size=(REPETITIONS, n_tests, 20))
    pvalues = stats.ttest_1samp(samples, popmean=50.0, axis=2).pvalue
    any_rejected = np.any(pvalues < ALPHA, axis=1).mean()
    bonferroni = np.any(pvalues < ALPHA / n_tests, axis=1).mean()
    theory = 1 - (1 - ALPHA) ** n_tests
    print(f"--- 検定を {n_tests} 回繰り返した場合 ---")
    print(f"少なくとも 1 回棄却する確率（理論値）: {theory:.4f}")
    print(f"少なくとも 1 回棄却する確率（シミュレーション）: "
          f"{any_rejected:.4f}")
    print(f"ボンフェローニ補正後: {bonferroni:.4f}")


def main() -> None:
    """第 8 章のサンプルをすべて実行する。"""
    rng = np.random.default_rng(SEED)
    show_coin_test()
    print()
    print("--- 帰無仮説「母平均は 50」を棄却した割合 ---")
    print(f"母平均が 50 のとき（第一種の過誤）: "
          f"{rejection_rate(rng, 50.0):.4f}")
    print(f"母平均が 55 のとき（検出力）: {rejection_rate(rng, 55.0):.4f}")
    print()
    show_multiple_testing(rng)


if __name__ == "__main__":
    main()
