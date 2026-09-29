# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import subprocess
import sys
import zipfile

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "色彩設計入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"

version = "1.0"
release = "1.0"

# -- General configuration ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # 出力先に .nojekyll を作る
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# 図に番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {"figure": "図 %s", "table": "表 %s", "code-block": "コード %s"}

# -- Options for HTML output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst のソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- Generate figures from examples/ ------------------------------------------

# 図を作るスクリプト。palette.py は ui_colors.py と print_colors.py から
# 読み込まれるだけでなく、自身も図を作る。color_utils.py は共通の関数だけを
# 定義している。
_FIGURE_SCRIPTS = [
    "color_basics.py",
    "color_spaces.py",
    "harmony.py",
    "palette.py",
    "dataviz.py",
    "accessibility.py",
    "ui_colors.py",
    "print_colors.py",
]


def generate_figures(app: Sphinx) -> None:
    """examples/ 以下のスクリプトを実行し、図を _static/figures に保存する。

    各スクリプトは、コマンドライン引数で受け取ったディレクトリに画像を
    保存する。
    """
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / "examples"
    figures_dir = src_dir / "_static" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               PYTHONDONTWRITEBYTECODE="1")
    for name in _FIGURE_SCRIPTS:
        subprocess.run(
            [sys.executable, str(examples_dir / name), str(figures_dir)],
            cwd=examples_dir,
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
        )


# -- Build examples.zip for download ------------------------------------------


def generate_examples_zip(app: Sphinx) -> None:
    """examples/ 以下の .py ファイルを _static/downloads/examples.zip にまとめる。"""
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / "examples"
    output_dir = src_dir / "_static" / "downloads"
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_dir / "examples.zip", "w",
                         zipfile.ZIP_DEFLATED) as zf:
        for py_file in sorted(examples_dir.glob("*.py")):
            zf.write(py_file, arcname=f"examples/{py_file.name}")


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", generate_figures)
    app.connect("builder-inited", generate_examples_zip)
