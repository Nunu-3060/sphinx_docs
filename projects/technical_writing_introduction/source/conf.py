# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Figures generated at build time -----------------------------------------
# matplotlib の図は _scripts/make_figures.py で生成し、_generated/ に出力する。
# Graphviz の図は sphinx.ext.graphviz がビルド時に生成する。

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

import make_figures  # noqa: E402

make_figures.generate(SOURCE_DIR / "_generated")

# -- Project information -----------------------------------------------------

project = "技術文書の書き方"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
exclude_patterns = ["_scripts"]

numfig = True

graphviz_output_format = "svg"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された html から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False


def remove_empty_sources_dir(app, exception):
    """html_copy_source = False でも空の _sources/ が作られるため、ビルド後に削除する。"""
    sources_dir = Path(app.outdir) / "_sources"
    if exception is None and sources_dir.is_dir() and not any(sources_dir.iterdir()):
        sources_dir.rmdir()


def setup(app):
    app.connect("build-finished", remove_empty_sources_dir)
