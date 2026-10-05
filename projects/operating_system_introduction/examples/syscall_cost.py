"""システムコールの費用を確かめるサンプル。

ファイルに 1 バイトずつ書き込む処理を 2 通りの方法で行い、
所要時間を比べます。

* os.write を直接呼ぶ方法: 1 バイトごとにシステムコールが発生する
* open() で開いたファイルに書く方法: Python がバッファに溜めてから、
  まとめて少ない回数のシステムコールで書き込む

実行方法::

    python syscall_cost.py
"""

import os
import tempfile
import time

# 書き込むバイト数
COUNT = 100_000


def write_unbuffered(path: str) -> float:
    """os.write で 1 バイトずつ書き込み、所要時間 (秒) を返す。"""
    start = time.perf_counter()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    try:
        for _ in range(COUNT):
            os.write(fd, b"x")  # 毎回システムコールになる
    finally:
        os.close(fd)
    return time.perf_counter() - start


def write_buffered(path: str) -> float:
    """バッファ付きのファイルに 1 バイトずつ書き込み、所要時間 (秒) を返す。"""
    start = time.perf_counter()
    with open(path, "wb") as f:  # 既定でバッファ付きになる
        for _ in range(COUNT):
            f.write(b"x")  # バッファに溜めるだけ
    return time.perf_counter() - start


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "data.bin")
        unbuffered = write_unbuffered(path)
        buffered = write_buffered(path)
    print(f"書き込んだバイト数      : {COUNT:,}")
    print(f"os.write (バッファなし) : {unbuffered:.3f} 秒")
    print(f"open() (バッファあり)   : {buffered:.3f} 秒")
    print(f"速度比                  : 約 {unbuffered / buffered:.0f} 倍")


if __name__ == "__main__":
    main()
