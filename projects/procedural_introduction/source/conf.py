# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "プロシージャル生成入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"

version = "1.0"
release = "1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# 図・表・コードに番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {"figure": "図 %s", "table": "表 %s", "code-block": "リスト %s", "section": "%s 節"}

# GLSL のデモはビルドの最後に _static/glsl へコピーするので、linkcheck の対象から外す。
linkcheck_ignore = [r"_static/glsl/.*"]

graphviz_output_format = "svg"
graphviz_dot_args = ["-Gfontname=Meiryo", "-Nfontname=Meiryo", "-Efontname=Meiryo"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
# 出力された HTML から rst のソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- Paths -------------------------------------------------------------------

SOURCE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SOURCE_DIR.parent
EXAMPLES_DIR = PROJECT_DIR / "examples"
PYTHON_DIR = EXAMPLES_DIR / "python"
GLSL_DIR = EXAMPLES_DIR / "glsl"
GENERATED_DIR = SOURCE_DIR / "_generated"
DOWNLOADS_DIR = GENERATED_DIR / "downloads"

logger = logging.getLogger(__name__)

# -- Generate figures and videos from examples/python ------------------------
#
# examples/python のスクリプトのうち `if __name__ == "__main__":` を持つものを
# 実行し、図と動画を _generated/<スクリプト名>/ に出力させる。スクリプトと、
# それが import するライブラリのどれよりも新しい出力があれば、実行を省く。
# build フォルダーを消しても _generated は残るので、2 回目以降のビルドは速い。
#
# 環境変数:
#   PROC_NO_GENERATE=1     生成を行わない（既にある _generated をそのまま使う）
#   PROC_ONLY=a.py,b.py    指定したスクリプトだけを対象にする

_IMPORT_PATTERN = re.compile(r"^(?:from\s+(\w+)\s+import|import\s+(\w+))", re.MULTILINE)


def _dependencies(script: Path, seen: set[Path] | None = None) -> set[Path]:
    """script と、それが import する examples/python 内のモジュールを再帰的に集める。"""
    seen = set() if seen is None else seen
    if script in seen:
        return seen
    seen.add(script)
    for match in _IMPORT_PATTERN.finditer(script.read_text(encoding="utf-8")):
        module = PYTHON_DIR / f"{match.group(1) or match.group(2)}.py"
        if module.is_file():
            _dependencies(module, seen)
    return seen


def _figure_scripts() -> list[Path]:
    """図や動画を出力するスクリプト（main として実行されるもの）の一覧。"""
    only = {name.strip() for name in os.environ.get("PROC_ONLY", "").split(",") if name.strip()}
    scripts = []
    for path in sorted(PYTHON_DIR.glob("*.py")):
        if only and path.name not in only:
            continue
        if 'if __name__ == "__main__":' in path.read_text(encoding="utf-8"):
            scripts.append(path)
    return scripts


def _is_up_to_date(script: Path) -> bool:
    stamp = GENERATED_DIR / script.stem / ".stamp"
    if not stamp.is_file():
        return False
    newest = max(path.stat().st_mtime for path in _dependencies(script))
    return stamp.stat().st_mtime >= newest


def _run_script(script: Path) -> str | None:
    """script を実行する。失敗したらエラーの内容を返す。"""
    output = GENERATED_DIR / script.stem
    shutil.rmtree(output, ignore_errors=True)
    result = subprocess.run(
        [sys.executable, script.name, str(GENERATED_DIR)],
        cwd=PYTHON_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "MPLBACKEND": "Agg"},
    )
    if result.returncode != 0:
        return f"{script.name}:\n{result.stdout}\n{result.stderr}"
    for line in (result.stdout + result.stderr).splitlines():
        if line.strip():
            logger.info(f"  {script.name}: {line}")
    (output / ".stamp").touch()
    return None


def generate_figures(app: Sphinx) -> None:
    if os.environ.get("PROC_NO_GENERATE"):
        return
    GENERATED_DIR.mkdir(exist_ok=True)
    targets = [script for script in _figure_scripts() if not _is_up_to_date(script)]
    if not targets:
        return
    logger.info(f"図と動画を生成する（{len(targets)} 本のスクリプト）")
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        errors = [error for error in executor.map(_run_script, targets) if error]
    if errors:
        raise ExtensionError("図・動画の生成に失敗した。\n" + "\n".join(errors))


# -- Archives for download ---------------------------------------------------

# zip に含めないフォルダー（キャッシュや実行結果）
_EXCLUDED_DIRS = {".godot", "__pycache__", ".mypy_cache", "out"}


def _write_zip(target: Path, sources: list[tuple[Path, Path]]) -> None:
    """(実際のパス, zip 内のパス) の組をまとめて zip にする。"""
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path, name in sources:
            archive.write(path, name.as_posix())


def _tree(directory: Path, prefix: str) -> list[tuple[Path, Path]]:
    files = []
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if path.is_file() and not _EXCLUDED_DIRS.intersection(relative.parts):
            files.append((path, Path(prefix) / relative))
    return files


def create_archives(app: Sphinx) -> None:
    """サンプルコードを種類ごとに zip にまとめる。"""
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    setup_cfg = [(EXAMPLES_DIR / "setup.cfg", Path("examples/setup.cfg"))]
    _write_zip(DOWNLOADS_DIR / "python_examples.zip", _tree(PYTHON_DIR, "examples/python") + setup_cfg)
    _write_zip(DOWNLOADS_DIR / "glsl_examples.zip", _tree(GLSL_DIR, "examples/glsl"))
    _write_zip(DOWNLOADS_DIR / "godot_examples.zip", _tree(EXAMPLES_DIR / "godot", "examples/godot"))
    _write_zip(DOWNLOADS_DIR / "houdini_examples.zip", _tree(EXAMPLES_DIR / "houdini", "examples/houdini") + setup_cfg)


# -- Video directive ---------------------------------------------------------
#
#   .. video:: _generated/loop_noise/loop.mp4
#      :width: 480
#
#      説明文（省略可）
#
# 動画は _static/videos/<スクリプト名>__<ファイル名> にコピーし、<video> タグで埋め込む。
# 本文のページはすべて source 直下に置くので、相対パスは _static/... でよい。


def _video_name(path: str) -> str:
    relative = Path(path)
    return f"{relative.parent.name}__{relative.name}"


class VideoDirective(SphinxDirective):
    required_arguments = 1
    has_content = True
    option_spec = {"width": directives.positive_int}

    def run(self) -> list[nodes.Node]:
        path = self.arguments[0]
        source = SOURCE_DIR / path
        if not source.is_file():
            logger.warning(f"動画が見つからない: {path}", location=self.get_location())
        self.env.note_dependency(str(source))
        videos: set[str] = getattr(self.env, "proc_videos", set())
        videos.add(path)
        self.env.proc_videos = videos  # type: ignore[attr-defined]
        width = self.options.get("width", 640)
        html = (
            f'<div class="video-figure"><video src="_static/videos/{_video_name(path)}" width="{width}" '
            'autoplay loop muted playsinline controls preload="metadata"></video>'
        )
        if self.content:
            caption = " ".join(line.strip() for line in self.content)
            html += f'<p class="caption"><span class="caption-text">{caption}</span></p>'
        html += "</div>"
        return [nodes.raw("", html, format="html")]


# -- Copy videos and GLSL demos, check the output size ----------------------

# GitHub は 50 MB を超えるファイルに警告を出す。それより十分小さい上限を設ける。
_SIZE_LIMITS = {".mp4": 2.0, ".webm": 2.0, ".gif": 2.0, ".png": 1.0, ".jpg": 1.0, ".zip": 5.0}
_TOTAL_LIMIT_MB = 50.0


def finish_build(app: Sphinx, exception: Exception | None) -> None:
    if exception is not None or app.builder.format != "html":
        return
    outdir = Path(app.outdir)

    videos_dir = outdir / "_static" / "videos"
    videos_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(getattr(app.env, "proc_videos", set())):
        source = SOURCE_DIR / path
        if source.is_file():
            shutil.copy2(source, videos_dir / _video_name(path))

    # GLSL のデモは、ブラウザーでそのまま開けるように HTML ファイルごとコピーする。
    glsl_dir = outdir / "_static" / "glsl"
    glsl_dir.mkdir(parents=True, exist_ok=True)
    for path in GLSL_DIR.glob("*.html"):
        shutil.copy2(path, glsl_dir / path.name)

    total = 0.0
    for path in outdir.rglob("*"):
        if not path.is_file():
            continue
        size_mb = path.stat().st_size / 1024 / 1024
        total += size_mb
        limit = _SIZE_LIMITS.get(path.suffix.lower())
        if limit is not None and size_mb > limit:
            logger.warning(f"ファイルが大きい（{size_mb:.2f} MB > {limit} MB）: {path.relative_to(outdir)}")
    logger.info(f"出力の合計: {total:.1f} MB")
    if total > _TOTAL_LIMIT_MB:
        logger.warning(f"出力の合計が大きい（{total:.1f} MB > {_TOTAL_LIMIT_MB} MB）")


def setup(app: Sphinx) -> None:
    app.add_directive("video", VideoDirective)
    app.connect("builder-inited", generate_figures)
    app.connect("builder-inited", create_archives)
    app.connect("build-finished", finish_build)
