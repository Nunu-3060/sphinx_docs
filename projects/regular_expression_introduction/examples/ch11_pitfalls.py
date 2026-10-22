"""第 11 章「落とし穴と性能」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch11_pitfalls.py
"""
import re
import time
from html.parser import HTMLParser


def time_search(pattern: str, text: str) -> float:
    """re.search() にかかった時間を秒単位で返す。"""
    start = time.perf_counter()
    re.search(pattern, text)
    return time.perf_counter() - start


def demo_catastrophic() -> None:
    """入れ子の量指定子は、一致に失敗するときに指数関数的な時間がかかる。"""
    for n in (16, 18, 20, 22):
        text = "a" * n + "b"
        print(f"n={n}: {time_search(r'(a+)+$', text):.3f} 秒")


def demo_catastrophic_fixed() -> None:
    """量指定子の入れ子をなくすか、バックトラックを禁止すると速くなる。"""
    text = "a" * 22 + "b"
    for pattern in (r"a+$", r"(?>a+)+$", r"(a++)+$"):
        print(f"{pattern}: {time_search(pattern, text):.6f} 秒")


def demo_match_vs_search() -> None:
    """match() は先頭からしか探さない。"""
    print(re.match(r"error", "fatal error"))  # -> None
    print(re.search(r"error", "fatal error"))  # -> <re.Match object; span=(6, 11), match='error'>


def demo_replacement_backslash() -> None:
    """置換文字列の中のバックスラッシュも特別な意味を持つ。"""
    try:
        re.sub(r"/", "\\", "a/b")
    except re.error as e:
        print(e)  # -> bad escape (end of pattern) at position 0
    print(re.sub(r"/", r"\\", "a/b"))  # -> a\b
    print(re.sub(r"/", lambda m: "\\", "a/b"))  # -> a\b


def demo_greedy_dot() -> None:
    """.* は思ったよりも長く一致する。"""
    line = 'name="Alice" city="Tokyo"'
    print(re.findall(r'"(.*)"', line))  # -> ['Alice" city="Tokyo']
    print(re.findall(r'"([^"]*)"', line))  # -> ['Alice', 'Tokyo']


class LinkCollector(HTMLParser):
    """a 要素の href 属性を集める HTML パーサー。"""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value is not None:
                    self.links.append(value)


def demo_html() -> None:
    """HTML は正規表現ではなく HTML パーサーで解析する。"""
    html = """<a href="/a">A</a> <a class="x" href='/b'>B</a> <A HREF="/c">C</A>"""
    print(re.findall(r'<a href="(.*?)">', html))  # -> ['/a']
    parser = LinkCollector()
    parser.feed(html)
    print(parser.links)  # -> ['/a', '/b', '/c']


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_catastrophic,
        demo_catastrophic_fixed,
        demo_match_vs_search,
        demo_replacement_backslash,
        demo_greedy_dot,
        demo_html,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
