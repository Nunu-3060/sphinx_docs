"""加算器のサンプル。

半加算器と全加算器を論理演算で作り、全加算器を並べた
リプルキャリー加算器で 8 ビットの加算を行います。

実行方法::

    python adder.py
"""

# 加算器のビット数
BITS = 8


def half_adder(a: int, b: int) -> tuple[int, int]:
    """半加算器: 1 ビット同士を足し、(和, 桁上がり) を返す。"""
    total = a ^ b  # XOR
    carry = a & b  # AND
    return total, carry


def full_adder(a: int, b: int, carry_in: int) -> tuple[int, int]:
    """全加算器: 下の桁からの桁上がりも含めて 3 ビットを足す。

    半加算器 2 個と OR ゲート 1 個で構成します。
    """
    partial, carry1 = half_adder(a, b)
    total, carry2 = half_adder(partial, carry_in)
    return total, carry1 | carry2  # OR


def ripple_carry_add(x: int, y: int, bits: int = BITS) -> tuple[int, int]:
    """全加算器を bits 個つないで x + y を計算する。

    戻り値は (bits ビットの和, 最上位からの桁上がり) です。
    """
    result = 0
    carry = 0
    for i in range(bits):
        # 下の桁から順に 1 ビットずつ取り出して足す
        a = (x >> i) & 1
        b = (y >> i) & 1
        total, carry = full_adder(a, b, carry)
        result |= total << i
    return result, carry


def main() -> None:
    """全加算器の真理値表と 8 ビット加算の例を表示する。"""
    print("全加算器: A B Cin | S Cout")
    for a in [0, 1]:
        for b in [0, 1]:
            for carry_in in [0, 1]:
                total, carry_out = full_adder(a, b, carry_in)
                print(f"          {a} {b}  {carry_in}  | {total}  {carry_out}")

    print(f"{BITS} ビットのリプルキャリー加算器")
    for x, y in [(5, 3), (100, 55), (200, 100)]:
        total, carry = ripple_carry_add(x, y)
        print(
            f"  {x:08b} + {y:08b} = {total:08b} "
            f"(桁上がり {carry}) ... {x} + {y} = {total + (carry << BITS)}"
        )


if __name__ == "__main__":
    main()
