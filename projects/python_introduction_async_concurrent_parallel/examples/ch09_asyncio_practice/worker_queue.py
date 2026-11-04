"""asyncio.Queue で決まった数のワーカーに仕事を分配するサンプル。

queue.join() ですべての仕事が終わるのを待ち、その後でワーカーのタスクをキャンセルして終了させる。
"""

import asyncio
import random


async def worker(name: str, jobs: "asyncio.Queue[int]", results: list[str]) -> None:
    while True:
        number = await jobs.get()
        try:
            await asyncio.sleep(random.uniform(0.1, 0.5))  # I/O 処理の代わり
            results.append(f"{name} が仕事 {number} を処理した")
        finally:
            jobs.task_done()  # 処理が終わったことをキューに知らせる


async def main() -> None:
    jobs: "asyncio.Queue[int]" = asyncio.Queue()
    for number in range(10):
        jobs.put_nowait(number)

    results: list[str] = []
    workers = [asyncio.create_task(worker(f"ワーカー {i}", jobs, results)) for i in range(3)]

    await jobs.join()  # すべての仕事で task_done() が呼ばれるまで待つ

    for task in workers:
        task.cancel()  # 無限ループで待ち続けているワーカーを終了させる
    await asyncio.gather(*workers, return_exceptions=True)

    print("\n".join(results))


if __name__ == "__main__":
    asyncio.run(main())
