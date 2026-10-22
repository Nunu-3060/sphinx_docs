# Configuration file for the Sphinx documentation builder.

project = '東京名所案内'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

language = 'ja'

extensions = [
    'sphinx.ext.githubpages',  # .nojekyll を出力する
    'sphinx.ext.graphviz',
    'matplotlib.sphinxext.plot_directive',
]

exclude_patterns: list[str] = []

# -- HTML 出力 ---------------------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = '東京名所案内'

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

# -- リンクの検査（sphinx -b linkcheck） -------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# 自動のアクセスを拒否する（403 を返す）が、ブラウザでは閲覧できるサイト
linkcheck_ignore = [
    r'https://www\.suntory\.co\.jp/sma/',
    r'https://www\.tokyometro\.jp/',
]
