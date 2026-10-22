"""第 5 章「コメントと docstring」の悪い例。"""


def shipping_fee(total: int) -> int:
    # total が 3000 以上なら 0 を返す
    if total >= 5000:
        return 0
    # 500 を返す
    return 500


if __name__ == "__main__":
    print(shipping_fee(4000))
    print(shipping_fee(6000))
