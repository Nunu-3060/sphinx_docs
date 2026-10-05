"""競合状態（レースコンディション）とロックによる排他制御を示すサンプル。

複数のスレッドが共有カウンタを「読み出し→加算→書き込み」で更新する。
読み出しと書き込みの間で time.sleep(0) を呼び、他のスレッドに実行を
譲ることで、GIL のある Python でも更新が失われる様子を再現する。
ロック無しの結果は実行ごとに変わり得る。ロック有りの結果は常に一致する。

実行方法: python ch09_race_condition.py
関連する章: 第 9 章「並行処理と入出力」
"""

import threading
import time

THREADS = 4
INCREMENTS = 1000


class Counter:
    """複数のスレッドから更新される共有カウンタ。"""

    def __init__(self) -> None:
        self.value = 0
        self.lock = threading.Lock()

    def increment_unsafe(self) -> None:
        """ロックを取らずに 1 を加える（競合状態が起きる）。"""
        current = self.value  # 読み出し
        time.sleep(0)  # ここで他のスレッドに切り替わり得る
        self.value = current + 1  # 書き込み

    def increment_safe(self) -> None:
        """ロックを取ってから 1 を加える（クリティカルセクションを保護）。"""
        with self.lock:
            current = self.value
            time.sleep(0)
            self.value = current + 1


def run(counter: Counter, use_lock: bool) -> None:
    """THREADS 個のスレッドで INCREMENTS 回ずつ加算する。"""

    def worker() -> None:
        for _ in range(INCREMENTS):
            if use_lock:
                counter.increment_safe()
            else:
                counter.increment_unsafe()

    threads = [threading.Thread(target=worker) for _ in range(THREADS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()  # すべてのスレッドの終了を待つ


def main() -> None:
    """ロック無しとロック有りでそれぞれ実行し、結果を比べる。"""
    expected = THREADS * INCREMENTS
    for use_lock in (False, True):
        counter = Counter()
        run(counter, use_lock)
        label = "ロック有り" if use_lock else "ロック無し"
        lost = expected - counter.value
        print(f"{label}: 期待値 {expected}, 実際 {counter.value}, "
              f"失われた更新 {lost}")


if __name__ == "__main__":
    main()
