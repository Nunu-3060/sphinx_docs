"""第 3 章「級数」の数値実験。

次の 3 つを計算して、結果を表形式で標準出力に表示する。

1. 調和級数と交代調和級数の部分和
2. 交代調和級数の項の並べ替えによる和の変化
3. 級数 1/n^2 の打ち切り誤差と、その上界（積分による評価）

実行方法::

    python ch03_series.py
"""

import math


def harmonic_partial_sum(n: int) -> float:
    """調和級数の第 n 部分和 1 + 1/2 + ... + 1/n を返す。"""
    return math.fsum(1.0 / k for k in range(1, n + 1))


def alternating_harmonic_partial_sum(n: int) -> float:
    """交代調和級数の第 n 部分和 1 - 1/2 + 1/3 - ... を返す。"""
    return math.fsum((-1.0) ** (k + 1) / k for k in range(1, n + 1))


def rearranged_partial_sum(num_terms: int, positives: int, negatives: int) -> float:
    """交代調和級数を「正の項 positives 個、負の項 negatives 個」の順に並べ替えた級数の部分和を返す。

    正の項は 1, 1/3, 1/5, ...、負の項は -1/2, -1/4, -1/6, ... を、それぞれ元の順序のまま使う。
    num_terms は足し合わせる項の総数である。
    """
    terms: list[float] = []
    next_odd = 1  # 次に使う正の項の分母
    next_even = 2  # 次に使う負の項の分母
    while len(terms) < num_terms:
        for _ in range(positives):
            terms.append(1.0 / next_odd)
            next_odd += 2
        for _ in range(negatives):
            terms.append(-1.0 / next_even)
            next_even += 2
    return math.fsum(terms[:num_terms])


def riemann_rearrangement(target: float, num_terms: int) -> float:
    """リーマンの再配列定理の証明と同じ方法で、交代調和級数の和を target に近づける。

    部分和が target 以下なら未使用の正の項を、target より大きければ未使用の負の項を足す。
    num_terms 項まで足した部分和を返す。
    """
    total = 0.0
    next_odd = 1
    next_even = 2
    for _ in range(num_terms):
        if total <= target:
            total += 1.0 / next_odd
            next_odd += 2
        else:
            total -= 1.0 / next_even
            next_even += 2
    return total


def basel_tail_error(n: int) -> tuple[float, float]:
    """1/k^2 の第 n 部分和の打ち切り誤差と、その上界 1/n を返す。

    真の値は pi^2 / 6 である。上界は積分判定法の評価から得られる。
    """
    partial = math.fsum(1.0 / k**2 for k in range(1, n + 1))
    error = math.pi**2 / 6.0 - partial
    return error, 1.0 / n


def main() -> None:
    """3 つの数値実験を順に実行して結果を表示する。"""
    print("1. 調和級数と交代調和級数の部分和")
    print("H_n: 調和級数の部分和、A_n: 交代調和級数の部分和")
    print(f"{'n':>8} {'H_n':>12} {'log n':>12} {'A_n':>14}")
    for n in [10, 100, 1000, 10000, 100000]:
        h = harmonic_partial_sum(n)
        a = alternating_harmonic_partial_sum(n)
        print(f"{n:>8} {h:>12.6f} {math.log(n):>12.6f} {a:>14.8f}")
    print(f"log 2 = {math.log(2):.8f}")
    print()

    print("2. 交代調和級数の並べ替え（100000 項までの部分和）")
    n_terms = 100000
    print(f"{alternating_harmonic_partial_sum(n_terms):>10.6f}  元の順序（log 2 = {math.log(2):.6f}）")
    print(f"{rearranged_partial_sum(n_terms, 2, 1):>10.6f}  正 2 個・負 1 個の順（3/2 log 2 = {1.5 * math.log(2):.6f}）")
    print(f"{rearranged_partial_sum(n_terms, 1, 2):>10.6f}  正 1 個・負 2 個の順（1/2 log 2 = {0.5 * math.log(2):.6f}）")
    for target in [0.0, 1.0, math.pi]:
        print(f"{riemann_rearrangement(target, n_terms):>10.6f}  目標 {target:.6f} に向けた並べ替え")
    print()

    print("3. 1/k^2 の打ち切り誤差と上界 1/n")
    print(f"{'n':>8} {'error':>14} {'1/n':>14}")
    for n in [10, 100, 1000, 10000]:
        error, bound = basel_tail_error(n)
        print(f"{n:>8} {error:>14.6e} {bound:>14.6e}")


if __name__ == "__main__":
    main()
