"""暗号理論入門 の Sphinx 設定ファイル。"""

import sys
from pathlib import Path

from sphinx.application import Sphinx

SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE_DIR / "figures"))

import make_figures  # noqa: E402

# -- プロジェクト情報 -----------------------------------------------------

project = "暗号理論入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
templates_path: list[str] = []
exclude_patterns = ["_build", "figures"]
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
}
math_numfig = True
# Web フォントに依存せず表示が崩れにくい SVG 出力を使う
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"

# -- Graphviz -------------------------------------------------------------

graphviz_output_format = "png"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
    "-Gfontsize=12",
    "-Nfontsize=12",
    "-Efontsize=11",
]

# -- HTML 出力 ------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_show_sourcelink = False  # rst へのリンクを表示しない
html_copy_source = False  # rst を _sources にコピーしない
html_search_language = "ja"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- linkcheck ------------------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2


def _generate_figures(app: Sphinx) -> None:
    """ビルド開始時に matplotlib / Pillow の図を生成する。"""
    make_figures.generate_all(SOURCE_DIR / "_generated")


def _remove_empty_sources(app: Sphinx, exception: Exception | None) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダを削除する。"""
    sources = Path(app.outdir) / "_sources"
    if exception is None and sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", _generate_figures)
    app.connect("build-finished", _remove_empty_sources)
