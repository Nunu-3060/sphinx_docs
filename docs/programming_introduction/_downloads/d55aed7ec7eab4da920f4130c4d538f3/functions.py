"""関数の定義と呼び出し、副作用の例。"""


def rectangle_area(width: float, height: float) -> float:
    """長方形の面積を返す（副作用のない関数）。"""
    return width * height


def add_item(items: list[str], item: str) -> None:
    """リストに要素を追加する（引数を書き換える副作用のある関数）。"""
    items.append(item)


def greet(name: str, greeting: str = "こんにちは") -> str:
    """挨拶の文字列を返す（greeting には既定値がある）。"""
    return f"{greeting}、{name}さん"


def main() -> None:
    """関数を呼び出し、戻り値と副作用を確かめる。"""
    print(rectangle_area(3.0, 4.0))  # 12.0

    fruits = ["りんご"]
    add_item(fruits, "みかん")
    print(fruits)  # ['りんご', 'みかん']（呼び出し元のリストが変わる）

    print(greet("佐藤"))  # こんにちは、佐藤さん
    print(greet("佐藤", "おはよう"))  # おはよう、佐藤さん


if __name__ == "__main__":
    main()
