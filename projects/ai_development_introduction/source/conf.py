# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

project = "AI を用いた開発"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "コード %s",
}

# -- 図の生成 ---------------------------------------------------------------

# matplotlib の図はビルドのたびに source/_generated/ に生成する
_here = Path(__file__).resolve().parent
sys.path.insert(0, str(_here / "figures"))
import context_budget  # noqa: E402

context_budget.make(_here / "_generated" / "context_budget.png")

# -- HTML 出力 --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "AI を用いた開発"
html_last_updated_fmt = "%Y-%m-%d"

# rst ソースを HTML から閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
html_context = {
    "display_github": False,
}

# -- Graphviz ---------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- linkcheck --------------------------------------------------------------

linkcheck_timeout = 30
