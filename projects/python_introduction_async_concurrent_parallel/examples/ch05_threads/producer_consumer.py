"""queue.Queue を使った生産者・消費者パターンのサンプル。

生産者スレッドが仕事をキューに入れ、複数の消費者スレッドがキューから取り出して処理する。
キューの大きさに上限を設けているため、消費が追いつかないときは生産者が待たされる。
仕事が無くなったことは、消費者の数だけ番兵（None）を入れて知らせる。
"""

import queue
import threading
import time

CONSUMERS = 3
JOBS = 10


def producer(jobs: "queue.Queue[int | None]") -> None:
    for number in range(JOBS):
        jobs.put(number)  # キューが満杯のときは空きができるまで待つ
        print(f"[生産者] 仕事 {number} を追加した")
    for _ in range(CONSUMERS):
        jobs.put(None)  # 番兵


def consumer(jobs: "queue.Queue[int | None]", results: list[int], lock: threading.Lock) -> None:
    name = threading.current_thread().name
    while True:
        number = jobs.get()  # キューが空のときは仕事が入るまで待つ
        if number is None:
            break
        time.sleep(0.2)  # 時間のかかる I/O 処理の代わり
        with lock:
            results.append(number * number)
        print(f"[{name}] 仕事 {number} を処理した")


def main() -> None:
    jobs: "queue.Queue[int | None]" = queue.Queue(maxsize=3)
    results: list[int] = []
    lock = threading.Lock()

    consumers = [
        threading.Thread(target=consumer, args=(jobs, results, lock), name=f"消費者 {i}")
        for i in range(CONSUMERS)
    ]
    for thread in consumers:
        thread.start()

    start = time.perf_counter()
    producer(jobs)
    for thread in consumers:
        thread.join()
    elapsed = time.perf_counter() - start

    print(f"結果: {sorted(results)}")
    print(f"経過時間: {elapsed:.2f} 秒")


if __name__ == "__main__":
    main()
