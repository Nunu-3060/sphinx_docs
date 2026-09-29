# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.machinery
import os
import sys

# script/ 配下のモジュールを autodoc から参照できるようにする。
# (このファイルは source/ に置かれているため、python_sand/script まで1階層上がる)
sys.path.insert(0, os.path.abspath('../script'))

# script/ 以下には SandGUI.pyw のように拡張子が .pyw のモジュールが存在する。
# Python の標準的な import 機構は .py 以外のソースファイルを解決できないため、
# 標準の拡張モジュール・バイトコード用ローダーはそのまま残しつつ、ソースファイル
# 用ローダーの対象拡張子に .pyw を加えた path hook を登録し、autodoc から
# `automodule:: SandGUI` のように参照できるようにする。
# (SourceFileLoader だけを差し替えると、他ディレクトリの .pyd 等の拡張モジュール
#  まで解決できなくなり tkinter 等の import が壊れるため、3種のローダーをまとめて
#  登録している)
_pyw_loader_details = [
    (importlib.machinery.ExtensionFileLoader, importlib.machinery.EXTENSION_SUFFIXES),
    (importlib.machinery.SourceFileLoader, importlib.machinery.SOURCE_SUFFIXES + ['.pyw']),
    (importlib.machinery.SourcelessFileLoader, importlib.machinery.BYTECODE_SUFFIXES),
]
sys.path_hooks.insert(
    0,
    importlib.machinery.FileFinder.path_hook(*_pyw_loader_details),
)
sys.path_importer_cache.clear()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python による飛砂のシミュレーションの実装'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    # 各モジュールのソースコードを html 上で閲覧できるようにする
    # ([source] リンクが自動で追加される)。
    'sphinx.ext.viewcode',
    # モデルの数式を表示するために使用する(数式の使用が許可されているため)。
    'sphinx.ext.mathjax',
    # GitHub Pages で公開できるように .nojekyll を出力する。
    'sphinx.ext.githubpages',
]

# script/ 内のクラス・関数には docstring が無い。
# automodule + :members: だけでは docstring の無いメンバーは(基底クラスから
# docstring を継承できるものを除いて)一覧から丸ごと除外されてしまうため、
# :undoc-members: を既定で有効にし、docstring の有無に関わらず全メンバーを
# 一覧に載せるようにする。
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
}

templates_path = ['_templates']
exclude_patterns = ['Thumbs.db', '.DS_Store']

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Read the Docs テーマを使用する。
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 出力された html から rst ソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False
