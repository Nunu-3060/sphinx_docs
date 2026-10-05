"""ハミング (7,4) 符号で 1 ビットの誤りを訂正できることを確かめるサンプル。

4 ビットのデータに 3 ビットのパリティを加えて 7 ビットの符号語を作り、
任意の 1 ビットを反転させても、シンドロームから誤りの位置を求めて
元のデータに戻せることを示す。さらに全体パリティを 1 ビット加えた
(8,4) 符号 (SECDED) で、2 ビットの誤りを「検出」できることも示す。

実行方法: python hamming_code.py
"""

# 符号語のビット位置は 1 から 7 で数える。
# 位置 1, 2, 4 (2 のべき乗) がパリティ、位置 3, 5, 6, 7 がデータ。
DATA_POSITIONS = (3, 5, 6, 7)
PARITY_POSITIONS = (1, 2, 4)


def encode(data: list[int]) -> list[int]:
    """4 ビットのデータを 7 ビットの符号語に符号化する。

    戻り値の添字 0 は使わず、添字 1..7 を符号語のビット位置とする。
    """
    word = [0] * 8
    for pos, bit in zip(DATA_POSITIONS, data):
        word[pos] = bit
    for p in PARITY_POSITIONS:
        # パリティ p は、位置番号と p の AND が 0 でない位置を担当する
        parity = 0
        for pos in range(1, 8):
            if pos != p and pos & p:
                parity ^= word[pos]
        word[p] = parity
    return word


def syndrome(word: list[int]) -> int:
    """シンドロームを計算する。0 なら誤りなし、それ以外は誤りの位置。"""
    s = 0
    for pos in range(1, 8):
        if word[pos]:
            s ^= pos  # 1 が立っている位置番号の XOR
    return s


def decode(word: list[int]) -> tuple[list[int], int]:
    """1 ビットの誤りを訂正し、(データ 4 ビット、シンドローム) を返す。"""
    fixed = word.copy()
    s = syndrome(fixed)
    if s != 0:
        fixed[s] ^= 1  # シンドロームが指す位置のビットを反転して訂正
    return [fixed[pos] for pos in DATA_POSITIONS], s


def to_str(bits: list[int]) -> str:
    """ビット列を文字列にする。"""
    return "".join(str(b) for b in bits)


def secded_check(word8: list[int]) -> str:
    """全体パリティ付き (8,4) 符号語を調べ、判定結果を返す。

    word8[0] に全体パリティ、word8[1..7] にハミング (7,4) 符号語を置く。
    """
    s = syndrome(word8)
    overall = sum(word8) % 2  # 全 8 ビットの XOR (偶数パリティなら 0)
    if s == 0 and overall == 0:
        return "誤りなし"
    if overall == 1:
        return f"1 ビット誤り (位置 {s}) を訂正可能"
    return "2 ビット誤りを検出 (訂正不能)"


def main() -> None:
    """符号化、1 ビット誤りの訂正、2 ビット誤りの検出を試す。"""
    data = [1, 0, 1, 1]
    word = encode(data)
    print(f"データ        : {to_str(data)}")
    print(f"符号語 (1..7) : {to_str(word[1:])}")
    print()

    # すべての位置について 1 ビット誤りを注入し、訂正できるか確かめる
    print("誤り位置  受信語   シンドローム  復号データ  判定")
    for err in range(1, 8):
        received = word.copy()
        received[err] ^= 1
        decoded, s = decode(received)
        ok = "OK" if decoded == data else "NG"
        print(f"{err:8d}  {to_str(received[1:])}  {s:12d}  "
              f"{to_str(decoded):>10s}  {ok}")

    # 16 通りすべてのデータで、7 通りの 1 ビット誤りを訂正できるか
    total = 0
    corrected = 0
    for value in range(16):
        d = [(value >> i) & 1 for i in (3, 2, 1, 0)]
        w = encode(d)
        for err in range(1, 8):
            r = w.copy()
            r[err] ^= 1
            total += 1
            if decode(r)[0] == d:
                corrected += 1
    print(f"\n全データ x 全誤り位置: {corrected}/{total} 件を訂正")

    # SECDED: 全体パリティを位置 0 に加えた (8,4) 符号
    word8 = word.copy()
    word8[0] = sum(word[1:]) % 2
    print(f"\nSECDED 符号語 (0..7): {to_str(word8)}")
    one = word8.copy()
    one[6] ^= 1
    two = word8.copy()
    two[3] ^= 1
    two[5] ^= 1
    print(f"誤りなし         : {secded_check(word8)}")
    print(f"位置 6 を反転    : {secded_check(one)}")
    print(f"位置 3, 5 を反転 : {secded_check(two)}")
    # 同じ 2 ビット誤りを (7,4) 符号だけで復号すると誤訂正になる
    wrong, s = decode(two)
    print(f"(7,4) で復号すると: シンドローム {s}、"
          f"データ {to_str(wrong)} (正しくは {to_str(data)})")


if __name__ == "__main__":
    main()
