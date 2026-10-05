"""基本的な TCP エコークライアント。

tcp_echo_server.py に接続してメッセージを送り、送り返された内容を
表示します。先にサーバーを起動しておく必要があります。

使い方::

    python tcp_echo_client.py こんにちは
    python tcp_echo_client.py --host 127.0.0.1 --port 50007 hello

メッセージを省略すると "hello" を送ります。
"""

import argparse
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 50007
BUFFER_SIZE = 4096
TIMEOUT = 5.0


def echo(host: str, port: int, message: str) -> str:
    """メッセージを送り、サーバーから返ってきた内容を返します。"""
    data = message.encode("utf-8")
    # create_connection() は名前解決と connect() をまとめて行う
    with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
        local = sock.getsockname()
        print(f"接続: {local[0]}:{local[1]} -> {host}:{port}")
        sock.sendall(data)
        print(f"送信 {len(data)} バイト: {message}")
        # これ以上送らないことを相手に伝える（FIN を送る）。
        # 受信の方向は開いたままなので、返信は引き続き受け取れる
        sock.shutdown(socket.SHUT_WR)
        chunks: list[bytes] = []
        while True:
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                break  # サーバーが接続を閉じた
            chunks.append(chunk)
    reply = b"".join(chunks)
    print(f"受信 {len(reply)} バイト")
    return reply.decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP エコークライアント")
    parser.add_argument("message", nargs="?", default="hello")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    try:
        reply = echo(args.host, args.port, args.message)
    except ConnectionRefusedError:
        print("接続を拒否されました（サーバーは起動していますか？）")
        return
    except TimeoutError:
        print("タイムアウトしました")
        return
    print(f"サーバーからの返信: {reply}")


if __name__ == "__main__":
    main()
