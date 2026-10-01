"""Sphinx configuration for "ソフトウェアテスト入門"."""

import os
import shutil
import zipfile
from pathlib import Path

project = "ソフトウェアテスト入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 3}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# コードブロックの既定の言語
highlight_language = "python"

# コピーボタンでプロンプト（$ や >>>）をコピー対象から除く
copybutton_prompt_text = r"\$ |>>> "
copybutton_prompt_is_regexp = True

# 図は拡大しても劣化しない SVG で出力し、日本語を含むフォントを既定にする
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "Graphviz", "bin")
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

# サンプルファイル一式を ZIP にまとめ、HTML の出力先に配置する
_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / "examples"
_EXTRA = _ROOT / "build" / "extra"
_ZIP_SUFFIXES = (".py", ".toml", ".cfg", ".yml", ".yaml", ".txt")
_ZIP_NAMES = ("Jenkinsfile",)  # 拡張子のないファイル
_CACHE_DIRS = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".hypothesis", ".venv",
}


def _make_examples_zip() -> None:
    """examples フォルダーのサンプルファイルを ZIP にまとめる."""
    _EXTRA.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in _EXAMPLES.rglob("*")
        if p.is_file()
        and (p.suffix in _ZIP_SUFFIXES or p.name in _ZIP_NAMES)
        and not _CACHE_DIRS.intersection(p.parts)
    )
    with zipfile.ZipFile(_EXTRA / "examples.zip", "w",
                         zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("examples") / path.relative_to(_EXAMPLES))


_make_examples_zip()
html_extra_path = [str(_EXTRA)]

# linkcheck の対象外とする URL
linkcheck_ignore = [
    r"^examples\.zip$",  # ビルド時に出力先へ生成するファイル
]
