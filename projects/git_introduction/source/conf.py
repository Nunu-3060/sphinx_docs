# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Git 入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',  # .nojekyll を出力する
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

html_search_language = 'ja'
