"""ファイルディスクリプタとファイルのメタデータを調べるサンプル。

OS のシステムコールに近い os モジュールの関数でファイルを開き、
次のことを確かめます。

* ファイルを開くとファイルディスクリプタ (小さな整数) が返る
* 同じファイルを 2 回開くと、別のファイルディスクリプタになる
* dup で複製したファイルディスクリプタは読み書きの位置を共有する
* fstat でファイルのメタデータ (inode 番号、サイズ、アクセス権など) が分かる

実行方法::

    python file_descriptor.py
"""

import os
import stat
import tempfile
import time


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "sample.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("0123456789")

        fd1 = os.open(path, os.O_RDONLY)
        fd2 = os.open(path, os.O_RDONLY)
        fd3 = os.dup(fd1)  # fd1 を複製する
        print(f"fd1={fd1}, fd2={fd2}, fd3 (fd1 の複製)={fd3}")

        # fd1 で 3 バイト読むと、読み書きの位置は fd1 と fd3 で共有される
        print(f"fd1 から読む: {os.read(fd1, 3)!r}")
        print(f"fd3 から読む: {os.read(fd3, 3)!r}  (fd1 の続きから)")
        print(f"fd2 から読む: {os.read(fd2, 3)!r}  (先頭から)")

        info = os.fstat(fd1)
        print(f"inode 番号 : {info.st_ino}")
        print(f"サイズ     : {info.st_size} バイト")
        print(f"種類と権限 : {stat.filemode(info.st_mode)}")
        print(f"リンク数   : {info.st_nlink}")
        print(f"更新時刻   : {time.ctime(info.st_mtime)}")

        for fd in (fd1, fd2, fd3):
            os.close(fd)


if __name__ == "__main__":
    main()
