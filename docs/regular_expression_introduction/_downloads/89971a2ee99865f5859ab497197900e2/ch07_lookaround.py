"""第 7 章「先読みと後読み」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch07_lookaround.py
"""
import re


def demo_lookahead() -> None:
    """(?=...) と (?!...) は直後に続く文字列を条件にする。"""
    text = "りんご 120円、みかん 80個、ぶどう 300円"
    print(re.findall(r"\d+(?=円)", text))  # -> ['120', '300']
    print(re.findall(r"\d+(?![\d円])", text))  # -> ['80']


def demo_lookbehind() -> None:
    """(?<=...) と (?<!...) は直前にある文字列を条件にする。"""
    text = "price: $30, qty: 5"
    print(re.findall(r"(?<=\$)\d+", text))  # -> ['30']
    print(re.findall(r"(?<![\d$])\d+", text))  # -> ['5']


def demo_zero_width() -> None:
    """先読みと後読みは文字を消費しない。"""
    m = re.search(r"\d+(?=円)", "合計 500円")
    if m:
        print(m.group(), m.span())  # -> 500 (3, 6)
    m = re.search(r"\d+円", "合計 500円")
    if m:
        print(m.group(), m.span())  # -> 500円 (3, 7)


def demo_password() -> None:
    """複数の先読みを並べると「すべての条件を満たす」を表せる。"""
    pattern = re.compile(r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}")
    for password in ("password", "Passw0rd", "PASSW0RD", "Pa55"):
        print(password, bool(pattern.fullmatch(password)))
    # -> password False
    # -> Passw0rd True
    # -> PASSW0RD False
    # -> Pa55 False


def demo_thousands_separator() -> None:
    """先読みと後読みで「位置」を指定して 3 桁ごとにカンマを挿入する。"""
    pattern = r"(?<=\d)(?=(?:\d{3})+(?!\d))"
    print(re.sub(pattern, ",", "1234567"))  # -> 1,234,567
    print(re.sub(pattern, ",", "残高 1000000 円"))  # -> 残高 1,000,000 円


def demo_fixed_width() -> None:
    """Python の後読みには固定長のパターンしか書けない。"""
    try:
        re.compile(r"(?<=a|bc)x")
    except re.error as e:
        print(e)  # -> look-behind requires fixed-width pattern
    print(re.findall(r"(?:(?<=a)|(?<=bc))x", "ax bcx dx"))  # -> ['x', 'x']


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_lookahead,
        demo_lookbehind,
        demo_zero_width,
        demo_password,
        demo_thousands_separator,
        demo_fixed_width,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
