"""浮動小数点数の誤差と内部表現を確かめるサンプル。

IEEE 754 binary64（Python の float）のビット列を符号・指数・仮数に
分解して表示し、0.1 + 0.2 が 0.3 にならない理由と、比較や金額計算での
対処方法（math.isclose、decimal、fractions）を示す。

実行方法: python ch01_float_error.py
関連する章: 第 1 章「情報の表現」
"""

import math
import struct
from decimal import Decimal
from fractions import Fraction


def float_bits(x: float) -> tuple[int, int, int]:
    """float を binary64 の (符号, 指数部, 仮数部) の整数 3 つに分解する。"""
    # ">d" はビッグエンディアンの 8 バイト浮動小数点数、">Q" は 8 バイト整数
    (bits,) = struct.unpack(">Q", struct.pack(">d", x))
    sign = bits >> 63
    exponent = (bits >> 52) & 0x7FF  # 11 ビット
    fraction = bits & ((1 << 52) - 1)  # 52 ビット
    return sign, exponent, fraction


def describe(x: float) -> str:
    """float の内部表現を人が読める形の文字列にする（正規化数のみ）。"""
    sign, exponent, fraction = float_bits(x)
    return (
        f"{x!r:>22}: 符号={sign} 指数部={exponent:4d}"
        f" (2^{exponent - 1023:+d}) 仮数部=0x{fraction:013x}"
    )


def main() -> None:
    """浮動小数点数の誤差の例を表示する。"""
    print("== 内部表現 ==")
    for x in [1.0, -2.5, 0.1, 0.2, 0.3, 0.1 + 0.2]:
        print(describe(x))

    print("== 0.1 が実際に表している値 ==")
    print(Decimal(0.1))

    print("== 比較 ==")
    print("0.1 + 0.2 == 0.3            :", 0.1 + 0.2 == 0.3)
    print("math.isclose(0.1 + 0.2, 0.3):", math.isclose(0.1 + 0.2, 0.3))

    print("== 0.1 を 10 回足す ==")
    total = 0.0
    for _ in range(10):
        total += 0.1
    print("float    :", total)
    print("math.fsum:", math.fsum([0.1] * 10))
    print("Decimal  :", sum([Decimal("0.1")] * 10, Decimal(0)))
    print("Fraction :", sum([Fraction(1, 10)] * 10, Fraction(0)))

    print("== 大きな数と小さな数 ==")
    big = 2.0**53
    print("2**53 + 1.0 == 2**53 :", big + 1.0 == big)
    print("math.ulp(1.0)        :", math.ulp(1.0))


if __name__ == "__main__":
    main()
