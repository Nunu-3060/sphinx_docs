"""array_methods.js と同じ処理を Python で書いた例.

JavaScript の配列メソッドと、Python のリスト内包表記や組み込み関数を
対比するためのスクリプト。

使い方::

    python compare_python.py
"""

from dataclasses import dataclass


@dataclass
class User:
    """利用者を表すデータクラス."""

    name: str
    age: int


def main() -> None:
    """配列操作の例を順に実行する."""
    numbers: list[int] = [1, 2, 3, 4, 5, 6]

    print("===== map に相当: リスト内包表記 =====")
    squares = [n * n for n in numbers]
    print(squares)  # [1, 4, 9, 16, 25, 36]

    print("===== filter に相当: 条件付きリスト内包表記 =====")
    evens = [n for n in numbers if n % 2 == 0]
    print(evens)  # [2, 4, 6]

    print("===== reduce に相当: sum =====")
    total = sum(numbers)
    print(total)  # 21

    print("===== メソッドチェーンに相当: ジェネレーター式 =====")
    sum_of_even_squares = sum(n * n for n in numbers if n % 2 == 0)
    print(sum_of_even_squares)  # 56

    print("===== find / some / every / includes に相当 =====")
    print(next((n for n in numbers if n > 3), None))  # 4
    print(any(n > 5 for n in numbers))  # True
    print(all(n > 0 for n in numbers))  # True
    print(3 in numbers)  # True

    print("===== 追加・削除・結合 =====")
    items: list[int] = [1, 2, 3]
    items.append(4)
    last = items.pop()
    print(items, last)  # [1, 2, 3] 4
    print(items[1:])  # [2, 3]
    print([*items, *[10, 20]])  # [1, 2, 3, 10, 20]
    print(", ".join(str(n) for n in items))  # "1, 2, 3"
    print(len(items))  # 3

    print("===== sort =====")
    # Python の sorted は数値を数値として比較する
    print(sorted([10, 9, 1, 100]))  # [1, 9, 10, 100]

    print("===== オブジェクトの配列に相当: データクラスのリスト =====")
    users = [User("山田", 30), User("佐藤", 25), User("鈴木", 35)]
    names = [u.name for u in users if u.age >= 30]
    print(names)  # ['山田', '鈴木']

    prices: dict[str, int] = {"apple": 100, "banana": 80}
    for key, value in prices.items():
        print(f"{key}: {value} 円")


if __name__ == "__main__":
    main()
