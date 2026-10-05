"""変数と型、式と演算子の例。"""


def main() -> None:
    """代表的な型の値を変数に代入し、演算の結果を表示する。"""
    count: int = 3
    price: float = 120.5
    name: str = "りんご"
    in_stock: bool = True

    total = count * price
    print(f"{name}を {count} 個買うと {total} 円")  # りんごを 3 個買うと 361.5 円
    print(type(count), type(price), type(name), type(in_stock))

    print(7 / 2)  # 3.5（除算の結果は float になる）
    print(7 // 2)  # 3（切り捨て除算）
    print(7 % 2)  # 1（剰余）
    print(2 ** 10)  # 1024（べき乗）
    print(count > 2 and in_stock)  # True（比較演算子と論理演算子）


if __name__ == "__main__":
    main()
