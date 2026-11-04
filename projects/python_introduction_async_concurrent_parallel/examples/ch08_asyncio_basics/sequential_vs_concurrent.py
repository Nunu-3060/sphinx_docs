"""コルーチンを順に await する場合と、タスクとして同時に実行する場合の違いを確かめるサンプル。"""

import asyncio
import time


async def fetch(name: str, seconds: float) -> str:
    """ネットワークからのデータ取得を asyncio.sleep() で模擬する。"""
    print(f"  {name}: 開始")
    await asyncio.sleep(seconds)  # 待っている間、イベントループは他のタスクを実行する
    print(f"  {name}: 終了")
    return f"{name} のデータ"


async def sequential() -> list[str]:
    """1 つずつ await する。前の処理が終わるまで次の処理は始まらない。"""
    return [await fetch("A", 1.0), await fetch("B", 1.0), await fetch("C", 1.0)]


async def with_gather() -> list[str]:
    """asyncio.gather() で 3 つのコルーチンを同時に実行する。"""
    return list(await asyncio.gather(fetch("A", 1.0), fetch("B", 1.0), fetch("C", 1.0)))


async def with_task_group() -> list[str]:
    """asyncio.TaskGroup で 3 つのタスクを同時に実行する（Python 3.11 以降）。"""
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(name, 1.0)) for name in ("A", "B", "C")]
    # async with ブロックを抜けた時点で、すべてのタスクが完了している
    return [task.result() for task in tasks]


async def main() -> None:
    for runner in (sequential, with_gather, with_task_group):
        print(f"{runner.__name__}:")
        start = time.perf_counter()
        results = await runner()
        print(f"  結果: {results}, {time.perf_counter() - start:.1f} 秒")


if __name__ == "__main__":
    asyncio.run(main())
