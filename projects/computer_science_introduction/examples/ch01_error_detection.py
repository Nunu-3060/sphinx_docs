"""誤り検出と誤り訂正の符号を実装して確かめるサンプル。

パリティ、インターネットチェックサム（RFC 1071）、CRC-32、
ハミング符号 (7,4) を実装し、ビット誤りを検出・訂正できるかを確かめる。
CRC-32 は標準ライブラリの zlib.crc32 / binascii.crc32 と結果を比較する。

実行方法: python ch01_error_detection.py
関連する章: 第 1 章「情報の表現」（誤り検出と符号化）
"""

import binascii
import zlib


def parity(data: bytes) -> int:
    """データ全体の 1 のビットの個数の偶奇（偶数パリティのビット）を返す。"""
    ones = sum(bin(b).count("1") for b in data)
    return ones % 2


def flip_bit(data: bytes, pos: int) -> bytes:
    """先頭から pos 番目（0 始まり）のビットを反転したバイト列を返す。"""
    buf = bytearray(data)
    buf[pos // 8] ^= 0x80 >> (pos % 8)
    return bytes(buf)


def internet_checksum(data: bytes) -> int:
    """RFC 1071 のインターネットチェックサムを計算する。"""
    if len(data) % 2 == 1:
        data += b"\x00"  # 奇数長なら 0 を補って 16 ビット単位にする
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)  # 桁上げを下位に戻す
    return ~total & 0xFFFF  # 1 の補数（ビット反転）を取る


def crc32(data: bytes) -> int:
    """CRC-32 をビット単位で計算する（zlib と同じ方式）。"""
    poly = 0xEDB88320  # 生成多項式 0x04C11DB7 をビット反転した表現
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly  # 多項式で割る（XOR で引く）
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF


def hamming74_encode(d: list[int]) -> list[int]:
    """4 ビットのデータを 7 ビットのハミング符号にする。

    位置 1, 2, 4 が検査ビット、位置 3, 5, 6, 7 がデータビットである。
    """
    p1 = d[0] ^ d[1] ^ d[3]  # 位置 1, 3, 5, 7 の偶数パリティ
    p2 = d[0] ^ d[2] ^ d[3]  # 位置 2, 3, 6, 7 の偶数パリティ
    p4 = d[1] ^ d[2] ^ d[3]  # 位置 4, 5, 6, 7 の偶数パリティ
    return [p1, p2, d[0], p4, d[1], d[2], d[3]]


def hamming74_decode(c: list[int]) -> tuple[list[int], int]:
    """7 ビットの符号語を復号し、(データ, 誤りの位置) を返す。

    誤りの位置はシンドローム（1〜7）で、0 なら誤りなしである。
    """
    c = c.copy()
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s4 = c[3] ^ c[4] ^ c[5] ^ c[6]
    syndrome = s1 + 2 * s2 + 4 * s4
    if syndrome != 0:
        c[syndrome - 1] ^= 1  # 誤った位置のビットを反転して訂正する
    return [c[2], c[4], c[5], c[6]], syndrome


def bits(v: list[int]) -> str:
    """ビットのリストを 0 と 1 の文字列にする。"""
    return "".join(str(b) for b in v)


def main() -> None:
    """各符号で誤りを検出・訂正できるかを確かめる。"""
    data = b"Hello, CRC!"
    one = flip_bit(data, 10)               # 1 ビットの誤り
    two = flip_bit(flip_bit(data, 10), 20)  # 2 ビットの誤り
    swapped = data[2:4] + data[0:2] + data[4:]  # 16 ビット単位の入れ替え

    print("== パリティ ==")
    print(f"  元: {parity(data)}  1 ビット誤り: {parity(one)}"
          f"  2 ビット誤り: {parity(two)}")

    print("== インターネットチェックサム ==")
    ck = internet_checksum(data)
    print(f"  元: 0x{ck:04x}  1 ビット誤り: 0x{internet_checksum(one):04x}"
          f"  入れ替え: 0x{internet_checksum(swapped):04x}")
    padded = data + b"\x00"  # 偶数長にそろえてからチェックサムを付ける
    check = internet_checksum(padded + ck.to_bytes(2, "big"))
    print(f"  チェックサムを付けて再計算: 0x{check:04x}")

    print("== CRC-32 ==")
    print(f"  自作         : 0x{crc32(data):08x}")
    print(f"  zlib.crc32   : 0x{zlib.crc32(data):08x}")
    print(f"  binascii     : 0x{binascii.crc32(data):08x}")
    print(f"  1 ビット誤り : 0x{crc32(one):08x}")
    print(f"  2 ビット誤り : 0x{crc32(two):08x}")
    print(f"  入れ替え     : 0x{crc32(swapped):08x}")

    print("== ハミング符号 (7,4) ==")
    d = [1, 0, 1, 1]
    code = hamming74_encode(d)
    print(f"  データ {bits(d)} -> 符号語 {bits(code)}")
    for pos in range(7):
        received = code.copy()
        received[pos] ^= 1
        decoded, syndrome = hamming74_decode(received)
        ok = "OK" if decoded == d else "NG"
        print(f"  位置 {pos + 1} を反転: {bits(received)}"
              f" シンドローム={syndrome} 復号={bits(decoded)} {ok}")


if __name__ == "__main__":
    main()
