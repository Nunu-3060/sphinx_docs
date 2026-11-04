"""タスクのキャンセルと後始末を確かめるサンプル。

task.cancel() を呼ぶと、タスクが次に await している箇所で asyncio.CancelledError が送出される。
try ... finally で後始末を書いておけば、キャンセルされても資源を確実に解放できる。
"""

import asyncio


class Connection:
    """後始末が必要な資源の例。"""

    def __init__(self, name: str) -> None:
        self.name = name
        print(f"{name}: 接続を開いた")

    def close(self) -> None:
        print(f"{self.name}: 接続を閉じた")


async def long_running(name: str) -> None:
    connection = Connection(name)
    try:
        for step in range(1, 11):
            await asyncio.sleep(0.3)
            print(f"{name}: ステップ {step}")
    finally:
        connection.close()  # キャンセルされた場合も必ず実行される


async def main() -> None:
    task = asyncio.create_task(long_running("タスク"))
    await asyncio.sleep(1.0)

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print(f"キャンセルされた: cancelled() = {task.cancelled()}")


if __name__ == "__main__":
    asyncio.run(main())
