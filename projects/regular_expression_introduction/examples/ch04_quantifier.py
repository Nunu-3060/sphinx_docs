"""第 4 章「量指定子」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch04_quantifier.py
"""
import re


def demo_basic() -> None:
    """*, +, ? は直前の要素の繰り返し回数を指定する。"""
    text = "a ab abbb"
    print(re.findall(r"ab*", text))  # -> ['a', 'ab', 'abbb']
    print(re.findall(r"ab+", text))  # -> ['ab', 'abbb']
    print(re.findall(r"ab?", text))  # -> ['a', 'ab', 'ab']


def demo_braces() -> None:
    """{m,n} で回数を数値で指定する。"""
    print(re.findall(r"\d{3}-\d{4}", "〒100-0001 / 1000-001"))  # -> ['100-0001']
    print(re.findall(r"\d{2,3}", "1 12 123 12345"))  # -> ['12', '123', '123', '45']
    print(re.findall(r"\d{2,}", "1 12 123"))  # -> ['12', '123']


def demo_greedy() -> None:
    """量指定子は既定で貪欲であり、できるだけ長く一致しようとする。"""
    html = "<b>bold</b>"
    m = re.search(r"<.+>", html)
    if m:
        print(m.group())  # -> <b>bold</b>
    m = re.search(r"<.+?>", html)
    if m:
        print(m.group())  # -> <b>
    print(re.findall(r"<.+?>", html))  # -> ['<b>', '</b>']
    print(re.findall(r"<[^>]+>", html))  # -> ['<b>', '</b>']


def demo_possessive() -> None:
    """強欲量指定子とアトミックグループはバックトラックしない (Python 3.11 以降)。"""
    print(re.fullmatch(r"\d+0", "1230"))  # -> <re.Match object; span=(0, 4), match='1230'>
    print(re.fullmatch(r"\d++0", "1230"))  # -> None
    print(re.fullmatch(r"(?>\d+)0", "1230"))  # -> None
    print(re.fullmatch(r"[a-z]++\d", "abc1"))  # -> <re.Match object; span=(0, 4), match='abc1'>


def main() -> None:
    """すべてのデモを順に実行する。"""
    for demo in (demo_basic, demo_braces, demo_greedy, demo_possessive):
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
