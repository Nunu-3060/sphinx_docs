# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "マネジメント入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # GitHub Pages 用に .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

language = "ja"

templates_path = ["_templates"]
exclude_patterns = ["figures/*.py"]

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 章",
}

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "png"
graphviz_dot_args = [
    "-Gfontname=Noto Sans JP",
    "-Nfontname=Noto Sans JP",
    "-Efontname=Noto Sans JP",
    "-Gdpi=110",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "マネジメント入門"

# 出力された html から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
