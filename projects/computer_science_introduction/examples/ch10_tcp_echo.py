"""localhost 上で TCP エコーサーバとクライアントを動かすサンプル。

サーバはスレッドで起動し、受け取った行をそのまま送り返す。ポート番号に
0 を指定して空いているポートを OS に割り当てさせるので、表示される
ポート番号は実行ごとに変わる。外部との通信は行わない。

実行方法: python ch10_tcp_echo.py
関連する章: 第 10 章「コンピュータネットワーク」
"""

import socket
import threading

HOST = "127.0.0.1"
TIMEOUT = 5.0  # 秒。応答が無いまま待ち続けないようにする


def serve_one(server: socket.socket) -> None:
    """接続を 1 つ受け付け、受け取った行を送り返す。"""
    conn, addr = server.accept()
    with conn, conn.makefile("rb") as reader:
        conn.settimeout(TIMEOUT)
        print(f"[サーバ] {addr[0]}:{addr[1]} から接続を受け付けた")
        # TCP はバイト列の流れでありメッセージの区切りを持たないので、
        # ここでは改行を区切りとして 1 行ずつ処理する
        for line in reader:
            conn.sendall(line)
    print("[サーバ] 接続が閉じられた")


def main() -> None:
    """サーバを起動し、クライアントから 3 行送って応答を表示する。"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with server:
        server.bind((HOST, 0))  # ポート 0: OS に割り当てさせる
        server.listen()
        port = server.getsockname()[1]
        print(f"[サーバ] {HOST}:{port} で待ち受け開始")
        thread = threading.Thread(target=serve_one, args=(server,))
        thread.start()

        # connect() の中で 3 ウェイハンドシェイクが行われる
        with socket.create_connection((HOST, port), timeout=TIMEOUT) as cli:
            with cli.makefile("rb") as reader:
                for text in ["hello", "こんにちは", "bye"]:
                    data = (text + "\n").encode("utf-8")
                    cli.sendall(data)
                    reply = reader.readline()
                    print(f"[クライアント] 送信 {len(data)} バイト, "
                          f"受信 {reply.decode('utf-8').rstrip()!r}")
        thread.join(TIMEOUT)


if __name__ == "__main__":
    main()
