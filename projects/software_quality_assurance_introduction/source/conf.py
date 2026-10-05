# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "ソフトウェア品質保証入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # .nojekyll を出力します。
]

exclude_patterns: list[str] = []

language = "ja"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された HTML から rst ソースを閲覧できないようにします。
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
