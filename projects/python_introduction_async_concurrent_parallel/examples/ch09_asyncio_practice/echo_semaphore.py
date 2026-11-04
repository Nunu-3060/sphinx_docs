"""asyncio のストリームで TCP サーバーとクライアントを動かし、Semaphore で同時接続数を制限するサンプル。

ローカルにエコーサーバーを起動し、CLIENTS 個のクライアントから接続する。
asyncio.Semaphore で同時に接続するクライアントの数を LIMIT 個までに制限する。
"""

import asyncio
import time

HOST = "127.0.0.1"
CLIENTS = 12
LIMIT = 4


class Stats:
    """サーバーが同時に処理している接続数を記録する。"""

    def __init__(self) -> None:
        self.current = 0
        self.peak = 0


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, stats: Stats) -> None:
    """受け取った 1 行を 0.5 秒後にそのまま送り返す。"""
    stats.current += 1
    stats.peak = max(stats.peak, stats.current)
    try:
        line = await reader.readline()
        await asyncio.sleep(0.5)  # 時間のかかる処理の代わり
        writer.write(line)
        await writer.drain()
    finally:
        stats.current -= 1
        writer.close()
        await writer.wait_closed()


async def client(number: int, port: int, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:  # 同時に LIMIT 個を超えて接続しない
        reader, writer = await asyncio.open_connection(HOST, port)
        try:
            writer.write(f"こんにちは {number}\n".encode())
            await writer.drain()
            reply = await reader.readline()
        finally:
            writer.close()
            await writer.wait_closed()
    return reply.decode().rstrip()


async def main() -> None:
    stats = Stats()

    async def on_connect(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        await handle(reader, writer, stats)

    server = await asyncio.start_server(on_connect, HOST, 0)  # ポート 0 で空いているポートを使う
    port = server.sockets[0].getsockname()[1]
    async with server:
        semaphore = asyncio.Semaphore(LIMIT)
        start = time.perf_counter()
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(client(i, port, semaphore)) for i in range(CLIENTS)]
        elapsed = time.perf_counter() - start

    for task in tasks:
        print(task.result())
    print(f"同時接続数の最大: {stats.peak}, 経過時間: {elapsed:.1f} 秒")


if __name__ == "__main__":
    asyncio.run(main())
