"""数値と文字がコンピュータの内部でどう表現されるかを確かめる。"""

import math


def to_binary(value: int) -> str:
    """0 以上の整数を 2 進数の文字列に変換する。"""
    if value < 0:
        raise ValueError("value は 0 以上でなければならない")
    if value == 0:
        return "0"
    digits: list[str] = []
    while value > 0:
        digits.append(str(value % 2))  # 2 で割った余りが下の桁になる
        value //= 2
    return "".join(reversed(digits))


def from_binary(text: str) -> int:
    """2 進数の文字列を整数に変換する。"""
    result = 0
    for digit in text:
        result = result * 2 + int(digit)
    return result


def main() -> None:
    """整数・文字・浮動小数点数の内部表現を表示する。"""
    print(to_binary(11))  # 1011
    print(from_binary("1011"))  # 11
    print(hex(255))  # 0xff（16 進数）

    print("あ".encode("utf-8"))  # b'\xe3\x81\x82'（3 バイト）

    print(0.1 + 0.2)  # 0.30000000000000004
    print(0.1 + 0.2 == 0.3)  # False
    print(math.isclose(0.1 + 0.2, 0.3))  # True


if __name__ == "__main__":
    main()
