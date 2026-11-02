"""Markdown のファイルを HTML のファイルに変換する。

使い方:
    python ch13_md_to_html.py input.md output.html

必要なパッケージ:
    python -m pip install markdown-it-py mdit-py-plugins
"""

import argparse
import html
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.gfm import gfm_plugin

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{title}</title>
</head>
<body>
{body}</body>
</html>
"""


def convert(source: str, title: str) -> str:
    """Markdown のソースを、HTML の文書全体に変換する。"""
    md = MarkdownIt("commonmark").use(gfm_plugin)
    body = md.render(source)
    return TEMPLATE.format(title=html.escape(title), body=body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Markdown のファイルを HTML のファイルに変換する。")
    parser.add_argument("input", type=Path, help="変換する Markdown のファイル")
    parser.add_argument("output", type=Path, help="出力する HTML のファイル")
    args = parser.parse_args()

    input_path: Path = args.input
    output_path: Path = args.output
    source = input_path.read_text(encoding="utf-8")
    output_path.write_text(convert(source, title=input_path.stem), encoding="utf-8")
    print(f"{input_path} を {output_path} に変換した。")


if __name__ == "__main__":
    main()
