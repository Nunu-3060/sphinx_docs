# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "_scripts"))
sys.path.insert(0, str(SOURCE_DIR.parent / "examples"))

# -- Project information -----------------------------------------------------

project = "税金と社会保険のしくみ"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

language = "ja"
exclude_patterns = ["_scripts", "_generated"]


# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Yu Gothic",
    "-Nfontname=Yu Gothic",
    "-Efontname=Yu Gothic",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "税金と社会保険のしくみ"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_copy_source = False  # _sources に rst をコピーしない
html_last_updated_fmt = "%Y-%m-%d"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- Linkcheck ---------------------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
# Python の TLS 設定では接続できないが、ブラウザ・curl では閲覧できることを確認済み
linkcheck_ignore = [r"https://www\.ideco-koushiki\.jp/"]


# -- Figure generation -------------------------------------------------------

def _generate_figures(app: object) -> None:
    """ビルド開始時に matplotlib の図を生成する。"""
    import make_figures

    make_figures.main(SOURCE_DIR / "_generated")


def setup(app):  # type: ignore[no-untyped-def]
    app.connect("builder-inited", _generate_figures)
