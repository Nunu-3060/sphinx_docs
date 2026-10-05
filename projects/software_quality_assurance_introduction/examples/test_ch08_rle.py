"""ch08_rle.py のテストです。

例示によるテストと、Hypothesis によるプロパティベーステストを並べています。
"""

from hypothesis import given
from hypothesis import strategies as st

from ch08_rle import decode, encode


def test_encode_example() -> None:
    assert encode("aaab") == [("a", 3), ("b", 1)]


def test_encode_empty() -> None:
    assert encode("") == []


@given(st.text())
def test_decode_restores_original(text: str) -> None:
    assert decode(encode(text)) == text


@given(st.text())
def test_adjacent_runs_have_different_chars(text: str) -> None:
    runs = encode(text)
    for (left, _), (right, _) in zip(runs, runs[1:]):
        assert left != right
