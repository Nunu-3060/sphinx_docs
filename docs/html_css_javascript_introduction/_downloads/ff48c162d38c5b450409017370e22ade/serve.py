"""サンプルコードをローカルの HTTP サーバーで公開するスクリプト.

examples フォルダーをドキュメントルートとして公開する。

使い方::

    python serve.py
    python serve.py --port 8080

起動後、ブラウザで http://localhost:8000/ を開く。Ctrl+C で終了する。
"""

import argparse
import functools
import http.server
from pathlib import Path

# このファイル (examples/ch01/serve.py) から見た examples フォルダー
DEFAULT_ROOT = Path(__file__).resolve().parent.parent


class SampleRequestHandler(http.server.SimpleHTTPRequestHandler):
    """JavaScript と JSON の MIME タイプを明示したリクエストハンドラー.

    Windows ではレジストリの設定により .js が text/plain として
    返されることがあり、その場合は JavaScript モジュールが動作しない。
    そのため、主要な拡張子の MIME タイプを明示的に指定する。
    """

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
    }


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description="サンプルコードをローカルの HTTP サーバーで公開する。"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="待ち受けるポート番号"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_ROOT,
        help="公開するフォルダー (既定値: examples フォルダー)",
    )
    return parser.parse_args()


def run_server(root: Path, port: int) -> None:
    """指定したフォルダーを公開する HTTP サーバーを起動する."""
    handler = functools.partial(SampleRequestHandler, directory=str(root))
    # 127.0.0.1 で待ち受けるため、同じ PC からしか接続できない
    address = ("127.0.0.1", port)
    with http.server.ThreadingHTTPServer(address, handler) as server:
        print(f"公開フォルダー: {root}")
        print(f"http://localhost:{port}/ を開いてください (Ctrl+C で終了)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nサーバーを終了しました。")


def main() -> None:
    """エントリーポイント."""
    args = parse_args()
    run_server(args.root.resolve(), args.port)


if __name__ == "__main__":
    main()
