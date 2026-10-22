"""第 3 章「名前の付け方」の悪い例。"""


def calc(d: list[int]) -> int:
    r = 0
    for x in d:
        if x >= 60:
            r += 1
    return r


def chk(s: int) -> bool:
    return s == 100


if __name__ == "__main__":
    lst = [72, 45, 100, 60, 38]
    print(calc(lst))
    print(chk(lst[2]))
