"""生の HTTP/1.1 リクエストを送り、レスポンスをそのまま表示するサンプル。

http.server でローカルの HTTP サーバをスレッドで起動し、socket で
組み立てたリクエストを送る。外部との通信は行わない。レスポンスの
Date ヘッダは実行時刻、Server ヘッダは Python のバージョンで変わる。

実行方法: python ch10_http_get.py
関連する章: 第 10 章「コンピュータネットワーク」
"""

import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
TIMEOUT = 5.0  # 秒


class Handler(BaseHTTPRequestHandler):
    """/hello には 200、それ以外には 404 を返すハンドラ。"""

    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        """GET リクエストを処理する。"""
        if self.path == "/hello":
            status, body = 200, "Hello, HTTP!\n"
        else:
            status, body = 404, "Not Found\n"
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()  # 空行を送り、ヘッダの終わりを示す
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        """アクセスログを表示しない。"""


def http_get(port: int, path: str) -> str:
    """socket で GET リクエストを送り、レスポンス全体を文字列で返す。"""
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {HOST}:{port}\r\n"
        "Connection: close\r\n"  # 応答後に接続を閉じてもらう
        "\r\n"  # 空行でヘッダの終わりを示す
    )
    chunks: list[bytes] = []
    with socket.create_connection((HOST, port), timeout=TIMEOUT) as sock:
        sock.sendall(request.encode("ascii"))
        while chunk := sock.recv(4096):  # サーバが閉じるまで読む
            chunks.append(chunk)
    return b"".join(chunks).decode("utf-8")


def main() -> None:
    """サーバを起動し、2 つのパスに GET リクエストを送る。"""
    server = ThreadingHTTPServer((HOST, 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    try:
        for path in ["/hello", "/missing"]:
            print(f"===== GET {path} =====")
            print(http_get(port, path).replace("\r\n", "\n"), end="")
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == "__main__":
    main()
