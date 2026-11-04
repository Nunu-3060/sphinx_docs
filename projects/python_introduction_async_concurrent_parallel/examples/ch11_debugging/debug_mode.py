"""asyncio のデバッグモードで、イベントループをブロックしている処理を見つけるサンプル。

デバッグモードでは、1 回の実行に loop.slow_callback_duration（既定は 0.1 秒）以上かかった処理が警告として出力される。
"""

import asyncio
import time


async def well_behaved() -> None:
    await asyncio.sleep(0.3)  # イベントループに制御を返しながら待つ


async def badly_behaved() -> None:
    time.sleep(0.3)  # イベントループごと止めてしまう


async def main() -> None:
    async with asyncio.TaskGroup() as group:
        group.create_task(well_behaved(), name="well_behaved")
        group.create_task(badly_behaved(), name="badly_behaved")


if __name__ == "__main__":
    # 環境変数 PYTHONASYNCIODEBUG=1 を設定するか、python -X dev で実行しても同じ効果がある
    asyncio.run(main(), debug=True)
