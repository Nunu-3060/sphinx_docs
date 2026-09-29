# Sphinx の設定ファイル
# https://www.sphinx-doc.org/ja/master/usage/configuration.html

# -- プロジェクト情報 ------------------------------------------------------

project = "Unity デバッグ・最適化入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 --------------------------------------------------------------

extensions = [
    # GitHub Pages 用に .nojekyll ファイルを出力する。
    "sphinx.ext.githubpages",
    # 数式を MathJax で表示する。
    "sphinx.ext.mathjax",
]

language = "ja"

exclude_patterns = []

# コードブロックの既定の言語
highlight_language = "csharp"

# -- HTML 出力の設定 -------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project

html_theme_options = {
    "navigation_depth": 3,
}

# 出力された HTML からソースの rst を閲覧できないようにする。
html_show_sourcelink = False
html_copy_source = False
