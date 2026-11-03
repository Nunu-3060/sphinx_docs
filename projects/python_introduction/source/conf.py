"""Sphinx configuration file for the "Python 入門" documentation."""

project = "Python 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

language = "ja"

extensions = []

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

highlight_language = "python3"

html_theme = "sphinx_rtd_theme"
# Copy source/_extra/.nojekyll to the output so that GitHub Pages serves the files as is.
html_extra_path = ["_extra"]

# Do not publish the rst sources with the HTML pages.
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
    "titles_only": False,
}
