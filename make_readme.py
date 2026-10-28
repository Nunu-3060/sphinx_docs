"""各 Sphinx プロジェクトの conf.py から project を読み取り、readme.md にグループごとの一覧表を出力する。

グループと所属する文書は ``categories.toml`` に書く。
グループの一覧表には、GitHub Pages の公開先 URL
（categories.toml の pages_base_url から作る）を載せる。
グループごとの表には、文書のタイトルと ``projects/<プロジェクト>`` のフォルダーを
対応付けて載せる（各文書の index.html へのリンクは載せない）。
公開用フォルダーは make_pages_site.py で作成する。
conf.py の解析は sphinx_projects.py で行う（実行はしない）。
"""

from __future__ import annotations

import os
from pathlib import Path

from sphinx_projects import (
    Categories,
    Category,
    conf_path_of,
    load_categories,
    read_project_name,
)

README_NAME = "readme.md"


def escape_cell(text: str) -> str:
    """Markdown の表のセルに入れられるように文字列を整える。"""
    return " ".join(text.split()).replace("|", r"\|")


def relative_link(path: Path, base_dir: Path) -> str:
    """base_dir から path への相対パスを、Markdown のリンク用に返す。"""
    return Path(os.path.relpath(path, base_dir)).as_posix()


def build_rows(category: Category, base_dir: Path) -> list[tuple[str, str]]:
    """(プロジェクト名, プロジェクトのフォルダーの相対パス) の一覧を返す。"""
    rows: list[tuple[str, str]] = []
    for project in category.projects:
        name = read_project_name(conf_path_of(project)) or project.name
        rows.append((name, relative_link(project, base_dir)))
    return rows


def render_markdown(categories: Categories, base_dir: Path) -> str:
    """readme.md の内容を作成する。"""
    total = sum(len(category.projects) for category in categories.items)
    lines = [
        "# Sphinx プロジェクト一覧",
        "",
        f"{len(categories.items)} グループ、{total} 件の文書がある。"
        "グループの分類は categories.toml に、"
        "公開用の出力先は sphinx_docs_<グループ>/docs にある。",
        "",
        "| グループ | 件数 | 公開先 URL |",
        "| --- | --- | --- |",
    ]
    for category in categories.items:
        lines.append(
            f"| [{escape_cell(category.title)}](#{category.folder}) "
            f"| {len(category.projects)} "
            f"| <{categories.pages_url_of(category)}> |"
        )
    for category in categories.items:
        lines += [
            "",
            f'<a id="{category.folder}"></a>',
            "",
            f"## {category.title}",
            "",
            category.description,
            "",
            "| タイトル | フォルダー |",
            "| --- | --- |",
        ]
        for name, folder in build_rows(category, base_dir):
            lines.append(f"| {escape_cell(name)} | [{folder}]({folder}) |")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path.cwd()
    categories = load_categories(base_dir)
    readme_path = base_dir / README_NAME
    readme_path.write_text(
        render_markdown(categories, base_dir), encoding="utf-8"
    )
    total = sum(len(category.projects) for category in categories.items)
    print(f"{readme_path} に {len(categories.items)} グループ、"
          f"{total} 件のプロジェクトを出力しました。")


if __name__ == "__main__":
    main()
