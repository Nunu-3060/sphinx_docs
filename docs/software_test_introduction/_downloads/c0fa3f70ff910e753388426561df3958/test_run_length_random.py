"""標準ライブラリの random だけで行う簡易なプロパティベーステスト."""

import random

from run_length import decode, encode


def random_text(rng: random.Random) -> str:
    """同じ文字が連続しやすいように、少ない種類の文字で文字列を作る."""
    length = rng.randint(0, 30)
    return "".join(rng.choice("aab") for _ in range(length))


def test_decode_restores_original_random() -> None:
    rng = random.Random(2026)  # シードを固定して、失敗を再現できるようにする
    for _ in range(1000):
        text = random_text(rng)
        assert decode(encode(text)) == text, f"失敗した入力: {text!r}"
