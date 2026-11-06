# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'numpy/pandas/matplotlib 入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.githubpages',
    'matplotlib.sphinxext.plot_directive',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_copy_source = False
html_show_sourcelink = False

# -- Options for matplotlib plot_directive ------------------------------------
# .. plot:: が生成する図に "Source code" へのダウンロードリンクを付けない
plot_html_show_source_link = False


# -- Line numbers for code examples -------------------------------------------
# code-block だけでなく、plot ディレクティブの :include-source: が生成する
# コードにも行番号を付けるため、すべての literal_block に linenos を設定する。

def _add_linenos(app, doctree):
    from docutils import nodes

    for node in doctree.findall(nodes.literal_block):
        node['linenos'] = True


def setup(app):
    app.connect('doctree-read', _add_linenos)
