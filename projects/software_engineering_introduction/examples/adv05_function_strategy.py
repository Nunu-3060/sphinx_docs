"""発展課題 5-A の解答例: 関数による Strategy パターン（第 5 章）.

Python では関数を値として扱えるため、戦略をクラスではなく関数で表せる。
``ch05_strategy.py`` のクラス版と同じ結果になる。
戦略は名前を付けて辞書に登録し、設定ファイルなどの文字列から選べるようにした。
"""

from collections.abc import Callable

ShippingFee = Callable[[float], int]
"""重さ（kg）を受け取り、送料（円）を返す関数の型."""


def flat_rate(amount: int) -> ShippingFee:
    """重さに関係なく一律の送料を返す関数を作る."""

    def fee(weight_kg: float) -> int:
        return amount

    return fee


def weight_based(base: int, per_kg: int) -> ShippingFee:
    """基本料金に 1 kg ごとの料金を加算する関数を作る."""

    def fee(weight_kg: float) -> int:
        return base + round(per_kg * weight_kg)

    return fee


STRATEGIES: dict[str, ShippingFee] = {
    "flat": flat_rate(500),
    "weight": weight_based(300, 100),
}


def total(price: int, weight_kg: float, fee: ShippingFee) -> int:
    """商品価格と送料の合計を返す."""
    return price + fee(weight_kg)


if __name__ == "__main__":
    for name, strategy in STRATEGIES.items():
        print(f"{name}: {total(price=3000, weight_kg=2.5, fee=strategy)} 円")
