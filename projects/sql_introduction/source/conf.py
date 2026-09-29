"""Sphinx configuration for "SQL 入門"."""

import zipfile
from pathlib import Path

project = "SQL 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
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
highlight_language = "sql"

# コピーボタンでプロンプト（$ や >>>）をコピー対象から除く
copybutton_prompt_text = r"\$ |>>> "
copybutton_prompt_is_regexp = True

# サンプルファイル一式を ZIP にまとめ、HTML の出力先に配置する
_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / "examples"
_EXTRA = _ROOT / "build" / "extra"


def _make_examples_zip() -> None:
    """examples フォルダーのサンプルファイルを ZIP にまとめる."""
    _EXTRA.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in _EXAMPLES.rglob("*")
        if p.is_file() and p.suffix in (".py", ".sql", ".cfg")
        and "__pycache__" not in p.parts
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
    r"^https://dev\.mysql\.com/",  # 自動アクセスを 403 で拒否するサイト
]
