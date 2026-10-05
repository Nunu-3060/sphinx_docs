"""代表的なデータ構造（リスト・タプル・辞書）の例。"""


def main() -> None:
    """各データ構造を作成し、基本的な操作を行う。"""
    # リスト：順序があり、後から変更できる
    scores: list[int] = [72, 85, 90]
    scores.append(64)
    print(scores[0], len(scores))  # 72 4

    # タプル：順序があり、作成後は変更できない
    point: tuple[int, int] = (3, 4)
    x, y = point
    print(x, y)  # 3 4

    # 辞書：キーから値を引く
    prices: dict[str, int] = {"りんご": 150, "みかん": 80}
    prices["ぶどう"] = 400
    print(prices["みかん"])  # 80
    for name, price in prices.items():
        print(f"{name}: {price} 円")


if __name__ == "__main__":
    main()
