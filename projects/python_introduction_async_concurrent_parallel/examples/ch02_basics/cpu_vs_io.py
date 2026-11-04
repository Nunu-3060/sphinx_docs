"""CPU バウンドな処理と I/O バウンドな処理の違いを確かめるサンプル。

time.perf_counter() で経過時間を、time.process_time() で CPU 時間を測る。
CPU バウンドな処理では両者がほぼ等しくなり、I/O バウンドな処理では CPU 時間がほぼ 0 になる。
"""

import time
from collections.abc import Callable


def cpu_bound() -> int:
    """整数の 2 乗の総和を計算する（CPU を使い続ける処理）。"""
    total = 0
    for i in range(5_000_000):
        total += i * i
    return total


def io_bound() -> None:
    """I/O の待ち時間を time.sleep() で模擬する（CPU をほとんど使わない処理）。"""
    time.sleep(0.5)


def measure(name: str, func: Callable[[], object]) -> None:
    """func を 1 回実行し、経過時間と CPU 時間を表示する。"""
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    func()
    wall = time.perf_counter() - wall_start
    cpu = time.process_time() - cpu_start
    print(f"{name}: 経過時間 {wall:.2f} 秒, CPU 時間 {cpu:.2f} 秒")


def main() -> None:
    measure("CPU バウンド", cpu_bound)
    measure("I/O バウンド", io_bound)


if __name__ == "__main__":
    main()
