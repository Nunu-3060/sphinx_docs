"""各 Sphinx プロジェクトのビルド結果を GitHub Pages 公開用の 1 つのフォルダーにまとめる。

カレントディレクトリの ``projects/*/build/html`` を ``<出力先>/<プロジェクト>/`` にコピーし、
次のファイルを出力先の直下に作成する。

* ``index.html``: 各文書へのリンクを並べたトップページ
  （見出しは conf.py の project）
* ``.nojekyll``: GitHub Pages の Jekyll 処理を無効にする
  （無いと ``_static`` などアンダースコアで始まるフォルダーが公開されない。
  公開するフォルダーの直下に必要で、各文書のフォルダー内の .nojekyll では効かない）

コピー後に、html 内の相対リンク（href, src）の参照先が存在するかを調べる
（ダウンロード用ファイルを置く ``_downloads`` 内の html は対象外）。
GitHub Pages は Windows と違ってファイル名の大文字・小文字を区別するため、
大文字・小文字だけが異なるリンクも問題として表示する。

使い方::

    python run_build_html.py        # 先に全文書をビルドしておく
    python make_pages_site.py       # docs フォルダーに出力する
    python make_pages_site.py -o site
"""

from __future__ import annotations

import argparse
import functools
import html
import os
import shutil
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from sphinx_projects import (
    HTML_RELATIVE_DIR,
    INDEX_NAME,
    conf_path_of,
    find_projects,
    get_projects_dir,
    read_project_name,
)

DEFAULT_OUTPUT = "docs"
# 出力先に残してよい、このスクリプトが作らないファイル（GitHub Pages の設定）
KEEP_IN_OUTPUT = {"CNAME"}

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>文書一覧</title>
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
  ul {{ padding-left: 0; list-style: none; }}
  li {{ margin: 0.4rem 0; }}
  a {{
    display: block;
    padding: 0.6rem 0.9rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    color: #2980b9;
    text-decoration: none;
  }}
  a:hover {{ background: #f3f8fc; }}
  @media (prefers-color-scheme: dark) {{
    body {{ color: #ddd; background: #1e1e1e; }}
    a {{ border-color: #444; color: #6ab0de; }}
    a:hover {{ background: #26303a; }}
  }}
</style>
</head>
<body>
<h1>文書一覧</h1>
<ul>
{items}
</ul>
</body>
</html>
"""


class LinkCollector(HTMLParser):
    """html から href / src 属性の値を集める。"""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)


def clear_output(output: Path) -> None:
    """出力先の中身を削除する（KEEP_IN_OUTPUT のファイルは残す）。"""
    if not output.exists():
        output.mkdir(parents=True)
        return
    for child in output.iterdir():
        if child.name in KEEP_IN_OUTPUT:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def render_index(entries: list[tuple[str, str]]) -> str:
    """トップページの html を作成する。"""
    items = "\n".join(
        f'<li><a href="{html.escape(folder)}/index.html">'
        f"{html.escape(' '.join(title.split()))}</a></li>"
        for title, folder in entries
    )
    return INDEX_TEMPLATE.format(items=items)


@functools.lru_cache(maxsize=None)
def list_dir(directory: Path) -> frozenset[str]:
    """フォルダー内のファイル名・フォルダー名を返す（結果はキャッシュする）。"""
    try:
        return frozenset(os.listdir(directory))
    except OSError:
        return frozenset()


def exists_exact_case(path: Path, root: Path) -> bool:
    """root 以下の path が、大文字・小文字まで一致して存在するか調べる。"""
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    current = root
    for part in parts:
        if part not in list_dir(current):
            return False
        current = current / part
    return True


def check_links(output: Path) -> list[str]:
    """出力先の html の相対リンクを調べ、問題のあるものを返す。"""
    root = output.resolve()
    problems: list[str] = []
    for page in sorted(root.rglob("*.html")):
        if "_downloads" in page.relative_to(root).parts:
            continue  # ダウンロード用のサンプルファイルはページではない
        collector = LinkCollector()
        collector.feed(page.read_text(encoding="utf-8", errors="replace"))
        for link in collector.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or not parts.path:
                continue  # 外部リンク・ページ内リンク
            if parts.path.startswith("/"):
                problems.append(f"{page.relative_to(root)}: 絶対パス {link}")
                continue
            target = (page.parent / unquote(parts.path)).resolve()
            if target.is_dir():
                target = target / INDEX_NAME
            if not exists_exact_case(target, root):
                problems.append(f"{page.relative_to(root)}: リンク切れ {link}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"出力先のフォルダー（既定: {DEFAULT_OUTPUT}）",
    )
    parser.add_argument(
        "--skip-link-check", action="store_true", help="リンクの確認を省く"
    )
    args = parser.parse_args()

    base_dir = Path.cwd()
    output: Path = args.output
    # 出力先は実行のたびに中身を削除するため、プロジェクトを含む場所は拒否する。
    projects_dir = get_projects_dir(base_dir).resolve()
    resolved = output.resolve()
    if resolved == base_dir.resolve() or resolved == projects_dir or (
        projects_dir in resolved.parents
    ):
        raise SystemExit(
            f"出力先に {resolved} は指定できません"
            "（カレントディレクトリと projects フォルダー以下は不可）。"
        )

    entries: list[tuple[str, str]] = []
    missing: list[str] = []
    projects = find_projects(base_dir)
    clear_output(output)
    for project in projects:
        html_dir = project / HTML_RELATIVE_DIR
        if not (html_dir / INDEX_NAME).is_file():
            missing.append(project.name)
            continue
        shutil.copytree(html_dir, output / project.name)
        title = read_project_name(conf_path_of(project)) or project.name
        entries.append((title, project.name))

    (output / INDEX_NAME).write_text(render_index(entries), encoding="utf-8")
    (output / ".nojekyll").write_bytes(b"")

    size_mb = sum(
        path.stat().st_size for path in output.rglob("*") if path.is_file()
    ) / 1024 / 1024
    print(f"{output} に {len(entries)} 件の文書を出力しました"
          f"（{size_mb:.1f} MB）。")

    failed = bool(missing)
    for name in missing:
        print(f"  ビルド結果がないため省略: {name}（先にビルドしてください）")

    if not args.skip_link_check:
        problems = check_links(output)
        for problem in problems:
            print(f"  {problem}")
        print(f"リンクの確認: 問題 {len(problems)} 件")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
