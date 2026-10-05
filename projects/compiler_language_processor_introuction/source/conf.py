# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, os.path.abspath("_ext"))

# -- サンプルコードの ZIP ファイルを作る ---------------------------------------
# 付録 A からダウンロードできるように、examples の中身を ZIP にまとめる。

_source_dir = Path(__file__).resolve().parent
_examples = _source_dir.parent / "examples"
_zip_path = _source_dir / "_generated" / "tiny_examples.zip"
_zip_path.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(_zip_path, "w", zipfile.ZIP_DEFLATED) as _zip:
    for _file in sorted([*_examples.glob("*.py"),
                         *_examples.glob("programs/*.tiny")]):
        _zip.write(_file, Path("tiny_examples") / _file.relative_to(_examples))

# -- Project information -----------------------------------------------------

project = "コンパイラ・言語処理系入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "tinylexer",  # Tiny 言語の構文の強調表示（_ext/tinylexer.py）
]

templates_path = ["_templates"]
exclude_patterns = []

language = "ja"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- Options for Graphviz ----------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=sans-serif",
    "-Nfontname=sans-serif",
    "-Efontname=sans-serif",
]
