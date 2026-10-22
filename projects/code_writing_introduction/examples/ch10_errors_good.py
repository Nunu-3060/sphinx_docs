"""第 10 章「エラーの扱い方」の良い例。"""

MIN_AGE = 0
MAX_AGE = 150


def parse_age(text: str) -> int:
    """文字列を年齢に変換する。

    Args:
        text: 年齢を表す文字列。

    Returns:
        年齢。

    Raises:
        ValueError: 整数として解釈できない場合、または範囲外の場合。
    """
    try:
        age = int(text)
    except ValueError as error:
        raise ValueError(f"年齢は整数で入力してください: {text!r}") from error
    if not MIN_AGE <= age <= MAX_AGE:
        raise ValueError(f"年齢は {MIN_AGE} 以上 {MAX_AGE} 以下で入力してください: {age}")
    return age


if __name__ == "__main__":
    for text in ["20", "abc", "-5"]:
        try:
            print(parse_age(text))
        except ValueError as error:
            print(f"エラー: {error}")
