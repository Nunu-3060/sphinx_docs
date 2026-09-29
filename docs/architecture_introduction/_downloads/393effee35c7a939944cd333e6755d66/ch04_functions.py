"""関数の設計の例.

次の 3 つの書き換えを示します。

1. 引数を書き換える関数を、新しい値を返す関数にする
2. 計算と入出力が混ざった関数を、純粋な計算と入出力に分ける
3. 真偽値の引数で動作を切り替える関数を、2 つの関数に分ける

実行方法::

    python ch04_functions.py
"""

from dataclasses import dataclass, replace

# ---------------------------------------------------------------------------
# 1. 引数を書き換えない
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Item:
    """商品を表します."""

    name: str
    price: int


def bad_apply_discount(items: list[dict[str, int]], rate: float) -> None:
    """商品の価格を割り引きます（悪い例: 引数のリストを書き換える）."""
    for item in items:
        item["price"] = int(item["price"] * (1 - rate))


def apply_discount(items: list[Item], rate: float) -> list[Item]:
    """割り引いた価格の商品のリストを新しく作って返します（良い例）."""
    if not 0 <= rate < 1:
        raise ValueError(f"rate must be in [0, 1): {rate}")
    return [replace(item, price=int(item.price * (1 - rate)))
            for item in items]


# ---------------------------------------------------------------------------
# 2. 計算と入出力を分ける
# ---------------------------------------------------------------------------


def bad_print_average(scores: list[int]) -> None:
    """平均点を計算して表示します（悪い例: 計算と表示が一体）."""
    total = 0
    for score in scores:
        total += score
    print(f"平均点: {total / len(scores):.1f}")


def average(scores: list[int]) -> float:
    """平均点を返します（良い例: 入出力を持たない純粋な関数）."""
    if not scores:
        raise ValueError("scores must not be empty")
    return sum(scores) / len(scores)


def format_average(value: float) -> str:
    """平均点を表示用の文字列にします."""
    return f"平均点: {value:.1f}"


# ---------------------------------------------------------------------------
# 3. 真偽値の引数（フラグ引数）で動作を切り替えない
# ---------------------------------------------------------------------------


def bad_format_name(first: str, last: str, western: bool) -> str:
    """氏名を整形します（悪い例: 呼び出し側から意味が読み取れない）."""
    if western:
        return f"{first} {last}"
    return f"{last} {first}"


def format_name_western(first: str, last: str) -> str:
    """名、姓の順に並べた氏名を返します（良い例）."""
    return f"{first} {last}"


def format_name_japanese(first: str, last: str) -> str:
    """姓、名の順に並べた氏名を返します（良い例）."""
    return f"{last} {first}"


def main() -> None:
    """それぞれの悪い例と良い例を実行します."""
    raw = [{"price": 1000}, {"price": 2000}]
    bad_apply_discount(raw, 0.1)
    print("悪い例（元のリストが変わる）:", raw)

    items = [Item("ノート", 1000), Item("ペン", 2000)]
    discounted = apply_discount(items, 0.1)
    print("良い例（元のリスト）:", items)
    print("良い例（新しいリスト）:", discounted)

    bad_print_average([70, 80, 95])
    print(format_average(average([70, 80, 95])))

    print(bad_format_name("Taro", "Yamada", True))  # True の意味が分からない
    print(format_name_western("Taro", "Yamada"))
    print(format_name_japanese("太郎", "山田"))


if __name__ == "__main__":
    main()
