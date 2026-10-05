"""例外によるエラー処理の例。"""


def parse_age(text: str) -> int:
    """文字列を年齢として解釈する。不正な値なら ValueError を送出する。"""
    age = int(text)  # 数字でなければ int() が ValueError を送出する
    if age < 0:
        raise ValueError(f"年齢は 0 以上でなければならない: {age}")
    return age


def main() -> None:
    """正しい入力と誤った入力を与え、例外を捕捉する。"""
    for text in ["30", "abc", "-5"]:
        try:
            age = parse_age(text)
        except ValueError as error:
            print(f"入力 {text!r} は不正: {error}")
        else:
            print(f"入力 {text!r} は {age} 歳")


if __name__ == "__main__":
    main()
