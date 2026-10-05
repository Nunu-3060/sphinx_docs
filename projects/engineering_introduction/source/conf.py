# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = '工学入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',      # 数式を MathJax で表示する
    'sphinx.ext.githubpages',  # 出力先に .nojekyll を作成する
]

exclude_patterns: list[str] = []
language = 'ja'

# 図・表・コードに番号を付け、:numref: で参照できるようにする
numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'リスト %s',
}

# 数式に番号を付けるときの書式
math_numfig = True
math_eqref_format = '式 ({number})'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = f'{project} {release}'
html_search_language = 'ja'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力した HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# 自動アクセスを 403 で拒否するが、ブラウザーでは閲覧できるサイト
linkcheck_ignore = [
    r'https://www\.acm\.org/code-of-ethics',
    r'https://www\.gao\.gov/',
]
