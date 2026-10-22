# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Figures -----------------------------------------------------------------
# matplotlib で描く図はビルドのたびに生成し直す。
_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR / "_scripts"))

import make_figures  # noqa: E402

make_figures.generate(_SOURCE_DIR / "figures")

# -- Project information -----------------------------------------------------

project = "代表的なプログラミング言語の概要・歴史・比較"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
version = "1.0"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # GitHub Pages 用に .nojekyll を出力する
    "sphinx.ext.graphviz",
]

language = "ja"
exclude_patterns: list[str] = ["_scripts"]
numfig = True
highlight_language = "none"

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_search_language = "ja"

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
