"""シーザー暗号の暗号化・復号と、全数探索による解読。

実行方法::

    python caesar.py
"""

import string

ALPHABET = string.ascii_uppercase


def shift_char(ch: str, key: int) -> str:
    """英大文字 ch をアルファベット順に key だけずらす。英大文字以外はそのまま返す。"""
    if ch not in ALPHABET:
        return ch
    return ALPHABET[(ALPHABET.index(ch) + key) % 26]


def encrypt(plaintext: str, key: int) -> str:
    """平文を大文字に変換し、各文字を key だけずらして暗号文を作る。"""
    return "".join(shift_char(ch, key) for ch in plaintext.upper())


def decrypt(ciphertext: str, key: int) -> str:
    """暗号文の各文字を key だけ逆方向にずらして平文に戻す。"""
    return encrypt(ciphertext, -key)


def brute_force(ciphertext: str) -> list[tuple[int, str]]:
    """26 通り全ての鍵で復号した結果を返す。"""
    return [(key, decrypt(ciphertext, key)) for key in range(26)]


def main() -> None:
    plaintext = "Attack at dawn"
    key = 3
    ciphertext = encrypt(plaintext, key)
    print(f"平文  : {plaintext}")
    print(f"暗号文: {ciphertext}")
    print(f"復号  : {decrypt(ciphertext, key)}")
    print()
    print("全数探索の結果:")
    for candidate_key, candidate in brute_force(ciphertext):
        print(f"  鍵 {candidate_key:2d}: {candidate}")


if __name__ == "__main__":
    main()
