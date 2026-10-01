"""Hypothesis が欠陥を見つける様子を確認するための例.

ランレングス符号化の結果を "a3b1" のような文字列で表す版である。元の文字列に
数字が含まれると正しく復元できない欠陥がある。ファイル名が test_ で始まらない
ため、引数なしで pytest を実行したときは収集されない。次のように実行する。

    python -m pytest ch12_techniques/buggy_codec_example.py
"""

import re

from hypothesis import given
from hypothesis import strategies as st


def encode_to_str(text: str) -> str:
    """文字列を "a3b1" の形に符号化する（"aaab" の場合）."""
    return "".join(f"{m.group(1)}{len(m.group(0))}"
                   for m in re.finditer(r"(.)\1*", text, re.DOTALL))


def decode_from_str(code: str) -> str:
    """encode_to_str の結果から元の文字列を復元する."""
    return "".join(char * int(count)
                   for char, count in re.findall(r"(\D)(\d+)", code))


@given(st.text())
def test_roundtrip(text: str) -> None:
    assert decode_from_str(encode_to_str(text)) == text
