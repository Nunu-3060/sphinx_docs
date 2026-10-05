"""asyncio によるエコーサーバと複数クライアントの並行実行を示すサンプル。

localhost（127.0.0.1）で OS が選んだ空きポート（ポート 0）にエコーサーバを
立て、5 つのクライアントを順に 1 つずつ動かした場合と、同時に動かした場合の
所要時間を比べる。サーバは応答の前に 0.2 秒待つ（遅い処理の代わり）。
すべて 1 つのスレッドのイベントループの上で動き、外部とは通信しない。
所要時間は環境によって多少変わるので、小数第 1 位に丸めて表示する。

実行方法: python ch09_asyncio_echo.py
関連する章: 第 9 章「並行処理と入出力」
"""

import asyncio
import time

DELAY = 0.2  # サーバが応答の前に待つ秒数
CLIENTS = 5


async def handle(reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter) -> None:
    """1 つの接続を担当するコルーチン。1 行受け取り、大文字にして返す。"""
    line = await reader.readline()  # データが届くまで待つ（他は動ける）
    await asyncio.sleep(DELAY)  # 遅い処理の代わり
    writer.write(line.upper())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def client(port: int, name: str) -> str:
    """サーバに接続し、1 行送って応答を受け取る。"""
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(f"hello from {name}\n".encode())
    await writer.drain()
    reply = await reader.readline()
    writer.close()
    await writer.wait_closed()
    return reply.decode().strip()


async def main_async() -> None:
    """サーバを起動し、逐次実行と並行実行の所要時間を比べる。"""
    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]  # OS が割り当てたポート
    names = [f"c{i}" for i in range(CLIENTS)]
    async with server:
        start = time.perf_counter()
        for name in names:  # 1 つずつ終わるのを待ってから次へ
            await client(port, name)
        sequential = time.perf_counter() - start

        start = time.perf_counter()
        replies = await asyncio.gather(*(client(port, n) for n in names))
        concurrent = time.perf_counter() - start
    for reply in replies:
        print(reply)
    print(f"逐次実行: 約 {sequential:.1f} 秒")
    print(f"並行実行: 約 {concurrent:.1f} 秒")


def main() -> None:
    """イベントループを起動して main_async を実行する。"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
