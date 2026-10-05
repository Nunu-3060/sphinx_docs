"""I/O 多重化を使ったエコーサーバーのサンプル。

1 つのスレッドで複数のクライアントの接続を同時に扱うサーバーです。
selectors モジュールは、OS が提供する I/O 多重化の仕組み
(Linux では epoll、macOS では kqueue、Windows では select) を使い、
「読み書きできる状態になったソケット」だけを教えてくれます。

動作を確かめるため、同じプログラムの中でクライアントを 3 つ起動し、
サーバーとの間でメッセージをやり取りします。

実行方法::

    python nonblocking_io.py
"""

import selectors
import socket
import threading

HOST = "127.0.0.1"
CLIENTS = 3


def serve(server: socket.socket, stop: threading.Event) -> None:
    """接続を受け付け、受け取ったデータをそのまま送り返す。"""
    selector = selectors.DefaultSelector()
    print(f"サーバー: {type(selector).__name__} を使用")
    server.setblocking(False)
    selector.register(server, selectors.EVENT_READ)
    while not stop.is_set():
        # 準備ができたソケットが現れるまで最大 0.1 秒待つ
        for key, _ in selector.select(timeout=0.1):
            sock = key.fileobj
            assert isinstance(sock, socket.socket)
            if sock is server:
                conn, address = server.accept()  # 新しい接続
                conn.setblocking(False)
                selector.register(conn, selectors.EVENT_READ)
                print(f"サーバー: {address} から接続")
                continue
            data = sock.recv(1024)
            if data:
                sock.sendall(data.upper())  # 大文字にして送り返す
            else:  # 相手が接続を閉じた
                selector.unregister(sock)
                sock.close()
    selector.close()


def client(port: int, number: int) -> None:
    """サーバーに接続し、メッセージを送って応答を受け取る。"""
    with socket.create_connection((HOST, port)) as sock:
        message = f"message from client {number}"
        sock.sendall(message.encode())
        reply = sock.recv(1024).decode()
        print(f"クライアント {number}: {reply!r} を受信")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, 0))  # ポート番号 0 は空いている番号を OS が選ぶ
        server.listen()
        port = server.getsockname()[1]
        stop = threading.Event()
        server_thread = threading.Thread(target=serve, args=(server, stop))
        server_thread.start()

        clients = [
            threading.Thread(target=client, args=(port, i))
            for i in range(1, CLIENTS + 1)
        ]
        for t in clients:
            t.start()
        for t in clients:
            t.join()

        stop.set()
        server_thread.join()


if __name__ == "__main__":
    main()
