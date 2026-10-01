"""文字列を整える関数（使い方の例を doctest として docstring に書いている）.

doctest は次のように実行する。

    python -m pytest --doctest-modules ch12_techniques/text_utils.py
"""


def format_zip_code(code: str) -> str:
    """7 桁の郵便番号を「3 桁-4 桁」の形にする.

    >>> format_zip_code("1000001")
    '100-0001'
    >>> format_zip_code("100-0001")
    '100-0001'
    >>> format_zip_code("12345")
    Traceback (most recent call last):
        ...
    ValueError: 郵便番号は 7 桁の数字です: '12345'
    """
    digits = code.replace("-", "")
    if len(digits) != 7 or not digits.isdecimal():
        raise ValueError(f"郵便番号は 7 桁の数字です: {code!r}")
    return f"{digits[:3]}-{digits[3:]}"


def format_price(price: int) -> str:
    """金額を 3 桁区切りの文字列にする.

    >>> format_price(1234567)
    '1,234,567 円'
    >>> format_price(0)
    '0 円'
    """
    return f"{price:,} 円"
