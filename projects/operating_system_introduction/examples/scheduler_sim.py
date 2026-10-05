"""CPU スケジューリングのシミュレーター。

到着時刻と CPU バースト時間 (CPU を使う時間) が決まった
プロセスの集まりに対して、次の 3 つのアルゴリズムを適用し、
実行の順序 (ガントチャート) と評価指標を比べます。

* FCFS: 到着順に実行する (横取りなし)
* SJF: CPU バースト時間が最も短いものから実行する (横取りなし)
* RR: タイムクォンタムごとに順番に実行する (横取りあり)

時間は 1 単位ずつ進めます。入出力による待ちはないものとします。

実行方法::

    python scheduler_sim.py
"""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    """スケジューリングの対象となるプロセス。"""

    name: str
    arrival: int  # 到着時刻
    burst: int  # CPU バースト時間


@dataclass
class Result:
    """1 つのプロセスについてのシミュレーション結果。"""

    process: Process
    first_run: int  # 初めて CPU を割り当てられた時刻
    finish: int  # 終了時刻

    @property
    def turnaround(self) -> int:
        """ターンアラウンド時間 = 終了時刻 - 到着時刻。"""
        return self.finish - self.process.arrival

    @property
    def waiting(self) -> int:
        """待ち時間 = ターンアラウンド時間 - CPU バースト時間。"""
        return self.turnaround - self.process.burst

    @property
    def response(self) -> int:
        """応答時間 = 初めて実行された時刻 - 到着時刻。"""
        return self.first_run - self.process.arrival


def summarize(
    processes: list[Process], timeline: list[str]
) -> list[Result]:
    """時刻ごとの実行プロセス名の列から、プロセスごとの結果を求める。"""
    results = []
    for p in processes:
        times = [t for t, name in enumerate(timeline) if name == p.name]
        results.append(Result(p, first_run=times[0], finish=times[-1] + 1))
    return results


def fcfs(processes: list[Process]) -> list[str]:
    """FCFS で実行した場合の、時刻ごとの実行プロセス名の列を返す。"""
    timeline: list[str] = []
    for p in sorted(processes, key=lambda p: p.arrival):
        while len(timeline) < p.arrival:
            timeline.append("-")  # CPU が空いている
        timeline.extend([p.name] * p.burst)
    return timeline


def sjf(processes: list[Process]) -> list[str]:
    """横取りなしの SJF で実行した場合の、時刻ごとの実行プロセス名の列を返す。"""
    timeline: list[str] = []
    waiting = list(processes)
    while waiting:
        now = len(timeline)
        ready = [p for p in waiting if p.arrival <= now]
        if not ready:
            timeline.append("-")
            continue
        # 到着済みのうち、CPU バースト時間が最も短いものを選ぶ
        chosen = min(ready, key=lambda p: (p.burst, p.arrival))
        timeline.extend([chosen.name] * chosen.burst)
        waiting.remove(chosen)
    return timeline


def round_robin(processes: list[Process], quantum: int) -> list[str]:
    """ラウンドロビンで実行した場合の、時刻ごとの実行プロセス名の列を返す。"""
    timeline: list[str] = []
    remaining = {p.name: p.burst for p in processes}
    not_arrived = sorted(processes, key=lambda p: p.arrival)
    queue: deque[str] = deque()

    def admit(now: int) -> None:
        """時刻 now までに到着したプロセスを実行可能キューに入れる。"""
        while not_arrived and not_arrived[0].arrival <= now:
            queue.append(not_arrived.pop(0).name)

    admit(0)
    while queue or not_arrived:
        if not queue:
            timeline.append("-")
            admit(len(timeline))
            continue
        name = queue.popleft()
        run = min(quantum, remaining[name])
        for _ in range(run):
            timeline.append(name)
            admit(len(timeline))  # 実行中に到着したプロセスを先に並べる
        remaining[name] -= run
        if remaining[name] > 0:
            queue.append(name)  # 使い切れなかったら最後尾に戻る
    return timeline


def report(
    title: str, processes: list[Process], timeline: list[str]
) -> None:
    """ガントチャートと評価指標を表示する。"""
    print(f"=== {title} ===")
    print("時刻 : " + "".join(f"{t % 10}" for t in range(len(timeline))))
    print("実行 : " + "".join(name[-1] for name in timeline))
    results = summarize(processes, timeline)
    print("プロセス  到着  バースト  終了  ターンアラウンド  待ち  応答")
    for r in results:
        p = r.process
        print(
            f"{p.name:>8}  {p.arrival:>4}  {p.burst:>8}  {r.finish:>4}"
            f"  {r.turnaround:>16}  {r.waiting:>4}  {r.response:>4}"
        )
    n = len(results)
    print(
        f"平均ターンアラウンド時間 {sum(r.turnaround for r in results) / n:.2f}"
        f" / 平均待ち時間 {sum(r.waiting for r in results) / n:.2f}"
        f" / 平均応答時間 {sum(r.response for r in results) / n:.2f}"
    )
    print()


def main() -> None:
    processes = [
        Process("P1", arrival=0, burst=7),
        Process("P2", arrival=2, burst=4),
        Process("P3", arrival=4, burst=1),
        Process("P4", arrival=5, burst=4),
    ]
    report("FCFS", processes, fcfs(processes))
    report("SJF", processes, sjf(processes))
    report("RR (タイムクォンタム 2)", processes, round_robin(processes, 2))


if __name__ == "__main__":
    main()
