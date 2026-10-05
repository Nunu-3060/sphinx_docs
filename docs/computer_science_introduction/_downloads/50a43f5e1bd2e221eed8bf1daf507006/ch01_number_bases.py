"""基数変換と 2 の補数を確かめるサンプル。

整数を 2 進数・16 進数の文字列に変換する関数を自前で実装し、
Python 組み込みの bin() / hex() / int() と結果を比較する。
また、8 ビットの 2 の補数表現とオーバーフローの様子を示す。

実行方法: python ch01_number_bases.py
関連する章: 第 1 章「情報の表現」
"""

DIGITS = "0123456789abcdef"


def to_base(value: int, base: int) -> str:
    """0 以上の整数 value を base 進数の文字列に変換する。

    base で割った余りを下の桁から順に求め、最後に逆順に並べる。
    """
    if not 2 <= base <= 16:
        raise ValueError("base は 2 以上 16 以下にする")
    if value < 0:
        raise ValueError("value は 0 以上にする")
    if value == 0:
        return "0"
    digits: list[str] = []
    while value > 0:
        value, remainder = divmod(value, base)
        digits.append(DIGITS[remainder])
    return "".join(reversed(digits))


def from_base(text: str, base: int) -> int:
    """base 進数の文字列 text を整数に変換する（ホーナー法）。"""
    value = 0
    for ch in text.lower():
        value = value * base + DIGITS.index(ch)
    return value


def to_twos_complement(value: int, bits: int) -> int:
    """符号付き整数 value を bits ビットの 2 の補数のビット列（整数）にする。"""
    if not -(1 << (bits - 1)) <= value < (1 << (bits - 1)):
        raise ValueError(f"{value} は {bits} ビットで表せない")
    # 負の数は 2**bits を足した値になる。& によるマスクで同じ結果が得られる
    return value & ((1 << bits) - 1)


def from_twos_complement(pattern: int, bits: int) -> int:
    """bits ビットの 2 の補数のビット列 pattern を符号付き整数に戻す。"""
    if pattern & (1 << (bits - 1)):  # 最上位ビットが 1 なら負の数
        return pattern - (1 << bits)
    return pattern


def add_int8(a: int, b: int) -> int:
    """8 ビット符号付き整数を加算し、結果を 8 ビットに切り詰める。"""
    raw = (to_twos_complement(a, 8) + to_twos_complement(b, 8)) & 0xFF
    return from_twos_complement(raw, 8)


def main() -> None:
    """基数変換と 2 の補数の例を表示する。"""
    print("== 基数変換 ==")
    for n in [10, 255, 2026]:
        b2 = to_base(n, 2)
        b16 = to_base(n, 16)
        assert b2 == bin(n)[2:] and b16 == hex(n)[2:]
        assert from_base(b2, 2) == n == int(b16, 16)
        print(f"{n:>5} = 0b{b2} = 0x{b16}")

    print("== 8 ビットの 2 の補数 ==")
    for n in [5, 1, 0, -1, -5, -128, 127]:
        pattern = to_twos_complement(n, 8)
        assert from_twos_complement(pattern, 8) == n
        print(f"{n:>5} -> {pattern:08b} (0x{pattern:02x})")

    print("== オーバーフロー ==")
    for a, b in [(100, 27), (100, 28), (-128, -1)]:
        print(f"{a} + {b} = {add_int8(a, b)} (数学的には {a + b})")


if __name__ == "__main__":
    main()
