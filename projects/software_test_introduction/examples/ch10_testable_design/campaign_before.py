"""テストしにくい書き方の例（改善前）."""

import random
from datetime import date


def announce_discount() -> None:
    """本日の割引率と、抽選で決まるクーポンコードを表示する."""
    today = date.today()
    if today.month == 12 and today.day >= 20:
        rate = 0.2
    else:
        rate = 0.0
    code = "".join(random.choice("ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(6))
    print(f"本日の割引率: {rate:.0%}")
    print(f"クーポンコード: {code}")
