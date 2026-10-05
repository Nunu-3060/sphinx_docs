"""2 の補数表現のサンプル。

符号付き整数を決まったビット数の 2 の補数で表し、
符号の反転とオーバーフローの様子を確かめます。

Python の int は桁数に上限がないため、ビットマスクを使って
計算機のレジスタと同じく「決まったビット数」の世界を再現しています。

実行方法::

    python twos_complement.py
"""

# 1 つの整数を表すビット数
BITS = 8


def mask(bits: int) -> int:
    """下位 bits ビットだけが 1 の値を返す (8 ビットなら 0b11111111)。"""
    return (1 << bits) - 1


def to_bits(value: int, bits: int = BITS) -> str:
    """符号付き整数 value を bits ビットの 2 の補数表現に変換する。"""
    lowest = -(1 << (bits - 1))
    highest = (1 << (bits - 1)) - 1
    if not lowest <= value <= highest:
        raise ValueError(f"{value} は {bits} ビットで表せません")
    # 負の数は 2 ** bits を足した値のビット列になる
    return format(value & mask(bits), f"0{bits}b")


def from_bits(bit_string: str) -> int:
    """2 の補数表現のビット列を符号付き整数に戻す。"""
    bits = len(bit_string)
    raw = int(bit_string, 2)
    # 最上位ビットが 1 なら負の数なので 2 ** bits を引く
    if bit_string[0] == "1":
        return raw - (1 << bits)
    return raw


def negate(bit_string: str) -> str:
    """全ビットを反転して 1 を足し、符号を反転したビット列を返す。"""
    bits = len(bit_string)
    inverted = int(bit_string, 2) ^ mask(bits)
    return format((inverted + 1) & mask(bits), f"0{bits}b")


def add(a: int, b: int, bits: int = BITS) -> tuple[int, bool]:
    """bits ビットの加算器と同じように a + b を計算する。

    戻り値は (計算結果, オーバーフローしたかどうか) です。
    """
    raw = (a + b) & mask(bits)
    result = from_bits(format(raw, f"0{bits}b"))
    return result, result != a + b


def main() -> None:
    """2 の補数表現、符号の反転、オーバーフローの例を表示する。"""
    print(f"{BITS} ビットの 2 の補数表現")
    for value in [0, 1, 5, 127, -1, -5, -128]:
        print(f"  {value:>5} -> {to_bits(value)}")

    print("全ビットを反転して 1 を足すと符号が反転する")
    for value in [5, -5, 1]:
        before = to_bits(value)
        after = negate(before)
        print(f"  {before} ({value:>2}) -> {after} ({from_bits(after):>2})")

    print("加算とオーバーフロー")
    for a, b in [(100, 27), (100, 28), (-100, -29)]:
        result, overflow = add(a, b)
        note = "オーバーフロー" if overflow else "正常"
        print(f"  {a:>4} + {b:>4} = {result:>4}  ({note})")


if __name__ == "__main__":
    main()
