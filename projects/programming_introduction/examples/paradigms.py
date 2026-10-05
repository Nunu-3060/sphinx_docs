"""同じ計算を手続き型と関数型の書き方で比べる。

計算内容：1 から 10 までの整数のうち、偶数だけを 2 乗して合計する。
"""


def sum_of_even_squares_procedural(limit: int) -> int:
    """手続き型：状態（total）を順に書き換えて結果を求める。"""
    total = 0
    for number in range(1, limit + 1):
        if number % 2 == 0:
            total += number * number
    return total


def sum_of_even_squares_functional(limit: int) -> int:
    """関数型：状態を書き換えず、式の組み合わせで結果を求める。"""
    return sum(n * n for n in range(1, limit + 1) if n % 2 == 0)


def main() -> None:
    """2 つの書き方の結果が一致することを確かめる。"""
    print(sum_of_even_squares_procedural(10))  # 220
    print(sum_of_even_squares_functional(10))  # 220


if __name__ == "__main__":
    main()
