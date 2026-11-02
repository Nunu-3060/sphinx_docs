"""正しいシャッフルと誤ったシャッフルの偏りを比べる（5 章）。

3 枚のカード ABC の並べ方 6 通りが、それぞれ何回出るかを数える。
誤ったシャッフルは乱数の組合せが 3^3 = 27 通りで、6 で割り切れないため必ず偏る。

実行方法: py shuffle.py
"""

import itertools
import random
from collections import Counter


def fisher_yates(cards: list[str], rng: random.Random) -> list[str]:
    """正しいシャッフル。後ろから順に、まだ決まっていない位置の中から 1 枚を選んで入れ替える。"""
    result = cards[:]
    for i in range(len(result) - 1, 0, -1):
        j = rng.randint(0, i)
        result[i], result[j] = result[j], result[i]
    return result


def naive_shuffle(cards: list[str], rng: random.Random) -> list[str]:
    """誤ったシャッフル。各位置を、全体の中から選んだ 1 枚と入れ替える。"""
    result = cards[:]
    for i in range(len(result)):
        j = rng.randrange(len(result))
        result[i], result[j] = result[j], result[i]
    return result


def naive_exact(cards: list[str]) -> Counter[str]:
    """誤ったシャッフルの乱数の組合せ 27 通りをすべて試し、並べ方ごとの回数を返す。"""
    counts: Counter[str] = Counter()
    n = len(cards)
    for choice in itertools.product(range(n), repeat=n):
        result = cards[:]
        for i, j in enumerate(choice):
            result[i], result[j] = result[j], result[i]
        counts["".join(result)] += 1
    return counts


def frequencies(trials: int, seed: int = 1) -> dict[str, tuple[float, float]]:
    """並べ方ごとに、(正しいシャッフルの割合, 誤ったシャッフルの割合) を返す。"""
    rng = random.Random(seed)
    cards = ["A", "B", "C"]
    good = Counter("".join(fisher_yates(cards, rng)) for _ in range(trials))
    bad = Counter("".join(naive_shuffle(cards, rng)) for _ in range(trials))
    orders = sorted("".join(p) for p in itertools.permutations(cards))
    return {o: (good[o] / trials, bad[o] / trials) for o in orders}


def main() -> None:
    print("並べ方  正しい  誤り   （理論値 1/6 = 0.167）")
    for order, (good, bad) in frequencies(60_000).items():
        print(f"{order}     {good:.3f}   {bad:.3f}")
    exact = naive_exact(["A", "B", "C"])
    print("誤ったシャッフルの正確な回数（27 通り中）: " + "、".join(f"{k} {v}" for k, v in sorted(exact.items())))


if __name__ == "__main__":
    main()
