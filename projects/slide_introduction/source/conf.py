# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import logging

# 図の生成スクリプトと Marp の変換スクリプトを読み込めるようにする
_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR / '_scripts'))

logger = logging.getLogger(__name__)

# -- Project information -----------------------------------------------------

project = 'スライド作成・プレゼンテーション入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
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
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_copy_source = False  # _sources に rst をコピーしない

# -- Figure and Marp sample generation ---------------------------------------


def _generate_figures(app: Sphinx) -> None:
    """HTML のビルド開始時に、本文で使う図を images に生成する."""
    if app.builder.format != 'html':
        return
    import generate_figures
    generate_figures.main()


def _convert_marp(app: Sphinx) -> None:
    """HTML のビルド開始時に、Marp のサンプルを HTML / PDF / PNG に変換する.

    marp-cli が見つからない、または変換に失敗した場合は、警告を出してビルドを続ける。
    """
    if app.builder.format != 'html':
        return
    import convert_marp
    try:
        outputs = convert_marp.convert_all()
    except convert_marp.MarpError as exc:
        logger.warning('Marp のサンプルを変換できなかった: %s', exc)
        return
    print(f'converted: {len(outputs)} Marp output files')


def setup(app: Sphinx) -> None:
    app.connect('builder-inited', _generate_figures)
    app.connect('builder-inited', _convert_marp)
