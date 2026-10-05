"""CPU スケジューリングのアルゴリズムを比較するサンプル。

FCFS、SJF（非プリエンプティブ）、ラウンドロビンの 3 つの方式で
同じプロセス群を実行したときの実行順序と平均待ち時間を表示する。
乱数は使わないので、結果は毎回同じになる。

実行方法: python ch08_scheduler.py
関連する章: 第 8 章「オペレーティングシステム」
"""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Proc:
    """プロセスの到着時刻と CPU バースト（必要な実行時間）を表す。"""

    name: str
    arrival: int
    burst: int


# (プロセス名, 実行を開始した時刻, 実行を終えた時刻) の並び
Timeline = list[tuple[str, int, int]]

PROCS = [Proc("A", 0, 8), Proc("B", 1, 4), Proc("C", 2, 9), Proc("D", 3, 5)]


def fcfs(procs: list[Proc]) -> Timeline:
    """到着順に、各プロセスを最後まで実行する。"""
    timeline: Timeline = []
    t = 0
    for p in sorted(procs, key=lambda p: p.arrival):
        t = max(t, p.arrival)  # CPU が空いていれば到着を待つ
        timeline.append((p.name, t, t + p.burst))
        t += p.burst
    return timeline


def sjf(procs: list[Proc]) -> Timeline:
    """到着済みのうちバーストが最短のものを選び、最後まで実行する。"""
    timeline: Timeline = []
    waiting = sorted(procs, key=lambda p: p.arrival)
    t = 0
    while waiting:
        ready = [p for p in waiting if p.arrival <= t]
        if not ready:
            t = waiting[0].arrival
            continue
        p = min(ready, key=lambda p: (p.burst, p.arrival))
        waiting.remove(p)
        timeline.append((p.name, t, t + p.burst))
        t += p.burst
    return timeline


def round_robin(procs: list[Proc], quantum: int) -> Timeline:
    """各プロセスを最大 quantum だけ実行し、終わらなければ列の末尾へ戻す。

    実行を中断した時刻に到着したプロセスは、中断したプロセスより先に
    列へ入れる。
    """
    timeline: Timeline = []
    pending = deque(sorted(procs, key=lambda p: p.arrival))
    remaining = {p.name: p.burst for p in procs}
    queue: deque[Proc] = deque()
    t = 0
    while pending or queue:
        if not queue:
            t = max(t, pending[0].arrival)
        while pending and pending[0].arrival <= t:
            queue.append(pending.popleft())
        p = queue.popleft()
        run = min(quantum, remaining[p.name])
        timeline.append((p.name, t, t + run))
        t += run
        remaining[p.name] -= run
        while pending and pending[0].arrival <= t:
            queue.append(pending.popleft())
        if remaining[p.name] > 0:
            queue.append(p)
    return timeline


def waiting_times(procs: list[Proc], timeline: Timeline) -> dict[str, int]:
    """待ち時間 = 終了時刻 - 到着時刻 - バースト を求める。"""
    finish = {name: end for name, _, end in timeline}
    return {p.name: finish[p.name] - p.arrival - p.burst for p in procs}


def report(title: str, timeline: Timeline) -> None:
    """実行順序と、各プロセスの待ち時間および平均を表示する。"""
    print(f"[{title}]")
    print("  実行順序: " + " ".join(f"{n}({s}-{e})" for n, s, e in timeline))
    waits = waiting_times(PROCS, timeline)
    print("  待ち時間: " + ", ".join(f"{n}={w}" for n, w in waits.items()))
    print(f"  平均待ち時間: {sum(waits.values()) / len(waits):.2f}")


def main() -> None:
    """3 つの方式の結果を順に表示する。"""
    print("プロセス: " + ", ".join(
        f"{p.name}(到着 {p.arrival}, バースト {p.burst})" for p in PROCS))
    report("FCFS", fcfs(PROCS))
    report("SJF", sjf(PROCS))
    report("ラウンドロビン（クォンタム 3）", round_robin(PROCS, 3))


if __name__ == "__main__":
    main()
