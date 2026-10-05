"""第 6 章: 動的計画法。

* フィボナッチ数: メモ化 (functools.lru_cache) で指数時間を線形時間にする。
* 0-1 ナップサック問題: O(nW) の表を埋め、選んだ品物も復元する。
* 最長共通部分列 (LCS): O(mn) の表を埋め、部分列を復元する。

実行例::

    python ch06_dynamic_programming.py
"""

from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    """n 番目のフィボナッチ数。メモ化により O(n) 回の呼び出しで済む。"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def knapsack(
    weights: list[int], values: list[int], capacity: int
) -> tuple[int, list[int]]:
    """容量 capacity に収まる価値の最大値と、選ぶ品物の番号を返す。"""
    n = len(weights)
    # dp[i][w]: 品物 0..i-1 から重さの合計 w 以下で選んだときの価値の最大値
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # 品物 i - 1 を選ばない
            if wt <= w and dp[i - 1][w - wt] + val > dp[i][w]:
                dp[i][w] = dp[i - 1][w - wt] + val  # 選ぶ
    chosen: list[int] = []
    w = capacity
    for i in range(n, 0, -1):  # 表を逆にたどって選んだ品物を復元する
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return dp[n][capacity], sorted(chosen)


def lcs(s: str, t: str) -> str:
    """文字列 s と t の最長共通部分列の 1 つを返す。"""
    m, n = len(s), len(t)
    # dp[i][j]: s[:i] と t[:j] の LCS の長さ
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    chars: list[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if s[i - 1] == t[j - 1]:
            chars.append(s[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))


def main() -> None:
    print("fib(80) =", fib(80))
    best, items = knapsack([2, 1, 3, 2], [3, 2, 4, 2], 5)
    print(f"ナップサック: 価値 {best}, 選ぶ品物 {items}")
    print("LCS('ABCBDAB', 'BDCABA') =", lcs("ABCBDAB", "BDCABA"))


if __name__ == "__main__":
    main()
