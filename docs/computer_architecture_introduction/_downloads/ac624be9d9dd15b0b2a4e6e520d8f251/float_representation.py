"""整数と浮動小数点数のビット表現を確かめるサンプル。

IEEE 754 の浮動小数点数を符号・指数・仮数のビットに分解して表示し、
0.1 + 0.2 の誤差、FP16 への丸め、2 の補数、バイトオーダーを確認します。

実行方法: python float_representation.py
"""

import struct
import sys


def decompose_double(x: float) -> tuple[int, int, int]:
    """倍精度浮動小数点数を（符号, 指数部, 仮数部）のビットに分解する。"""
    (bits,) = struct.unpack(">Q", struct.pack(">d", x))
    sign = bits >> 63
    exponent = (bits >> 52) & 0x7FF  # 11 ビット
    fraction = bits & ((1 << 52) - 1)  # 52 ビット
    return sign, exponent, fraction


def show_double(x: float) -> None:
    """倍精度の各フィールドと、指数のバイアスを引いた値を表示する。"""
    sign, exponent, fraction = decompose_double(x)
    if exponent == 0x7FF:
        kind = "NaN" if fraction else "無限大"
    elif exponent == 0:
        kind = "ゼロ" if fraction == 0 else "非正規化数"
    else:
        kind = f"正規化数 2^{exponent - 1023}"
    print(f"{x!r:>24}: 符号 {sign} 指数 {exponent:011b}"
          f" 仮数 {fraction:013x}（16 進）{kind}")


def to_fp16(x: float) -> float:
    """半精度（FP16）に丸めてから倍精度に戻した値を返す。"""
    (y,) = struct.unpack("<e", struct.pack("<e", x))
    result: float = y
    return result


def main() -> None:
    """各項目を順に表示する。"""
    print("=== 倍精度のビット分解 ===")
    for x in [1.0, -2.5, 0.1, 5e-324, float("inf"), float("nan")]:
        show_double(x)
    print()

    print("=== 0.1 + 0.2 ===")
    s = 0.1 + 0.2
    print(f"0.1 + 0.2 = {s!r}, 0.3 と等しいか: {s == 0.3}")
    print(f"0.1 を小数点以下 30 桁まで表示: {0.1:.30f}")
    print()

    print("=== 半精度（FP16）への丸め ===")
    for x in [0.1, 3.14159265, 65504.0, 70000.0, 2049.0]:
        try:
            print(f"{x:>12} -> {to_fp16(x)!r}")
        except OverflowError:
            print(f"{x:>12} -> FP16 の範囲外（OverflowError）")
    print()

    print("=== 2 の補数（8 ビット）===")
    for v in [5, -5, 127, -128]:
        print(f"{v:>5}: {v & 0xFF:08b}")
    total = (100 + 100) & 0xFF  # 8 ビットに切り詰める
    signed = total - 256 if total >= 128 else total
    print(f"100 + 100 を 8 ビットで計算: {total:08b} -> 符号付きでは {signed}")
    print()

    print("=== バイトオーダー ===")
    value = 0x12345678
    print(f"このマシンのバイトオーダー: {sys.byteorder}")
    print(f"リトルエンディアン: {struct.pack('<I', value).hex(' ')}")
    print(f"ビッグエンディアン: {struct.pack('>I', value).hex(' ')}")


if __name__ == "__main__":
    main()
