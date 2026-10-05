"""自分自身のプロセスの情報を表示するサンプル。

OS は実行中のプログラム (プロセス) ごとに、プロセス ID や
カレントディレクトリ、環境変数などの情報を管理しています。
このプログラムは、自分のプロセスについてそれらの情報を表示します。

実行方法::

    python process_info.py
"""

import os
import platform
import sys


def main() -> None:
    print(f"OS                  : {platform.system()} {platform.release()}")
    print(f"プロセス ID (PID)   : {os.getpid()}")
    print(f"親プロセス ID       : {os.getppid()}")
    print(f"実行ファイル        : {sys.executable}")
    print(f"コマンドライン引数  : {sys.argv}")
    print(f"カレントディレクトリ: {os.getcwd()}")
    print(f"環境変数の数        : {len(os.environ)}")
    print(f"論理 CPU 数         : {os.cpu_count()}")
    # 標準入出力も OS から見ればファイルディスクリプタ 0, 1, 2 である
    print(f"標準入力の fd       : {sys.stdin.fileno()}")
    print(f"標準出力の fd       : {sys.stdout.fileno()}")
    print(f"標準エラー出力の fd : {sys.stderr.fileno()}")


if __name__ == "__main__":
    main()
