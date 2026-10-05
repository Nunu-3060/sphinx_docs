"""p5.js のサンプルをローカルで確認するための HTTP サーバー。

使い方::

    python serve.py              # このファイルがあるフォルダーを公開する
    python serve.py --port 8080  # ポート番号を指定する

起動すると既定のブラウザーで http://localhost:8000/ が開きます。
終了するには Ctrl+C を押します。
"""

import argparse
import functools
import http.server
import webbrowser
from pathlib import Path

DEFAULT_PORT = 8000


class SketchRequestHandler(http.server.SimpleHTTPRequestHandler):
    """JavaScript と JSON を正しい MIME タイプで返すハンドラー。

    Windows では、レジストリの設定によって .js が text/plain として
    返される場合があるため、明示的に指定する。
    """

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".json": "application/json",
    }


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="p5.js のサンプルを配信する HTTP サーバー"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"待ち受けるポート番号（既定値: {DEFAULT_PORT}）",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="公開するフォルダー（既定値: このファイルがあるフォルダー）",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="起動時にブラウザーを開かない",
    )
    return parser.parse_args()


def serve(directory: Path, port: int, open_browser: bool) -> None:
    """指定したフォルダーを HTTP で公開し、Ctrl+C が押されるまで待つ。"""
    handler = functools.partial(SketchRequestHandler, directory=str(directory))
    address = ("localhost", port)
    with http.server.ThreadingHTTPServer(address, handler) as httpd:
        url = f"http://localhost:{port}/"
        print(f"{directory} を {url} で公開しています（Ctrl+C で終了）")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nサーバーを終了しました")


def main() -> None:
    """エントリポイント。"""
    args = parse_args()
    serve(args.directory, args.port, not args.no_browser)


if __name__ == "__main__":
    main()
