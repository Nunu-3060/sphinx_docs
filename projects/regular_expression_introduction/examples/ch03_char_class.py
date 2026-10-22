"""第 3 章「文字クラス」のサンプルコード。

各 demo_* 関数は本文から引用している。
行末の「# ->」コメントは、その行で表示される内容を示す。

実行方法::

    python ch03_char_class.py
"""
import re


def demo_char_set() -> None:
    """[...] は列挙した文字のどれか 1 文字に一致する。"""
    print(re.findall(r"gr[ae]y", "gray grey groy"))  # -> ['gray', 'grey']
    print(re.findall(r"[aeiou]", "regex"))  # -> ['e', 'e']


def demo_range() -> None:
    """ハイフンで文字の範囲を指定する。"""
    print(re.findall(r"[0-9]", "ver 3.11"))  # -> ['3', '1', '1']
    print(re.findall(r"[A-Fa-f0-9]", "#1aG"))  # -> ['1', 'a']


def demo_negation() -> None:
    """先頭の ^ は「列挙した文字以外」を表す。"""
    print(re.findall(r"[^0-9]", "a1b2"))  # -> ['a', 'b']
    print(re.findall(r"[^ ]", "a b"))  # -> ['a', 'b']


def demo_metachar_in_class() -> None:
    """文字クラスの中では多くのメタ文字がただの文字になる。"""
    print(re.findall(r"[.+*]", "1.5 + 2*3"))  # -> ['.', '+', '*']
    print(re.findall(r"[a-]", "a-b"))  # -> ['a', '-']
    print(re.findall(r"[\]\\]", r"[a]\b"))  # -> [']', '\\']


def demo_dot() -> None:
    """. は改行以外の任意の 1 文字に一致する。"""
    print(re.findall(r"c.t", "cat cut c t c\nt"))  # -> ['cat', 'cut', 'c t']


def demo_shorthand() -> None:
    r"""\d, \w, \s とその否定形。"""
    text = "ID: A-12_x"
    print(re.findall(r"\d", text))  # -> ['1', '2']
    print(re.findall(r"\w", text))  # -> ['I', 'D', 'A', '1', '2', '_', 'x']
    print(re.findall(r"\s", text))  # -> [' ']
    print(re.findall(r"\W", text))  # -> [':', ' ', '-']


def demo_unicode() -> None:
    r"""str のパターンでは \d や \w が Unicode 文字にも一致する。"""
    text = "価格は１２３円"
    print(re.findall(r"\d", text))  # -> ['１', '２', '３']
    print(re.findall(r"[0-9]", text))  # -> []
    print(re.findall(r"\d", text, flags=re.ASCII))  # -> []
    print(re.findall(r"\w", "東京a"))  # -> ['東', '京', 'a']


def main() -> None:
    """すべてのデモを順に実行する。"""
    demos = (
        demo_char_set,
        demo_range,
        demo_negation,
        demo_metachar_in_class,
        demo_dot,
        demo_shorthand,
        demo_unicode,
    )
    for demo in demos:
        print(f"=== {demo.__name__} ===")
        demo()


if __name__ == "__main__":
    main()
