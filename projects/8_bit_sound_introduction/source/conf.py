# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx

# 図の生成スクリプトと、それが使う examples のモジュールを読み込めるようにする
_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR.parent / 'examples'))
sys.path.insert(0, str(_SOURCE_DIR / '_scripts'))

# -- Project information -----------------------------------------------------

project = '8 bit Game Sound 作成入門'
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

# -- Options for linkcheck ---------------------------------------------------

# 自動アクセスを拒否する（403 を返す）ため、linkcheck の対象外とするサイト。
linkcheck_ignore = [
    r'https://www\.nesdev\.org/.*',
    r'https://tech\.ebu\.ch/.*',
    r'https://laws\.e-gov\.go\.jp/.*',
]

# -- Audio and figure generation ---------------------------------------------


def _generate_audio(app: Sphinx) -> None:
    """HTML のビルド開始時に、本文に埋め込む音声を _static/audio に生成する."""
    if app.builder.format != 'html':
        return
    import make_all
    paths = make_all.generate_all(_SOURCE_DIR / '_static' / 'audio')
    print(f'generated: {len(paths)} audio files')


def _generate_figures(app: Sphinx) -> None:
    """HTML のビルド開始時に、本文で使う図を images に生成する."""
    if app.builder.format != 'html':
        return
    import generate_figures
    generate_figures.main()


def setup(app: Sphinx) -> None:
    # 登録した順に、音声、図の順で生成される
    app.connect('builder-inited', _generate_audio)
    app.connect('builder-inited', _generate_figures)
