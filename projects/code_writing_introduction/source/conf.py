# Sphinx の設定ファイル

project = '良いコード・悪いコード'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'

extensions = [
    'sphinx.ext.githubpages',  # GitHub Pages 用に .nojekyll を出力する
    'sphinx.ext.graphviz',
]

language = 'ja'
templates_path: list[str] = []
exclude_patterns: list[str] = []

# 図・表・コードに番号を付ける
numfig = True

# Graphviz
graphviz_output_format = 'svg'

# HTML 出力
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 3,
}
html_static_path: list[str] = []

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False
