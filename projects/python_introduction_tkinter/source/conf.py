"""Sphinx の設定ファイルです。

設定項目の一覧は次を参照してください。
https://www.sphinx-doc.org/ja/master/usage/configuration.html
"""

import sys
from pathlib import Path

# ローカルの拡張 (_ext フォルダー) を読み込めるようにします
sys.path.insert(0, str(Path(__file__).parent / "_ext"))
sys.dont_write_bytecode = True  # _ext に __pycache__ を作らないようにします

# -- プロジェクト情報 ---------------------------------------------------------

project = "Python tkinter 解説"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力します
    "sphinx.ext.mathjax",  # 数式を表示します
    "sphinx_copybutton",  # コードブロックにコピーボタンを付けます
    "screenshot",  # サンプルコードのスクリーンショットを撮影します
]

language = "ja"
exclude_patterns: list[str] = []

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]  # 表のセルを折り返すための調整
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# 出力された HTML から rst ソースを閲覧できないようにします
html_show_sourcelink = False
html_copy_source = False

# -- スクリーンショットの設定 (_ext/screenshot.py) -----------------------------

# "auto": 画像がない場合と、サンプルコードが画像より新しい場合に撮影します
# "always": すべて撮影し直します
# "never": 撮影しません
# 環境変数 SCREENSHOT_MODE を設定すると、この値より優先されます
screenshot_mode = "auto"
screenshot_examples_dir = "../examples"
screenshot_output_dir = "images"
