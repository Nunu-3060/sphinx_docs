"""変数の宣言と print 関数の使い方を示すサンプルです。"""


def main() -> None:
    """変数を定義し、その内容を表示します。"""
    name: str = "太郎"
    age: int = 20
    height: float = 170.5
    is_student: bool = True

    print("名前:", name)
    print("年齢:", age)
    print("身長:", height)
    print("学生かどうか:", is_student)


if __name__ == "__main__":
    main()
