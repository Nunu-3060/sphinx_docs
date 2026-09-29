"""ツール用スクリプトで共通して使う、Sphinx プロジェクトの探索と conf.py の解析。

各スクリプト（make_pages_site.py, make_readme.py, run_build_html.py,
unify_build_html.py, update_conf.py）から import して使う。

* Sphinx プロジェクトは、カレントディレクトリの ``projects`` フォルダー直下にある
  ``source/conf.py`` を持つフォルダーとする。
* conf.py は副作用のある処理を含む場合があるため、実行せずに ast で解析する。
  ``project = "..."`` のほか、型ヒント付きの ``project: str = "..."`` にも対応する。
"""

from __future__ import annotations

import argparse
import ast
import io
from dataclasses import dataclass
from pathlib import Path

PROJECTS_DIR = "projects"
CONF_RELATIVE_PATH = Path("source") / "conf.py"
BAT_NAME = "build_html.bat"
BUILD_DIR_NAME = "build"
HTML_RELATIVE_DIR = Path(BUILD_DIR_NAME) / "html"
INDEX_NAME = "index.html"


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
