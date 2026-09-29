"""文字列操作の基本的な方法を示すサンプルです。"""


def build_greeting(name: str) -> str:
    """名前を受け取り、f 文字列を使った挨拶文を返します。"""
    return f"こんにちは、{name} さん。"


def main() -> None:
    """文字列メソッドの使用例を表示します。"""
    text: str = "  Python Programming  "

    print("元の文字列:", repr(text))
    print("前後の空白を除去:", repr(text.strip()))
    print("小文字に変換:", text.strip().lower())
    print("大文字に変換:", text.strip().upper())
    print("置換:", text.strip().replace("Python", "PYTHON"))

    words: list[str] = text.strip().split(" ")
    print("分割結果:", words)
    print("結合結果:", "-".join(words))

    print(build_greeting("高橋"))

    sentence: str = "Python は 1991 年に誕生しました。"
    print("先頭 6 文字:", sentence[:6])


if __name__ == "__main__":
    main()
