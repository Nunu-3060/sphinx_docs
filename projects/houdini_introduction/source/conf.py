# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import pathlib
import subprocess
import sys
import zipfile

from pygments.lexer import inherit
from pygments.lexers.c_cpp import CLexer
from pygments.token import Name
from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Houdini 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"

version = "1.0"
release = "1.0"

# -- General configuration ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # 出力先に .nojekyll を作る
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# 図と表に番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {"figure": "図 %s", "table": "表 %s", "code-block": "コード %s"}

# コピーボタンで行番号やプロンプトをコピーしないようにする。
copybutton_exclude = ".linenos, .gp"

# -- Options for Graphviz -----------------------------------------------------

graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
    "-Gbgcolor=transparent",
]

# -- Options for linkcheck ----------------------------------------------------

linkcheck_timeout = 30

# -- Options for HTML output ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst のソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- VEX のシンタックスハイライト ------------------------------------------------


class VexLexer(CLexer):
    """VEX 用の簡易的なレキサー。

    Pygments には VEX のレキサーが無い。VEX は C に近い文法なので、C の
    レキサーに @P、v@scale のようなアトリビュートの記法だけを追加する。
    """

    name = "VEX"
    aliases = ["vex"]
    filenames = ["*.vex", "*.vfl"]
    tokens = {
        "statements": [
            (r"[fuvpis234d]?@[A-Za-z_][A-Za-z0-9_]*", Name.Variable),
            (r"\b(vector2|vector4|vector|matrix2|matrix3|matrix|string|dict|"
             r"foreach|export|function)\b", Name.Builtin),
            (r"\bPI\b", Name.Constant),
            inherit,
        ],
    }


# -- Generate figures ---------------------------------------------------------


def generate_figures(app: Sphinx) -> None:
    """source/_scripts/make_figures.py を実行し、図を _static/figures に保存する。"""
    src_dir = pathlib.Path(app.srcdir)
    figures_dir = src_dir / "_static" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    subprocess.run(
        [sys.executable, str(src_dir / "_scripts" / "make_figures.py"), str(figures_dir)],
        cwd=src_dir / "_scripts",
        env=env,
        check=True,
        stdout=subprocess.DEVNULL,
    )


# -- Build examples.zip for download ------------------------------------------


def generate_examples_zip(app: Sphinx) -> None:
    """examples/ のスクリプト、VEX のコード、setup.cfg を examples.zip にまとめる。"""
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / "examples"
    output_dir = src_dir / "_static" / "downloads"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(examples_dir.glob("*.py")) + sorted((examples_dir / "vex").glob("*.vex"))
    files.append(examples_dir / "setup.cfg")
    with zipfile.ZipFile(output_dir / "examples.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=f"examples/{path.relative_to(examples_dir).as_posix()}")


def setup(app: Sphinx) -> None:
    app.add_lexer("vex", VexLexer)
    app.connect("builder-inited", generate_figures)
    app.connect("builder-inited", generate_examples_zip)
