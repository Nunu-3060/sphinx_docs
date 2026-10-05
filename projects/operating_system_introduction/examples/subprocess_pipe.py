"""子プロセスを起動し、パイプで通信するサンプル。

親プロセスが Python の子プロセスを起動し、子プロセスの標準入力に
文字列を送ります。子プロセスは受け取った文字列を大文字に変換して
標準出力に書き出し、親プロセスはそれをパイプ経由で受け取ります。

実行方法::

    python subprocess_pipe.py
"""

import os
import subprocess
import sys

# 子プロセスで実行するプログラム
CHILD_CODE = """
import os
import sys

print(f"子プロセス: PID={os.getpid()}, 親 PID={os.getppid()}",
      file=sys.stderr, flush=True)
for line in sys.stdin:
    sys.stdout.write(line.upper())
sys.exit(3)
"""


def main() -> None:
    print(f"親プロセス: PID={os.getpid()}", flush=True)
    message = "hello, pipe\noperating system\n"
    # 子プロセスの標準入力と標準出力をパイプにつないで起動する
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", CHILD_CODE],
        input=message,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    print("子プロセスから受け取った文字列:")
    print(result.stdout, end="")
    # 子プロセスの終了ステータスは親プロセスが受け取る
    print(f"子プロセスの終了ステータス: {result.returncode}")


if __name__ == "__main__":
    main()
