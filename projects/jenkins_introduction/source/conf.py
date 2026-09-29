# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import zipfile

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Jenkins & Jenkins Pipeline 入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
]

# 執筆中は TODO を出力に表示する（完成稿では False にする）
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# セクション名の重複による警告を避けるため、ドキュメントごとに一意なラベルにする
autosectionlabel_prefix_document = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_copy_source = False
html_show_sourcelink = False

highlight_language = 'groovy'

# -- sample-app を一括ダウンロード可能な zip にまとめる ------------------------
# sample-app/ はドキュメントのソースツリー外（プロジェクトルート）にあるため、
# ビルドのたびに sample-app.zip を作り直し、:download: から参照できるようにする。

_SAMPLE_APP_EXCLUDE_DIRS = {'.git', '__pycache__', '.pytest_cache', '.ruff_cache', '.venv'}
_SAMPLE_APP_EXCLUDE_FILES = {'app.tar.gz'}


def _zip_sample_app(app):
    project_root = os.path.dirname(str(app.srcdir))
    sample_dir = os.path.join(project_root, 'sample-app')
    if not os.path.isdir(sample_dir):
        return

    zip_path = os.path.join(project_root, 'sample-app.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(sample_dir):
            dirs[:] = [d for d in dirs if d not in _SAMPLE_APP_EXCLUDE_DIRS]
            for filename in files:
                if filename in _SAMPLE_APP_EXCLUDE_FILES:
                    continue
                full_path = os.path.join(root, filename)
                arcname = os.path.join('sample-app', os.path.relpath(full_path, sample_dir))
                zf.write(full_path, arcname)


def setup(app):
    app.connect('builder-inited', _zip_sample_app)
