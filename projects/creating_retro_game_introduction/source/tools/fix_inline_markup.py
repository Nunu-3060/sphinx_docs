"""rst のインラインマークアップと全角の括弧が隣接する箇所に「\\ 」(エスケープした空白) を挿入する。

docutils は、インラインマークアップの終わりの直後に開き括弧が来たり、始まりの直前に閉じ括弧が来たりすると、
マークアップとして認識しない。「\\ 」は HTML では何も表示されないので、見た目を変えずにこの問題を避けられる。
また、見出しの下線が見出しの表示幅より短い場合は、下線を伸ばす。

使い方:
    python fix_inline_markup.py
"""

import re
import unicodedata
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent

OPENING = "（「『【"
CLOSING = "）」』】"
END_MARKUP = re.compile(rf"(``|\*\*|`__|`_|`)(?=[{OPENING}])")
START_MARKUP = re.compile(rf"(?<=[{CLOSING}])(``|:[a-z]+:`)")
UNDERLINE = re.compile(r"^([=\-^~\"'#*+])\1+$")

# 日本語の文字 (ひらがな、カタカナ、漢字、全角記号)
JA = r"[　-ヿ一-鿿＀-￯]"
# 表示が日本語で始まる、または終わるマークアップと日本語の間の空白は、「\ 」に置き換える
JA_SPACING = [
    # 強調の終わり (中身が日本語で終わる) の後の空白
    (re.compile(rf"(\*\*[^*\s][^*]*?{JA}\*\*) (?={JA})"), r"\1\\ "),
    # 強調の始まり (中身が日本語で始まる) の前の空白
    (re.compile(rf"(?<={JA}) (\*\*{JA})"), r"\\ \1"),
    # 図表番号の参照 (「図 3.1」のように日本語で始まる) の前の空白
    (re.compile(rf"(?<={JA}) (:numref:`)"), r"\\ \1"),
    # 章や節の参照 (表示が日本語のタイトル) の前後の空白
    (re.compile(rf"(?<={JA}) (:(?:doc|ref):`[^`<]+`)"), r"\\ \1"),
    (re.compile(rf"(:(?:doc|ref):`[^`<]+`) (?={JA})"), r"\1\\ "),
]


def display_width(s: str) -> int:
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def insert_before_opening(m: re.Match[str], line: str) -> str:
    """開きのマークアップ (その位置より前にある `` の数が偶数) の場合だけ「\\ 」を挿入する。"""
    if m.group(1) == "``" and line[: m.start()].count("``") % 2 == 1:
        return m.group(1)
    return "\\ " + m.group(1)


def fix(text: str) -> str:
    lines = text.split("\n")
    in_code = False
    for i, line in enumerate(lines):
        if line.startswith(".. ") and ("code-block" in line or "graphviz" in line or line.strip() == ".. math::"):
            in_code = True
            continue
        if in_code:
            if line and not line.startswith(" "):
                in_code = False
            else:
                continue
        if i > 0 and UNDERLINE.match(line) and lines[i - 1].strip() and not UNDERLINE.match(lines[i - 1]):
            width = display_width(lines[i - 1])
            if len(line) < width:
                lines[i] = line[0] * width
            continue
        line = END_MARKUP.sub(lambda m: m.group(1) + "\\ ", line)
        current = line
        line = START_MARKUP.sub(lambda m: insert_before_opening(m, current), line)
        for pattern, repl in JA_SPACING:
            line = pattern.sub(repl, line)
        lines[i] = line
    return "\n".join(lines)


def main() -> None:
    for path in sorted(SOURCE.glob("*.rst")):
        text = path.read_text(encoding="utf-8")
        fixed = fix(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            print(f"fixed: {path.name}")


if __name__ == "__main__":
    main()
