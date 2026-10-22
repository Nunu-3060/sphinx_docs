# Sphinx 設定ファイル
# 詳細: https://www.sphinx-doc.org/ja/master/usage/configuration.html

# -- プロジェクト情報 ---------------------------------------------------------
project = "正規表現入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -----------------------------------------------------------------
extensions = [
    "sphinx.ext.githubpages",  # GitHub Pages 用に .nojekyll を出力する
    "sphinx.ext.graphviz",
]

language = "ja"
exclude_patterns: list[str] = []
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 章",
}

# -- Graphviz -----------------------------------------------------------------
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- HTML 出力 ----------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_copy_source = False  # rst ソースを _sources に複製しない
html_search_language = "ja"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- linkcheck ----------------------------------------------------------------
linkcheck_timeout = 30
linkcheck_retries = 2
