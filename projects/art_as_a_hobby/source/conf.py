# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx

# 図の生成スクリプトを読み込めるようにする
_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR / '_scripts'))

# -- Project information -----------------------------------------------------

project = '趣味としての芸術'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.graphviz',
]

exclude_patterns = ['_scripts', 'Thumbs.db', '.DS_Store']

language = 'ja'

numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'リスト %s',
}

# -- Options for Graphviz ----------------------------------------------------

graphviz_output_format = 'svg'
graphviz_dot_args = [
    '-Gfontname=Meiryo',
    '-Nfontname=Meiryo',
    '-Efontname=Meiryo',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_title = '趣味としての芸術'

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Figure generation -------------------------------------------------------


def _generate_figures(app: Sphinx) -> None:
    """HTML のビルド開始時に、本文で使う図を images に生成する."""
    if app.builder.format != 'html':
        return
    import generate_figures
    generate_figures.main()


def setup(app: Sphinx) -> None:
    app.connect('builder-inited', _generate_figures)
