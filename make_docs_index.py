"""GitHub Pages の各公開先へのリンクとタイトルを並べた docs/index.html を出力する。

グループと所属する文書は ``categories.toml`` に書く。グループの公開先 URL は
categories.toml の pages_base_url とリポジトリ名から
``<pages_base_url>sphinx_docs_<グループ>/`` として作る。
カレントディレクトリの ``docs/index.html`` に、
グループごとに次の内容を並べたページを出力する。

* グループのタイトル（categories.toml の title）と、公開先 URL へのリンク
* グループの説明（categories.toml の description）
* 所属する各文書のタイトル（conf.py の project）と、
  公開先 URL の ``<プロジェクト>/index.html`` へのリンク

各文書の URL は、make_pages_site.py が公開用フォルダーに
``docs/<プロジェクト>/`` としてコピーし、そのまま公開している前提で作る
（公開先にその文書が実際にあるかは確かめない）。

使い方::

    python make_docs_index.py
    python make_docs_index.py -o site/index.html
"""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from sphinx_projects import (
    INDEX_NAME,
    PAGES_DIR_NAME,
    Categories,
    Category,
    conf_path_of,
    load_categories,
    read_project_name,
)

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sphinx 文書一覧</title>
<style>
  body {{
    margin: 0 auto;
    max-width: 48rem;
    padding: 2rem 1rem;
    font-family: "Segoe UI", "Hiragino Sans", "Meiryo", sans-serif;
    line-height: 1.6;
    color: #222;
    background: #fff;
  }}
  h1 {{ font-size: 1.6rem; border-bottom: 2px solid #2980b9; }}
  h2 {{ font-size: 1.3rem; margin: 2rem 0 0.2rem; }}
  h2 a {{ color: #2980b9; text-decoration: none; }}
  h2 a:hover {{ text-decoration: underline; }}
  .summary, .description, .count {{ color: #555; }}
  .description {{ margin: 0 0 0.6rem; }}
  .count {{ font-size: 0.9rem; font-weight: normal; }}
  nav ul {{ padding-left: 1.2rem; }}
  nav a {{ color: #2980b9; }}
  ul.documents {{ padding-left: 0; list-style: none; }}
  ul.documents li {{ margin: 0.4rem 0; }}
  ul.documents a {{
    display: block;
    padding: 0.6rem 0.9rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    color: #2980b9;
    text-decoration: none;
  }}
  ul.documents a:hover {{ background: #f3f8fc; }}
  @media (prefers-color-scheme: dark) {{
    body {{ color: #ddd; background: #1e1e1e; }}
    .summary, .description, .count {{ color: #aaa; }}
    h2 a, nav a {{ color: #6ab0de; }}
    ul.documents a {{ border-color: #444; color: #6ab0de; }}
    ul.documents a:hover {{ background: #26303a; }}
  }}
</style>
</head>
<body>
<h1>Sphinx 文書一覧</h1>
<p class="summary">{summary}</p>
<nav>
<ul>
{toc}
</ul>
</nav>
{sections}
</body>
</html>
"""

SECTION_TEMPLATE = """\
<section id="{folder}">
<h2><a href="{url}">{title}</a> <span class="count">（{count} 件）</span></h2>
<p class="description">{description}</p>
<ul class="documents">
{items}
</ul>
</section>"""


def clean_text(text: str) -> str:
    """空白・改行をまとめ、html に入れられるように文字列を整える。"""
    return html.escape(" ".join(text.split()))


def render_section(category: Category, url: str) -> str:
    """1 グループ分の html を作成する。"""
    items = []
    for project in category.projects:
        title = read_project_name(conf_path_of(project)) or project.name
        href = f"{url}{project.name}/{INDEX_NAME}"
        items.append(
            f'<li><a href="{html.escape(href)}">{clean_text(title)}</a></li>'
        )
    return SECTION_TEMPLATE.format(
        folder=html.escape(category.folder),
        url=html.escape(url),
        title=clean_text(category.title),
        count=len(category.projects),
        description=clean_text(category.description),
        items="\n".join(items),
    )


def render_index(categories: Categories) -> str:
    """docs/index.html の内容を作成する。"""
    total = sum(len(category.projects) for category in categories.items)
    toc = "\n".join(
        f'<li><a href="#{html.escape(category.folder)}">'
        f"{clean_text(category.title)}</a></li>"
        for category in categories.items
    )
    sections = "\n".join(
        render_section(category, categories.pages_url_of(category))
        for category in categories.items
    )
    return INDEX_TEMPLATE.format(
        summary=f"{len(categories.items)} グループ、{total} 件の文書がある。",
        toc=toc,
        sections=sections,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(PAGES_DIR_NAME) / INDEX_NAME,
        help=f"出力先のファイル（既定: {PAGES_DIR_NAME}/{INDEX_NAME}）",
    )
    args = parser.parse_args()

    base_dir = Path.cwd()
    categories = load_categories(base_dir)
    output: Path = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_index(categories), encoding="utf-8")
    total = sum(len(category.projects) for category in categories.items)
    print(f"{output} に {len(categories.items)} グループ、"
          f"{total} 件の文書へのリンクを出力しました。")


if __name__ == "__main__":
    main()
