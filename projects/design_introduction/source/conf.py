# Sphinx の設定ファイル
#
# 設定項目の一覧:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- プロジェクト情報 ---------------------------------------------------------

project = "デザイン入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",  # 数式を MathJax で表示する
    "sphinx.ext.githubpages",  # 出力先に .nojekyll を作成する
    "sphinx_copybutton",  # コードブロックにコピーボタンを付ける
]

language = "ja"
exclude_patterns: list[str] = []

# 図・表・コードに番号を付ける
numfig = True

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "デザイン入門"

# rst ソースを HTML から閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False
