"""Sphinx configuration for 薩摩焼酎入門."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_scripts"))

# -- Project information -----------------------------------------------------

project = "薩摩焼酎入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

language = "ja"
exclude_patterns = ["_scripts"]
numfig = True
numfig_format = {"figure": "図 %s", "table": "表 %s"}

graphviz_output_format = "svg"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_copy_source = False
html_show_sourcelink = False
html_theme_options = {
    "navigation_depth": 3,
}

# -- Figure generation -------------------------------------------------------


def generate_figures(app):
    """ビルド開始時に matplotlib の図を生成する。"""
    import make_figures

    make_figures.main(os.path.join(app.srcdir, "_images"))


def remove_empty_sources_dir(app, exception):
    """html_copy_source = False でも残る空の _sources フォルダを削除する。"""
    sources_dir = os.path.join(app.outdir, "_sources")
    if exception is None and os.path.isdir(sources_dir) and not os.listdir(sources_dir):
        os.rmdir(sources_dir)


def setup(app):
    app.connect("builder-inited", generate_figures)
    app.connect("build-finished", remove_empty_sources_dir)
