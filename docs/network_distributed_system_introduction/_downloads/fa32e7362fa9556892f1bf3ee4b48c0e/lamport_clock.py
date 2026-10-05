"""ランポート時計（Lamport clock）の動きを示すサンプルです。

3 つのプロセス P1、P2、P3 が、内部イベント、メッセージの送信、
メッセージの受信からなる固定のシナリオを実行します。各イベントに
ランポート時計の値（タイムスタンプ）を割り当てて表示し、最後に
(タイムスタンプ, プロセス ID) の組で並べた全順序を表示します。

シナリオ（vector_clock.py と同じ）:

    P1: a1 内部、a2 m1 を P2 へ送信、a3 m3 を受信、a4 内部
    P2: b1 内部、b2 m1 を受信、b3 m2 を P3 へ送信
    P3: c1 内部、c2 m3 を P1 へ送信、c3 m2 を受信

実行方法:

    python lamport_clock.py
"""

from dataclasses import dataclass

# プロセス名とプロセス ID（全順序の同点を決めるのに使う）
PROCESS_IDS: dict[str, int] = {"P1": 1, "P2": 2, "P3": 3}


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


class LamportClock:
    """1 つのプロセスが持つランポート時計です。"""

    def __init__(self) -> None:
        self.time = 0

    def tick(self) -> int:
        """内部イベントと送信の前に、時計を 1 進めます。"""
        self.time += 1
        return self.time

    def receive(self, timestamp: int) -> int:
        """受信時は、自分の値と受け取った値の大きい方に 1 を足します。"""
        self.time = max(self.time, timestamp) + 1
        return self.time


def describe(step: Step) -> str:
    """イベントの内容を表す文字列を返します。"""
    if step.kind == "send":
        return f"送信 {step.message} → {step.peer}"
    if step.kind == "receive":
        return f"受信 {step.message} ← {step.peer}"
    return "内部"


def run() -> dict[str, int]:
    """シナリオを実行し、イベント名からタイムスタンプへの辞書を返します。"""
    clocks = {name: LamportClock() for name in PROCESS_IDS}
    # 送信中のメッセージ（名前 → 付けられたタイムスタンプ）
    in_flight: dict[str, int] = {}
    stamps: dict[str, int] = {}

    print("イベントの処理（実行順）")
    for step in SCENARIO:
        clock = clocks[step.process]
        before = clock.time
        note = ""
        if step.kind == "receive":
            received = in_flight.pop(step.message)
            stamp = clock.receive(received)
            note = f"max({before}, {received}) + 1"
        else:
            stamp = clock.tick()
            note = f"{before} + 1"
            if step.kind == "send":
                # メッセージには送信イベントのタイムスタンプを付ける
                in_flight[step.message] = stamp
        stamps[step.name] = stamp
        print(
            f"  {step.name} {step.process} {describe(step):<12}"
            f" L = {stamp}  ({note})"
        )
    return stamps


def main() -> None:
    stamps = run()

    print()
    print("プロセスごとのタイムスタンプ")
    for process in PROCESS_IDS:
        line = ", ".join(
            f"{s.name}={stamps[s.name]}"
            for s in SCENARIO
            if s.process == process
        )
        print(f"  {process}: {line}")

    # (タイムスタンプ, プロセス ID) の辞書式順序で全順序を作る
    steps = sorted(
        SCENARIO,
        key=lambda s: (stamps[s.name], PROCESS_IDS[s.process]),
    )
    print()
    print("全順序（タイムスタンプ, プロセス ID の順に並べる）")
    items = [
        f"{s.name}({stamps[s.name]},{PROCESS_IDS[s.process]})"
        for s in steps
    ]
    # 1 行が長くなるので、5 件ずつ折り返して表示する
    for i in range(0, len(items), 5):
        prefix = "  " if i == 0 else "  < "
        print(prefix + " < ".join(items[i:i + 5]))


if __name__ == "__main__":
    main()
