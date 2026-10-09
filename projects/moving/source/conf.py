# Configuration file for the Sphinx documentation builder.

project = '引越し手続きガイド'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

language = 'ja'

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
    'matplotlib.sphinxext.plot_directive',
]

exclude_patterns: list[str] = []

# -- HTML 出力 ---------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = '引越し手続きガイド'

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = 'png'

# -- matplotlib plot ディレクティブ ------------------------------------------

plot_html_show_source_link = False
plot_html_show_formats = False
plot_include_source = False
plot_formats = [('png', 120)]
