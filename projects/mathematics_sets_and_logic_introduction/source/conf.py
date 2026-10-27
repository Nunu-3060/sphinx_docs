# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

from make_figures import make_all  # noqa: E402

# ビルドのたびに matplotlib の図を生成する。
make_all(SOURCE_DIR / "_figures")

# -- Project information -----------------------------------------------------

project = "論理・集合入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
exclude_patterns = ["_build", "_scripts"]

graphviz_output_format = "svg"

# 数式は MathJax の SVG 出力で表示する（Web フォントの読み込みに依存しない）。
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された html から rst のソースを閲覧できないようにする。
html_show_sourcelink = False
html_copy_source = False
