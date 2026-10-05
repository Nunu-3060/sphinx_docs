"""UTF-8 の符号化規則を自前で実装するサンプル。

コードポイントを UTF-8 のバイト列に変換する関数を書き、
Python の str.encode("utf-8") の結果と一致することを確かめる。
最後に、UTF-8 のバイト列を別の文字コードで解釈したときの文字化けを示す。

実行方法: python ch01_utf8_encode.py
関連する章: 第 1 章「情報の表現」
"""


def encode_code_point(cp: int) -> bytes:
    """1 つのコードポイントを UTF-8 のバイト列に変換する。"""
    if cp < 0 or cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
        raise ValueError(f"U+{cp:04X} は符号化できない")
    if cp <= 0x7F:  # 1 バイト: 0xxxxxxx
        return bytes([cp])
    if cp <= 0x7FF:  # 2 バイト: 110xxxxx 10xxxxxx
        return bytes([0xC0 | (cp >> 6), 0x80 | (cp & 0x3F)])
    if cp <= 0xFFFF:  # 3 バイト: 1110xxxx 10xxxxxx 10xxxxxx
        return bytes([
            0xE0 | (cp >> 12),
            0x80 | ((cp >> 6) & 0x3F),
            0x80 | (cp & 0x3F),
        ])
    # 4 バイト: 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
    return bytes([
        0xF0 | (cp >> 18),
        0x80 | ((cp >> 12) & 0x3F),
        0x80 | ((cp >> 6) & 0x3F),
        0x80 | (cp & 0x3F),
    ])


def encode_utf8(text: str) -> bytes:
    """文字列を 1 文字ずつ UTF-8 に変換して連結する。"""
    return b"".join(encode_code_point(ord(ch)) for ch in text)


def bit_string(data: bytes) -> str:
    """バイト列を 8 桁の 2 進数を空白で区切った文字列にする。"""
    return " ".join(f"{b:08b}" for b in data)


def main() -> None:
    """UTF-8 の符号化結果と文字化けの例を表示する。"""
    print("== 1 文字ずつの符号化 ==")
    for ch in ["A", "é", "あ", "😀"]:
        mine = encode_code_point(ord(ch))
        assert mine == ch.encode("utf-8")
        print(f"{ch} U+{ord(ch):04X} {mine.hex(' '):<11} {bit_string(mine)}")

    print("== 文字列全体 ==")
    text = "Hello, 世界"
    data = encode_utf8(text)
    assert data == text.encode("utf-8")
    print(f"{text!r}: {len(text)} 文字, {len(data)} バイト")

    print("== 文字化け ==")
    word = "文字化け"
    utf8 = word.encode("utf-8")
    print("UTF-8 を cp1252 で解釈 :", utf8.decode("cp1252", errors="replace"))
    print("UTF-8 を Shift_JIS で解釈:", utf8.decode("shift_jis", "replace"))
    sjis = word.encode("shift_jis")
    print("Shift_JIS を UTF-8 で解釈:", sjis.decode("utf-8", "replace"))


if __name__ == "__main__":
    main()
