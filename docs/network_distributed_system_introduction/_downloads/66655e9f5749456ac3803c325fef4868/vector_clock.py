"""ベクトル時計（vector clock）で因果関係と並行性を判定するサンプルです。

lamport_clock.py と同じシナリオを 3 つのプロセス P1、P2、P3 で実行し、
各イベントのベクトル時計を計算して表示します。その後、2 つのイベントの
組について、一方が他方の「前」か「後」か、それとも「並行」かを、
ベクトル時計の比較だけで判定して表示します。

シナリオ:

    P1: a1 内部、a2 m1 を P2 へ送信、a3 m3 を受信、a4 内部
    P2: b1 内部、b2 m1 を受信、b3 m2 を P3 へ送信
    P3: c1 内部、c2 m3 を P1 へ送信、c3 m2 を受信

実行方法:

    python vector_clock.py            # 用意した組について判定する
    python vector_clock.py a3 b2      # 指定した 2 つのイベントを判定する
"""

import sys
from dataclasses import dataclass

# プロセスの並び。ベクトルの何番目の要素がどのプロセスかを表す。
PROCESSES: list[str] = ["P1", "P2", "P3"]

# 引数がないときに判定するイベントの組
DEFAULT_PAIRS: list[tuple[str, str]] = [
    ("a1", "b2"),
    ("c3", "a2"),
    ("c2", "a4"),
    ("a1", "b1"),
    ("c1", "b2"),
    ("a3", "b2"),
    ("a4", "b3"),
    ("a3", "c3"),
]


@dataclass(frozen=True)
class Step:
    """シナリオの 1 つのイベントを表します。"""

    process: str  # イベントが起きるプロセス
    name: str  # イベントの名前（a1 など）
    kind: str  # "internal"（内部）、"send"（送信）、"receive"（受信）
    message: str = ""  # 送受信するメッセージの名前
    peer: str = ""  # 送信先または送信元のプロセス


# 実行順に並べたシナリオ。受信は必ず対応する送信より後に置く。
SCENARIO: list[Step] = [
    Step("P1", "a1", "internal"),
    Step("P2", "b1", "internal"),
    Step("P3", "c1", "internal"),
    Step("P1", "a2", "send", "m1", "P2"),
    Step("P3", "c2", "send", "m3", "P1"),
    Step("P2", "b2", "receive", "m1", "P1"),
    Step("P1", "a3", "receive", "m3", "P3"),
    Step("P2", "b3", "send", "m2", "P3"),
    Step("P1", "a4", "internal"),
    Step("P3", "c3", "receive", "m2", "P2"),
]

Vector = tuple[int, ...]


class VectorClock:
    """1 つのプロセスが持つベクトル時計です。"""

    def __init__(self, index: int, size: int) -> None:
        self.index = index  # 自分のプロセスに対応する要素の位置
        self.vector = [0] * size

    def tick(self) -> Vector:
        """内部イベントと送信の前に、自分の要素だけを 1 進めます。"""
        self.vector[self.index] += 1
        return tuple(self.vector)

    def receive(self, other: Vector) -> Vector:
        """受信時は、要素ごとの最大値をとってから自分の要素を進めます。"""
        self.vector = [max(a, b) for a, b in zip(self.vector, other)]
        return self.tick()


def less_equal(u: Vector, v: Vector) -> bool:
    """すべての要素について u[i] <= v[i] なら True を返します。"""
    return all(a <= b for a, b in zip(u, v))


def compare(u: Vector, v: Vector) -> str:
    """ベクトル u と v のイベントの関係を判定します。"""
    if u == v:
        return "同じ"
    if less_equal(u, v):
        return "前"  # u のイベントが v のイベントより前に起きた
    if less_equal(v, u):
        return "後"  # u のイベントが v のイベントより後に起きた
    return "並行"  # どちらも他方より前ではない


def fmt(v: Vector) -> str:
    """ベクトルを [1,0,0] の形の文字列にします。"""
    return "[" + ",".join(str(x) for x in v) + "]"


def run() -> dict[str, Vector]:
    """シナリオを実行し、イベント名からベクトル時計への辞書を返します。"""
    clocks = {
        name: VectorClock(i, len(PROCESSES))
        for i, name in enumerate(PROCESSES)
    }
    in_flight: dict[str, Vector] = {}  # 送信中のメッセージとその値
    vectors: dict[str, Vector] = {}

    print("イベントの処理（実行順）")
    for step in SCENARIO:
        clock = clocks[step.process]
        if step.kind == "receive":
            received = in_flight.pop(step.message)
            vec = clock.receive(received)
            what = f"受信 {step.message} {fmt(received)} ← {step.peer}"
        else:
            vec = clock.tick()
            what = "内部"
            if step.kind == "send":
                in_flight[step.message] = vec
                what = f"送信 {step.message} → {step.peer}"
        vectors[step.name] = vec
        print(f"  {step.name} {step.process} V = {fmt(vec)}  {what}")
    return vectors


def main() -> None:
    vectors = run()

    if len(sys.argv) == 3:
        pairs = [(sys.argv[1], sys.argv[2])]
    else:
        pairs = DEFAULT_PAIRS

    print()
    print("2 つのイベントの関係")
    for x, y in pairs:
        if x not in vectors or y not in vectors:
            print(f"  {x}, {y}: 存在しないイベントです")
            continue
        u, v = vectors[x], vectors[y]
        relation = compare(u, v)
        if relation == "前":
            detail = f"{x} → {y}"
        elif relation == "後":
            detail = f"{y} → {x}"
        elif relation == "並行":
            detail = f"{x} ∥ {y}"
        else:
            detail = "同じイベント"
        print(f"  {x} {fmt(u)} と {y} {fmt(v)}: {relation}（{detail}）")


if __name__ == "__main__":
    main()
