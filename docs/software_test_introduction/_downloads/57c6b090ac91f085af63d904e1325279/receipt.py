"""カートの内容から領収書の文面を作る."""

from shop.cart import Cart, Item


def format_receipt(cart: Cart, items: list[Item], shipping_fee: int) -> str:
    """items の順に明細を並べた、領収書の文面を返す."""
    lines = ["領収書", ""]
    for item in items:
        quantity = cart.quantity_of(item)
        amount = item.price * quantity
        lines.append(
            f"{item.name} {item.price:,} 円 × {quantity} 個 = {amount:,} 円")
    subtotal = cart.subtotal()
    lines.append("")
    lines.append(f"小計 {subtotal:,} 円")
    lines.append(f"送料 {shipping_fee:,} 円")
    lines.append(f"合計 {subtotal + shipping_fee:,} 円")
    return "\n".join(lines) + "\n"
