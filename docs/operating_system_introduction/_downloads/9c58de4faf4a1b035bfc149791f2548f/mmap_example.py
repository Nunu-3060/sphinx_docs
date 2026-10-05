"""メモリマップトファイルのサンプル。

ファイルをメモリ空間に対応付け (マップし)、bytearray のように
添字で読み書きします。メモリへの書き込みは OS によってファイルに
反映されるので、read や write を呼ばずにファイルを更新できます。

実行方法::

    python mmap_example.py
"""

import mmap
import os
import tempfile


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "data.txt")
        with open(path, "wb") as f:
            f.write(b"hello, operating system!")

        with open(path, "r+b") as f:
            # ファイル全体 (長さ 0 を指定) をメモリにマップする
            with mmap.mmap(f.fileno(), 0) as memory:
                print(f"マップした長さ : {len(memory)} バイト")
                print(f"先頭 5 バイト  : {memory[:5]!r}")
                # メモリを書き換えるだけで、ファイルの内容が変わる
                memory[:5] = b"HELLO"
                memory.flush()  # 変更をファイルに書き戻す

        # 通常のファイル読み込みで、変更が反映されたことを確かめる
        with open(path, "rb") as f:
            print(f"ファイルの内容 : {f.read()!r}")


if __name__ == "__main__":
    main()
