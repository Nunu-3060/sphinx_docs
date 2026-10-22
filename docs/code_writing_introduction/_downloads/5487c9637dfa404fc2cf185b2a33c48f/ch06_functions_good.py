"""第 6 章「関数を小さく分ける」の良い例。"""

Item = tuple[str, int, int]  # (商品名, 単価, 個数)

DISCOUNT_THRESHOLD = 5000
DISCOUNT_RATE_PERCENT = 10


def is_valid_item(item: Item) -> bool:
    _, unit_price, quantity = item
    return unit_price >= 0 and quantity > 0


def subtotal_of(item: Item) -> int:
    _, unit_price, quantity = item
    return unit_price * quantity


def calculate_discount(total: int) -> int:
    if total >= DISCOUNT_THRESHOLD:
        return total * DISCOUNT_RATE_PERCENT // 100
    return 0


def format_item_line(item: Item) -> str:
    name, _, quantity = item
    return f"{name} x{quantity} = {subtotal_of(item)}円"


def print_receipt(items: list[Item]) -> None:
    for item in items:
        if not is_valid_item(item):
            print(f"不正な商品: {item[0]}")

    valid_items = [item for item in items if is_valid_item(item)]
    total = sum(subtotal_of(item) for item in valid_items)
    discount = calculate_discount(total)

    for item in valid_items:
        print(format_item_line(item))
    print(f"割引: {discount}円")
    print(f"合計: {total - discount}円")


if __name__ == "__main__":
    print_receipt([("ノート", 150, 10), ("ペン", 120, 30), ("消しゴム", 80, 0)])
