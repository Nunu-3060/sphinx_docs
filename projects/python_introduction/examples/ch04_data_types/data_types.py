"""データ型と演算子の基本的な使い方を示すサンプルです。"""


def calculate_circle_area(radius: float) -> float:
    """円の半径から面積を計算して返します。"""
    pi: float = 3.14159
    return pi * radius ** 2


def main() -> None:
    """数値演算と文字列演算の結果を表示します。"""
    a: int = 7
    b: int = 3

    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * b =", a * b)
    print("a / b =", a / b)
    print("a // b =", a // b)
    print("a % b =", a % b)
    print("a ** b =", a ** b)

    area: float = calculate_circle_area(2.0)
    print("半径 2.0 の円の面積:", area)

    first_name: str = "山田"
    last_name: str = "花子"
    full_name: str = first_name + last_name
    print("氏名:", full_name)

    nickname: str | None = None
    print("ニックネーム:", nickname)
    nickname = "たなか"
    print("ニックネーム:", nickname)


if __name__ == "__main__":
    main()
