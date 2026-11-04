"""Sphinx の設定ファイル。"""

from __future__ import annotations

import sys
from pathlib import Path

from sphinx.application import Sphinx

SOURCE_DIR = Path(__file__).resolve().parent
FIGURES_DIR = SOURCE_DIR / "_figures"
GENERATED_DIR = SOURCE_DIR / "_generated"

# 図の生成スクリプトを import できるようにする。
sys.path.insert(0, str(FIGURES_DIR))

# -- プロジェクト情報 ---------------------------------------------------------

project = "Python による非同期処理・並行処理・並列処理"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
]

# 数式の表示には MathJax 3 を使う。
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"

language = "ja"
exclude_patterns = ["_figures"]
highlight_language = "python3"
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "コード %s",
    "section": "%s 節",
}

# -- HTML 出力 ----------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ページのソースを表示」のリンクを出さない
html_copy_source = False      # rst ファイルを _sources にコピーしない
html_theme_options = {
    "navigation_depth": 3,
}

# -- Graphviz -----------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- linkcheck ----------------------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2


# -- ビルド時の図の生成 ---------------------------------------------------------

def generate_figures(app: Sphinx) -> None:
    """ビルド開始時に本文で使う図を _generated に出力する。"""
    import make_figures

    make_figures.generate(GENERATED_DIR)


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", generate_figures)
