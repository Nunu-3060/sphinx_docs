"""第 5 章「アンカーと境界」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch05_anchor.py
"""
import re


def demo_caret_dollar() -> None:
    """^ は文字列の先頭、$ は文字列の末尾に一致する。"""
    print(re.findall(r"^\d+", "123abc456"))  # -> ['123']
    print(re.findall(r"\d+$", "123abc456"))  # -> ['456']
    print(re.search(r"^\d+$", "12345"))  # -> <re.Match object; span=(0, 5), match='12345'>
    print(re.search(r"^\d+$", "123a5"))  # -> None


def demo_multiline() -> None:
    """re.MULTILINE を指定すると ^ と $ が各行の先頭と末尾にも一致する。"""
    text = "apple\nbanana\ncherry"
    print(re.findall(r"^\w+$", text))  # -> []
    print(re.findall(r"^\w+$", text, flags=re.MULTILINE))  # -> ['apple', 'banana', 'cherry']
    print(re.findall(r"\A\w+", text, flags=re.MULTILINE))  # -> ['apple']


def demo_trailing_newline() -> None:
    r"""$ は末尾の改行の直前にも一致するが、\Z は一致しない。"""
    print(re.search(r"^\d+$", "123\n"))  # -> <re.Match object; span=(0, 3), match='123'>
    print(re.search(r"\A\d+\Z", "123\n"))  # -> None
    print(re.fullmatch(r"\d+", "123\n"))  # -> None


def demo_word_boundary() -> None:
    r"""\b は単語の境界に、\B は単語の境界以外に一致する。"""
    text = "cat concat cats cat."
    print(re.findall(r"\bcat\b", text))  # -> ['cat', 'cat']
    print([m.start() for m in re.finditer(r"\Bcat", text)])  # -> [7]
    print(re.findall(r"\bcat\b", "ねこcat"))  # -> []
    print(re.findall(r"\bcat\b", "ねこcat", flags=re.ASCII))  # -> ['cat']


def main() -> None:
    """すべてのデモを順に実行する。"""
    for demo in (demo_caret_dollar, demo_multiline, demo_trailing_newline, demo_word_boundary):
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
