# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = '健康的な生活'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
]

templates_path = ['_templates']
exclude_patterns: list[str] = ['_scripts']

language = 'ja'

# 図・表に番号を付ける
numfig = True

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
html_static_path = ['_static']
html_css_files = ['custom.css']
html_title = '健康的な生活'

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
