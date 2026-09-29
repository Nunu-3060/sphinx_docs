"""match 文を使った条件分岐のサンプルです。"""


def describe_weekday(day: int) -> str:
    """曜日を表す数値（1 から 7）を受け取り、曜日名を返します。"""
    match day:
        case 1:
            return "月曜日"
        case 2:
            return "火曜日"
        case 3:
            return "水曜日"
        case 4:
            return "木曜日"
        case 5:
            return "金曜日"
        case 6 | 7:
            return "週末"
        case _:
            return "不明な曜日です。"


def main() -> None:
    """1 から 7 までの数値に対応する曜日を表示します。"""
    for day in range(1, 8):
        print(day, ":", describe_weekday(day))


if __name__ == "__main__":
    main()
