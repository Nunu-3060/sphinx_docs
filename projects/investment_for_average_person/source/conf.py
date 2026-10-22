# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Project information -----------------------------------------------------

project = '一般人のための投資入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
]

exclude_patterns: list[str] = ['_scripts']

language = 'ja'

# 図・表に番号を付ける
numfig = True

# -- Figures -----------------------------------------------------------------

# ビルドのたびに matplotlib の図を source/figures に作成する
sys.path.insert(0, str(Path(__file__).resolve().parent / '_scripts'))
import make_figures  # noqa: E402

make_figures.main()

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
html_title = f'{project} {release}'
html_search_language = 'ja'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# 自動アクセスを 403・429・503 で拒否するが、ブラウザーでは閲覧できるサイト
linkcheck_ignore = [
    r'https://www\.dic\.go\.jp/',
    r'https://www\.gov-online\.go\.jp/',
    r'https://www\.j-flec\.go\.jp/',
    r'https://www\.jsda\.or\.jp/',
    r'https://www\.nta\.go\.jp/',
    # Python の SSL ライブラリとの TLS ハンドシェイクに失敗するが、ブラウザーでは閲覧できるサイト
    r'https://www\.ideco-koushiki\.jp/',
]
