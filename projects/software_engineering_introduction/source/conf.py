# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "ソフトウェア工学入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # build/html/.nojekyll を出力する
    "sphinx.ext.graphviz",
]

language = "ja"

exclude_patterns: list[str] = []
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
}

# -- Options for Graphviz ----------------------------------------------------
# 図は PNG で出力し、閲覧環境のフォントに左右されないようにする。
# 配色は source/figures/make_figures.py で生成する図と共通にしている。

graphviz_output_format = "png"
graphviz_dot_args = [
    "-Gdpi=144",
    "-Gfontname=Meiryo",
    "-Gbgcolor=white",
    "-Nfontname=Meiryo",
    "-Nfontsize=12",
    "-Nshape=box",
    "-Nstyle=rounded,filled",
    "-Nfillcolor=#e3eefb",
    "-Ncolor=#2a78d6",
    "-Npenwidth=1.5",
    "-Efontname=Meiryo",
    "-Efontsize=11",
    "-Ecolor=#52514e",
    "-Efontcolor=#52514e",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_copy_source = False  # rst を _sources/ にコピーしない
html_search_language = "ja"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
