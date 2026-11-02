"""ガチャで全種類をそろえるまでの回数を計算・シミュレーションする（5 章）。

どの種類も同じ確率で出るとき、n 種類をそろえるまでの回数の期待値は
n × (1 + 1/2 + ... + 1/n) になる（クーポンコレクター問題）。

実行方法:
    py gacha.py          10 種類で計算する
    py gacha.py 30       種類の数を指定する
"""

import random
import statistics
import sys


def expected_draws(kinds: int) -> float:
    """全種類をそろえるまでの回数の期待値を返す。"""
    return kinds * sum(1 / k for k in range(1, kinds + 1))


def draws_to_complete(kinds: int, rng: random.Random) -> int:
    """1 回分のシミュレーション。全種類がそろうまでに引いた回数を返す。"""
    owned: set[int] = set()
    draws = 0
    while len(owned) < kinds:
        owned.add(rng.randrange(kinds))
        draws += 1
    return draws


def simulate(kinds: int, trials: int, seed: int = 1) -> list[int]:
    rng = random.Random(seed)
    return [draws_to_complete(kinds, rng) for _ in range(trials)]


def main() -> None:
    kinds = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    results = sorted(simulate(kinds, 20_000))
    print(f"{kinds} 種類をそろえるまでの回数")
    print(f"  期待値（計算）:           {expected_draws(kinds):.2f}")
    print(f"  平均（シミュレーション）: {statistics.mean(results):.2f}")
    print(f"  中央値:                   {statistics.median(results):.0f}")
    print(f"  運の悪い 10 % の人:       {results[int(len(results) * 0.9)]} 回以上")


if __name__ == "__main__":
    main()
