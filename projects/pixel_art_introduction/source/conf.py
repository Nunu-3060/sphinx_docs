# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------

project = "ドット絵作成入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

language = "ja"
exclude_patterns = ["_figures", "_generated"]
numfig = True
numfig_format = {"figure": "図 %s", "table": "表 %s", "code-block": "リスト %s"}

graphviz_output_format = "svg"
graphviz_dot_args = ["-Gfontname=Meiryo", "-Nfontname=Meiryo", "-Efontname=Meiryo"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ソースを表示」のリンクを出さない
html_copy_source = False      # rst ファイルを出力先にコピーしない
html_theme_options = {"navigation_depth": 3}

# -- 図の生成 -----------------------------------------------------------------

SOURCE_DIR = Path(__file__).resolve().parent


def generate_figures(app: Sphinx) -> None:
    """ビルドの開始時に本文で使う図を生成する。"""
    sys.path.insert(0, str(SOURCE_DIR / "_figures"))
    import make_figures

    make_figures.generate_all(SOURCE_DIR / "_generated")


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", generate_figures)
