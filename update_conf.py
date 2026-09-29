"""各 Sphinx プロジェクトの conf.py の copyright, author, release を一括で変更する。

カレントディレクトリの ``projects/*/source/conf.py`` が対象である。

* copyright, author, release の代入文を指定した値に書き換える。
  型ヒント付きの代入（``author: str = "..."``）にも対応し、型ヒントはそのまま残す。
* 定義されていない項目は ``project`` の近くに copyright → author → release の順で
  追加する（project に型ヒントがあれば、追加する行にも ``: str`` を付ける）。
* ``version`` が定義されている場合は release と同じ値に書き換える
  （``--keep-version`` で無効にできる）。
* 引用符の種類と改行コードは各ファイルの書き方に合わせる。
* それ以外の行は変更しない。

使い方::

    python update_conf.py --release 1.1
    python update_conf.py --copyright "2026, prometech" --author prometech
    python update_conf.py --check                  # 書き換えずに差分を表示する
    python update_conf.py --release 1.1 python_introduction
"""

from __future__ import annotations

import argparse
import ast
import sys
from datetime import date
from pathlib import Path

from sphinx_projects import (
    ConfAssignment,
    add_projects_argument,
    conf_path_of,
    find_assignment,
    find_projects,
    parse_assignments,
    read_conf_text,
    split_lines,
)

DEFAULT_AUTHOR = "Nunu_3060"
DEFAULT_COPYRIGHT = f"2026, {DEFAULT_AUTHOR}"
DEFAULT_RELEASE = "1.0"

# 追加するときの並び順
KEYS = ("copyright", "author", "release")
# 追加する位置の目安にする項目
PROJECT_INFO_KEYS = ("project",) + KEYS


def line_ending(line: str) -> str:
    """行末の改行コードを返す（改行が無ければ空文字列）。"""
    for newline in ("\r\n", "\r", "\n"):
        if line.endswith(newline):
            return newline
    return ""


def file_newline(lines: list[str]) -> str:
    """ファイルで使われている改行コードを返す（最初に見つかったもの）。"""
    for line in lines:
        if newline := line_ending(line):
            return newline
    return "\n"


def trailing_text(line: str, end_col_offset: int) -> str:
    """代入文の後ろにある行末コメントなど（改行は除く）を返す。"""
    body = line[: len(line) - len(line_ending(line))]
    return body.encode("utf-8")[end_col_offset:].decode("utf-8")


def quote_of(project: ConfAssignment) -> str:
    """project の値に使われている引用符を返す。"""
    source = project.value_source.lstrip("rRuU")
    return source[0] if source[:1] in ("'", '"') else '"'


def make_assignment(
    key: str,
    value: str,
    quote: str,
    annotation: str | None,
    newline: str,
    trailing: str = "",
) -> str:
    """``key = 'value'`` または ``key: str = 'value'`` の 1 行を作る。

    trailing には行末コメントなど、代入文の後ろに残す文字列を渡す。
    """
    # repr で引用符やバックスラッシュを正しくエスケープする
    literal = repr(value)
    if literal[0] != quote and quote not in value:
        literal = quote + literal[1:-1] + quote
    hint = f": {annotation}" if annotation else ""
    return f"{key}{hint} = {literal}{trailing}{newline}"


def update_text(text: str, values: dict[str, str]) -> str:
    """conf.py の内容を受け取り、values の値に書き換えた内容を返す。"""
    project = find_assignment(parse_assignments(text), "project")
    if project is None:
        raise ValueError("project の代入文が見つかりません")
    quote = quote_of(project)
    # 追加する行に付ける型ヒント（project に型ヒントがあるときだけ）
    new_annotation = "str" if project.annotation else None

    # 既存の代入文を書き換える。行番号がずれないように後ろから置き換える。
    lines = split_lines(text)
    newline = file_newline(lines)
    assignments = parse_assignments(text)
    existing = [
        item
        for key in values
        if (item := find_assignment(assignments, key)) is not None
    ]
    for item in sorted(existing, key=lambda a: a.lineno, reverse=True):
        last_line = lines[item.end_lineno - 1]
        lines[item.lineno - 1:item.end_lineno] = [
            make_assignment(
                item.name,
                values[item.name],
                quote,
                item.annotation,
                # ファイル末尾の改行の有無もそのまま残す
                line_ending(last_line),
                trailing_text(last_line, item.end_col_offset),
            )
        ]

    # 定義されていない項目を追加する。
    for position, key in enumerate(KEYS):
        text = "".join(lines)
        assignments = parse_assignments(text)
        if key not in values or find_assignment(assignments, key):
            continue
        info = [a for a in assignments if a.name in PROJECT_INFO_KEYS]
        # 後ろに来るべき項目（author に対する release など）があればその前に、
        # なければ project 情報の最後の行の後ろに追加する。
        later = [a for a in info if a.name in KEYS[position + 1:]]
        if later:
            insert_at = min(a.lineno for a in later) - 1
        else:
            insert_at = max(a.end_lineno for a in info)
        if insert_at == len(lines) and not line_ending(lines[-1]):
            lines[-1] += newline
        lines.insert(
            insert_at,
            make_assignment(key, values[key], quote, new_annotation, newline),
        )
    return "".join(lines)


def describe_changes(old: str, new: str, keys: list[str]) -> str:
    """値が変わる項目を ``author: 'a' -> 'b'`` の形で返す。"""
    old_assignments = parse_assignments(old)
    new_assignments = parse_assignments(new)
    changes = []
    for key in keys:
        before = find_assignment(old_assignments, key)
        after = find_assignment(new_assignments, key)
        if before is None and after is None:
            continue  # 追加しない項目（version）が元から無い
        before_value = before.value if before else None
        after_value = after.value if after else None
        if before is None or before_value != after_value:
            shown = "（なし）" if before is None else repr(before_value)
            changes.append(f"{key}: {shown} -> {after_value!r}")
    return ", ".join(changes)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_projects_argument(parser)
    parser.add_argument("--copyright", default=DEFAULT_COPYRIGHT)
    parser.add_argument("--author", default=DEFAULT_AUTHOR)
    parser.add_argument("--release", default=DEFAULT_RELEASE)
    parser.add_argument(
        "--keep-version",
        action="store_true",
        help="version を release に合わせて書き換えない",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="書き換えずに、値が異なる conf.py を表示する",
    )
    args = parser.parse_args()

    values = {
        "copyright": args.copyright,
        "author": args.author,
        "release": args.release,
    }
    if not args.keep_version:
        values["version"] = args.release

    changed = 0
    for project in find_projects(Path.cwd(), args.projects):
        conf_path = conf_path_of(project)
        text = read_conf_text(conf_path)
        new_text = update_text(text, values)
        ast.parse(new_text, str(conf_path))  # 壊れた conf.py を書き出さない
        if new_text == text:
            print(f"変更なし: {conf_path}")
            continue
        changed += 1
        detail = describe_changes(text, new_text, list(values))
        if args.check:
            print(f"差分あり: {conf_path}\n    {detail}")
        else:
            with conf_path.open("w", encoding="utf-8", newline="") as file:
                file.write(new_text)
            print(f"更新    : {conf_path}\n    {detail}")

    print(f"{changed} 件の conf.py が"
          f"{'指定した値と異なります' if args.check else '更新されました'}。")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
