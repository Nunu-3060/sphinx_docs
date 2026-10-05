"""論理ゲートを組み合わせて加算器を作るサンプル。

NAND ゲートだけを基本要素とし、そこから NOT・AND・OR・XOR を作る。
さらに半加算器・全加算器を組み立て、全加算器を n 個つないだ
リプルキャリー加算器で整数の加算を行う。

実行方法: python ch02_adder.py
関連する章: 第 2 章「論理回路」
"""

Bit = int  # 0 または 1 だけを値に取る


def nand(a: Bit, b: Bit) -> Bit:
    """NAND ゲート。両方の入力が 1 のときだけ 0 を出力する。"""
    return 0 if a == 1 and b == 1 else 1


def not_(a: Bit) -> Bit:
    """NOT ゲート（NAND の 2 入力を同じ信号につなぐ）。"""
    return nand(a, a)


def and_(a: Bit, b: Bit) -> Bit:
    """AND ゲート（NAND の出力を反転する）。"""
    return not_(nand(a, b))


def or_(a: Bit, b: Bit) -> Bit:
    """OR ゲート（ド・モルガンの法則: A + B = NOT(NOT A ・ NOT B)）。"""
    return nand(not_(a), not_(b))


def xor(a: Bit, b: Bit) -> Bit:
    """XOR ゲート（NAND 4 個による構成）。"""
    n = nand(a, b)
    return nand(nand(a, n), nand(b, n))


def half_adder(a: Bit, b: Bit) -> tuple[Bit, Bit]:
    """半加算器。(和, 桁上げ) を返す。"""
    return xor(a, b), and_(a, b)


def full_adder(a: Bit, b: Bit, c_in: Bit) -> tuple[Bit, Bit]:
    """全加算器。半加算器 2 個と OR 1 個で構成し、(和, 桁上げ) を返す。"""
    s1, c1 = half_adder(a, b)
    s, c2 = half_adder(s1, c_in)
    return s, or_(c1, c2)


def to_bits(value: int, n: int) -> list[Bit]:
    """整数を n ビットのリストにする（添字 0 が最下位ビット）。"""
    return [(value >> i) & 1 for i in range(n)]


def from_bits(bits: list[Bit]) -> int:
    """ビットのリスト（添字 0 が最下位ビット）を整数に戻す。"""
    return sum(bit << i for i, bit in enumerate(bits))


def ripple_carry_add(a: int, b: int, n: int) -> tuple[int, Bit]:
    """n ビットのリプルキャリー加算器。(和, 最上位からの桁上げ) を返す。"""
    carry: Bit = 0
    result: list[Bit] = []
    for a_i, b_i in zip(to_bits(a, n), to_bits(b, n)):
        s, carry = full_adder(a_i, b_i, carry)  # 桁上げを次の桁へ渡す
        result.append(s)
    return from_bits(result), carry


def main() -> None:
    """ゲートと全加算器の真理値表、および加算の例を表示する。"""
    print("A B | AND OR XOR NAND")
    for a in (0, 1):
        for b in (0, 1):
            print(f"{a} {b} |  {and_(a, b)}   {or_(a, b)}   {xor(a, b)}"
                  f"    {nand(a, b)}")

    print()
    print("A B Cin | S Cout")
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                s, c_out = full_adder(a, b, c)
                print(f"{a} {b}  {c}  | {s}  {c_out}")

    print()
    n = 8
    for a, b in [(23, 42), (100, 155), (200, 100)]:
        total, carry = ripple_carry_add(a, b, n)
        print(f"{a:08b} + {b:08b} = {total:08b} 桁上げ={carry}"
              f"  ({a} + {b} = {total}"
              f"{'、桁あふれ' if carry else ''})")
        assert total + (carry << n) == a + b


if __name__ == "__main__":
    main()
