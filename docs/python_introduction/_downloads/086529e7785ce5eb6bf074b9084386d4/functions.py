"""関数の定義と引数の使い方を示すサンプルです。"""


def celsius_to_fahrenheit(celsius: float) -> float:
    """摂氏温度を華氏温度に変換して返します。"""
    return celsius * 9 / 5 + 32


def introduce(name: str, age: int = 20) -> str:
    """名前と年齢を受け取り、自己紹介の文字列を返します。"""
    return "私は " + name + " です。年齢は " + str(age) + " 歳です。"


def greet(name: str, nickname: str | None = None) -> str:
    """名前とニックネームを受け取り、挨拶の文字列を返します。"""
    if nickname is None:
        return name + " です。"
    return name + "（" + nickname + "）です。"


def total(*numbers: int) -> int:
    """可変長引数として受け取った数値の合計を返します。"""
    return sum(numbers)


def show_profile(**info: str) -> dict[str, str]:
    """可変長のキーワード引数として受け取った情報を辞書のまま返します。"""
    return info


def main() -> None:
    """関数の呼び出し例を表示します。"""
    print("摂氏 25 度は華氏", celsius_to_fahrenheit(25.0), "度です。")
    print(introduce("鈴木"))
    print(introduce("田中", 35))
    print(greet("田中"))
    print(greet("田中", "たなか"))
    print("合計:", total(1, 2, 3, 4, 5))
    print(show_profile(name="田中", city="東京"))


if __name__ == "__main__":
    main()
