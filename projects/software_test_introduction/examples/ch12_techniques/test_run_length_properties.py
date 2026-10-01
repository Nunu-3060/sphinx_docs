"""Hypothesis によるプロパティベーステスト."""

from hypothesis import given
from hypothesis import strategies as st

from run_length import decode, encode
from shop.shipping import calc_shipping_fee


@given(st.text())
def test_decode_restores_original(text: str) -> None:
    # 性質 1: 符号化してから復元すると元に戻る
    assert decode(encode(text)) == text


@given(st.text())
def test_adjacent_runs_have_different_chars(text: str) -> None:
    # 性質 2: 隣り合う組の文字は異なり、個数は 1 以上である
    runs = encode(text)
    assert all(count >= 1 for _, count in runs)
    assert all(a[0] != b[0] for a, b in zip(runs, runs[1:]))


@given(st.integers(min_value=0, max_value=10**7),
       st.integers(min_value=0, max_value=10**7),
       st.booleans(), st.booleans())
def test_shipping_fee_never_increases_with_subtotal(
        a: int, b: int, is_premium: bool, is_remote: bool) -> None:
    # 性質 3: 注文金額が増えても送料は増えない
    low, high = min(a, b), max(a, b)
    assert (calc_shipping_fee(high, is_premium, is_remote)
            <= calc_shipping_fee(low, is_premium, is_remote))
