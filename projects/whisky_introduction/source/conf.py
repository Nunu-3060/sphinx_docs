"""Sphinx の設定ファイル。"""

import sys
from pathlib import Path

from sphinx.application import Sphinx

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

import make_figures  # noqa: E402

# -- プロジェクト情報 --------------------------------------------------------

project = "ウイスキー入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 ----------------------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

language = "ja"
exclude_patterns = ["_scripts"]
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 章",
}

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- HTML 出力の設定 ---------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "ウイスキー入門"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_copy_source = False  # rst を出力に含めない
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_search_language = "ja"
html_theme_options = {
    "navigation_depth": 3,
}

# -- リンクチェックの設定 ----------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2


def _generate_figures(app: Sphinx) -> None:
    """ビルド開始時に本文で使う図を生成する。"""
    make_figures.generate_all(SOURCE_DIR / "_generated")


def _remove_empty_sources_dir(app: Sphinx, exception: Exception | None) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダを削除する。"""
    sources_dir = Path(app.outdir) / "_sources"
    if exception is None and sources_dir.is_dir() and not any(sources_dir.iterdir()):
        sources_dir.rmdir()


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", _generate_figures)
    app.connect("build-finished", _remove_empty_sources_dir)
