# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

import figures  # noqa: E402

# -- Project information -----------------------------------------------------

project = "代表的な Linux ディストリビューション"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
templates_path: list[str] = []
exclude_patterns = ["_scripts"]

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
}

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Yu Gothic",
    "-Nfontname=Yu Gothic",
    "-Efontname=Yu Gothic",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

# -- Figures -----------------------------------------------------------------

# matplotlib の図をビルドの度に生成する
figures.generate(SOURCE_DIR / "_generated")
