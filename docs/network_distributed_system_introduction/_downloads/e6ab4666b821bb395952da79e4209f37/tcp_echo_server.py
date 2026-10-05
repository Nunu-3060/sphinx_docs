"""基本的な TCP エコーサーバー。

クライアントから受け取ったバイト列を、そのまま送り返します。
クライアントは 1 つずつ順番に処理します（複数のクライアントを同時に
扱う方法は本文の「複数のクライアントを扱う」を参照してください）。

使い方（tcp_echo_client.py と組み合わせて使います）::

    # 端末 1：サーバーを起動する（Ctrl+C で終了）
    python tcp_echo_server.py

    # 端末 2：クライアントからメッセージを送る
    python tcp_echo_client.py こんにちは

待ち受けるアドレスとポート番号は --host と --port で変更できます。
"""

import argparse
import os
import socket

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 50007
BUFFER_SIZE = 4096
# accept() で待つ時間の上限（秒）。Windows では accept() で待っている間は
# Ctrl+C が効かないため、短い間隔で待ちを抜けて Ctrl+C を受け付けます。
ACCEPT_INTERVAL = 0.5
# 接続したクライアントが何も送ってこない場合に、あきらめるまでの時間（秒）
CLIENT_TIMEOUT = 10.0


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """1 つのクライアントとの通信を、相手が切断するまで続けます。"""
    print(f"接続: {addr[0]}:{addr[1]}")
    conn.settimeout(CLIENT_TIMEOUT)
    total = 0
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                # recv() が空のバイト列を返したら、相手が送信を終えた印
                break
            print(f"  受信 {len(data)} バイト: {data!r}")
            conn.sendall(data)
            total += len(data)
    except TimeoutError:
        print("  タイムアウトしたので切断します")
    except ConnectionError as e:
        print(f"  通信エラー: {e}")
    print(f"切断: {addr[0]}:{addr[1]}（合計 {total} バイトを返信）")


def serve(host: str, port: int) -> None:
    """接続を待ち受け、来たクライアントを順に処理します。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        if os.name != "nt":
            # Linux などで、終了直後でも同じポート番号で再起動できるように
            # する（Windows の SO_REUSEADDR は意味が異なるので設定しない）
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()
        server.settimeout(ACCEPT_INTERVAL)
        print(f"待ち受け中: {host}:{port}（Ctrl+C で終了）")
        while True:
            try:
                conn, addr = server.accept()
            except TimeoutError:
                continue  # 接続が来ていないので、もう一度待つ
            with conn:
                handle_client(conn, addr)


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP エコーサーバー")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    try:
        serve(args.host, args.port)
    except KeyboardInterrupt:
        print("\nCtrl+C を受け付けたので、サーバーを終了します")


if __name__ == "__main__":
    main()
