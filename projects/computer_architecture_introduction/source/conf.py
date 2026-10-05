# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import shutil
from pathlib import Path

# -- Project information -----------------------------------------------------

project = "コンピューターアーキテクチャ入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",  # 数式を表示する
    "sphinx.ext.graphviz",  # 図を描く
]

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = []

# 図・表・コードブロックに番号を付ける
numfig = True

# -- Graphviz ----------------------------------------------------------------

# 図は拡大しても劣化しない SVG で出力する
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=sans-serif",
    "-Nfontname=sans-serif",
    "-Efontname=sans-serif",
]

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(
        os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin"
    )
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# rst ソースを HTML から閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
