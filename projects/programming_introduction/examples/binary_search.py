"""二分探索の実装。"""

from collections.abc import Sequence


def binary_search(items: Sequence[int], target: int) -> int:
    """昇順に並んだ items から target の位置を返す。見つからなければ -1 を返す。"""
    low = 0
    high = len(items) - 1
    while low <= high:
        middle = (low + high) // 2
        if items[middle] == target:
            return middle
        if items[middle] < target:
            low = middle + 1  # 探す範囲を後半に絞る
        else:
            high = middle - 1  # 探す範囲を前半に絞る
    return -1


def main() -> None:
    """二分探索を試す。"""
    numbers = [1, 2, 3, 5, 8, 9]  # 昇順に並んでいる必要がある
    print(binary_search(numbers, 8))  # 4
    print(binary_search(numbers, 7))  # -1


if __name__ == "__main__":
    main()
