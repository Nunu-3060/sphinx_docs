# Sphinx の設定ファイル
#
# 設定項目の一覧は次を参照:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- プロジェクト情報 ---------------------------------------------------------

project = "計算機科学入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",      # 数式の表示
    "sphinx.ext.githubpages",  # .nojekyll の出力
]

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = []

# 図表番号は使用しない (章・節番号は index.rst の toctree で付ける)
numfig = False

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "計算機科学入門"
html_static_path: list[str] = []

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "navigation_depth": 3,
    "prev_next_buttons_location": "both",
}

html_search_language = "ja"

# -- linkcheck の設定 ---------------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
