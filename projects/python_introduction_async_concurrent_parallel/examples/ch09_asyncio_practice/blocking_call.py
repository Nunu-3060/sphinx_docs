"""コルーチンの中でブロッキングする関数を呼んだときの問題と、asyncio.to_thread() による解決を確かめるサンプル。

heartbeat() は 0.2 秒ごとに経過時間を表示する。
イベントループがブロックされると、その間は表示が止まる。
"""

import asyncio
import time


class Clock:
    """開始からの経過時間を付けてメッセージを表示する。"""

    def __init__(self) -> None:
        self.start = time.perf_counter()

    def log(self, message: str) -> None:
        print(f"{time.perf_counter() - self.start:4.1f} 秒: {message}")


def blocking_io() -> str:
    """同期 API しか持たないライブラリの呼び出しを、time.sleep() で模擬する。"""
    time.sleep(1.0)
    return "同期処理の結果"


async def heartbeat(clock: Clock) -> None:
    for _ in range(6):
        clock.log("heartbeat")
        await asyncio.sleep(0.2)


async def call_directly(clock: Clock) -> None:
    clock.log("blocking_io() を直接呼ぶ")
    clock.log(blocking_io())  # この 1 秒間、イベントループは止まる


async def call_in_thread(clock: Clock) -> None:
    clock.log("blocking_io() を asyncio.to_thread() で呼ぶ")
    clock.log(await asyncio.to_thread(blocking_io))  # 別のスレッドで実行し、完了を await で待つ


async def main() -> None:
    print("--- 直接呼ぶ場合 ---")
    clock = Clock()
    await asyncio.gather(heartbeat(clock), call_directly(clock))

    print("--- asyncio.to_thread() を使う場合 ---")
    clock = Clock()
    await asyncio.gather(heartbeat(clock), call_in_thread(clock))


if __name__ == "__main__":
    asyncio.run(main())
