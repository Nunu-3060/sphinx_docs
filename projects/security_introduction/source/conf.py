# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "セキュリティ入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "セキュリティ入門"

# 出力した HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
