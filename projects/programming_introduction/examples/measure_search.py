"""線形探索と二分探索の実行時間を比べる。"""

import timeit

from binary_search import binary_search
from linear_search import linear_search


def main() -> None:
    """データ数を変えながら、末尾の要素を探す時間を測定する。"""
    print(f"{'データ数':>10} {'線形探索[ms]':>14} {'二分探索[ms]':>14}")
    for size in [1_000, 10_000, 100_000, 1_000_000]:
        numbers = list(range(size))
        target = size - 1  # 線形探索にとって最も不利な位置
        linear = timeit.timeit(
            lambda: linear_search(numbers, target), number=10
        )
        binary = timeit.timeit(
            lambda: binary_search(numbers, target), number=10
        )
        # 10 回分の合計時間を 1 回あたりのミリ秒に換算する
        print(f"{size:>10} {linear * 100:>14.4f} {binary * 100:>14.4f}")


if __name__ == "__main__":
    main()
