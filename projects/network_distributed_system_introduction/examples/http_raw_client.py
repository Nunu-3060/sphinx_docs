"""ソケットで生の HTTP/1.1 リクエストを送り、レスポンスを読むサンプル。

``http.server`` を使った小さな Web サーバーをスレッドで localhost に
起動し、そこへ TCP のソケットで HTTP/1.1 のリクエストを文字列として
送ります。返ってきたレスポンスのステータス行、ヘッダー、ボディを
表示します。

1 本の TCP コネクションの上で 2 回リクエストを送り (キープアライブ)、
2 回目は ``Connection: close`` を付けて、サーバーがコネクションを
閉じることを確かめます。

インターネット接続は不要です。

実行方法::

    python http_raw_client.py
"""

import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import BinaryIO


class Handler(BaseHTTPRequestHandler):
    """/hello にだけ応答し、それ以外は 404 を返すハンドラー。"""

    protocol_version = "HTTP/1.1"  # キープアライブを有効にする
    server_version = "SampleServer/1.0"

    def version_string(self) -> str:
        # Server ヘッダーに Python のバージョンを含めない
        return self.server_version

    def do_GET(self) -> None:
        if self.path == "/hello":
            status, body = 200, "こんにちは、HTTP!\n"
        else:
            status, body = 404, "見つかりません\n"
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        # ボディの長さを知らせないと、クライアントはボディの終わりが
        # 分からない (キープアライブでは特に重要)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        pass  # サーバーのアクセスログは表示しない


def read_response(reader: BinaryIO) -> tuple[str, list[str], bytes]:
    """レスポンスを 1 つ読み、(ステータス行, ヘッダー行, ボディ) を返す。"""
    status_line = reader.readline().decode("ascii").rstrip("\r\n")
    if not status_line:
        raise ConnectionError("サーバーがコネクションを閉じました")
    headers: list[str] = []
    length = 0
    while True:
        line = reader.readline().decode("latin-1").rstrip("\r\n")
        if line == "":  # 空行でヘッダーが終わる
            break
        headers.append(line)
        name, _, value = line.partition(":")
        if name.strip().lower() == "content-length":
            length = int(value.strip())
    # ボディは Content-Length のバイト数だけ読む
    body = reader.read(length)
    return status_line, headers, body


def send_and_show(
    sock: socket.socket, reader: BinaryIO, path: str, close: bool
) -> None:
    """GET リクエストを送り、レスポンスを表示する。"""
    host, port = sock.getpeername()[:2]
    lines = [
        f"GET {path} HTTP/1.1",
        f"Host: {host}:{port}",
        "User-Agent: http_raw_client.py",
    ]
    if close:
        lines.append("Connection: close")
    # 各行は CRLF で終わり、空行 (CRLF だけの行) でヘッダーが終わる
    request = "\r\n".join(lines) + "\r\n\r\n"
    local_port = sock.getsockname()[1]
    print(f"--- リクエスト (クライアント側ポート {local_port}) ---")
    print(request.replace("\r\n", "\\r\\n\n"), end="")
    sock.sendall(request.encode("ascii"))

    status_line, headers, body = read_response(reader)
    print("--- レスポンス ---")
    print(f"ステータス行: {status_line}")
    for h in headers:
        print(f"ヘッダー    : {h}")
    print(f"ボディ      : {body.decode('utf-8')!r}")
    print()


def main() -> None:
    # ポート 0 を指定して、空いているポートを OS に選ばせる
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = "127.0.0.1", server.server_address[1]
    print(f"サーバーを {host}:{port} で起動しました\n")

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with sock.makefile("rb") as reader:
                # 1 回目: キープアライブ (HTTP/1.1 の既定) で送る
                send_and_show(sock, reader, "/hello", close=False)
                # 2 回目: 同じコネクションで送り、閉じるよう依頼する
                send_and_show(sock, reader, "/missing", close=True)
                # サーバーが閉じたので、これ以上読むと EOF (空) になる
                rest = reader.read()
                print(f"2 回目の後に読んだデータ: {rest!r} "
                      "(サーバーがコネクションを閉じました)")
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
