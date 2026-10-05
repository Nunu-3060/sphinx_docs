"""分岐予測器の的中率を、いくつかの分岐パターンで比較するサンプル。

常に成立と予測する方式、1 ビットカウンタ、2 ビット飽和カウンタ、
gshare の 4 つの予測器に同じ分岐列を与え、的中率を表にして表示します。
分岐列は、ループの分岐、交互に成立する分岐、相関のある 2 つの分岐、
偏りのある乱数の分岐、偏りのない乱数の分岐です。

実行方法: python branch_predictor.py
"""

import random
import unicodedata

Trace = list[tuple[int, bool]]  # (分岐命令のアドレス, 成立したか)


class Predictor:
    """分岐予測器の基底クラス（常に成立と予測する）。"""

    name = "常に成立"

    def predict(self, pc: int) -> bool:
        """アドレス pc の分岐が成立するかを予測する。"""
        return True

    def update(self, pc: int, taken: bool) -> None:
        """実際の結果 taken で内部状態を更新する。"""


class OneBit(Predictor):
    """前回の結果をそのまま予測に使う 1 ビットの予測器。"""

    name = "1 ビット"

    def __init__(self, bits: int = 10) -> None:
        self.mask = (1 << bits) - 1
        self.table = [True] * (1 << bits)

    def predict(self, pc: int) -> bool:
        return self.table[(pc >> 2) & self.mask]

    def update(self, pc: int, taken: bool) -> None:
        self.table[(pc >> 2) & self.mask] = taken


class TwoBit(Predictor):
    """2 ビット飽和カウンタ（0, 1: 不成立と予測、2, 3: 成立と予測）。"""

    name = "2 ビット"

    def __init__(self, bits: int = 10) -> None:
        self.mask = (1 << bits) - 1
        self.table = [2] * (1 << bits)  # 初期値は「弱く成立」

    def index(self, pc: int) -> int:
        """カウンタ表の添字を求める。"""
        return (pc >> 2) & self.mask

    def predict(self, pc: int) -> bool:
        return self.table[self.index(pc)] >= 2

    def update(self, pc: int, taken: bool) -> None:
        i = self.index(pc)
        if taken:
            self.table[i] = min(self.table[i] + 1, 3)
        else:
            self.table[i] = max(self.table[i] - 1, 0)


class Gshare(TwoBit):
    """大域分岐履歴とアドレスの XOR で 2 ビットカウンタを選ぶ予測器。"""

    name = "gshare"

    def __init__(self, bits: int = 10) -> None:
        super().__init__(bits)
        self.history = 0  # 直近の分岐結果（1 = 成立）を並べたビット列

    def index(self, pc: int) -> int:
        return ((pc >> 2) ^ self.history) & self.mask

    def update(self, pc: int, taken: bool) -> None:
        super().update(pc, taken)  # 履歴を更新する前の添字で更新する
        self.history = ((self.history << 1) | int(taken)) & self.mask


def pad(text: str, width: int, left: bool = False) -> str:
    """全角文字を幅 2 として、text を幅 width にそろえる。"""
    w = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
            for c in text)
    space = " " * max(width - w, 0)
    return text + space if left else space + text


def make_traces() -> dict[str, Trace]:
    """比較に使う分岐列を作る。"""
    rng = random.Random(1)  # 毎回同じ結果になるよう種を固定する
    n = 10000
    loop: Trace = []
    for _ in range(n // 10):  # 10 回まわるループの末尾の分岐
        loop += [(0x100, True)] * 9 + [(0x100, False)]
    alternate: Trace = [(0x200, i % 2 == 0) for i in range(n)]
    correlated: Trace = []
    for _ in range(n // 2):
        a = rng.random() < 0.5
        correlated.append((0x300, a))  # 乱数で決まる分岐
        correlated.append((0x304, a))  # 直前の分岐と同じ条件の分岐
    return {
        "ループ（10 回）": loop,
        "交互": alternate,
        "相関あり": correlated,
        "乱数 90% 成立": [(0x400, rng.random() < 0.9) for _ in range(n)],
        "乱数 50% 成立": [(0x500, rng.random() < 0.5) for _ in range(n)],
    }


def accuracy(pred: Predictor, trace: Trace) -> float:
    """分岐列 trace に対する予測器 pred の的中率を返す。"""
    hits = 0
    for pc, taken in trace:
        hits += pred.predict(pc) == taken
        pred.update(pc, taken)
    return hits / len(trace)


def main() -> None:
    """各分岐列について、4 つの予測器の的中率を表示する。"""
    kinds: list[type[Predictor]] = [Predictor, OneBit, TwoBit, Gshare]
    head = "".join(pad(k.name, 10) for k in kinds)
    print(pad("分岐列", 16, left=True) + head)
    for label, trace in make_traces().items():
        cells = "".join(pad(f"{accuracy(k(), trace):.1%}", 10)
                        for k in kinds)
        print(pad(label, 16, left=True) + cells)


if __name__ == "__main__":
    main()
