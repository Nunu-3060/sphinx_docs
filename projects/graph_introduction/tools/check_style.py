"""rst ファイルの表記を検査するスクリプト.

source/ の rst ファイルのうち、コードブロックやディレクティブを除いた文章に
ついて、次の点を検査する。

* no-space      日本語の文字と英数字の間に半角空白がない
* space-punct   全角の句読点や括弧の前後に不要な半角空白がある
* polite-form   丁寧語（です・ます調）の文末がある（本書は普通語で統一する）
* double-space  連続した半角空白がある

問題が見つかった場合は、その行を表示して終了コード 1 で終了する。

使い方（プロジェクトのルートで実行する）::

    python tools/check_style.py
"""

import re
import sys
from collections.abc import Iterator
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent / "source"

# 日本語の文字（ひらがな、カタカナ、漢字）
JAPANESE = r"[ぁ-ヺー-ヿ一-鿿]"
ALNUM = r"[A-Za-z0-9]"
# 表示が日本語になるロール（用語、文書へのリンク）は日本語の仮の文字に、
# 図の番号は「図 1」に、それ以外のインラインのマークアップは X に置き換える
JAPANESE_ROLE = re.compile(r":(term|doc):`[^`]+`")
NUMREF_ROLE = re.compile(r":numref:`[^`]+`")
OTHER_MARKUP = re.compile(
    r"(:[\w-]+:`[^`]+`|``[^`]+``|\[[A-Za-z0-9]+\]_|`[^`]+`_{1,2})")
CODE_DIRECTIVE = re.compile(
    r"^\s*\.\. (code-block|literalinclude|math|graphviz)::")
LIST_MARKER = re.compile(r"^\s*(\* - |\* |- |[0-9]+\. |#\. )")

CHECKS = {
    "no-space": re.compile(f"{JAPANESE}{ALNUM}|{ALNUM}{JAPANESE}"),
    "space-punct": re.compile(r"(?<=\S) [、。（）「」：]|[、。（）「」：] (?=\S)"),
    "polite-form": re.compile(r"(です|ます|でした|ました|ません)[。）]"),
}


def starts_code_block(line: str) -> bool:
    """コードブロック（ディレクティブまたはリテラルブロック）の開始行かを返す."""
    if CODE_DIRECTIVE.match(line):
        return True
    stripped = line.strip()
    return stripped.endswith("::") and not stripped.startswith("..")


def text_lines(path: Path) -> Iterator[tuple[int, str]]:
    """コードブロックとディレクティブの行を除いた行を、行番号とともに返す."""
    code_indent: int | None = None
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
        stripped = line.lstrip()
        if stripped.startswith("..") and not stripped.startswith(".. ["):
            continue
        if stripped.startswith(":") and not stripped.startswith(":term:") \
                and not stripped.startswith(":doc:") \
                and not stripped.startswith(":numref:") \
                and not stripped.startswith(":math:"):
            continue  # ディレクティブのオプション
        yield number, line


def normalize(line: str) -> str:
    """インラインのマークアップを置き換え、検査用の文字列にする."""
    text = JAPANESE_ROLE.sub("語", line)
    text = NUMREF_ROLE.sub("図 1", text)
    text = OTHER_MARKUP.sub("X", text)
    text = text.replace("\\ ", "").replace("**", "")
    return LIST_MARKER.sub("", text).strip()


def check_line(line: str) -> list[str]:
    """1 行を検査し、見つかった問題の種類のリストを返す."""
    text = normalize(line)
    problems = [name for name, pattern in CHECKS.items()
                if pattern.search(text)]
    if re.search(r"\S  +\S", line.strip()):
        problems.append("double-space")
    return problems


def main() -> int:
    """すべての rst ファイルを検査する."""
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
