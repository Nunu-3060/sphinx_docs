"""生成された rst ファイルの表記を検査するスクリプト.

source/ の rst ファイルのうち、コードブロックと SQL の実行結果の表を除いた
文章について、次の点を検査します。

* no-space      日本語の文字と英数字の間に半角空白がない
* space-punct   全角の句読点や括弧の前後に不要な空白がある
* plain-form    普通語（である調）の文末がある
* double-space  連続した空白がある

問題が見つかった場合は、その行を表示して終了コード 1 で終了します。

使い方（プロジェクトのルートで実行します）::

    python tools/check_style.py
"""

import re
import sys
from collections.abc import Iterator
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent / "source"

# 日本語の文字（ひらがな、カタカナ、漢字）。中黒「・」（U+30FB）は記号なので除きます。
JAPANESE = r"[ぁ-ヺー-ヿ一-鿿]"
ALNUM = r"[A-Za-z0-9]"
INLINE_MARKUP = re.compile(r"(:[\w-]+:`[^`]+`|``[^`]+``|`[^`]+`_{1,2})")
CODE_DIRECTIVE = re.compile(r"^\s*\.\. (code-block|literalinclude|math)::")
LIST_MARKER = re.compile(r"^\s*(\* - |\* |- |[0-9]+\. )")

CHECKS = {
    "no-space": re.compile(f"{JAPANESE}{ALNUM}|{ALNUM}{JAPANESE}"),
    "space-punct": re.compile(r"(?<=\S) [、。（）「」：]|[、。（「：] (?=\S)"),
    # 「ました。」「でした。」は丁寧語なので、「した。」の前が「ま」「で」の場合は除きます。
    "plain-form": re.compile(
        r"(である|だ|する|(?<![まで])した|ない|できる|なる|いる|れる|ある)。"
    ),
    "double-space": re.compile(r"  \S"),
}


def starts_code_block(line: str) -> bool:
    """コードブロック（ディレクティブまたはリテラルブロック）の開始行かを返します."""
    if CODE_DIRECTIVE.match(line):
        return True
    stripped = line.strip()
    return stripped.endswith("::") and not stripped.startswith("..")


def text_lines(path: Path) -> Iterator[tuple[int, str]]:
    """コードブロックと実行結果の表を除いた行を、行番号とともに返します."""
    code_indent: int | None = None
    in_result = False
    in_result_body = False
    lines = path.read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines, start=1):
        indent = len(line) - len(line.lstrip())
        if code_indent is not None:
            if not line.strip() or indent > code_indent:
                continue
            code_indent = None
        if starts_code_block(line):
            code_indent = indent
            continue
        if ":class: sql-result" in line:
            in_result = True
        if in_result:
            stripped = line.lstrip()
            if not line.strip():
                if in_result_body:
                    in_result = in_result_body = False
                continue
            if stripped.startswith(("*", "-", ":")):
                if stripped.startswith(("*", "-")):
                    in_result_body = True
                continue
            in_result = in_result_body = False
        if line.lstrip().startswith(".."):
            continue
        yield number, line


def check_line(line: str) -> list[str]:
    """1 行を検査し、見つかった問題の種類のリストを返します."""
    text = INLINE_MARKUP.sub("X", line).replace("\\ ", "")
    text = LIST_MARKER.sub("", text)
    problems = [
        name for name, pattern in CHECKS.items()
        if name != "double-space" and pattern.search(text)
    ]
    if CHECKS["double-space"].search(line.strip()):
        problems.append("double-space")
    return problems


def main() -> int:
    """すべての rst ファイルを検査します."""
    count = 0
    for path in sorted(SOURCE_DIR.glob("*.rst")):
        for number, line in text_lines(path):
            problems = check_line(line)
            if problems:
                count += 1
                print(f"{path.name}:{number}: {','.join(problems)}: "
                      f"{line.strip()[:100]}")
    print(f"問題のある行: {count} 行")
    return 1 if count else 0


if __name__ == "__main__":
    sys.exit(main())
