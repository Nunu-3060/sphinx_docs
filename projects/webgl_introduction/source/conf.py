"""Sphinx の設定ファイル。"""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

from sphinx.application import Sphinx

# -- プロジェクト情報 ---------------------------------------------------------

project = "WebGL 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",      # 数式
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

templates_path: list[str] = []
exclude_patterns: list[str] = []
language = "ja"

# 図・表・コードに番号を付け、章は「第 N 章」として参照できるようにする
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "第 %s 章",
}

highlight_language = "javascript"

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = f"{project} {release}"

# 出力した HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# -- リンクチェックの設定 -------------------------------------------------------

# examples/ と zip ファイルはビルド完了時（copy_examples）に出力先へ配置するため、
# linkcheck ではソースツリー上に存在しないリンクとして扱われる。
# これらは出力された HTML に対して別途存在を確認する。
linkcheck_ignore = [r"^examples/", r"^webgl_introduction_examples\.zip$"]

# -- サンプルコードの配置 -----------------------------------------------------

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
IGNORE = shutil.ignore_patterns("__pycache__", ".mypy_cache", "*.pyc")
ZIP_NAME = "webgl_introduction_examples.zip"


def copy_examples(app: Sphinx, exception: Exception | None) -> None:
    """HTML の出力先に examples フォルダーと、その zip ファイルを配置する。

    各サンプルは build/html/examples/ に置かれるので、文書中のリンクから
    ブラウザーで直接開ける。
    """
    if exception is not None or app.builder.format != "html":
        return
    outdir = Path(app.outdir)
    shutil.copytree(
        EXAMPLES_DIR, outdir / "examples", ignore=IGNORE, dirs_exist_ok=True
    )
    with zipfile.ZipFile(outdir / ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(EXAMPLES_DIR.rglob("*")):
            relative = path.relative_to(EXAMPLES_DIR)
            ignored = {"__pycache__", ".mypy_cache"} & set(relative.parts)
            if path.is_file() and not ignored:
                zf.write(path, Path("examples") / relative)


def setup(app: Sphinx) -> None:
    app.connect("build-finished", copy_examples)
