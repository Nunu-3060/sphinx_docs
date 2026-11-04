"""python -m asyncio ps / pstree でタスクの状態を調べるための、しばらく動き続けるプログラム（Python 3.14 以降）。

このプログラムを実行したまま、別の端末で次のコマンドを実行する（PID は表示された値に置き換える）。

    python -m asyncio ps PID
    python -m asyncio pstree PID
"""

import asyncio
import os


async def download(name: str) -> None:
    await asyncio.sleep(60)


async def crawler(name: str) -> None:
    async with asyncio.TaskGroup() as group:
        for page in range(2):
            group.create_task(download(f"{name}-{page}"), name=f"download-{name}-{page}")


async def main() -> None:
    print(f"PID: {os.getpid()}（60 秒後に終了する）")
    async with asyncio.TaskGroup() as group:
        group.create_task(crawler("A"), name="crawler-A")
        group.create_task(crawler("B"), name="crawler-B")


if __name__ == "__main__":
    asyncio.run(main())
