"""会員ランクを判定する."""


def member_rank(total_purchase: int, years: int) -> str:
    """累計購入金額と会員歴から会員ランクを判定する.

    Args:
        total_purchase: 累計購入金額（円）。
        years: 会員歴（年）。

    Returns:
        "gold"、"silver"、"bronze" のいずれか。
    """
    if total_purchase >= 100_000 and years >= 3:
        return "gold"
    if total_purchase >= 50_000 or years >= 5:
        return "silver"
    return "bronze"
