"""循環的複雑度を下げる書き換えの例.

配送料の計算を例に、分岐が入れ子になった実装と、表（辞書）を使って
分岐を減らした実装を比べます。

実行方法::

    python ch03_complexity.py
"""

# ---------------------------------------------------------------------------
# 悪い例: 分岐が入れ子になっている（循環的複雑度 8）
# ---------------------------------------------------------------------------


def bad_shipping_fee(region: str, weight_kg: float, is_member: bool) -> int:
    """配送料を返します（悪い例）."""
    if region == "local":
        if weight_kg <= 5:
            fee = 500
        else:
            fee = 800
    elif region == "remote":
        if weight_kg <= 5:
            fee = 1000
        else:
            fee = 1500
    elif region == "island":
        if weight_kg <= 5:
            fee = 2000
        else:
            fee = 3000
    else:
        raise ValueError(f"unknown region: {region}")
    if is_member:
        fee = fee // 2
    return fee


# ---------------------------------------------------------------------------
# 良い例: 料金表をデータとして分離する（循環的複雑度 4）
# ---------------------------------------------------------------------------

LIGHT_WEIGHT_LIMIT_KG = 5.0

# 地域ごとの（軽量の料金, 重量の料金）
FEE_TABLE: dict[str, tuple[int, int]] = {
    "local": (500, 800),
    "remote": (1000, 1500),
    "island": (2000, 3000),
}


def shipping_fee(region: str, weight_kg: float, is_member: bool) -> int:
    """配送料を返します（良い例）.

    料金の値は FEE_TABLE にまとめたので、地域の追加や料金の改定では
    この関数を変更する必要がありません。
    """
    if region not in FEE_TABLE:
        raise ValueError(f"unknown region: {region}")
    light_fee, heavy_fee = FEE_TABLE[region]
    fee = light_fee if weight_kg <= LIGHT_WEIGHT_LIMIT_KG else heavy_fee
    return fee // 2 if is_member else fee


def main() -> None:
    """2 つの実装が、すべての組み合わせで同じ結果を返すことを確認します."""
    for region in FEE_TABLE:
        for weight in (1.0, 5.0, 10.0):
            for is_member in (False, True):
                expected = bad_shipping_fee(region, weight, is_member)
                actual = shipping_fee(region, weight, is_member)
                assert expected == actual, (region, weight, is_member)
    print("すべての組み合わせで結果が一致しました。")


if __name__ == "__main__":
    main()
