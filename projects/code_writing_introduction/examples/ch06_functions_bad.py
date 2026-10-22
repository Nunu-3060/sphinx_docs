"""第 6 章「関数を小さく分ける」の悪い例。"""


def process(items: list[tuple[str, int, int]]) -> None:
    total = 0
    lines: list[str] = []
    for item in items:
        if item[1] < 0 or item[2] <= 0:
            print("不正な商品: " + item[0])
            continue
        subtotal = item[1] * item[2]
        total += subtotal
        lines.append(item[0] + " x" + str(item[2]) + " = " + str(subtotal) + "円")
    if total >= 5000:
        discount = total // 10
    else:
        discount = 0
    total -= discount
    for line in lines:
        print(line)
    print("割引: " + str(discount) + "円")
    print("合計: " + str(total) + "円")


if __name__ == "__main__":
    process([("ノート", 150, 10), ("ペン", 120, 30), ("消しゴム", 80, 0)])
