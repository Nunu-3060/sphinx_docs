# Sphinx の設定ファイル
# 設定項目の詳細: https://www.sphinx-doc.org/ja/master/usage/configuration.html

import sys
import zipfile
from pathlib import Path

# -- プロジェクト情報 ---------------------------------------------------------

project = "Godot 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    # 数式を MathJax で表示する。
    "sphinx.ext.mathjax",
    # Graphviz で図を描く。
    "sphinx.ext.graphviz",
    # GitHub Pages で公開できるように .nojekyll を出力する。
    "sphinx.ext.githubpages",
]

language = "ja"
templates_path: list[str] = []
# _generated の rst は付録から include するだけで、単独のページにはしない。
exclude_patterns: list[str] = ["_generated/*.rst"]

# コードブロックの既定の言語を GDScript にする。
highlight_language = "gdscript"

# 図・表・コードに番号を付ける。
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
}

# -- Graphviz の設定 ----------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
    "-Gbgcolor=transparent",
]

# -- リンクの検査（linkcheck）の設定 -----------------------------------------

# 自動的なアクセスを拒否する（HTTP 454 を返す）サイト。ブラウザーで手動確認する。
linkcheck_ignore = [r"https://godotshaders\.com/.*"]

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "Godot 入門"
html_theme_options = {
    "navigation_depth": 3,
    "prev_next_buttons_location": "both",
}

# 表の折り返しなど、テーマの表示を調整する CSS
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst のソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- ビルド時に生成するファイル ------------------------------------------------

_SOURCE_DIR = Path(__file__).resolve().parent
_EXAMPLES_DIR = _SOURCE_DIR.parent / "examples"
_GENERATED_DIR = _SOURCE_DIR / "_generated"
EXAMPLES_ZIP = _GENERATED_DIR / "godot_introduction_examples.zip"

# zip に含めないフォルダー（Godot のキャッシュなど）
_EXCLUDED_DIRS = {".godot", "_tmp", "__pycache__", ".mypy_cache"}


def _create_examples_zip() -> None:
    """examples フォルダーの内容を zip ファイルにまとめる。"""
    _GENERATED_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(EXAMPLES_ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(_EXAMPLES_DIR.rglob("*")):
            relative = path.relative_to(_EXAMPLES_DIR)
            if not path.is_file() or _EXCLUDED_DIRS.intersection(relative.parts):
                continue
            archive.write(path, Path("godot_introduction_examples") / relative)


# サンプルファイルの一覧に載せないファイル（Godot が自動で作る管理用のファイル）
_UNLISTED_SUFFIXES = {".uid", ".import"}

# 拡張子ごとのファイルの種類
_FILE_KINDS = {
    ".gd": "GDScript",
    ".tscn": "シーン",
    ".tres": "リソース",
    ".gdshader": "シェーダー",
    ".py": "Python スクリプト",
    ".png": "画像",
    ".svg": "画像",
    ".wav": "音声",
    ".godot": "プロジェクトの設定",
    ".cfg": "設定ファイル",
}


def _create_examples_list() -> None:
    """サンプルファイルを個別に閲覧・ダウンロードするためのリンクの一覧（rst）を作る。"""
    lines = [
        ".. list-table:: サンプルファイルの一覧",
        "   :header-rows: 1",
        "   :widths: 60 40",
        "",
        "   * - ファイル",
        "     - 種類",
    ]
    for path in sorted(_EXAMPLES_DIR.rglob("*")):
        relative = path.relative_to(_EXAMPLES_DIR)
        if not path.is_file() or _EXCLUDED_DIRS.intersection(relative.parts):
            continue
        if path.suffix in _UNLISTED_SUFFIXES:
            continue
        posix = relative.as_posix()
        kind = _FILE_KINDS.get(path.suffix, "設定ファイル")
        lines.append(f"   * - :download:`{posix} </../examples/{posix}>`")
        lines.append(f"     - {kind}")
    (_GENERATED_DIR / "examples_list.rst").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _create_figures() -> None:
    """matplotlib で本文の図を描く。"""
    # source フォルダーに __pycache__ を作らないようにする。
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(_SOURCE_DIR / "_scripts"))
    import make_figures

    make_figures.main(_GENERATED_DIR / "figures")


_create_examples_zip()
_create_examples_list()
_create_figures()


def setup(app: object) -> None:
    """Godot 4 の文法に対応した GDScript の字句解析器を登録する。"""
    from gdscript4_lexer import GDScript4Lexer

    app.add_lexer("gdscript", GDScript4Lexer)  # type: ignore[attr-defined]
