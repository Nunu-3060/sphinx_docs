# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
sys.path.insert(0, str(_here / "_scripts"))

from make_figures import generate_all  # noqa: E402

# matplotlib の図をビルドのたびに生成する
generate_all(_here / "figures")

# -- Project information -----------------------------------------------------

project = "自作 PC 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
]

language = "ja"
exclude_patterns = ["_scripts"]
numfig = True

graphviz_output_format = "svg"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"

# rst ソースを html から閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_static_path = ["_static"]
html_css_files = ["custom.css"]
