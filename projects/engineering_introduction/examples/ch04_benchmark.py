"""第 4 章: 処理時間を繰り返し測定し、ばらつきを要約する。

ソフトウェアの性能測定も計測の一種です。同じ処理でも、実行のたびに
処理時間はばらつきます。このサンプルでは、リストの並べ替えにかかる
時間を何度も測定し、次の点を確かめます。

* 1 回だけの測定値は当てにならないこと
* 最小値・中央値・平均値・標準偏差など、要約の仕方で印象が変わること
* 最初の数回 (ウォームアップ) は遅くなる場合があること

実行例::

    python ch04_benchmark.py --repeat 30
"""

from __future__ import annotations

import argparse
import random
import statistics
import time
from collections.abc import Callable


def measure(func: Callable[[], object], repeat: int) -> list[float]:
    """func を repeat 回実行し、それぞれの処理時間 [ms] を返す。"""
    durations = []
    for _ in range(repeat):
        start = time.perf_counter()  # 単調増加で分解能の高い時計
        func()
        durations.append((time.perf_counter() - start) * 1000)
    return durations


def summarize(durations: list[float]) -> None:
    """処理時間の要約統計量を表示する。"""
    quartiles = statistics.quantiles(durations, n=4)
    print(f"  回数      : {len(durations)}")
    print(f"  最小値    : {min(durations):8.3f} ms")
    print(f"  第 1 四分位: {quartiles[0]:8.3f} ms")
    print(f"  中央値    : {statistics.median(durations):8.3f} ms")
    print(f"  平均値    : {statistics.mean(durations):8.3f} ms")
    print(f"  第 3 四分位: {quartiles[2]:8.3f} ms")
    print(f"  最大値    : {max(durations):8.3f} ms")
    print(f"  標準偏差  : {statistics.stdev(durations):8.3f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=200_000,
                        help="並べ替える要素の数")
    parser.add_argument("--repeat", type=int, default=30,
                        help="測定を繰り返す回数")
    args = parser.parse_args()

    rng = random.Random(0)
    data = [rng.random() for _ in range(args.size)]

    def task() -> list[float]:
        return sorted(data)

    durations = measure(task, args.repeat)
    print("最初の 3 回の測定値 [ms]:",
          ", ".join(f"{d:.3f}" for d in durations[:3]))
    print("全測定値の要約:")
    summarize(durations)

    # 外れ値 (中央値の 1.5 倍を超える値) の数を数える
    limit = statistics.median(durations) * 1.5
    outliers = [d for d in durations if d > limit]
    print(f"中央値の 1.5 倍を超えた測定値: {len(outliers)} 個")


if __name__ == "__main__":
    main()
