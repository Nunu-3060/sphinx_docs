"""第 9 章: ゲームでよく使う乱数の道具。

画面は使わず、結果をコンソールに表示する。

実行方法:
    py random_tools.py
"""

import bisect
import itertools
import math
import random
from collections import Counter
from collections.abc import Sequence
from typing import Generic, TypeVar

T = TypeVar('T')


def weighted_choice(rng: random.Random, items: Sequence[T], weights: Sequence[float]) -> T:
    """重みに比例した確率で 1 つ選ぶ（random.choices と同じ考え方）。"""
    cumulative = list(itertools.accumulate(weights))  # 重みの累積和
    r = rng.random() * cumulative[-1]  # 0 以上、重みの合計未満の一様乱数
    return items[bisect.bisect_right(cumulative, r)]


class Bag(Generic[T]):
    """袋から札を引くように選ぶ。袋が空になったら全部戻してよく混ぜる。同じものが長く出ない（または出続けない）。"""

    def __init__(self, rng: random.Random, items: Sequence[T]) -> None:
        self.rng = rng
        self.items = list(items)
        self.remaining: list[T] = []

    def draw(self) -> T:
        if not self.remaining:
            self.remaining = list(self.items)
            self.rng.shuffle(self.remaining)  # フィッシャー–イェーツのシャッフル
        return self.remaining.pop()


def random_point_in_circle(rng: random.Random, radius: float) -> tuple[float, float]:
    """半径 radius の円の内部から、一様に点を選ぶ。"""
    angle = rng.uniform(0, math.tau)
    r = radius * math.sqrt(rng.random())  # 平方根を取らないと中心付近に偏る
    return r * math.cos(angle), r * math.sin(angle)


def probability_at_least_once(p: float, n: int) -> float:
    """確率 p で当たる抽選を n 回行ったとき、少なくとも 1 回当たる確率。"""
    return 1 - (1 - p) ** n


def tries_needed(p: float, target: float) -> int:
    """少なくとも 1 回当たる確率が target 以上になるのに必要な回数。"""
    return math.ceil(math.log(1 - target) / math.log(1 - p))


def main() -> None:
    print('--- 同じシードからは同じ列が出る ---')
    for _ in range(2):
        rng = random.Random(42)
        print([rng.randint(1, 6) for _ in range(10)])

    print('--- 重み付き抽選（10 万回） ---')
    rng = random.Random(1)
    items = ['ノーマル', 'レア', 'スーパーレア']
    weights = [80, 17, 3]
    counts = Counter(weighted_choice(rng, items, weights) for _ in range(100_000))
    for item, weight in zip(items, weights):
        print(f'{item}: 期待 {weight} %  結果 {counts[item] / 1000:.2f} %')

    print('--- 袋方式（1～4 の札を 12 回引く） ---')
    bag = Bag(random.Random(3), [1, 2, 3, 4])
    print([bag.draw() for _ in range(12)])

    print('--- 確率 1 % の抽選 ---')
    p = 0.01
    print(f'期待値: 平均 {1 / p:.0f} 回で初めて当たる')
    for n in (10, 50, 100, 200, 300):
        print(f'{n:3d} 回で少なくとも 1 回当たる確率: {probability_at_least_once(p, n) * 100:5.1f} %')
    for target in (0.5, 0.9, 0.99):
        print(f'{target * 100:.0f} % の人が当たるまでに必要な回数: {tries_needed(p, target)} 回')


if __name__ == '__main__':
    main()
