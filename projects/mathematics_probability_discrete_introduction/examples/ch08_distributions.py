"""第 8 章 代表的な離散分布のサンプルコード。

各分布の確率質量関数を定義どおりに実装し、scipy.stats の結果と照合する。
"""

import math

from scipy import stats


def binomial_pmf(k: int, n: int, p: float) -> float:
    """二項分布 Bin(n, p) の確率質量関数。"""
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def geometric_pmf(k: int, p: float) -> float:
    """幾何分布 Geo(p)（初めて成功するまでの試行回数）の確率質量関数。k = 1, 2, ..."""
    return (1 - p) ** (k - 1) * p


def negative_binomial_pmf(k: int, r: int, p: float) -> float:
    """負の二項分布（r 回目の成功までの試行回数）の確率質量関数。k = r, r+1, ..."""
    return math.comb(k - 1, r - 1) * p ** r * (1 - p) ** (k - r)


def hypergeometric_pmf(k: int, population: int, successes: int, draws: int) -> float:
    """超幾何分布の確率質量関数。

    当たり successes 個を含む population 個から draws 個を非復元抽出したとき、
    当たりがちょうど k 個含まれる確率。
    """
    return (math.comb(successes, k) * math.comb(population - successes, draws - k)
            / math.comb(population, draws))


def poisson_pmf(k: int, lam: float) -> float:
    """ポアソン分布 Po(λ) の確率質量関数。

    k が大きいと λ^k や k! が浮動小数点数の範囲を超えるので、対数をとって計算する。
    """
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def compare_with_scipy() -> None:
    """自作の確率質量関数と scipy.stats の値の差の最大値を表示する。"""
    n, p, r, lam = 20, 0.3, 3, 4.0
    pop, succ, draws = 50, 12, 10
    errors = {
        "二項分布": max(abs(binomial_pmf(k, n, p) - stats.binom.pmf(k, n, p)) for k in range(n + 1)),
        "幾何分布": max(abs(geometric_pmf(k, p) - stats.geom.pmf(k, p)) for k in range(1, 50)),
        # scipy の nbinom は「r 回目の成功までの失敗回数」の分布なので k - r を渡す
        "負の二項分布": max(
            abs(negative_binomial_pmf(k, r, p) - stats.nbinom.pmf(k - r, r, p)) for k in range(r, 80)
        ),
        "超幾何分布": max(
            abs(hypergeometric_pmf(k, pop, succ, draws) - stats.hypergeom.pmf(k, pop, succ, draws))
            for k in range(draws + 1)
        ),
        "ポアソン分布": max(abs(poisson_pmf(k, lam) - stats.poisson.pmf(k, lam)) for k in range(40)),
    }
    for name, err in errors.items():
        print(f"{name:<8} 最大誤差 = {err:.2e}")


def show_moments() -> None:
    """scipy.stats で期待値と分散を求め、理論式と比較する。"""
    n, p, r, lam = 20, 0.3, 3, 4.0
    rows = [
        ("Bin(20, 0.3)", stats.binom(n, p), n * p, n * p * (1 - p)),
        ("Geo(0.3)", stats.geom(p), 1 / p, (1 - p) / p ** 2),
        ("Po(4)", stats.poisson(lam), lam, lam),
    ]
    for name, dist, mean, var in rows:
        print(f"{name:<13} E: scipy={float(dist.mean()):.4f} 理論={mean:.4f}  "
              f"V: scipy={float(dist.var()):.4f} 理論={var:.4f}")
    nb = stats.nbinom(r, p)
    print(f"{'NB(3, 0.3)':<13} E: scipy={float(nb.mean()) + r:.4f} 理論={r / p:.4f}  "
          f"V: scipy={float(nb.var()):.4f} 理論={r * (1 - p) / p ** 2:.4f}")


def memoryless(p: float, m: int, n: int) -> None:
    """幾何分布の無記憶性 P(X > m + n | X > m) = P(X > n) を確かめる。"""
    def tail(k: int) -> float:
        return (1 - p) ** k  # P(X > k)
    print(f"P(X > {m + n} | X > {m}) = {tail(m + n) / tail(m):.6f}, P(X > {n}) = {tail(n):.6f}")


def poisson_approximation() -> None:
    """np = 3 を保ったまま n を大きくしたときの二項分布とポアソン分布の差を調べる。"""
    lam = 3.0
    for n in [10, 30, 100, 1000]:
        p = lam / n
        # 全変動距離 (1/2) Σ |P(X=k) - P(Y=k)|
        distance = 0.5 * sum(abs(binomial_pmf(k, n, p) - poisson_pmf(k, lam)) for k in range(n + 1))
        distance += 0.5 * sum(poisson_pmf(k, lam) for k in range(n + 1, n + 60))
        print(f"n={n:>4}, p={p:.4f}: 全変動距離 = {distance:.5f}")


def main() -> None:
    print("--- scipy.stats との照合 ---")
    compare_with_scipy()
    print("--- 期待値と分散 ---")
    show_moments()
    print("--- 幾何分布の無記憶性 ---")
    memoryless(0.3, 4, 2)
    print("--- ポアソン近似 ---")
    poisson_approximation()


if __name__ == "__main__":
    main()
