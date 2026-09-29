# sphinx-quickstart が生成する conf.py に、型ヒントを追加したものです。
#
# 設定値の一覧は次のページを参照してください。
# https://www.sphinx-doc.org/ja/master/usage/configuration.html

# -- プロジェクト情報 --------------------------------------------------------

project: str = "demo"
copyright: str = "2026, author"
author: str = "author"
release: str = "0.1"

# -- 一般設定 ----------------------------------------------------------------

extensions: list[str] = []

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

language: str = "ja"

# -- HTML 出力の設定 ---------------------------------------------------------

html_theme: str = "alabaster"
html_static_path: list[str] = ["_static"]
