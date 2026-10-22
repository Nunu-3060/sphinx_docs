# Configuration file for the Sphinx documentation builder.

project = '解析学入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'
version = '1.0'

language = 'ja'

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
    'sphinx.ext.githubpages',
]

templates_path: list[str] = []
exclude_patterns: list[str] = []

# 図・表・コード・数式に章番号付きの番号を振る
numfig = True
numfig_secnum_depth = 1
math_numfig = True
math_eqref_format = '({number})'

# Graphviz
graphviz_output_format = 'svg'
_graphviz_fonts = 'Noto Sans JP, Yu Gothic, Meiryo'
graphviz_dot_args = [
    f'-Gfontname={_graphviz_fonts}',
    f'-Nfontname={_graphviz_fonts}',
    f'-Efontname={_graphviz_fonts}',
]

# HTML
html_theme = 'sphinx_rtd_theme'
html_title = '解析学入門'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_show_sourcelink = False
html_copy_source = False
html_theme_options = {
    'navigation_depth': 3,
}
