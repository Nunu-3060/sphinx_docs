"""Sphinx の設定ファイル（p5.js 入門）。"""

import shutil
from pathlib import Path

from sphinx.application import Sphinx

# -- プロジェクト情報 ---------------------------------------------------------

project = "p5.js 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",  # 数式を MathJax で表示する
]

language = "ja"
exclude_patterns: list[str] = []
numfig = True

# リンクチェック（make linkcheck）の設定
linkcheck_timeout = 30
linkcheck_retries = 2
# examples/ と examples.zip はビルド後に copy_examples() で出力先に置くため、
# linkcheck ではソースフォルダーに存在しない扱いになる。存在確認は別途行う。
linkcheck_ignore = [r"^examples(/|\.zip$)"]

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "p5.js 入門"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 2,
    "collapse_navigation": False,
}

# -- サンプルコードを HTML と一緒に公開する ----------------------------------

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


def copy_examples(app: Sphinx, exception: Exception | None) -> None:
    """ビルド後に examples を出力先へコピーし、一括ダウンロード用の zip を作る。"""
    if exception is not None or app.builder.format != "html":
        return
    outdir = Path(app.outdir)
    target = outdir / "examples"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        EXAMPLES_DIR,
        target,
        ignore=shutil.ignore_patterns("__pycache__", ".mypy_cache"),
    )
    shutil.make_archive(str(outdir / "examples"), "zip", root_dir=target)

    # html_copy_source = False でも空の _sources フォルダーが残るため削除する
    sources = outdir / "_sources"
    if sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: Sphinx) -> None:
    """Sphinx の拡張ポイント。"""
    app.connect("build-finished", copy_examples)
