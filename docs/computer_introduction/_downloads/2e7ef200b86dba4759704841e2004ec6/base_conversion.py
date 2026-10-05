"""基数変換のサンプル。

10 進数の整数を 2 進数・16 進数の文字列に変換する処理と、その逆変換を
自分で実装し、Python の組み込み関数の結果と一致することを確かめます。

実行方法::

    python base_conversion.py
"""

# 0 から 15 までの値を表す 1 桁の記号
DIGITS = "0123456789ABCDEF"


def to_base(value: int, base: int) -> str:
    """0 以上の整数 value を base 進数の文字列に変換する。

    value を base で割った余りが最下位の桁になります。
    商に対して同じ処理を繰り返し、下の桁から順に求めます。
    """
    if not 2 <= base <= 16:
        raise ValueError("base は 2 以上 16 以下で指定してください")
    if value < 0:
        raise ValueError("value は 0 以上で指定してください")
    if value == 0:
        return "0"

    digits: list[str] = []
    while value > 0:
        value, remainder = divmod(value, base)
        digits.append(DIGITS[remainder])
    # 下の桁から求めたので、逆順に並べ替える
    return "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    """base 進数の文字列 text を整数に変換する。

    上の桁から順に「これまでの値 × base + 次の桁」を繰り返します。
    """
    value = 0
    for char in text.upper():
        digit = DIGITS.find(char)
        if not 0 <= digit < base:
            raise ValueError(f"{char!r} は {base} 進数の桁ではありません")
        value = value * base + digit
    return value


def main() -> None:
    """いくつかの値で変換結果を表示する。"""
    for number in [0, 5, 10, 255, 2026]:
        binary = to_base(number, 2)
        hexadecimal = to_base(number, 16)

        # 組み込み関数 format() の結果と一致するか確認する
        assert binary == format(number, "b")
        assert hexadecimal == format(number, "X")
        # 逆変換で元の値に戻るか確認する
        assert from_base(binary, 2) == number
        assert from_base(hexadecimal, 16) == number

        print(f"{number:>4} = 0b{binary:<11} = 0x{hexadecimal}")


if __name__ == "__main__":
    main()
