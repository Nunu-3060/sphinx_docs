"""「Sphinx 入門」の Sphinx 設定ファイル。"""

import sys
from pathlib import Path

# examples ディレクトリを import できるようにする（autodoc と自作拡張機能で使用）。
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
sys.path.insert(0, str(EXAMPLES_DIR))

# -- プロジェクト情報 --------------------------------------------------------

project: str = "Sphinx 入門"
author: str = "Nunu_3060"
copyright: str = "2026, Nunu_3060"
release: str = "1.0"

# -- 一般設定 ----------------------------------------------------------------

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx_copybutton",
    "my_extension",  # examples/my_extension.py（第 8 章で解説）
]

exclude_patterns: list[str] = []

language: str = "ja"

# 図・表・コードに番号を付け、:numref: で参照できるようにする。
numfig: bool = True

# -- autodoc -----------------------------------------------------------------

autodoc_typehints: str = "description"
autodoc_member_order: str = "bysource"

# docstring の Attributes セクションを、クラスの説明の中の「変数」欄として表示する。
napoleon_use_ivar: bool = True

# -- intersphinx -------------------------------------------------------------

intersphinx_mapping: dict[str, tuple[str, str | None]] = {
    "python": ("https://docs.python.org/3", None),
}

# objects.inv の取得を待つ時間の上限（秒）。既定値は None（上限なし）。
intersphinx_timeout: int = 30

# -- doctest -----------------------------------------------------------------

# docstring のコード例を実行する前に、サンプルのクラスと関数を import しておく。
doctest_global_setup: str = (
    "from sample_package.shapes import Circle, Rectangle, total_area"
)

# -- linkcheck ---------------------------------------------------------------

# docutils.sourceforge.io は linkcheck からのアクセスを 403 で拒否するため除外する
# （ブラウザや curl では閲覧できることを確認済み）。
linkcheck_ignore: list[str] = [r"https://docutils\.sourceforge\.io/.*"]

# -- HTML 出力 ---------------------------------------------------------------

html_theme: str = "sphinx_rtd_theme"
html_title: str = "Sphinx 入門"
html_static_path: list[str] = ["_static"]
html_css_files: list[str] = ["custom.css"]  # 表の折り返しと数式番号の位置の調整

# 出力した HTML から rst ソースを閲覧できないようにする。
html_show_sourcelink: bool = False
html_copy_source: bool = False
