"""実行中の Python が free-threaded ビルドかどうかと、GIL の有無によるスレッドの速さの違いを確かめるサンプル。

通常のビルドでは、CPU バウンドな処理をスレッドに分けても速くならない。
free-threaded ビルド（python3.14t など）で GIL が無効な場合は、スレッドの数に応じて速くなる。
"""

import sys
import sysconfig
import threading
import time

THREADS = 4
LOOPS = 3_000_000


def gil_status() -> str:
    free_threaded_build = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
    if sys.version_info >= (3, 13):
        enabled = sys._is_gil_enabled()
    else:
        enabled = True  # 3.12 以前には free-threaded ビルドが無い
    return f"free-threaded ビルド: {free_threaded_build}, GIL 有効: {enabled}"


def cpu_task() -> None:
    total = 0
    for i in range(LOOPS):
        total += i * i


def main() -> None:
    print(f"Python {sys.version.split()[0]}, {gil_status()}")

    start = time.perf_counter()
    for _ in range(THREADS):
        cpu_task()
    print(f"逐次: {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    threads = [threading.Thread(target=cpu_task) for _ in range(THREADS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f"スレッド {THREADS} 個: {time.perf_counter() - start:.2f} 秒")


if __name__ == "__main__":
    main()
