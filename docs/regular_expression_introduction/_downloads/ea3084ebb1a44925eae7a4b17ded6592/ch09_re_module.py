"""第 9 章「Python の re モジュール」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch09_re_module.py
"""
import re


def demo_search_match_fullmatch() -> None:
    """search(), match(), fullmatch() は一致を判定する位置が異なる。"""
    print(re.search(r"\d+", "abc123"))  # -> <re.Match object; span=(3, 6), match='123'>
    print(re.match(r"\d+", "abc123"))  # -> None
    print(re.match(r"\d+", "123abc"))  # -> <re.Match object; span=(0, 3), match='123'>
    print(re.fullmatch(r"\d+", "123abc"))  # -> None
    print(re.fullmatch(r"\d+", "123"))  # -> <re.Match object; span=(0, 3), match='123'>


def demo_findall_finditer() -> None:
    """findall() は文字列のリストを、finditer() は Match のイテレーターを返す。"""
    text = "x=10, y=200"
    print(re.findall(r"\d+", text))  # -> ['10', '200']
    for m in re.finditer(r"\d+", text):
        print(m.group(), m.span())
    # -> 10 (2, 4)
    # -> 200 (8, 11)


def demo_sub() -> None:
    """sub() は一致した部分を置換する。"""
    text = "2026-10-19"
    print(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", text))  # -> 19/10/2026
    print(re.sub(r"(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})", r"\g<y>年\g<m>月\g<d>日", text))  # -> 2026年10月19日
    print(re.sub(r"\d", "#", "a1b22c333", count=3))  # -> a#b##c333
    print(re.subn(r"\d", "#", "a1b22c333"))  # -> ('a#b##c###', 6)


def demo_sub_with_function() -> None:
    """置換文字列の代わりに関数を渡すと、一致ごとに置換結果を計算できる。"""

    def double(m: re.Match[str]) -> str:
        return str(int(m.group()) * 2)

    print(re.sub(r"\d+", double, "a=3, b=50"))  # -> a=6, b=100


def demo_split() -> None:
    """split() はパターンに一致した部分で文字列を分割する。"""
    print(re.split(r"\s*[,;]\s*", "a, b;c ,d"))  # -> ['a', 'b', 'c', 'd']
    print(re.split(r"\s*[,;]\s*", "a, b;c ,d", maxsplit=1))  # -> ['a', 'b;c ,d']
    print(re.split(r"([,;])", "a,b;c"))  # -> ['a', ',', 'b', ';', 'c']


def demo_compile() -> None:
    """compile() でパターンオブジェクトを作り、繰り返し使う。"""
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    print(date_pattern.pattern)  # -> (\d{4})-(\d{2})-(\d{2})
    print(date_pattern.groups)  # -> 3
    for line in ("start: 2026-10-19", "no date", "end: 2026-12-31"):
        m = date_pattern.search(line)
        print(m.group() if m else "(なし)")
    # -> 2026-10-19
    # -> (なし)
    # -> 2026-12-31


def demo_match_object() -> None:
    """Match オブジェクトから一致した情報を取り出す。"""
    m = re.search(r"(?P<key>\w+)=(?P<value>\w+)?", "name=")
    if m:
        print(m.group(), m.start(), m.end(), m.span())  # -> name= 0 5 (0, 5)
        print(m.groups())  # -> ('name', None)
        print(m.groups(default=""))  # -> ('name', '')
        print(m.groupdict())  # -> {'key': 'name', 'value': None}
        print(m[0], m["key"])  # -> name= name


def demo_escape() -> None:
    """利用者が入力した文字列をパターンに埋め込むときは escape() を使う。"""
    keyword = "*重要*"
    text = "これは *重要* な点だ"
    print(re.findall(re.escape(keyword), text))  # -> ['*重要*']
    try:
        re.findall(keyword, text)
    except re.error as e:
        print(e)  # -> nothing to repeat at position 0
    # escape() しないと、エラーにならなくても意図しないパターンになることがある
    print(re.findall("(株)", "(株)山田商店"))  # -> ['株']


def demo_error() -> None:
    """不正なパターンは re.error を送出する。"""
    try:
        re.compile(r"(abc")
    except re.error as e:
        print(e.msg, e.pos)  # -> missing ), unterminated subpattern 0


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_search_match_fullmatch,
        demo_findall_finditer,
        demo_sub,
        demo_sub_with_function,
        demo_split,
        demo_compile,
        demo_match_object,
        demo_escape,
        demo_error,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
