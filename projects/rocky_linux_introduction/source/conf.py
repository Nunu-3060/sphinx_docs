# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "Rocky Linux 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    # .nojekyll を出力する
    "sphinx.ext.githubpages",
    # 数式を表示する
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# 図表番号を付ける
numfig = True

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "Rocky Linux 入門"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
# docs.redhat.com は自動アクセスに対して常に 403 を返すため、検査から除外する
# (旧 URL の access.redhat.com からの転送先として、URL が存在することを確認済み)
linkcheck_ignore = [
    r"https://docs\.redhat\.com/.*",
]
