"""第 5 章「コメントと docstring」の良い例。"""

import math

FREE_SHIPPING_THRESHOLD = 5000
STANDARD_SHIPPING_FEE = 500


def shipping_fee(total: int) -> int:
    """注文金額から送料を求める。

    Args:
        total: 注文金額（円）。

    Returns:
        送料（円）。注文金額が送料無料の基準額以上なら 0 を返す。
    """
    if total >= FREE_SHIPPING_THRESHOLD:
        return 0
    return STANDARD_SHIPPING_FEE


def round_half_up(price: float) -> int:
    """0 以上の金額を小数第 1 位で四捨五入し、整数にする。"""
    # 組み込み関数 round() は偶数丸め（round(2.5) は 2）になるため、
    # 店頭での表示に合わせて四捨五入を自前で行う。
    return math.floor(price + 0.5)


if __name__ == "__main__":
    print(shipping_fee(4000))
    print(shipping_fee(6000))
    print(round(2.5), round_half_up(2.5))
