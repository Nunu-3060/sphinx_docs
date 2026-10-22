"""Sphinx の設定ファイル。"""

import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

from make_figures import make_all  # noqa: E402

# -- プロジェクト情報 --------------------------------------------------------

project = "茨城名所案内"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
language = "ja"

# -- 一般設定 ----------------------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
]

exclude_patterns = ["_scripts"]

# Graphviz の図は PNG で出力し、日本語フォントを指定する。
graphviz_output_format = "png"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
    "-Gdpi=110",
]

linkcheck_timeout = 30
linkcheck_retries = 2

# -- HTML 出力 ---------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された HTML から rst ソースを閲覧できないようにする。
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "navigation_depth": 3,
}

# -- 図の生成 ----------------------------------------------------------------

# ビルドのたびに matplotlib の図を source/_figures に出力する。
make_all(SOURCE_DIR / "_figures")
