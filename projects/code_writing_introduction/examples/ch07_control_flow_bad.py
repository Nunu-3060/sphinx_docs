"""第 7 章「処理の流れを分かりやすくする」の悪い例。"""


def check_loan(is_member: bool, has_overdue: bool, borrowed_count: int) -> str:
    if is_member:
        if not has_overdue:
            if borrowed_count < 5:
                return "貸し出しできる"
            else:
                return "貸し出し冊数の上限に達している"
        else:
            return "返却期限を過ぎた本がある"
    else:
        return "会員登録が必要である"


def is_discount_day(weekday: int, day: int, is_member: bool) -> bool:
    return (weekday == 5 or weekday == 6) and not (day > 7) or is_member and day == 15


def print_ranking(names: list[str]) -> None:
    for i in range(len(names)):
        print(str(i + 1) + "位: " + names[i])


if __name__ == "__main__":
    print(check_loan(True, False, 3))
    print(check_loan(True, False, 5))
    print(is_discount_day(5, 3, False))
    print(is_discount_day(2, 15, True))
    print_ranking(["佐藤", "鈴木", "高橋"])
