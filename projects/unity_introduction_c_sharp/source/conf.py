# Configuration file for the Sphinx documentation builder.
#
# 「Unity C# 入門」の設定ファイルです。

import pathlib
import zipfile

# -- Project information -----------------------------------------------------

project = "Unity C# 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",      # 数式を表示する
]

language = "ja"
templates_path = []
exclude_patterns = []
highlight_language = "csharp"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# 出力された HTML から rst のソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# -- サンプルコード一式の zip ファイル ---------------------------------------
# examples フォルダーと .editorconfig をまとめた zip を作り、本文からダウンロードできるようにします。

_SOURCE_DIR = pathlib.Path(__file__).resolve().parent
_ROOT_DIR = _SOURCE_DIR.parent


def _make_examples_zip():
    examples_dir = _ROOT_DIR / "examples"
    output = _SOURCE_DIR / "_generated" / "unity_csharp_examples.zip"
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(examples_dir.rglob("*.cs")):
            archive.write(path, pathlib.Path("examples") / path.relative_to(examples_dir))
        archive.write(_ROOT_DIR / ".editorconfig", ".editorconfig")


_make_examples_zip()


# -- ビルド後の処理 ----------------------------------------------------------
# html_copy_source = False でも空の _sources フォルダーが作られるため、削除します。


def _remove_empty_sources(app, exception):
    if exception is not None or app.builder.format != "html":
        return
    sources = pathlib.Path(app.outdir) / "_sources"
    if sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app):
    app.connect("build-finished", _remove_empty_sources)
