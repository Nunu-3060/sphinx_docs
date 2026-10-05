"""バイトオーダー（エンディアン）の違いを確かめるサンプル。

同じ整数を、ビッグエンディアンとリトルエンディアンのバイト列に変換して
比較する。また、バイトオーダーを取り違えて読んだときに値が変わることや、
バイナリ形式のヘッダを ``struct`` で組み立て・解釈する例を示す。

実行方法: python ch01_endian.py
関連する章: 第 1 章「情報の表現」（バイトオーダー）
"""

import struct
import sys


def hex_bytes(data: bytes) -> str:
    """バイト列を空白区切りの 16 進数の文字列にする。"""
    return " ".join(f"{b:02x}" for b in data)


def show_orders(value: int) -> None:
    """32 ビットの符号なし整数を、各バイトオーダーで表示する。"""
    print(f"値: {value} (0x{value:08x})")
    # struct の書式: > はビッグ、< はリトル、! はネットワークバイトオーダー
    # I は 4 バイトの符号なし整数を表す
    for label, fmt in [("ビッグ   (>I)", ">I"),
                       ("リトル   (<I)", "<I"),
                       ("ネット   (!I)", "!I")]:
        print(f"  {label}: {hex_bytes(struct.pack(fmt, value))}")
    # int.to_bytes でも同じ変換ができる
    big = value.to_bytes(4, "big")
    little = value.to_bytes(4, "little")
    print(f"  to_bytes big   : {hex_bytes(big)}")
    print(f"  to_bytes little: {hex_bytes(little)}")


def misread(data: bytes) -> None:
    """同じバイト列を 2 通りのバイトオーダーで読む。"""
    print(f"バイト列 {hex_bytes(data)} を読むと:")
    print(f"  ビッグとして  : {int.from_bytes(data, 'big')}")
    print(f"  リトルとして  : {int.from_bytes(data, 'little')}")


def build_header(version: int, length: int, offset: float) -> bytes:
    """簡単なバイナリ形式のヘッダを組み立てる。

    形式: マジック 4 バイト、版 2 バイト、長さ 4 バイト、実数 8 バイト。
    すべてビッグエンディアンで格納する。
    """
    return struct.pack(">4sHId", b"DEMO", version, length, offset)


def main() -> None:
    """各例を順に実行する。"""
    print(f"この計算機のバイトオーダー: {sys.byteorder}")
    print("== 整数のバイト列 ==")
    show_orders(0x12345678)
    print("== 取り違え ==")
    misread((1000).to_bytes(4, "big"))
    print("== 符号付き整数 ==")
    print(f"  -2 (>i): {hex_bytes(struct.pack('>i', -2))}")
    print(f"  -2 (<i): {hex_bytes(struct.pack('<i', -2))}")
    print("== ヘッダの組み立てと解釈 ==")
    header = build_header(3, 1000, 0.5)
    print(f"  {len(header)} バイト: {hex_bytes(header)}")
    magic, version, length, offset = struct.unpack(">4sHId", header)
    print(f"  正しく解釈: {magic!r} 版={version} 長さ={length} 実数={offset}")
    _, version, length, _ = struct.unpack("<4sHId", header)
    print(f"  リトルで解釈: 版={version} 長さ={length}")


if __name__ == "__main__":
    main()
