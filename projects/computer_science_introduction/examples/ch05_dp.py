"""動的計画法と貪欲法のサンプル。

1. フィボナッチ数を素朴な再帰とメモ化で計算し、関数の呼び出し回数を
   比べる。
2. 最長共通部分列（LCS）の長さと、その 1 つを表を埋めて求める。
3. 硬貨の枚数を最小にする問題を貪欲法と動的計画法で解き、硬貨の種類に
   よっては貪欲法が最適解を出さないことを示す。

実行方法: python ch05_dp.py
関連する章: 第 5 章「アルゴリズムと計算量」
"""

from functools import cache

calls = 0  # 素朴な再帰での呼び出し回数


def fib_naive(n: int) -> int:
    """定義どおりに再帰で計算する。同じ引数で何度も呼ばれる。"""
    global calls
    calls += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@cache
def fib_memo(n: int) -> int:
    """一度計算した結果を覚えておく（メモ化）再帰。"""
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def lcs(a: str, b: str) -> str:
    """文字列 a と b の最長共通部分列の 1 つを返す。"""
    m, n = len(a), len(b)
    # t[i][j] は a[:i] と b[:j] の LCS の長さ
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    # 表を右下から逆にたどって部分列を復元する
    chars: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i, j = i - 1, j - 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))


def coins_greedy(coins: list[int], amount: int) -> list[int]:
    """額の大きい硬貨から使えるだけ使う（貪欲法）。"""
    result: list[int] = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            result.append(c)
            amount -= c
    return result


def coins_dp(coins: list[int], amount: int) -> list[int]:
    """金額 0 から amount までの最小枚数を順に求める（動的計画法）。"""
    inf = amount + 1
    best = [0] + [inf] * amount  # best[x] は金額 x の最小枚数
    last = [0] * (amount + 1)  # 金額 x の最適解で最後に使った硬貨
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and best[x - c] + 1 < best[x]:
                best[x] = best[x - c] + 1
                last[x] = c
    result: list[int] = []
    while amount > 0:
        result.append(last[amount])
        amount -= last[amount]
    return result


def main() -> None:
    """3 つの例の結果を表示する。"""
    global calls
    for n in [10, 20, 30]:
        calls = 0
        value = fib_naive(n)
        fib_memo.cache_clear()
        assert fib_memo(n) == value
        memo_calls = fib_memo.cache_info().misses
        print(f"fib({n}) = {value}: 素朴な再帰 {calls:,} 回, "
              f"メモ化 {memo_calls} 回の計算")

    a, b = "AGCAT", "GACTA"
    print(f"LCS({a}, {b}) = {lcs(a, b)}")

    for coins in [[1, 5, 10, 50, 100, 500], [1, 3, 4]]:
        amount = 6
        print(f"硬貨 {coins}, {amount} 円: 貪欲法 "
              f"{coins_greedy(coins, amount)}, "
              f"動的計画法 {coins_dp(coins, amount)}")


if __name__ == "__main__":
    main()
