"""逐次・スレッド・プロセス・asyncio の実行時間を比較するベンチマーク。

CPU バウンドな処理と I/O バウンドな処理を、それぞれ 4 通りの方法で TASKS 個ずつ実行し、経過時間を表示する。
プロセスの計測時間には、プロセスプールの起動と終了にかかる時間も含まれる。
結果は CPU のコア数や OS によって変わるため、目安として扱うこと。
"""

import asyncio
import os
import time
from collections.abc import Callable, Coroutine
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any

TASKS = 8
CPU_LOOPS = 3_000_000
IO_MILLISECONDS = 500

Task = Callable[[int], object]


def cpu_task(loops: int) -> int:
    """整数の 2 乗の総和を計算する（CPU バウンド）。"""
    total = 0
    for i in range(loops):
        total += i * i
    return total


def io_task(milliseconds: int) -> int:
    """指定したミリ秒だけ待つ（I/O バウンドの模擬）。"""
    time.sleep(milliseconds / 1000)
    return milliseconds


async def cpu_task_async(loops: int) -> int:
    """cpu_task をそのままコルーチンにしたもの。await する箇所が無いため、他のタスクに切り替わらない。"""
    return cpu_task(loops)


async def io_task_async(milliseconds: int) -> int:
    """asyncio.sleep() で待つ。待っている間は他のタスクが実行される。"""
    await asyncio.sleep(milliseconds / 1000)
    return milliseconds


def run_sequential(task: Task, arg: int) -> None:
    for _ in range(TASKS):
        task(arg)


def run_threads(task: Task, arg: int) -> None:
    with ThreadPoolExecutor(max_workers=TASKS) as executor:
        list(executor.map(task, [arg] * TASKS))


def run_processes(task: Task, arg: int) -> None:
    workers = min(TASKS, os.cpu_count() or 1)
    with ProcessPoolExecutor(max_workers=workers) as executor:
        list(executor.map(task, [arg] * TASKS))


def run_asyncio(task: Callable[[int], Coroutine[Any, Any, int]], arg: int) -> None:
    async def runner() -> None:
        async with asyncio.TaskGroup() as group:
            for _ in range(TASKS):
                group.create_task(task(arg))

    asyncio.run(runner())


def measure(func: Callable[[], None]) -> float:
    """func の実行にかかった時間（秒）を返す。"""
    start = time.perf_counter()
    func()
    return time.perf_counter() - start


def main() -> None:
    print(f"CPU コア数: {os.cpu_count()}, タスク数: {TASKS}")
    rows: list[tuple[str, Callable[[], None], Callable[[], None]]] = [
        ("逐次", lambda: run_sequential(cpu_task, CPU_LOOPS), lambda: run_sequential(io_task, IO_MILLISECONDS)),
        ("スレッド", lambda: run_threads(cpu_task, CPU_LOOPS), lambda: run_threads(io_task, IO_MILLISECONDS)),
        ("プロセス", lambda: run_processes(cpu_task, CPU_LOOPS), lambda: run_processes(io_task, IO_MILLISECONDS)),
        ("asyncio", lambda: run_asyncio(cpu_task_async, CPU_LOOPS),
         lambda: run_asyncio(io_task_async, IO_MILLISECONDS)),
    ]
    for name, cpu_run, io_run in rows:
        cpu_seconds = measure(cpu_run)
        io_seconds = measure(io_run)
        print(f"{name}: CPU バウンド {cpu_seconds:.2f} 秒, I/O バウンド {io_seconds:.2f} 秒")


if __name__ == "__main__":
    main()
