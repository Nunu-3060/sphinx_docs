"""第 10 章「エラーの扱い方」の悪い例。"""


def parse_age(text: str) -> int:
    try:
        return int(text)
    except Exception:
        return 0


if __name__ == "__main__":
    for text in ["20", "abc", "-5"]:
        print(parse_age(text))
