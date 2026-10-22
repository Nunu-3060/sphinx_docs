# Sphinx の設定ファイル
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import logging

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"

# -- プロジェクト情報 --------------------------------------------------------

project = "Pyxel によるレトロゲーム作成入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

# -- 一般設定 ----------------------------------------------------------------

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
]

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = ["tools"]

numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 節",
}

# -- Graphviz ----------------------------------------------------------------

graphviz_output_format = "png"
graphviz_dot_args = [
    "-Gdpi=96",
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- HTML 出力 ---------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "navigation_depth": 3,
}
# 出力した HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

# -- リンクチェック ----------------------------------------------------------

linkcheck_ignore = [
    r"downloads/.*",
    r"play/.*",
    r"http://localhost.*",
]
linkcheck_timeout = 30


# -- ビルド後の処理 ----------------------------------------------------------
#
# サンプルコード一式の zip と、ブラウザで遊べる完成版ゲーム (HTML) を出力先に置く。


def _ignore_caches(directory: str, names: list[str]) -> list[str]:
    return [n for n in names if n in ("__pycache__", ".mypy_cache", ".pytest_cache") or n.endswith(".pyxapp")]


def _make_examples_zip(outdir: Path) -> None:
    dst = outdir / "downloads" / "examples.zip"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(EXAMPLES.rglob("*")):
            rel = path.relative_to(EXAMPLES)
            if path.is_dir() or _ignore_caches("", list(rel.parts)):
                continue
            zf.write(path, Path("examples") / rel)


def _make_web_game(outdir: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(EXAMPLES / "cosmo_rush", work / "cosmo_rush", ignore=_ignore_caches)
        run = {"cwd": work, "check": True, "capture_output": True}
        subprocess.run([sys.executable, "-m", "pyxel", "package", "cosmo_rush", "cosmo_rush/main.py"], **run)
        subprocess.run([sys.executable, "-m", "pyxel", "app2html", "cosmo_rush.pyxapp"], **run)
        (outdir / "play").mkdir(parents=True, exist_ok=True)
        (outdir / "downloads").mkdir(parents=True, exist_ok=True)
        shutil.copy(work / "cosmo_rush.html", outdir / "play" / "cosmo_rush.html")
        shutil.copy(work / "cosmo_rush.pyxapp", outdir / "downloads" / "cosmo_rush.pyxapp")


def _on_build_finished(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.format != "html":
        return
    logger = logging.getLogger(__name__)
    outdir = Path(app.outdir)
    # html_copy_source = False でも空の _sources ディレクトリが残るので削除する
    sources = outdir / "_sources"
    if sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()
    _make_examples_zip(outdir)
    try:
        _make_web_game(outdir)
    except (OSError, subprocess.CalledProcessError) as e:
        logger.warning(f"ブラウザ版ゲームを生成できなかった: {e}")


def setup(app: Sphinx) -> None:
    app.connect("build-finished", _on_build_finished)
