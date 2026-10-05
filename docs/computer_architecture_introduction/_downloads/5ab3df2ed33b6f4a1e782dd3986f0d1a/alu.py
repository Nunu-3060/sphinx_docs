"""論理ゲートから全加算器・リプルキャリー加算器・ALU を組み立てるサンプル。

各信号は「値」と「入力から数えたゲート段数」の組で表します。8 ビットの ALU
で加算・減算・AND・OR・比較を計算してフラグを表示し、さらにリプルキャリー
加算器の段数が桁数に比例して増えることを確かめます。

実行方法: python alu.py
"""

Signal = tuple[int, int]  # (値 0 または 1, 入力から数えたゲート段数)


# --- 論理ゲート：出力の段数は「遅い方の入力の段数 + 1」 ---
def g_not(a: Signal) -> Signal:
    return (1 - a[0], a[1] + 1)


def g_and(a: Signal, b: Signal) -> Signal:
    return (a[0] & b[0], max(a[1], b[1]) + 1)


def g_or(a: Signal, b: Signal) -> Signal:
    return (a[0] | b[0], max(a[1], b[1]) + 1)


def g_xor(a: Signal, b: Signal) -> Signal:
    return (a[0] ^ b[0], max(a[1], b[1]) + 1)


def mux2(i0: Signal, i1: Signal, sel: Signal) -> Signal:
    """sel が 0 なら i0、1 なら i1 を選ぶマルチプレクサ。"""
    return g_or(g_and(i0, g_not(sel)), g_and(i1, sel))


def full_adder(a: Signal, b: Signal, cin: Signal) -> tuple[Signal, Signal]:
    """全加算器。和とキャリー出力を返す。"""
    p = g_xor(a, b)
    s = g_xor(p, cin)
    cout = g_or(g_and(a, b), g_and(p, cin))
    return s, cout


def ripple_carry_add(a: list[Signal], b: list[Signal],
                     cin: Signal) -> tuple[list[Signal], Signal, Signal]:
    """リプルキャリー加算器（ビットは下位から並べる）。

    和、最上位からのキャリー、最上位へのキャリーを返す。
    """
    sums: list[Signal] = []
    carry_in_msb = carry = cin
    for x, y in zip(a, b):
        carry_in_msb = carry
        s, carry = full_adder(x, y, carry)  # キャリーが次の桁へ伝わる
        sums.append(s)
    return sums, carry, carry_in_msb


def to_bits(value: int, width: int) -> list[Signal]:
    """整数を下位ビットから並べた信号のリストにする（段数は 0）。"""
    return [((value >> i) & 1, 0) for i in range(width)]


def to_int(bits: list[Signal], signed: bool = True) -> int:
    """信号のリストを整数に戻す。"""
    value = sum(bit[0] << i for i, bit in enumerate(bits))
    if signed and bits[-1][0]:
        value -= 1 << len(bits)
    return value


# 演算ごとの制御信号 (sub, sel1, sel0)。sel で結果を選ぶ。
CONTROL = {"add": (0, 0, 0), "sub": (1, 0, 0), "and": (0, 0, 1),
           "or": (0, 1, 0), "slt": (1, 1, 1)}


def alu(a: int, b: int, op: str,
        width: int = 8) -> tuple[list[Signal], dict[str, int], int]:
    """ALU。結果、フラグ、結果が確定するまでのゲート段数を返す。"""
    sub, sel1, sel0 = ((c, 0) for c in CONTROL[op])
    xa, xb = to_bits(a, width), to_bits(b, width)
    # 減算は a + (b の各ビットを反転) + 1 として計算する（2 の補数）
    nb = [g_xor(bit, sub) for bit in xb]
    sums, cout, c_msb = ripple_carry_add(xa, nb, sub)
    overflow = g_xor(cout, c_msb)
    less = g_xor(sums[-1], overflow)  # 符号付きで a < b なら 1
    zero_bit: Signal = (0, 0)
    result = []
    for i in range(width):
        and_i, or_i = g_and(xa[i], xb[i]), g_or(xa[i], xb[i])
        slt_i = less if i == 0 else zero_bit
        low = mux2(sums[i], and_i, sel0)  # 4 入力のマルチプレクサ
        high = mux2(or_i, slt_i, sel0)
        result.append(mux2(low, high, sel1))
    any_one = result
    while len(any_one) > 1:  # OR の木で 1 のビットがあるかを調べる
        any_one = [g_or(any_one[i], any_one[i + 1])
                   for i in range(0, len(any_one), 2)]
    zero = g_not(any_one[0])
    flags = {"Z": zero[0], "N": result[-1][0],
             "C": cout[0], "V": overflow[0]}
    depth = max(bit[1] for bit in result + [zero])
    return result, flags, depth


def main() -> None:
    """8 ビット ALU の計算例と、加算器の段数を表示する。"""
    print("8 ビット ALU の計算例")
    print(" 演算    a     b  結果  2 進数     Z N C V 段数")
    cases = [("add", 100, 27), ("add", 100, 28), ("add", -56, 100),
             ("sub", 50, 80), ("sub", 7, 7), ("and", 0x5A, 0x0F),
             ("or", 0x50, 0x0F), ("slt", 3, -5), ("slt", -5, 3)]
    for op, a, b in cases:
        result, flags, depth = alu(a, b, op)
        bits = "".join(str(bit[0]) for bit in reversed(result))
        f = " ".join(str(v) for v in flags.values())
        print(f" {op:<4}{a:>5}{b:>6}{to_int(result):>6}  {bits}  {f}"
              f"{depth:>4}")

    print()
    print("リプルキャリー加算器のゲート段数（キャリー出力まで）")
    for width in (4, 8, 16, 32, 64):
        zero = to_bits(0, width)
        _, cout, _ = ripple_carry_add(zero, zero, (0, 0))
        print(f"  {width:>2} ビット: {cout[1]:>3} 段")


if __name__ == "__main__":
    main()
