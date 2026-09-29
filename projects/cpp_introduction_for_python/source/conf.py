# Configuration file for the Sphinx documentation builder.

project = 'C++ 入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.mathjax',
]

language = 'ja'
exclude_patterns = []

highlight_language = 'cpp'

# -- HTML 出力 ---------------------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'C++ 入門'

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
}
