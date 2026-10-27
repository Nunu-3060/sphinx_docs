# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

# -- 図の生成 -----------------------------------------------------------------
# ビルドのたびに matplotlib で図を生成し、source/_generated に出力する。

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))

import figures  # noqa: E402

figures.generate_all(SOURCE_DIR / "_generated")

# -- Project information -----------------------------------------------------

project = "グラフ理論入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
exclude_patterns = ["_scripts"]

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 節",
}

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "navigation_depth": 3,
}


def _remove_empty_sources_dir(app, exception):
    """html_copy_source = False でも作られる空の _sources フォルダを削除する。"""
    if exception is None and app.builder.format == "html":
        sources_dir = Path(app.outdir) / "_sources"
        if sources_dir.is_dir() and not any(sources_dir.iterdir()):
            sources_dir.rmdir()


def setup(app):
    app.connect("build-finished", _remove_empty_sources_dir)
