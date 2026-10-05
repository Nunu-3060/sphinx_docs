"""演習問題 7-3 の対象となる関数（第 7 章）.

会員で、かつ購入金額が 5000 円以上の場合に送料を無料にする。
"""

FREE_SHIPPING_THRESHOLD = 5000


def is_free_shipping(is_member: bool, amount: int) -> bool:
    """送料が無料になる場合に True を返す."""
    return is_member and amount >= FREE_SHIPPING_THRESHOLD


if __name__ == "__main__":
    print(is_free_shipping(is_member=True, amount=6000))
    print(is_free_shipping(is_member=False, amount=6000))
