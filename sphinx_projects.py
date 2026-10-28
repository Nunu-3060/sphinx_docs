"""ツール用スクリプトで共通して使う、Sphinx プロジェクトの探索と conf.py の解析。

各スクリプト（make_pages_site.py, make_readme.py, make_docs_index.py,
run_build_html.py, unify_build_html.py, update_conf.py）から import して使う。

* Sphinx プロジェクトは、カレントディレクトリの ``projects`` フォルダー直下にある
  ``source/conf.py`` を持つフォルダーとする。
* conf.py は副作用のある処理を含む場合があるため、実行せずに ast で解析する。
  ``project = "..."`` のほか、型ヒント付きの ``project: str = "..."`` にも対応する。
* 文書の分類（グループ）と公開用の出力先は、カレントディレクトリの
  ``categories.toml`` に書く（読み込みは load_categories）。
  GitHub Pages の公開先 URL も、categories.toml の pages_base_url から作る
  （Categories.pages_url_of）。
"""

from __future__ import annotations

import argparse
import ast
import io
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

PROJECTS_DIR = "projects"
CONF_RELATIVE_PATH = Path("source") / "conf.py"
BAT_NAME = "build_html.bat"
BUILD_DIR_NAME = "build"
HTML_RELATIVE_DIR = Path(BUILD_DIR_NAME) / "html"
INDEX_NAME = "index.html"
CATEGORIES_NAME = "categories.toml"
# グループごとの公開用リポジトリのフォルダー名の接頭辞と、その中の公開フォルダー
REPOSITORY_PREFIX = "sphinx_docs_"
PAGES_DIR_NAME = "docs"


def get_projects_dir(base_dir: Path) -> Path:
    """projects フォルダーを返す。無ければエラーで終了する。"""
    projects_dir = base_dir / PROJECTS_DIR
    if not projects_dir.is_dir():
        raise SystemExit(
            f"{projects_dir} がありません。"
            "projects フォルダーのあるフォルダーで実行してください。"
        )
    return projects_dir


def find_projects(
    base_dir: Path,
    names: list[str] | None = None,
    marker: Path | str = CONF_RELATIVE_PATH,
) -> list[Path]:
    """marker（既定は source/conf.py）を持つプロジェクトのフォルダーを返す。

    names が空なら全件を、指定されていればその名前のプロジェクトを
    指定された順に返す。見つからない名前があればエラーで終了する。
    """
    projects_dir = get_projects_dir(base_dir)
    projects = sorted(
        child
        for child in projects_dir.iterdir()
        if child.is_dir() and (child / marker).is_file()
    )
    if not names:
        return projects
    by_name = {project.name: project for project in projects}
    unknown = [name for name in names if name not in by_name]
    if unknown:
        raise SystemExit(
            f"{Path(marker).as_posix()} を持つプロジェクトが見つかりません: "
            f"{unknown}"
        )
    return [by_name[name] for name in names]


def add_projects_argument(parser: argparse.ArgumentParser) -> None:
    """対象のプロジェクト名を受け取る位置引数を追加する。"""
    parser.add_argument(
        "projects", nargs="*", help="対象のプロジェクト（省略時は全件）"
    )


def conf_path_of(project: Path) -> Path:
    """プロジェクトの conf.py のパスを返す。"""
    return project / CONF_RELATIVE_PATH


def read_conf_text(conf_path: Path) -> str:
    """conf.py の内容を、改行コードを変えずに読み込む。"""
    with conf_path.open(encoding="utf-8", newline="") as file:
        return file.read()


def split_lines(text: str) -> list[str]:
    """行末の改行コードを残したまま、ast と同じ規則（CRLF, LF, CR）で行に分ける。"""
    return io.StringIO(text, newline="").readlines()


@dataclass(frozen=True)
class ConfAssignment:
    """conf.py の最上位にある ``name = value`` / ``name: type = value`` の 1 つ。"""

    name: str
    # 値が文字列リテラルのときはその文字列、それ以外（式など）は None
    value: str | None
    # 値の書き方（引用符など）を調べるための、ソース上の値の文字列
    value_source: str
    # 型ヒントのソース上の文字列（例: "str"）。型ヒントが無ければ None
    annotation: str | None
    # 1 から始まる行番号（複数行にわたる場合は最初と最後の行）
    lineno: int
    end_lineno: int
    # 最後の行で、代入文が終わる位置（UTF-8 のバイト数）
    end_col_offset: int


def parse_assignments(
    text: str, filename: str = "conf.py"
) -> list[ConfAssignment]:
    """conf.py の最上位の代入文を、出現順に返す。"""
    tree = ast.parse(text, filename)
    assignments: list[ConfAssignment] = []
    for node in tree.body:
        value: ast.expr
        if isinstance(node, ast.Assign):
            targets = node.targets
            value = node.value
            annotation = None
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            # 型ヒント付きの代入（値の無い ``name: str`` だけの文は対象外）
            targets = [node.target]
            value = node.value
            annotation = ast.get_source_segment(text, node.annotation)
        else:
            continue
        literal = (
            value.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str)
            else None
        )
        for target in targets:
            if isinstance(target, ast.Name):
                assignments.append(
                    ConfAssignment(
                        name=target.id,
                        value=literal,
                        value_source=ast.get_source_segment(text, value) or "",
                        annotation=annotation,
                        lineno=node.lineno,
                        end_lineno=node.end_lineno or node.lineno,
                        end_col_offset=node.end_col_offset or 0,
                    )
                )
    return assignments


def find_assignment(
    assignments: list[ConfAssignment], name: str
) -> ConfAssignment | None:
    """name への代入を返す（複数あるときは、実際に使われる最後のもの）。"""
    found = [item for item in assignments if item.name == name]
    return found[-1] if found else None


def read_project_name(conf_path: Path) -> str | None:
    """conf.py の project に代入されている文字列を返す。"""
    text = read_conf_text(conf_path)
    assignments = parse_assignments(text, str(conf_path))
    project = find_assignment(assignments, "project")
    return project.value if project else None


@dataclass(frozen=True)
class Category:
    """categories.toml の 1 グループ。"""

    # 公開用リポジトリのフォルダー名（sphinx_docs_<folder>）に使う名前
    folder: str
    # 文書一覧に表示するグループ名
    title: str
    description: str
    # 所属する Sphinx プロジェクトのフォルダー（一覧に並べる順）
    projects: list[Path]

    @property
    def repository_name(self) -> str:
        """公開用リポジトリのフォルダー名を返す。"""
        return REPOSITORY_PREFIX + self.folder


@dataclass(frozen=True)
class Categories:
    """categories.toml の内容。"""

    # 公開用リポジトリを置く親フォルダー
    output_root: Path
    # GitHub Pages の公開先 URL の共通部分（https://<ユーザー>.github.io/）
    # 末尾は / にそろえる
    pages_base_url: str
    items: list[Category]

    def pages_dir_of(self, category: Category) -> Path:
        """グループの公開フォルダー（<output_root>/sphinx_docs_<folder>/docs）を返す。"""
        return self.output_root / category.repository_name / PAGES_DIR_NAME

    def pages_url_of(self, category: Category) -> str:
        """グループの公開先 URL（<pages_base_url>sphinx_docs_<folder>/）を返す。

        GitHub Pages のプロジェクトサイトは、リポジトリ名がそのまま URL のパスになる。
        文書の URL を後ろに付け足せるように、末尾は / にする。
        """
        return f"{self.pages_base_url}{category.repository_name}/"


def load_categories(base_dir: Path) -> Categories:
    """categories.toml を読み込み、projects の全文書が 1 回ずつ分類されているか確かめる。

    分類漏れ・重複・存在しないプロジェクト名があればエラーで終了する。
    """
    path = base_dir / CATEGORIES_NAME
    if not path.is_file():
        raise SystemExit(f"{path} がありません。")
    with path.open("rb") as file:
        data = tomllib.load(file)

    by_name = {project.name: project for project in find_projects(base_dir)}
    errors: list[str] = []
    seen: dict[str, str] = {}
    folders: set[str] = set()
    items: list[Category] = []
    for raw in data.get("categories", []):
        folder = str(raw["folder"])
        if folder in folders:
            errors.append(f"folder が重複しています: {folder}")
        folders.add(folder)
        projects: list[Path] = []
        for name in raw.get("projects", []):
            if name in seen:
                errors.append(f"{name} が {seen[name]} と {folder} の両方にあります")
            elif name not in by_name:
                errors.append(f"{folder} の {name} は projects にありません")
            else:
                projects.append(by_name[name])
            seen.setdefault(name, folder)
        items.append(
            Category(
                folder=folder,
                title=str(raw["title"]),
                description=str(raw.get("description", "")),
                projects=projects,
            )
        )
    for name in sorted(by_name.keys() - seen.keys()):
        errors.append(f"{name} がどのグループにもありません")
    pages_base_url = str(data.get("pages_base_url", ""))
    parts = urlsplit(pages_base_url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        errors.append(
            f"pages_base_url が URL ではありません: {pages_base_url!r}"
        )
    if errors:
        raise SystemExit(
            f"{path} に問題があります:\n"
            + "\n".join(f"  {error}" for error in errors)
        )
    output_root = (base_dir / str(data.get("output_root", ".."))).resolve()
    return Categories(
        output_root=output_root,
        pages_base_url=pages_base_url.rstrip("/") + "/",
        items=items,
    )
