# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Project information -----------------------------------------------------

project = '機械学習・深層学習入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
    'sphinx.ext.githubpages',  # .nojekyll を出力する
]

exclude_patterns = ['_figures']

language = 'ja'

# 数式は Web フォントに依存しない SVG 出力で描画する
mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-svg.js'

numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'コード %s',
    'section': '%s 章',
}

# -- Options for Graphviz ----------------------------------------------------

graphviz_output_format = 'png'
graphviz_dot_args = [
    '-Gfontname=Meiryo',
    '-Nfontname=Meiryo',
    '-Efontname=Meiryo',
    '-Gdpi=110',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = project
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された html から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Figures generated at build time -----------------------------------------

_SOURCE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SOURCE_DIR / '_figures'))

import generate_figures  # noqa: E402

generate_figures.generate_all(_SOURCE_DIR / '_generated')
