"""日本語の技術文書を対象とした簡易文章チェッカー。

次の 4 種類の問題を検出し、「ファイル名:行番号:列番号: [規則名] メッセージ」の形式で出力する。

* long-sentence: 一文（句点「。」で区切った範囲）が指定した文字数を超えている。
* spacing: 日本語の文字と英数字の間に半角空白がない。
* variant: 本書の表記規則と異なる表記（表記ゆれ）がある。
* vague: 曖昧な表現がある。

Markdown のコードブロック（``` で囲まれた範囲）とインラインコード（` で囲まれた範囲）は検査しない。
一文の長さは行単位で数えるため、一文を複数の行に分けて書いている文書では正しく数えられない。

使い方:
    python check_style.py 文書.md [文書.md ...] [--max-length 文字数]

問題が見つかった場合は終了コード 1 を、ファイルを読めなかった場合は終了コード 2 を返す。
"""

import argparse
import re
import sys
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MAX_LENGTH = 80

# 日本語の文字（ひらがな、カタカナ、長音記号、漢字、「々」）と英数字
JAPANESE = r"[ぁ-ゖァ-ヺー一-鿿々]"
ALNUM = r"[A-Za-z0-9]"

# 日本語の直後の英数字、または英数字の直後の日本語に一致する
MISSING_SPACE = re.compile(f"(?<={JAPANESE}){ALNUM}|(?<={ALNUM}){JAPANESE}")

# インラインコード（`code` や ``code``）
INLINE_CODE = re.compile(r"`+[^`]*`+")

# (検出する表記, 推奨する表記)
VARIANT_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"サーバ(?!ー)"), "サーバー"),
    (re.compile(r"ユーザ(?![ービ])"), "ユーザー"),
    (re.compile(r"出来(?=[るなま])"), "でき"),
    (re.compile(r"全て"), "すべて"),
    (re.compile(r"下さい"), "ください"),
)

VAGUE_WORDS: tuple[str, ...] = ("適宜", "なるべく", "できるだけ", "しばらく", "高速に")


@dataclass(frozen=True)
class Issue:
    """検出した問題を 1 件表す。"""

    path: str
    line: int
    column: int
    rule: str
    message: str

    def format(self) -> str:
        """コンパイラーの警告と同じ形式の文字列にする。"""
        return f"{self.path}:{self.line}:{self.column}: [{self.rule}] {self.message}"


def mask_inline_code(line: str) -> str:
    """インラインコードを同じ長さの空白に置き換える（列番号を変えないため）。"""
    return INLINE_CODE.sub(lambda match: " " * len(match.group(0)), line)


def iter_target_lines(text: str) -> Iterator[tuple[int, str]]:
    """検査対象の行を (行番号, 行) の組で返す。コードブロックの中の行は返さない。"""
    in_code_block = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if not in_code_block:
            yield number, mask_inline_code(line)


def check_sentence_length(path: str, number: int, line: str, max_length: int) -> Iterator[Issue]:
    """一文の長さを検査する。"""
    start = 0
    for sentence in line.split("。"):
        length = len(sentence.strip())
        if length > max_length:
            column = start + len(sentence) - len(sentence.lstrip()) + 1
            message = f"一文が {length} 文字ある（上限 {max_length} 文字）。文を分けられないか検討する。"
            yield Issue(path, number, column, "long-sentence", message)
        start += len(sentence) + 1


def check_spacing(path: str, number: int, line: str) -> Iterator[Issue]:
    """日本語と英数字の間の半角空白を検査する。"""
    for match in MISSING_SPACE.finditer(line):
        yield Issue(path, number, match.start() + 1, "spacing", "日本語と英数字の間に半角空白を入れる。")


def check_variants(path: str, number: int, line: str) -> Iterator[Issue]:
    """表記ゆれを検査する。"""
    for pattern, preferred in VARIANT_RULES:
        for match in pattern.finditer(line):
            message = f"「{match.group(0)}」は「{preferred}」と書く。"
            yield Issue(path, number, match.start() + 1, "variant", message)


def check_vague_words(path: str, number: int, line: str) -> Iterator[Issue]:
    """曖昧な表現を検査する。"""
    for word in VAGUE_WORDS:
        for match in re.finditer(re.escape(word), line):
            message = f"曖昧な表現「{word}」がある。条件や数値で具体的に書けないか検討する。"
            yield Issue(path, number, match.start() + 1, "vague", message)


def check_text(path: str, text: str, max_length: int = DEFAULT_MAX_LENGTH) -> list[Issue]:
    """文書全体を検査し、見つかった問題を行番号と列番号の順に並べて返す。"""
    issues: list[Issue] = []
    for number, line in iter_target_lines(text):
        issues.extend(check_sentence_length(path, number, line, max_length))
        issues.extend(check_spacing(path, number, line))
        issues.extend(check_variants(path, number, line))
        issues.extend(check_vague_words(path, number, line))
    return sorted(issues, key=lambda issue: (issue.line, issue.column))


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(description="日本語の技術文書を対象とした簡易文章チェッカー")
    parser.add_argument("paths", nargs="+", type=Path, help="検査する文書（UTF-8）")
    parser.add_argument(
        "--max-length",
        type=int,
        default=DEFAULT_MAX_LENGTH,
        help=f"一文の文字数の上限（既定値: {DEFAULT_MAX_LENGTH}）",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """エントリーポイント。終了コードを返す。"""
    args = parse_args(argv)
    found = False
    for path in args.paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            print(f"{path}: ファイルを読めない: {error}", file=sys.stderr)
            return 2
        for issue in check_text(str(path), text, args.max_length):
            print(issue.format())
            found = True
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
