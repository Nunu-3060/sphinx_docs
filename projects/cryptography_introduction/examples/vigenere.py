"""ヴィジュネル暗号の暗号化・復号と、頻度分析による解読。

解読は次の 2 段階で行う。

1. 一致指数（index of coincidence）を使って鍵の長さを推定する。
2. 鍵の各文字について、カイ二乗値が最小になるずらし量を選ぶ。

実行方法::

    python vigenere.py
"""

import string

ALPHABET = string.ascii_uppercase

# 英文における各アルファベットの出現頻度 [%]（A〜Z）
ENGLISH_FREQ = [
    8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406,
    6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074,
]


def normalize(text: str) -> str:
    """英字だけを取り出して大文字にする。"""
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def encrypt(plaintext: str, key: str) -> str:
    """i 文字目を鍵の (i mod 鍵長) 文字目の分だけずらす。"""
    text = normalize(plaintext)
    shifts = [ALPHABET.index(k) for k in key.upper()]
    return "".join(
        ALPHABET[(ALPHABET.index(ch) + shifts[i % len(shifts)]) % 26] for i, ch in enumerate(text)
    )


def decrypt(ciphertext: str, key: str) -> str:
    """encrypt() と逆方向にずらして平文に戻す。"""
    inverse_key = "".join(ALPHABET[(-ALPHABET.index(k)) % 26] for k in key.upper())
    return encrypt(ciphertext, inverse_key)


def index_of_coincidence(text: str) -> float:
    """文字列から無作為に選んだ 2 文字が一致する確率を求める。"""
    n = len(text)
    if n < 2:
        return 0.0
    counts = [text.count(ch) for ch in ALPHABET]
    return sum(c * (c - 1) for c in counts) / (n * (n - 1))


def guess_key_length(ciphertext: str, max_length: int = 12, threshold: float = 0.055) -> int:
    """鍵長の候補ごとに暗号文を列に分け、平均一致指数がしきい値を超える最小の長さを返す。

    英文の一致指数は約 0.066、一様な乱数列では 1/26 ≒ 0.038 である。鍵長の倍数でも一致指数は高くなるため、
    条件を満たす最小の長さを選ぶ。
    """
    averages = {}
    for length in range(1, max_length + 1):
        columns = [ciphertext[i::length] for i in range(length)]
        averages[length] = sum(index_of_coincidence(col) for col in columns) / length
        if averages[length] > threshold:
            return length
    return max(averages, key=lambda length: averages[length])


def chi_squared(text: str) -> float:
    """文字の出現回数と英文の期待出現回数とのカイ二乗値を求める。"""
    n = len(text)
    total = 0.0
    for ch, freq in zip(ALPHABET, ENGLISH_FREQ):
        expected = n * freq / 100
        total += (text.count(ch) - expected) ** 2 / expected
    return total


def guess_key(ciphertext: str, key_length: int) -> str:
    """鍵の各文字について、復号結果が最も英文らしくなるずらし量を選ぶ。"""
    key = ""
    for i in range(key_length):
        column = ciphertext[i::key_length]
        best = min(range(26), key=lambda s: chi_squared(decrypt(column, ALPHABET[s])))
        key += ALPHABET[best]
    return key


def main() -> None:
    plaintext = (
        "Cryptography is the practice and study of techniques for secure communication in the "
        "presence of adversarial behavior. More generally, cryptography is about constructing and "
        "analyzing protocols that prevent third parties or the public from reading private messages. "
        "Modern cryptography exists at the intersection of the disciplines of mathematics, computer "
        "science, information security, electrical engineering, digital signal processing, physics, "
        "and others. Core concepts related to information security, such as data confidentiality, "
        "data integrity, authentication, and non-repudiation are also central to cryptography."
    )
    key = "PYTHON"
    ciphertext = encrypt(plaintext, key)
    print(f"暗号文（先頭 60 文字）: {ciphertext[:60]}")

    length = guess_key_length(ciphertext)
    guessed = guess_key(ciphertext, length)
    print(f"推定した鍵長: {length}")
    print(f"推定した鍵  : {guessed}")
    print(f"復号（先頭 60 文字）  : {decrypt(ciphertext, guessed)[:60]}")


if __name__ == "__main__":
    main()
