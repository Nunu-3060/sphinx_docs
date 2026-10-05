"""生産者・消費者問題を 2 通りの方法で解くサンプル。

1. queue.Queue（内部でロックと条件変数を使うスレッド安全なキュー）
2. threading.Condition で自作した容量付きバッファ

どちらも、生産者スレッドが作った品物を容量 2 のバッファ経由で
消費者スレッドが受け取る。どのスレッドがいつ動くかは実行ごとに
変わるが、表示するのは個数と検査結果だけなので出力は毎回同じになる。

実行方法: python ch09_producer_consumer.py
関連する章: 第 9 章「並行処理と入出力」
"""

import queue
import threading
from collections import deque

CAPACITY = 2  # バッファの容量
PRODUCERS = 2
CONSUMERS = 3
ITEMS_PER_PRODUCER = 50


class BoundedBuffer:
    """条件変数で実装した容量付きの FIFO バッファ。"""

    def __init__(self, capacity: int) -> None:
        self.items: deque[int | None] = deque()
        self.capacity = capacity
        self.cond = threading.Condition()  # ロックと待ち行列を兼ねる
        self.max_seen = 0  # 観測した最大の要素数

    def put(self, item: int | None) -> None:
        """空きができるまで待ってから item を入れる。"""
        with self.cond:
            while len(self.items) >= self.capacity:  # if ではなく while
                self.cond.wait()  # ロックを手放して眠り、起きたら再取得
            self.items.append(item)
            self.max_seen = max(self.max_seen, len(self.items))
            self.cond.notify_all()  # 待っている消費者を起こす

    def get(self) -> int | None:
        """品物が来るまで待ってから 1 つ取り出す。"""
        with self.cond:
            while not self.items:
                self.cond.wait()
            item = self.items.popleft()
            self.cond.notify_all()  # 待っている生産者を起こす
            return item


def run(use_queue: bool) -> tuple[list[int], int]:
    """生産者と消費者を動かす。

    消費された品物の一覧と、自作バッファで観測した最大要素数を返す。
    """
    q: queue.Queue[int | None] = queue.Queue(maxsize=CAPACITY)
    buf = BoundedBuffer(CAPACITY)
    put = q.put if use_queue else buf.put
    get = q.get if use_queue else buf.get
    consumed: list[int] = []
    lock = threading.Lock()  # consumed を守るロック

    def producer(pid: int) -> None:
        for i in range(ITEMS_PER_PRODUCER):
            put(pid * 1000 + i)  # 品物の番号（生産者ごとに異なる）

    def consumer() -> None:
        while (item := get()) is not None:  # None は終了の合図
            with lock:
                consumed.append(item)

    producers = [threading.Thread(target=producer, args=(p,))
                 for p in range(PRODUCERS)]
    consumers = [threading.Thread(target=consumer) for _ in range(CONSUMERS)]
    for t in producers + consumers:
        t.start()
    for t in producers:
        t.join()
    for _ in consumers:
        put(None)  # 消費者の数だけ終了の合図を送る
    for t in consumers:
        t.join()
    return consumed, buf.max_seen


def main() -> None:
    """2 つの方法で実行し、品物の欠落や重複が無いことを確かめる。"""
    expected = sorted(p * 1000 + i for p in range(PRODUCERS)
                      for i in range(ITEMS_PER_PRODUCER))
    for use_queue in (True, False):
        print("[queue.Queue]" if use_queue else "[threading.Condition]")
        consumed, max_seen = run(use_queue)
        print(f"  生産 {len(expected)} 個, 消費 {len(consumed)} 個, "
              f"欠落・重複なし: {sorted(consumed) == expected}")
        if not use_queue:
            print(f"  バッファの最大要素数が容量 {CAPACITY} 以下: "
                  f"{max_seen <= CAPACITY}")


if __name__ == "__main__":
    main()
