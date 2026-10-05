"""WebGL のサンプルを閲覧するためのローカル HTTP サーバー。

テクスチャ画像を読み込むサンプルは、HTML ファイルを直接開く (file://) と
ブラウザーのセキュリティー制限により動作しない。このスクリプトで
HTTP サーバーを起動し、http://localhost:8000/ から開くこと。

使い方:
    python serve.py                       # このスクリプトのフォルダーを配信
    python serve.py --port 8080           # ポート番号を変更
    python serve.py --directory ../build/html --open

終了するには Ctrl+C を押す。
"""

from __future__ import annotations

import argparse
import functools
import http.server
import sys
import webbrowser
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="指定したフォルダーを HTTP で配信します。"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="ポート番号（既定: 8000）"
    )
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="待ち受けるアドレス（既定: 127.0.0.1。自分の PC からのみ接続可能）",
    )
    parser.add_argument(
        "--directory",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="配信するフォルダー（既定: このスクリプトのフォルダー）",
    )
    parser.add_argument(
        "--open", action="store_true", help="起動後に既定のブラウザーで開く"
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    directory: Path = args.directory.resolve()
    if not directory.is_dir():
        print(f"フォルダーが見つかりません: {directory}", file=sys.stderr)
        return 1

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(directory)
    )
    try:
        server = http.server.ThreadingHTTPServer(
            (args.bind, args.port), handler
        )
    except OSError as error:
        print(f"サーバーを起動できません: {error}", file=sys.stderr)
        return 1

    url = f"http://localhost:{args.port}/"
    print(f"配信フォルダー: {directory}")
    print(f"{url} を開いてください。終了するには Ctrl+C を押します。")
    if args.open:
        webbrowser.open(url)

    with server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nサーバーを終了しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
