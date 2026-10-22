"""第 6 章「グループと選択」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch06_group.py
"""
import re


def demo_alternation() -> None:
    """| はいずれかのパターンに一致する。"""
    print(re.findall(r"cat|dog", "cat, dog, bird"))  # -> ['cat', 'dog']
    # | は優先順位が最も低いので、^ と $ がそれぞれ片側にしか掛からない
    print(re.search(r"^cat|dog$", "catfish"))  # -> <re.Match object; span=(0, 3), match='cat'>
    print(re.search(r"^(?:cat|dog)$", "catfish"))  # -> None


def demo_alternation_order() -> None:
    """選択肢は左から順に試され、最初に一致したものが採用される。"""
    print(re.findall(r"Java|JavaScript", "JavaScript"))  # -> ['Java']
    print(re.findall(r"JavaScript|Java", "JavaScript"))  # -> ['JavaScript']


def demo_group_quantifier() -> None:
    """グループにまとめると、量指定子を複数の文字に掛けられる。"""
    print(re.fullmatch(r"(?:ab)+", "ababab"))  # -> <re.Match object; span=(0, 6), match='ababab'>
    print(re.fullmatch(r"ab+", "ababab"))  # -> None


def demo_capture() -> None:
    """(...) で囲んだ部分は後から取り出せる。"""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "日付: 2026-10-19")
    if m:
        print(m.group(0))  # -> 2026-10-19
        print(m.group(1), m.group(2), m.group(3))  # -> 2026 10 19
        print(m.groups())  # -> ('2026', '10', '19')


def demo_named_group() -> None:
    """(?P<name>...) でグループに名前を付ける。"""
    m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", "日付: 2026-10-19")
    if m:
        print(m.group("year"))  # -> 2026
        print(m["month"])  # -> 10
        print(m.groupdict())  # -> {'year': '2026', 'month': '10', 'day': '19'}


def demo_backreference() -> None:
    r"""\1 や (?P=name) で、グループが一致した文字列そのものを参照する。"""
    m = re.search(r"\b(\w+) \1\b", "this is is a pen")
    if m:
        print(m.group())  # -> is is
    html = "<b>bold</b> <i>italic</b>"
    print(re.findall(r"<(?P<tag>\w+)>.*?</(?P=tag)>", html))  # -> ['b']


def demo_findall_with_groups() -> None:
    """findall() の戻り値はグループの数によって変わる。"""
    text = "2026-10-19, 2027-01-01"
    print(re.findall(r"\d{4}-\d{2}-\d{2}", text))  # -> ['2026-10-19', '2027-01-01']
    print(re.findall(r"(\d{4})-\d{2}-\d{2}", text))  # -> ['2026', '2027']
    print(re.findall(r"(\d{4})-(\d{2})-\d{2}", text))  # -> [('2026', '10'), ('2027', '01')]


def demo_repeated_group() -> None:
    """繰り返したグループには最後に一致した文字列だけが残る。"""
    m = re.fullmatch(r"(\d)+", "123")
    if m:
        print(m.group(1))  # -> 3
    m = re.fullmatch(r"(\d+)", "123")
    if m:
        print(m.group(1))  # -> 123


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_alternation,
        demo_alternation_order,
        demo_group_quantifier,
        demo_capture,
        demo_named_group,
        demo_backreference,
        demo_findall_with_groups,
        demo_repeated_group,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
