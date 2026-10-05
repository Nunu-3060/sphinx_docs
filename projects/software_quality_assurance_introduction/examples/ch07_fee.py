"""第 7 章のサンプル: 年齢から入場料金を求めます。

料金表は次のとおりです。

* 0 歳以上 5 歳以下: 無料
* 6 歳以上 12 歳以下: 500 円
* 13 歳以上 64 歳以下: 1,000 円
* 65 歳以上 120 歳以下: 700 円

上記以外の年齢は不正な入力として ValueError を送出します。
"""

MIN_AGE = 0
MAX_AGE = 120


def admission_fee(age: int) -> int:
    """年齢に対応する入場料金（円）を返します。

    Args:
        age: 年齢です。0 以上 120 以下でなければなりません。

    Returns:
        入場料金（円）です。

    Raises:
        ValueError: 年齢が範囲外の場合に送出します。
    """
    if age < MIN_AGE or age > MAX_AGE:
        raise ValueError(f"年齢が範囲外です: {age}")
    if age <= 5:
        return 0
    if age <= 12:
        return 500
    if age <= 64:
        return 1000
    return 700
