# Configuration file for the Sphinx documentation builder.
#
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = 'Unity アニメーション入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    # .nojekyll を出力する（GitHub Pages で _static などのフォルダーを公開するため）
    'sphinx.ext.githubpages',
]

exclude_patterns = []

language = 'ja'

# サンプルコードの既定のハイライト言語
highlight_language = 'csharp'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = project

html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
}

# rst ソースを html から閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_show_sphinx = False
html_last_updated_fmt = '%Y-%m-%d'
