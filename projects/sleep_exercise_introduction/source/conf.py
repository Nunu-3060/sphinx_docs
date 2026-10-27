# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx

# 図の生成スクリプトと、それが使う examples のモジュールを読み込めるようにする。
# examples に __pycache__ が作られないよう、バイトコードは書き出さない。
sys.dont_write_bytecode = True
_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR.parent / 'examples'))
sys.path.insert(0, str(_SOURCE_DIR / '_scripts'))

# -- Project information -----------------------------------------------------

project = '睡眠・姿勢・運動入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_scripts', 'Thumbs.db', '.DS_Store']

language = 'ja'

# 図・表・コードに番号を付ける
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
html_title = '睡眠・姿勢・運動入門'

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# 自動アクセスを拒否する（403 を返す）ため、linkcheck の対象外とするリンク。
# DOI から出版社のページへ転送されることは確認済みである（転送先が 403 を返す）。
linkcheck_ignore = [
    r'https://doi\.org/10\.1002/ejsp\.674',
]

# -- Figure generation -------------------------------------------------------


def _generate_figures(app: Sphinx) -> None:
    """HTML のビルド開始時に、本文で使う図を figures に生成する."""
    if app.builder.format != 'html':
        return
    import generate_figures
    paths = generate_figures.main()
    print(f'generated: {len(paths)} figures')


def setup(app: Sphinx) -> None:
    app.connect('builder-inited', _generate_figures)
