"""制御構造（順次・分岐・反復）の例。"""


def grade(score: int) -> str:
    """点数を A・B・C の評価に変換する（分岐）。"""
    if score >= 80:
        return "A"
    elif score >= 60:
        return "B"
    else:
        return "C"


def sum_up_to(n: int) -> int:
    """1 から n までの整数の合計を求める（回数が決まった反復）。"""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def count_digits(n: int) -> int:
    """0 以上の整数の桁数を求める（条件を満たす間の反復）。"""
    digits = 1
    while n >= 10:
        n //= 10
        digits += 1
    return digits


def main() -> None:
    """各関数を順に呼び出す（順次）。"""
    print(grade(85))  # A
    print(grade(59))  # C
    print(sum_up_to(100))  # 5050
    print(count_digits(2026))  # 4


if __name__ == "__main__":
    main()
