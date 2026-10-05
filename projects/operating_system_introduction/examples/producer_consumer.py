"""条件変数を使って生産者・消費者問題を解くサンプル。

容量に上限のあるバッファを、生産者スレッドと消費者スレッドが
共有します。

* 生産者はバッファが満杯なら、空きができるまで待つ
* 消費者はバッファが空なら、データが入るまで待つ

待ち合わせには threading.Condition (条件変数) を使います。

実行方法::

    python producer_consumer.py
"""

import threading
import time
from collections import deque

CAPACITY = 3  # バッファの容量
ITEMS = 8  # 生産するデータの個数


class BoundedBuffer:
    """容量に上限のあるスレッドセーフなバッファ。"""

    def __init__(self, capacity: int) -> None:
        self._items: deque[int] = deque()
        self._capacity = capacity
        self._condition = threading.Condition()

    def put(self, item: int) -> None:
        """データを追加する。満杯なら空きができるまで待つ。"""
        with self._condition:
            while len(self._items) >= self._capacity:
                print(f"生産者: 満杯なので待つ (データ {item})")
                self._condition.wait()  # ロックを解放して眠る
            self._items.append(item)
            print(f"生産: {item}  バッファ={list(self._items)}")
            self._condition.notify_all()  # 待っている消費者を起こす

    def get(self) -> int:
        """データを取り出す。空ならデータが入るまで待つ。"""
        with self._condition:
            while not self._items:
                self._condition.wait()
            item = self._items.popleft()
            print(f"消費: {item}  バッファ={list(self._items)}")
            self._condition.notify_all()  # 待っている生産者を起こす
            return item


def producer(buffer: BoundedBuffer) -> None:
    for item in range(1, ITEMS + 1):
        buffer.put(item)
        time.sleep(0.01)  # 生産は速い


def consumer(buffer: BoundedBuffer) -> None:
    for _ in range(ITEMS):
        buffer.get()
        time.sleep(0.05)  # 消費は遅い


def main() -> None:
    buffer = BoundedBuffer(CAPACITY)
    threads = [
        threading.Thread(target=producer, args=(buffer,)),
        threading.Thread(target=consumer, args=(buffer,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
