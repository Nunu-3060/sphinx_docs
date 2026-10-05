"""第 6 章: 周期処理のタイミングのずれ (ジッターとドリフト) を測定する。

制御プログラムは、一定の周期で計算を繰り返します。周期を作る方法を
2 つ比べます。

* 方法 1: 処理の後に「周期と同じ時間だけ待つ」
  処理時間の分だけ周期が延び、ずれが積み重なる (ドリフト)
* 方法 2: 「次に実行すべき時刻」まで待つ
  1 回ごとのばらつき (ジッター) はあるが、ずれは積み重ならない

汎用の OS の上では、どちらの方法でも待ち時間はある程度ばらつきます。

実行例::

    python ch06_jitter.py --period 10 --count 200
"""

from __future__ import annotations

import argparse
import statistics
import time


def work() -> None:
    """制御の計算の代わりに、約 2 ms かかる処理を行う。"""
    end = time.perf_counter() + 0.002
    while time.perf_counter() < end:
        pass


def run_fixed_sleep(period: float, count: int) -> list[float]:
    """方法 1: 処理の後に周期と同じ時間だけ待つ。開始時刻の列を返す。"""
    starts = []
    for _ in range(count):
        starts.append(time.perf_counter())
        work()
        time.sleep(period)
    return starts


def run_deadline(period: float, count: int) -> list[float]:
    """方法 2: 次に実行すべき時刻まで待つ。開始時刻の列を返す。"""
    starts = []
    next_time = time.perf_counter()
    for _ in range(count):
        starts.append(time.perf_counter())
        work()
        next_time += period
        delay = next_time - time.perf_counter()
        if delay > 0:
            time.sleep(delay)
    return starts


def report(name: str, starts: list[float], period: float) -> None:
    """周期の統計と、累積のずれを表示する。"""
    intervals = [(b - a) * 1000 for a, b in zip(starts, starts[1:])]
    drift = (starts[-1] - starts[0] - period * (len(starts) - 1)) * 1000
    print(f"{name}")
    print(f"  周期の平均   : {statistics.mean(intervals):7.2f} ms")
    print(f"  周期の標準偏差: {statistics.stdev(intervals):7.2f} ms")
    print(f"  周期の最大   : {max(intervals):7.2f} ms")
    print(f"  累積のずれ   : {drift:7.1f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", type=float, default=10.0,
                        help="目標の周期 [ms]")
    parser.add_argument("--count", type=int, default=200,
                        help="繰り返す回数")
    args = parser.parse_args()
    period = args.period / 1000

    print(f"目標の周期 {args.period} ms、{args.count} 回")
    report("方法 1: 毎回、周期と同じ時間だけ待つ",
           run_fixed_sleep(period, args.count), period)
    report("方法 2: 次に実行すべき時刻まで待つ",
           run_deadline(period, args.count), period)


if __name__ == "__main__":
    main()
