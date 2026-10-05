"""第 6 章: 貪欲法。

* 区間スケジューリング: 終了時刻の早い順に選ぶ貪欲法で最適解が得られる。
* 硬貨の両替: 額面によっては「大きい硬貨から使う」貪欲法が最適にならない。

実行例::

    python ch06_greedy.py
"""

from __future__ import annotations


def interval_scheduling(
    intervals: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """互いに重ならない区間 [start, end) をできるだけ多く選ぶ。"""
    chosen: list[tuple[int, int]] = []
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):
        if start >= last_end:
            chosen.append((start, end))
            last_end = end
    return chosen


def greedy_coin_change(coins: list[int], amount: int) -> list[int]:
    """大きい額面から順に使えるだけ使う。最適とは限らない。"""
    used: list[int] = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    if amount != 0:
        raise ValueError("この額面では支払えない")
    return used


def optimal_coin_count(coins: list[int], amount: int) -> int:
    """動的計画法で最小の硬貨枚数を求める (比較用)。"""
    inf = amount + 1
    best = [0] + [inf] * amount  # best[x] は x 円を払う最小枚数
    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x and best[x - coin] + 1 < best[x]:
                best[x] = best[x - coin] + 1
    return best[amount] if best[amount] < inf else -1


def main() -> None:
    intervals = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10),
                 (8, 11), (8, 12), (2, 14), (12, 16)]
    print("選んだ区間:", interval_scheduling(intervals))

    for coins in ([1, 5, 10, 50, 100, 500], [1, 3, 4]):
        amount = 6
        greedy = greedy_coin_change(coins, amount)
        print(f"額面 {coins}, {amount} 円: 貪欲法 {greedy} ({len(greedy)} 枚),"
              f" 最適 {optimal_coin_count(coins, amount)} 枚")


if __name__ == "__main__":
    main()
