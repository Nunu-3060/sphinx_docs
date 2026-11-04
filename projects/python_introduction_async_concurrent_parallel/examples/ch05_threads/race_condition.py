"""スレッド間の競合状態と、Lock による修正を確かめるサンプル。

increment_unsafe() は、値の読み出しと書き込みの間に他のスレッドが割り込めるため、更新が失われる。
increment_safe() は、読み出しから書き込みまでを Lock で保護しているため、更新が失われない。
"""

import threading
import time
from collections.abc import Callable

THREADS = 4
TIMES = 1000


class Counter:
    """複数のスレッドから更新されるカウンター。"""

    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increment_unsafe(self) -> None:
        current = self.value
        time.sleep(0)  # 読み出しと書き込みの間で、他のスレッドに切り替わりやすくする
        self.value = current + 1

    def increment_safe(self) -> None:
        with self._lock:
            current = self.value
            time.sleep(0)
            self.value = current + 1


def run(increment: Callable[[], None]) -> None:
    """THREADS 個のスレッドで、それぞれ increment を TIMES 回呼び出す。"""

    def worker() -> None:
        for _ in range(TIMES):
            increment()

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main() -> None:
    expected = THREADS * TIMES

    counter = Counter()
    run(counter.increment_unsafe)
    print(f"Lock なし: {counter.value} (期待値 {expected})")

    counter = Counter()
    run(counter.increment_safe)
    print(f"Lock あり: {counter.value} (期待値 {expected})")


if __name__ == "__main__":
    main()
