"""asyncio.TaskGroup の例外処理と asyncio.timeout() を確かめるサンプル。

TaskGroup の中で 1 つのタスクが例外を送出すると、残りのタスクはキャンセルされる。
発生した例外は ExceptionGroup にまとめて送出されるため、except* で種類ごとに受け取る。
"""

import asyncio


async def work(name: str, seconds: float, fail: bool = False) -> str:
    try:
        await asyncio.sleep(seconds)
    except asyncio.CancelledError:
        print(f"  {name}: キャンセルされた")
        raise  # CancelledError は握りつぶさずに送出し直す
    if fail:
        raise ValueError(f"{name} が失敗した")
    print(f"  {name}: 完了")
    return name


async def task_group_with_error() -> None:
    print("TaskGroup の中で例外が発生する場合:")
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(work("A", 0.5))
            group.create_task(work("B", 1.0, fail=True))
            group.create_task(work("C", 2.0))
    except* ValueError as group_error:
        for error in group_error.exceptions:
            print(f"  ValueError を受け取った: {error}")


async def timeout_example() -> None:
    print("asyncio.timeout() で時間を制限する場合:")
    try:
        async with asyncio.timeout(1.0):
            await work("D", 3.0)
    except TimeoutError:
        print("  1 秒以内に終わらなかったため打ち切った")


async def main() -> None:
    await task_group_with_error()
    await timeout_example()


if __name__ == "__main__":
    asyncio.run(main())
