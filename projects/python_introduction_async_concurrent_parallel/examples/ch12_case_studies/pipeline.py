"""I/O と CPU の処理が混在するパイプラインのケーススタディ（asyncio とプロセスプールの併用）。

データの取得（I/O バウンド）は asyncio で並行に行い、取得したデータの解析（CPU バウンド）は
loop.run_in_executor() でプロセスプールに任せる。
解析をイベントループの中で直接実行する場合と比べると、取得と解析が重なって実行されるため速くなる。
"""

import asyncio
import hashlib
import time
from concurrent.futures import ProcessPoolExecutor

ITEMS = 12
CONCURRENCY = 4


async def download(item_id: int) -> bytes:
    """データの取得を模擬する（0.3 秒かかる I/O）。"""
    await asyncio.sleep(0.3)
    return f"data-{item_id}".encode() * 1000


def analyze(data: bytes) -> str:
    """データの解析を模擬する（CPU バウンド）。ハッシュ値を繰り返し計算する。"""
    digest = data
    for _ in range(200_000):
        digest = hashlib.sha256(digest).digest()
    return digest.hex()[:12]


async def process_blocking(item_id: int, semaphore: asyncio.Semaphore) -> str:
    """解析をイベントループの中で直接実行する（悪い例）。解析中は他のタスクがすべて止まる。"""
    async with semaphore:
        data = await download(item_id)
    return analyze(data)


async def process_offloaded(item_id: int, semaphore: asyncio.Semaphore, executor: ProcessPoolExecutor) -> str:
    """解析をプロセスプールで実行する。解析中も他のタスクの取得は進む。"""
    async with semaphore:
        data = await download(item_id)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, analyze, data)


async def main() -> None:
    semaphore = asyncio.Semaphore(CONCURRENCY)

    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        for i in range(ITEMS):
            group.create_task(process_blocking(i, semaphore))
    print(f"イベントループの中で解析: {time.perf_counter() - start:.2f} 秒")

    with ProcessPoolExecutor() as executor:
        executor.submit(int).result()  # プロセスの起動を計測から除くため、先に一度使っておく
        start = time.perf_counter()
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(process_offloaded(i, semaphore, executor)) for i in range(ITEMS)]
        print(f"プロセスプールで解析: {time.perf_counter() - start:.2f} 秒")

    print(f"解析結果の例: {tasks[0].result()}")


if __name__ == "__main__":
    asyncio.run(main())
