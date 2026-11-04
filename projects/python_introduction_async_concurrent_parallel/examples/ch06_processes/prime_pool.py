"""ProcessPoolExecutor で素数の個数を並列に数えるサンプル。

範囲を CHUNKS 個に分割し、それぞれを別のプロセスで数えて合計する。
逐次処理との経過時間を比べると、CPU バウンドな処理がプロセスで速くなることが分かる。
"""

import math
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor

LIMIT = 2_000_000
CHUNKS = 16


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for divisor in range(3, math.isqrt(n) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def count_primes(start: int, stop: int) -> int:
    """start 以上 stop 未満の素数の個数を返す。"""
    return sum(1 for n in range(start, stop) if is_prime(n))


def split_range(limit: int, chunks: int) -> list[tuple[int, int]]:
    """0 以上 limit 未満の範囲を chunks 個に分割する。"""
    size = math.ceil(limit / chunks)
    return [(start, min(start + size, limit)) for start in range(0, limit, size)]


def main() -> None:
    print(f"起動方式: {multiprocessing.get_start_method()}, CPU コア数: {os.cpu_count()}")
    ranges = split_range(LIMIT, CHUNKS)

    start = time.perf_counter()
    total = sum(count_primes(a, b) for a, b in ranges)
    print(f"逐次: {total} 個, {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    with ProcessPoolExecutor() as executor:
        starts = [a for a, _ in ranges]
        stops = [b for _, b in ranges]
        total = sum(executor.map(count_primes, starts, stops))
    print(f"プロセス: {total} 個, {time.perf_counter() - start:.2f} 秒")


# spawn 方式では子プロセスがこのファイルを import するため、この判定が必要になる。
if __name__ == "__main__":
    main()
