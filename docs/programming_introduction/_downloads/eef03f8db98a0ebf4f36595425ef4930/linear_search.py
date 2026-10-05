"""線形探索の実装。"""

from collections.abc import Sequence


def linear_search(items: Sequence[int], target: int) -> int:
    """先頭から順に調べ、target の位置を返す。見つからなければ -1 を返す。"""
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def main() -> None:
    """線形探索を試す。"""
    numbers = [8, 3, 5, 1, 9, 2]
    print(linear_search(numbers, 9))  # 4
    print(linear_search(numbers, 7))  # -1


if __name__ == "__main__":
    main()
