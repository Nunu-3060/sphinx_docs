"""浮動小数点数の誤差のサンプル。

0.1 + 0.2 が 0.3 と等しくならない理由を、
IEEE 754 倍精度 (64 ビット) のビット列を表示して確かめます。

実行方法::

    python float_error.py
"""

import math
import struct
from decimal import Decimal


def float_to_bits(value: float) -> str:
    """倍精度浮動小数点数を「符号 指数部 仮数部」のビット列で返す。"""
    # 8 バイトの float を、同じビット並びの 64 ビット符号なし整数とみなす
    (raw,) = struct.unpack(">Q", struct.pack(">d", value))
    bits = format(raw, "064b")
    return f"{bits[0]} {bits[1:12]} {bits[12:]}"


def main() -> None:
    """誤差の例とビット列を表示する。"""
    total = 0.1 + 0.2
    print(f"0.1 + 0.2        = {total!r}")
    print(f"0.1 + 0.2 == 0.3 : {total == 0.3}")
    print(f"math.isclose()   : {math.isclose(total, 0.3)}")

    # Decimal(float) は float が実際に保持している値を正確に表示する
    print("0.1 として実際に記憶されている値:")
    print(f"  {Decimal(0.1)}")

    print("ビット列 (符号 指数部 仮数部):")
    for value in [1.0, 0.5, -2.0, 0.1]:
        print(f"  {value:>4}: {float_to_bits(value)}")


if __name__ == "__main__":
    main()
