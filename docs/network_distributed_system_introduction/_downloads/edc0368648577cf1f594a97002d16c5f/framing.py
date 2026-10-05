"""TCP のバイトストリームと、長さの前置によるフレーミング。

TCP はバイトの並び（バイトストリーム）を届けるだけで、送信側が
send() を呼んだ単位（メッセージの境界）は保存されません。
このサンプルでは、次の 2 つを示します。

1. 3 回に分けて送ったデータが、受信側では 1 回の recv() でまとめて
   読めてしまうこと（境界が失われること）
2. 各メッセージの前に 4 バイトのビッグエンディアンで長さを付ける
   （長さの前置）ことで、メッセージを正しく取り出せること。
   recv() が要求より少ないバイト数しか返さない場合に備えて、
   指定したバイト数がそろうまで読み続ける recv_exact() を使います。

localhost にサーバーのスレッドを立てて通信するので、単体で実行できます::

    python framing.py
"""

import socket
import struct
import threading
import time

HOST = "127.0.0.1"
# 長さのヘッダー：ネットワークバイトオーダー（ビッグエンディアン）の
# 符号なし 32 ビット整数
HEADER = struct.Struct("!I")
# 受け付けるメッセージの最大長。不正な長さで巨大なメモリを
# 確保させられないよう、上限を決めておく
MAX_MESSAGE = 1024 * 1024


class IncompleteMessage(ConnectionError):
    """必要なバイト数がそろう前に、相手が接続を閉じたことを表します。"""

    def __init__(self, expected: int, received: int) -> None:
        super().__init__(f"{expected} バイト中 {received} バイトで切断")
        self.received = received


def recv_exact(sock: socket.socket, n: int, trace: bool = False) -> bytes:
    """ちょうど n バイトを受信して返します。

    recv(n) は n バイト「以下」を返すので、そろうまで繰り返します。
    途中で相手が切断した場合は IncompleteMessage を送出します。
    trace が真なら、各 recv() で受け取ったバイト数を表示します。
    """
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise IncompleteMessage(n, len(buf))
        if trace:
            print(f"    recv(): {len(chunk)} バイト（要求 {n - len(buf)}）")
        buf += chunk
    return bytes(buf)


def send_message(sock: socket.socket, payload: bytes) -> None:
    """長さのヘッダーを付けて 1 つのメッセージを送ります。"""
    sock.sendall(HEADER.pack(len(payload)) + payload)


def recv_message(sock: socket.socket, trace: bool = False) -> bytes | None:
    """1 つのメッセージを受信します。相手が送信を終えていれば None。"""
    try:
        header = recv_exact(sock, HEADER.size, trace)
    except IncompleteMessage as e:
        if e.received == 0:
            return None  # メッセージの切れ目で正常に切断された
        raise
    (length,) = HEADER.unpack(header)
    if length > MAX_MESSAGE:
        raise ValueError(f"メッセージが長すぎます: {length} バイト")
    return recv_exact(sock, length, trace)


def demo_no_framing() -> None:
    """境界のないバイトストリームの様子を示します。"""
    print("== 1. フレーミングなし ==")
    sent = threading.Event()
    with socket.create_server((HOST, 0)) as server:
        port = server.getsockname()[1]

        def client() -> None:
            with socket.create_connection((HOST, port)) as sock:
                for word in [b"apple", b"banana", b"cherry"]:
                    sock.sendall(word)
                    print(f"  送信: {word!r}")
                sent.set()  # すべて送り終えたことを受信側に知らせる
                time.sleep(0.2)

        t = threading.Thread(target=client)
        t.start()
        conn, _ = server.accept()
        with conn:
            sent.wait()
            time.sleep(0.1)  # データが受信側に届くのを待つ
            data = conn.recv(4096)
            print(f"  1 回の recv() で受信: {data!r}")
        t.join()
    print("  -> 3 回の送信の境界は、受信側からは区別できません")


def demo_framing() -> None:
    """長さの前置でメッセージを正しく区切れることを示します。"""
    print("== 2. 長さの前置によるフレーミング ==")
    messages = [b"apple", b"banana", "こんにちは".encode("utf-8")]
    ready = threading.Event()
    with socket.create_server((HOST, 0)) as server:
        port = server.getsockname()[1]

        def client() -> None:
            with socket.create_connection((HOST, port)) as sock:
                for m in messages:
                    send_message(sock, m)
                ready.wait()  # 受信側が 3 つを読み終えるのを待つ
                # 最後のメッセージは、わざと細切れにして間隔を空けて送る。
                # 受信側では recv() が要求より少ないバイト数を返す
                frame = HEADER.pack(10) + b"0123456789"
                for piece in [frame[:2], frame[2:7], frame[7:]]:
                    sock.sendall(piece)
                    time.sleep(0.2)

        t = threading.Thread(target=client)
        t.start()
        conn, _ = server.accept()
        with conn:
            count = 0
            while True:
                count += 1
                # 4 つ目のメッセージだけ、recv() の様子を表示する
                trace = count == 4
                if trace:
                    ready.set()  # 細切れの送信を始めてもらう
                    print("  4 つ目のメッセージ（細切れに届く）:")
                msg = recv_message(conn, trace)
                if msg is None:
                    break
                text = msg.decode("utf-8")
                print(f"  受信 {count}: {len(msg)} バイト {text!r}")
        t.join()
    print("  -> 送信したとおりの単位でメッセージを取り出せました")


def main() -> None:
    demo_no_framing()
    print()
    demo_framing()


if __name__ == "__main__":
    main()
