# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.machinery
import subprocess
import sys
from pathlib import Path

# autodoc が script 以下のモジュールを import できるようにする
script: Path = Path(__file__).resolve().parent.parent.joinpath("script")
sys.path.insert(0, str(script))

# html ビルド前に png 画像を出力する。
#subprocess.run([sys.executable, str(script.joinpath("lifegame_fullHD_0000.py"))])

# autodoc が LifeGameGUI.pyw を通常の import 文で読み込めるようにする
importlib.machinery.SOURCE_SUFFIXES.append('.pyw')

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python によるライフゲームの実装'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_copy_source = False
html_show_sourcelink = False

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    'PIL': ('https://pillow.readthedocs.io/en/stable/', None),
}
