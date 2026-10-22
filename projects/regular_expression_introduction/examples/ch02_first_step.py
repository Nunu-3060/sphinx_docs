"""第 2 章「最初の一歩」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch02_first_step.py
"""
import re


def demo_search() -> None:
    """re.search() で文字列中からパターンを探す。"""
    text = "I have a cat and a dog."
    m = re.search(r"cat", text)
    print(m)  # -> <re.Match object; span=(9, 12), match='cat'>
    if m:
        print(m.group())  # -> cat
        print(m.start(), m.end())  # -> 9 12
    print(re.search(r"bird", text))  # -> None


def demo_case_sensitive() -> None:
    """既定では大文字と小文字を区別する。"""
    print(re.search(r"cat", "Cat"))  # -> None
    print(re.search(r"cat", "concatenate"))  # -> <re.Match object; span=(3, 6), match='cat'>


def demo_metachar() -> None:
    """メタ文字はエスケープしないとリテラルとして扱われない。"""
    text = "1+1=2"
    print(re.search(r"1+1", text))  # -> None
    print(re.search(r"1\+1", text))  # -> <re.Match object; span=(0, 3), match='1+1'>
    print(re.escape("1+1=2?"))  # -> 1\+1=2\?


def demo_raw_string() -> None:
    """パターンは raw 文字列で書く。"""
    print(len("\n"), len(r"\n"))  # -> 1 2
    # 通常の文字列では "\b" がバックスペース文字 (U+0008) になってしまう
    print(re.search("\bcat\b", "a cat"))  # -> None
    print(re.search(r"\bcat\b", "a cat"))  # -> <re.Match object; span=(2, 5), match='cat'>


def main() -> None:
    """すべてのデモを順に実行する。"""
    for demo in (demo_search, demo_case_sensitive, demo_metachar, demo_raw_string):
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
