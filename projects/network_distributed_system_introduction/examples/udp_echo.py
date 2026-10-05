"""UDP のエコーサーバーとクライアントで、パケット損失を模擬するサンプル。

localhost（127.0.0.1）で UDP のエコーサーバーをスレッドで起動し、
クライアントがメッセージを送って応答を待ちます。
サーバーは一定の確率で応答を送らずに捨て、パケット損失を模擬します。
UDP には再送の仕組みがないので、クライアントはタイムアウトで損失を
検出し、自分で再送します。乱数のシードを固定しているので、
実行結果は毎回同じになります。

実行方法:
    python udp_echo.py
"""

import random
import socket
import threading

HOST = "127.0.0.1"
DROP_RATE = 0.3  # サーバーが応答を捨てる確率
TIMEOUT = 0.3  # クライアントが応答を待つ時間（秒）
MAX_TRIES = 3  # 1 つのメッセージを送る最大回数


def run_server(sock: socket.socket, stop: threading.Event) -> None:
    """届いたデータグラムを送信元にそのまま送り返す（ときどき捨てる）。"""
    rng = random.Random(1)  # シードを固定して結果を再現可能にする
    sock.settimeout(0.1)  # 停止の指示を定期的に確かめるため
    while not stop.is_set():
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue
        if rng.random() < DROP_RATE:
            print(f"  [サーバー] {data.decode()} を受信したが、応答を捨てる")
            continue
        sock.sendto(data, addr)


def send_with_retry(sock: socket.socket, server: tuple[str, int],
                    message: str) -> bool:
    """メッセージを送り、応答がなければ再送する。成功したら True。"""
    for attempt in range(1, MAX_TRIES + 1):
        sock.sendto(message.encode(), server)
        try:
            data, _ = sock.recvfrom(1024)
        except socket.timeout:
            print(f"[クライアント] {message}: {attempt} 回目 タイムアウト")
            continue
        print(f"[クライアント] {message}: {attempt} 回目 応答 "
              f"{data.decode()!r}")
        return True
    return False


def main() -> None:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind((HOST, 0))  # ポート番号は OS に割り当てさせる
    server_addr = server_sock.getsockname()
    stop = threading.Event()
    server = threading.Thread(target=run_server, args=(server_sock, stop))
    server.start()

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_sock.settimeout(TIMEOUT)
    success = 0
    total = 8
    try:
        for i in range(1, total + 1):
            if send_with_retry(client_sock, server_addr, f"msg-{i}"):
                success += 1
            else:
                print(f"[クライアント] msg-{i}: あきらめる")
    finally:
        stop.set()
        server.join()
        client_sock.close()
        server_sock.close()
    print(f"成功: {success} / {total}")


if __name__ == "__main__":
    main()
