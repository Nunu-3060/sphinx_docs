"""第 8 章「フラグ」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch08_flags.py
"""
import re


def demo_ignorecase() -> None:
    """re.IGNORECASE (re.I) は大文字と小文字を区別しない。"""
    text = "Python PYTHON python"
    print(re.findall(r"python", text))  # -> ['python']
    print(re.findall(r"python", text, flags=re.IGNORECASE))  # -> ['Python', 'PYTHON', 'python']


def demo_dotall() -> None:
    """re.DOTALL (re.S) を指定すると . が改行にも一致する。"""
    text = "<p>line1\nline2</p>"
    print(re.search(r"<p>.*</p>", text))  # -> None
    m = re.search(r"<p>.*</p>", text, flags=re.DOTALL)
    if m:
        print(repr(m.group()))  # -> '<p>line1\nline2</p>'


def demo_combine() -> None:
    """複数のフラグは | で組み合わせる。"""
    text = "Error: disk full\nwarning: low memory\nERROR: timeout"
    print(re.findall(r"^error: (.*)$", text, flags=re.IGNORECASE | re.MULTILINE))  # -> ['disk full', 'timeout']


def demo_inline_flags() -> None:
    """パターンの中にフラグを書くこともできる。"""
    print(re.findall(r"(?i)python", "Python PYTHON"))  # -> ['Python', 'PYTHON']
    print(re.findall(r"(?i:py)thon", "Python PYthon PYTHON"))  # -> ['Python', 'PYthon']
    try:
        re.compile(r"py(?i)thon")
    except re.error as e:
        print(e)  # -> global flags not at the start of the expression at position 2


def demo_verbose() -> None:
    """re.VERBOSE (re.X) を指定すると空白とコメントを書ける。"""
    phone = re.compile(
        r"""
        (?P<area>0\d{1,4})   # 市外局番
        -
        (?P<local>\d{1,4})   # 市内局番
        -
        (?P<number>\d{4})    # 加入者番号
        """,
        flags=re.VERBOSE,
    )
    m = phone.fullmatch("03-1234-5678")
    if m:
        print(m.groupdict())  # -> {'area': '03', 'local': '1234', 'number': '5678'}


def demo_ascii() -> None:
    r"""re.ASCII (re.A) を指定すると \d, \w, \s, \b が ASCII 文字だけを対象にする。"""
    text = "abc 東京 １２３"
    print(re.findall(r"\w+", text))  # -> ['abc', '東京', '１２３']
    print(re.findall(r"\w+", text, flags=re.ASCII))  # -> ['abc']


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (demo_ignorecase, demo_dotall, demo_combine, demo_inline_flags, demo_verbose, demo_ascii)
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
