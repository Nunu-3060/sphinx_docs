"""InterpreterPoolExecutor でサブインタプリタを使って並列に計算するサンプル（Python 3.14 以降）。

サブインタプリタはそれぞれ独立した GIL を持つため、1 つのプロセスの中で CPU バウンドな処理を並列に実行できる。
使い方は ThreadPoolExecutor や ProcessPoolExecutor と同じである。
"""

import math
import sys
import time

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
    """start 以上 stop 未満の素数の個数を返す。

    sum(1 for n in ... if is_prime(n)) のように、ジェネレーター式の中からグローバルな関数を参照すると、
    Python 3.14.6 の InterpreterPoolExecutor では NameError になるため、for 文で書いている。
    """
    count = 0
    for n in range(start, stop):
        if is_prime(n):
            count += 1
    return count


def run_in_subinterpreters(starts: list[int], stops: list[int]) -> int:
    if sys.version_info < (3, 14):
        raise RuntimeError("InterpreterPoolExecutor は Python 3.14 以降で使用できる")
    else:
        from concurrent.futures import InterpreterPoolExecutor

        with InterpreterPoolExecutor() as executor:
            return sum(executor.map(count_primes, starts, stops))


def main() -> None:
    if sys.version_info < (3, 14):
        print("このサンプルの実行には Python 3.14 以降が必要である。")
        return

    size = LIMIT // CHUNKS
    starts = [i * size for i in range(CHUNKS)]
    stops = [start + size for start in starts]

    start = time.perf_counter()
    total = sum(map(count_primes, starts, stops))
    print(f"逐次: {total} 個, {time.perf_counter() - start:.2f} 秒")

    start = time.perf_counter()
    total = run_in_subinterpreters(starts, stops)
    print(f"サブインタプリタ: {total} 個, {time.perf_counter() - start:.2f} 秒")


if __name__ == "__main__":
    main()
