"""第 7 章「処理の流れを分かりやすくする」の良い例。"""

import calendar

MAX_LOAN_COUNT = 5
FIRST_WEEK_LAST_DAY = 7
MEMBER_DAY = 15


def check_loan(is_member: bool, has_overdue: bool, borrowed_count: int) -> str:
    if not is_member:
        return "会員登録が必要である"
    if has_overdue:
        return "返却期限を過ぎた本がある"
    if borrowed_count >= MAX_LOAN_COUNT:
        return "貸し出し冊数の上限に達している"
    return "貸し出しできる"


def is_discount_day(weekday: int, day: int, is_member: bool) -> bool:
    is_weekend = weekday in (calendar.SATURDAY, calendar.SUNDAY)
    is_first_week = day <= FIRST_WEEK_LAST_DAY
    is_member_day = is_member and day == MEMBER_DAY
    return (is_weekend and is_first_week) or is_member_day


def print_ranking(names: list[str]) -> None:
    for rank, name in enumerate(names, start=1):
        print(f"{rank}位: {name}")


if __name__ == "__main__":
    print(check_loan(True, False, 3))
    print(check_loan(True, False, 5))
    print(is_discount_day(5, 3, False))
    print(is_discount_day(2, 15, True))
    print_ranking(["佐藤", "鈴木", "高橋"])
