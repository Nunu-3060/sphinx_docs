# Configuration file for the Sphinx documentation builder.

project = "Claude 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "matplotlib.sphinxext.plot_directive",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "コード %s",
}

# -- HTML 出力 --------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "Claude 入門"
html_last_updated_fmt = "%Y-%m-%d"

# rst ソースを HTML から閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
html_context = {
    "display_github": False,
}

# -- Graphviz ---------------------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- matplotlib plot ディレクティブ -----------------------------------------

plot_include_source = False
plot_html_show_source_link = False
plot_html_show_formats = False
plot_formats = [("png", 150)]
plot_rcparams = {
    "font.family": ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"],
    "axes.unicode_minus": False,
}

# -- linkcheck --------------------------------------------------------------

# claude.ai は自動アクセスに 403 を返すため、リンク確認の対象から外す
linkcheck_ignore = [r"https://claude\.ai/$"]
