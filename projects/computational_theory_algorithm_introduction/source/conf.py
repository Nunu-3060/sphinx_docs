# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = '計算理論・アルゴリズム入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',      # 数式の表示
    'sphinx.ext.githubpages',  # .nojekyll の出力
]

exclude_patterns: list[str] = []

language = 'ja'

# 図・表・コードに番号を付ける
numfig = True

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_title = project

# rst ソースを HTML から閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 60
linkcheck_retries = 2
