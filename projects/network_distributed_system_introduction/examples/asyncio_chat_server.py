"""asyncio による、複数のクライアントに対応したチャットサーバー。

1 つのスレッドの中で、多数のクライアントとのコネクションを同時に
扱います。プロトコルは改行区切りのテキストで、接続したクライアントが
最初に送る 1 行を名前とし、以降の各行を参加者全員に配信します。

使い方::

    # デモ：サーバーを起動し、3 つのクライアントを接続して
    # メッセージをやり取りする様子を表示して終了する
    python asyncio_chat_server.py

    # サーバーとして常駐させる（Ctrl+C で終了）
    python asyncio_chat_server.py --serve --port 50008

常駐させたサーバーには、nc（netcat）などの、TCP で 1 行ずつ
送受信できるツールで接続できます（最初に送る 1 行が名前になります）。
"""

import argparse
import asyncio

HOST = "127.0.0.1"
DEFAULT_PORT = 50008
MAX_LINE = 1024  # 1 行の最大長（バイト）


class ChatServer:
    """参加者の一覧を持ち、受け取ったメッセージを全員に配信します。"""

    def __init__(self) -> None:
        # 参加者に書き込むための StreamWriter から、その参加者の名前への対応
        self.members: dict[asyncio.StreamWriter, str] = {}

    async def broadcast(self, text: str) -> None:
        """全参加者に 1 行を送ります。"""
        data = (text + "\n").encode("utf-8")
        for writer in list(self.members):
            try:
                writer.write(data)
                # 送信バッファがあふれそうなら空くまで待つ（背圧）
                await writer.drain()
            except ConnectionError:
                pass  # 切断済みの相手は、その相手の処理側で片付ける

    async def handle(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """1 つのクライアントとのやり取り。接続ごとにタスクとして動きます。"""
        name = "?"
        try:
            line = await reader.readline()  # 1 行目は名前
            name = line.decode("utf-8").strip() or "名無し"
            self.members[writer] = name
            await self.broadcast(f"* {name} が参加しました")
            while True:
                # readline() を待っている間、他のクライアントの処理が進む
                line = await reader.readline()
                if not line:
                    break  # 相手が接続を閉じた
                if len(line) > MAX_LINE:
                    break  # 長すぎる行を送る相手とは通信をやめる
                text = line.decode("utf-8").rstrip("\n")
                await self.broadcast(f"[{name}] {text}")
        except (ConnectionError, UnicodeDecodeError, ValueError):
            pass
        finally:
            if writer in self.members:
                del self.members[writer]
                await self.broadcast(f"* {name} が退出しました")
            writer.close()
            try:
                await writer.wait_closed()
            except ConnectionError:
                pass


async def serve_forever(port: int) -> None:
    """サーバーを起動し、止められるまで動かし続けます。"""
    chat = ChatServer()
    server = await asyncio.start_server(chat.handle, HOST, port)
    print(f"待ち受け中: {HOST}:{port}（Ctrl+C で終了）")
    async with server:
        await server.serve_forever()


class DemoClient:
    """デモ用のクライアント。受信した行を名前付きで表示します。"""

    def __init__(
        self, name: str, reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter
    ) -> None:
        self.name = name
        self.reader = reader
        self.writer = writer

    @classmethod
    async def connect(cls, name: str, port: int) -> "DemoClient":
        reader, writer = await asyncio.open_connection(HOST, port)
        writer.write((name + "\n").encode("utf-8"))
        await writer.drain()
        return cls(name, reader, writer)

    async def say(self, text: str) -> None:
        print(f"{self.name} が送信: {text}")
        self.writer.write((text + "\n").encode("utf-8"))
        await self.writer.drain()

    async def receive(self) -> None:
        """1 行を受信して表示します（1 秒以内に届かなければエラー）。"""
        line = await asyncio.wait_for(self.reader.readline(), timeout=1.0)
        print(f"  {self.name} が受信: {line.decode('utf-8').rstrip()}")

    async def close(self) -> None:
        self.writer.close()
        await self.writer.wait_closed()


async def receive_all(clients: list[DemoClient]) -> None:
    """各クライアントが 1 行ずつ受信するのを、名前の順に表示します。"""
    for c in clients:
        await c.receive()


async def demo() -> None:
    """サーバーと 3 つのクライアントを 1 つのイベントループで動かします。"""
    chat = ChatServer()
    # ポート番号 0 を指定して、空いているポートを OS に選ばせる
    server = await asyncio.start_server(chat.handle, HOST, 0)
    port = server.sockets[0].getsockname()[1]
    print(f"サーバーを起動しました: {HOST}:{port}")

    clients: list[DemoClient] = []
    for name in ["alice", "bob", "carol"]:
        clients.append(await DemoClient.connect(name, port))
        print(f"{name} が接続しました")
        await receive_all(clients)  # 参加の通知が全員に届く

    alice, bob, carol = clients
    await alice.say("こんにちは")
    await receive_all(clients)
    await bob.say("やあ、alice")
    await receive_all(clients)
    await carol.say("みなさん、よろしく")
    await receive_all(clients)

    await carol.close()
    print("carol が切断しました")
    await receive_all([alice, bob])  # 退出の通知は残った 2 人に届く

    await alice.close()
    await bob.close()
    server.close()
    await server.wait_closed()
    print("サーバーを停止しました")


def main() -> None:
    parser = argparse.ArgumentParser(description="asyncio チャットサーバー")
    parser.add_argument("--serve", action="store_true",
                        help="デモではなくサーバーとして常駐する")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    if not args.serve:
        asyncio.run(demo())
        return
    try:
        asyncio.run(serve_forever(args.port))
    except KeyboardInterrupt:
        print("\nCtrl+C を受け付けたので、サーバーを終了します")


if __name__ == "__main__":
    main()
