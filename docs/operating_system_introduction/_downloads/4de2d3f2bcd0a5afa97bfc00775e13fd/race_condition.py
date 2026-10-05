"""競合状態を再現し、ロックで解消するサンプル。

複数のスレッドが共有変数 counter を「読む → 1 を足す → 書く」の
3 段階で更新します。段階の途中で別のスレッドに切り替わると、
更新が失われます (競合状態)。

切り替えを起こりやすくするため、読んだ直後に time.sleep(0) を
呼んで CPU を手放しています。

実行方法::

    python race_condition.py
"""

import threading
import time
from collections.abc import Callable

# スレッドの数と、各スレッドが足す回数
THREADS = 4
ITERATIONS = 1_000

counter = 0
lock = threading.Lock()


def increment_unsafe() -> None:
    """ロックを使わずに counter を増やす。"""
    global counter
    for _ in range(ITERATIONS):
        value = counter  # 読む
        time.sleep(0)  # ここで別のスレッドに切り替わりやすくする
        counter = value + 1  # 書く


def increment_safe() -> None:
    """ロックで保護して counter を増やす。"""
    global counter
    for _ in range(ITERATIONS):
        with lock:  # クリティカルセクションの開始
            value = counter
            time.sleep(0)
            counter = value + 1
        # with を抜けるとロックが解放される


def run(func: Callable[[], None]) -> int:
    """func を複数のスレッドで実行し、最終的な counter の値を返す。"""
    global counter
    counter = 0
    threads = [threading.Thread(target=func) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return counter


def main() -> None:
    print(f"期待される値    : {THREADS * ITERATIONS}")
    print(f"ロックなしの結果: {run(increment_unsafe)}")
    print(f"ロックありの結果: {run(increment_safe)}")


if __name__ == "__main__":
    main()
