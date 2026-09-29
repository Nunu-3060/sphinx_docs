"""各 Sphinx プロジェクトの conf.py から project を読み取り、readme.md に一覧表を出力する。

カレントディレクトリの ``projects/*/source/conf.py`` を探し、
プロジェクト名と GitHub Pages 公開用フォルダー内の
``docs/<プロジェクト>/index.html`` への相対パスを対応付けた表を作成する。
表の前には文書一覧のトップページ ``docs/index.html`` へのリンクを置く。
docs は make_pages_site.py で作成する。
conf.py の解析は sphinx_projects.py で行う（実行はしない）。
"""

from __future__ import annotations

from pathlib import Path

from sphinx_projects import (
    INDEX_NAME,
    conf_path_of,
    find_projects,
    read_project_name,
)

DOCS_DIR = "docs"
README_NAME = "readme.md"


def escape_cell(text: str) -> str:
    """Markdown の表のセルに入れられるように文字列を整える。"""
    return " ".join(text.split()).replace("|", r"\|")


def build_rows(base_dir: Path) -> list[tuple[str, str]]:
    """(プロジェクト名, index.html への相対パス) の一覧を返す。"""
    rows: list[tuple[str, str]] = []
    for project in find_projects(base_dir):
        name = read_project_name(conf_path_of(project)) or project.name
        index_path = Path(DOCS_DIR) / project.name / INDEX_NAME
        rows.append((name, index_path.as_posix()))
    return rows


def render_markdown(rows: list[tuple[str, str]]) -> str:
    """readme.md の内容を作成する。"""
    top_page = f"{DOCS_DIR}/{INDEX_NAME}"
    lines = [
        "# Sphinx プロジェクト一覧",
        "",
        f"文書一覧のトップページ: [{top_page}]({top_page})",
        "",
        "| プロジェクト | index.html |",
        "| --- | --- |",
    ]
    for name, path in rows:
        lines.append(f"| {escape_cell(name)} | [{path}]({path}) |")
    return "\n".join(lines) + "\n"


def main() -> None:
    base_dir = Path.cwd()
    rows = build_rows(base_dir)
    readme_path = base_dir / README_NAME
    readme_path.write_text(render_markdown(rows), encoding="utf-8")
    print(f"{readme_path} に {len(rows)} 件のプロジェクトを出力しました。")
    # リンク先はファイルとして存在しなくても出力する（docs は後から作れる）。
    missing = [path for _, path in rows if not (base_dir / path).is_file()]
    if not (base_dir / DOCS_DIR / INDEX_NAME).is_file():
        missing.insert(0, f"{DOCS_DIR}/{INDEX_NAME}")
    for path in missing:
        print(f"  リンク先がありません: {path}"
              "（python make_pages_site.py で作成してください）")


if __name__ == "__main__":
    main()
