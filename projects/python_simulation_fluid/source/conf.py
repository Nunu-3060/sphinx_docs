# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import zipfile
from pathlib import Path

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python による流体・粒子シミュレーション入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 数式を表示する。
    'sphinx.ext.mathjax',
    # アルゴリズムの流れ図を Graphviz で描く。
    'sphinx.ext.graphviz',
    # GitHub Pages で公開できるように .nojekyll を出力する。
    'sphinx.ext.githubpages',
]

exclude_patterns = ['Thumbs.db', '.DS_Store', '_scripts', '_generated']

language = 'ja'

# 図表番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'リスト %s',
}

# Graphviz の図は SVG で出力する(拡大しても文字がつぶれない)。
graphviz_output_format = 'svg'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された html から rst ソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- サンプルコードの zip ファイルの作成 -------------------------------------
# examples/ のサンプルコード一式を zip にまとめ、html からダウンロードできるようにする。
# zip はビルドのたびに作り直し、本文からは :download: で参照する。

_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / 'examples'
_GENERATED = Path(__file__).resolve().parent / '_generated'


def _make_examples_zip() -> None:
    _GENERATED.mkdir(exist_ok=True)
    files = sorted(_EXAMPLES.glob('*.py')) + [_EXAMPLES / 'setup.cfg']
    with zipfile.ZipFile(_GENERATED / 'examples.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path('examples') / path.name)


_make_examples_zip()
