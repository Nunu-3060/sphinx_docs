"""ランポート時計（論理時計）をシミュレートするサンプル。

3 つのプロセス P1、P2、P3 がローカル処理とメッセージの送受信を
行う筋書きを決めておき、各イベントに付くランポート時刻を表示する。
最後に、ランポート時刻とプロセス名の組でイベントを全順序に並べる。
筋書きは固定なので、出力は毎回同じになる。

実行方法: python ch12_lamport_clock.py
関連する章: 第 12 章「分散システム」
"""

from dataclasses import dataclass


@dataclass
class Process:
    """ランポート時計を持つプロセス。"""

    name: str
    clock: int = 0

    def local_event(self) -> int:
        """ローカル処理: 時計を 1 進める。"""
        self.clock += 1
        return self.clock

    def send(self) -> int:
        """送信: 時計を 1 進め、その値をメッセージに付ける。"""
        self.clock += 1
        return self.clock

    def receive(self, timestamp: int) -> int:
        """受信: 自分の時計とメッセージの時刻の大きい方に 1 を足す。"""
        self.clock = max(self.clock, timestamp) + 1
        return self.clock


@dataclass
class Event:
    """記録したイベント。"""

    process: str
    timestamp: int
    description: str


# 筋書き: (種類, プロセス名, メッセージ名, 宛先)
SCENARIO: list[tuple[str, str, str, str]] = [
    ("local", "P1", "", ""),
    ("send", "P1", "m1", "P2"),
    ("local", "P3", "", ""),
    ("local", "P3", "", ""),
    ("send", "P3", "m2", "P2"),
    ("recv", "P2", "m1", ""),
    ("recv", "P2", "m2", ""),
    ("send", "P2", "m3", "P1"),
    ("local", "P3", "", ""),
    ("recv", "P1", "m3", ""),
]


def run(scenario: list[tuple[str, str, str, str]]) -> list[Event]:
    """筋書きを順に実行し、イベントの記録を返す。"""
    procs = {name: Process(name) for name in ("P1", "P2", "P3")}
    in_flight: dict[str, int] = {}  # 送信中のメッセージ名 -> 付いた時刻
    events: list[Event] = []
    for kind, name, msg, dest in scenario:
        proc = procs[name]
        if kind == "local":
            ts = proc.local_event()
            desc = "ローカル処理"
        elif kind == "send":
            ts = proc.send()
            in_flight[msg] = ts
            desc = f"{msg} を {dest} へ送信"
        else:
            sent_ts = in_flight.pop(msg)
            ts = proc.receive(sent_ts)
            desc = f"{msg} を受信（メッセージの時刻 {sent_ts}）"
        events.append(Event(name, ts, desc))
    return events


def main() -> None:
    """筋書きを実行し、実行順と全順序の 2 通りで表示する。"""
    events = run(SCENARIO)
    print("== 実行順 ==")
    for e in events:
        print(f"{e.process}  L={e.timestamp}  {e.description}")
    print("== (ランポート時刻, プロセス名) による全順序 ==")
    for e in sorted(events, key=lambda e: (e.timestamp, e.process)):
        print(f"L={e.timestamp}  {e.process}  {e.description}")


if __name__ == "__main__":
    main()
