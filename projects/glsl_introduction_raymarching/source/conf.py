"""Sphinx の設定ファイル。"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import logging

# -- パス ----------------------------------------------------------------------

SOURCE_DIR = Path(__file__).resolve().parent
EXAMPLES_DIR = SOURCE_DIR.parent / "examples"
SHADER_DIR = EXAMPLES_DIR / "shaders"
IMAGE_DIR = SOURCE_DIR / "_static" / "images"

# examples/viewer に __pycache__ を作らないようにする
sys.dont_write_bytecode = True
sys.path.insert(0, str(EXAMPLES_DIR / "viewer"))
import capture_images  # noqa: E402
from shader_viewer import write_html  # noqa: E402

logger = logging.getLogger(__name__)

# -- プロジェクト情報 ----------------------------------------------------------

project = "GLSL によるレイマーチング入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 ------------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = []
highlight_language = "glsl"

# -- HTML 出力 -----------------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# linkcheck で確認しない URL
# (Shadertoy は自動アクセスに 403 を返すため除外する)
linkcheck_ignore = [r"demos/.*", r"https://www\.shadertoy\.com/.*"]

# -- シェーダーの関数の行番号 --------------------------------------------------
#
# rst 中の {glsl:ファイル名:関数名} を、その関数 (直前のコメントを含む) の
# 行範囲 "開始-終了" に置き換える。literalinclude の :lines: で使う。
# 関数名を "a..b" と書くと、関数 a の先頭から関数 b の末尾までを返す。

GLSL_PLACEHOLDER = re.compile(r"\{glsl:([\w.]+):(\w+)(?:\.\.(\w+))?\}")


def _declaration(name: str) -> re.Pattern[str]:
    """関数・定数・変数 name の宣言の行に一致する正規表現を返す。"""
    return re.compile(rf"^(const\s+)?\w+\s+{name}\s*[(=;]")


def _find_start(lines: list[str], name: str) -> int:
    """関数または定数 name の定義の先頭行 (直前のコメントを含む) を返す。"""
    pattern = _declaration(name)
    for index, line in enumerate(lines):
        if pattern.match(line):
            while index > 0 and lines[index - 1].startswith("//"):
                index -= 1
            return index
    raise ValueError(f"{name} が見つからない")


def _find_end(lines: list[str], name: str) -> int:
    """関数または定数 name の定義の末尾行を返す。"""
    pattern = _declaration(name)
    for index, line in enumerate(lines):
        if pattern.match(line):
            # 1 行で終わる定義 (定数など)。行末のコメントは除いて判定する
            if line.split("//")[0].rstrip().endswith(";"):
                return index
            for end in range(index, len(lines)):
                if lines[end] == "}":
                    return end
    raise ValueError(f"{name} の末尾が見つからない")


def glsl_line_range(file_name: str, first: str, last: str | None) -> str:
    """シェーダー中の関数の行範囲を "開始-終了" (1 始まり) で返す。"""
    lines = (SHADER_DIR / file_name).read_text(encoding="utf-8").splitlines()
    start = _find_start(lines, first)
    end = _find_end(lines, last or first)
    return f"{start + 1}-{end + 1}"


def replace_placeholders(app: Sphinx, docname: str,
                         source: list[str]) -> None:
    """source-read イベント: プレースホルダーを行範囲に置き換える。"""
    source[0] = GLSL_PLACEHOLDER.sub(
        lambda m: glsl_line_range(m.group(1), m.group(2), m.group(3)),
        source[0])


# -- 図の撮影 ------------------------------------------------------------------
#
# source/_static/images の図のうち、存在しないものと、シェーダーより古いものを
# headless ブラウザーで撮影し直す (examples/viewer/capture_images.py)。
# 環境変数 SKIP_SHADER_CAPTURE=1 で無効にできる。


def update_images(app: Sphinx) -> None:
    """builder-inited イベント: 古い図を撮影し直す。"""
    if app.builder.name == "linkcheck":
        return
    if os.environ.get("SKIP_SHADER_CAPTURE") == "1":
        return
    shaders = capture_images.select_shaders(SHADER_DIR, IMAGE_DIR, [],
                                            force=False)
    if not shaders:
        return
    browser = capture_images.find_browser()
    if browser is None:
        logger.info("Chrome または Edge が見つからないため、既存の図を使う "
                    "(更新が必要な図: %d 個)", len(shaders))
        return
    logger.info("シェーダーの図を撮影する: %d 個 (%s)", len(shaders),
                browser.name)
    for result in capture_images.capture_all(shaders, IMAGE_DIR, browser):
        if result.error is not None:
            logger.warning("%s の撮影に失敗した: %s", result.shader.name,
                           result.error)


# -- ブラウザーで実行できるデモページ ------------------------------------------


def build_demos(app: Sphinx, exception: Exception | None) -> None:
    """build-finished イベント: 各シェーダーの実行用 HTML を demos/ に出力する。"""
    if exception is not None or app.builder.format != "html":
        return
    demo_dir = Path(app.outdir) / "demos"
    for shader in sorted(SHADER_DIR.glob("*.frag")):
        write_html(shader, demo_dir / f"{shader.stem}.html")

    # html_copy_source = False でも空の _sources が作られるため削除する
    sources_dir = Path(app.outdir) / "_sources"
    if sources_dir.is_dir() and not any(sources_dir.iterdir()):
        sources_dir.rmdir()


def setup(app: Sphinx) -> None:
    """Sphinx 拡張としての初期化。"""
    app.connect("builder-inited", update_images)
    app.connect("source-read", replace_placeholders)
    app.connect("build-finished", build_demos)
