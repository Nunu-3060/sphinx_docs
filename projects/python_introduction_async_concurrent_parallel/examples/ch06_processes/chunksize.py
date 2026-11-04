"""ProcessPoolExecutor.map() の chunksize による違いを確かめるサンプル。

1 回あたりの処理が小さい場合、プロセス間でのデータの受け渡しにかかる時間が処理そのものより大きくなる。
chunksize を大きくすると、まとめて受け渡すことで受け渡しの回数が減り、速くなる。
"""

import time
from concurrent.futures import ProcessPoolExecutor

ITEMS = 10_000


def square(n: int) -> int:
    return n * n


def main() -> None:
    numbers = range(ITEMS)

    start = time.perf_counter()
    expected = [square(n) for n in numbers]
    print(f"逐次: {time.perf_counter() - start:.2f} 秒")

    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(square, range(10)))  # プロセスの起動を計測から除くため、先に一度使っておく
        for chunksize in (1, 100, 1000):
            start = time.perf_counter()
            results = list(executor.map(square, numbers, chunksize=chunksize))
            elapsed = time.perf_counter() - start
            assert results == expected
            print(f"プロセス (chunksize={chunksize}): {elapsed:.2f} 秒")


if __name__ == "__main__":
    main()
