# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import shutil
from pathlib import Path

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------

project = "HTML & CSS & JavaScript 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_ignore = [
    # examples フォルダーと ZIP ファイルはビルド後に出力先へコピーするため除外する
    r"^examples(/|\.zip$)",
    # W3C のサイトは linkcheck からのアクセスに 403 を返すため除外する
    # (ブラウザからは閲覧できることを確認済み)
    r"^https://(validator|www)\.w3\.org/",
]

# -- サンプルコードの配布 ----------------------------------------------------

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__", ".mypy_cache", "*.pyc"
)


def copy_examples(app: Sphinx, exception: Exception | None) -> None:
    """examples フォルダーを出力先にコピーし、ZIP ファイルも作成する."""
    if exception is not None or app.builder.format != "html":
        return
    out_dir = Path(app.outdir)
    # html_copy_source = False でも空の _sources フォルダーが作られるため削除する
    shutil.rmtree(out_dir / "_sources", ignore_errors=True)
    dest = out_dir / "examples"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(EXAMPLES_DIR, dest, ignore=IGNORE_PATTERNS)
    shutil.make_archive(
        str(out_dir / "examples"),
        "zip",
        root_dir=out_dir,
        base_dir="examples",
    )


def setup(app: Sphinx) -> None:
    app.connect("build-finished", copy_examples)
