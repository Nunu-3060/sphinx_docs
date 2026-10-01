"""送料を計算する."""

BASE_FEE = 500
"""基本送料（円）."""

REMOTE_SURCHARGE = 1000
"""離島への配送で加算する料金（円）."""

FREE_THRESHOLD = 5000
"""一般会員の送料無料となる注文金額（円）."""

MEMBER_FREE_THRESHOLD = 3000
"""プレミアム会員の送料無料となる注文金額（円）."""


def calc_shipping_fee(subtotal: int, is_premium: bool,
                      is_remote: bool) -> int:
    """注文金額と条件から送料を求める.

    Args:
        subtotal: 注文金額（円）。0 以上とする。
        is_premium: プレミアム会員なら True。
        is_remote: 配送先が離島なら True。

    Returns:
        送料（円）。

    Raises:
        ValueError: 注文金額が負の場合。
    """
    if subtotal < 0:
        raise ValueError(f"注文金額が負です: {subtotal}")
    threshold = MEMBER_FREE_THRESHOLD if is_premium else FREE_THRESHOLD
    fee = 0 if subtotal >= threshold else BASE_FEE
    if is_remote:
        fee += REMOTE_SURCHARGE
    return fee
