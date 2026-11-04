"""multiprocessing.shared_memory でプロセス間にデータを共有するサンプル。

親プロセスが共有メモリに浮動小数点数の配列を書き込み、子プロセスは共有メモリの名前と担当範囲だけを受け取って部分和を計算する。
配列そのものを pickle で送らないため、データが大きい場合に受け渡しの時間とメモリを節約できる。
"""

import struct
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import shared_memory

COUNT = 1_000_000
WORKERS = 4
ITEM_SIZE = struct.calcsize("d")  # double（8 バイト）


def as_doubles(memory: shared_memory.SharedMemory) -> "memoryview[float]":
    """共有メモリを double の配列として読み書きできる memoryview を返す。"""
    if memory.buf is None:
        raise ValueError("共有メモリは既に閉じられている")
    return memory.buf.cast("d")


def partial_sum(name: str, start: int, stop: int) -> float:
    """共有メモリ name に置かれた配列の start 番目から stop - 1 番目までの和を返す。"""
    memory = shared_memory.SharedMemory(name=name)
    try:
        values = as_doubles(memory)
        try:
            return sum(values[start:stop])
        finally:
            values.release()  # memoryview を解放してから close する
    finally:
        memory.close()


def main() -> None:
    memory = shared_memory.SharedMemory(create=True, size=COUNT * ITEM_SIZE)
    try:
        values = as_doubles(memory)
        for i in range(COUNT):
            values[i] = i * 0.5
        values.release()

        size = COUNT // WORKERS
        starts = [i * size for i in range(WORKERS)]
        stops = [start + size for start in starts]
        stops[-1] = COUNT
        with ProcessPoolExecutor(max_workers=WORKERS) as executor:
            sums = list(executor.map(partial_sum, [memory.name] * WORKERS, starts, stops))

        print(f"部分和: {sums}")
        print(f"合計: {sum(sums)} (期待値 {sum(i * 0.5 for i in range(COUNT))})")
    finally:
        memory.close()
        memory.unlink()  # 共有メモリを作ったプロセスが最後に削除する


if __name__ == "__main__":
    main()
