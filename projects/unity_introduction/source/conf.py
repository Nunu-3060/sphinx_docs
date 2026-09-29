# Sphinx の設定ファイルです。
# 設定項目の詳細: https://www.sphinx-doc.org/ja/master/usage/configuration.html

import zipfile
from pathlib import Path

# -- プロジェクト情報 ---------------------------------------------------------

project = "Unity 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    # 数式を MathJax で表示します。
    "sphinx.ext.mathjax",
    # GitHub Pages で公開できるように .nojekyll を出力します。
    "sphinx.ext.githubpages",
]

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = []

# コードブロックの既定の言語を C# にします。
highlight_language = "csharp"

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "Unity 入門"
html_theme_options = {
    "navigation_depth": 3,
    "prev_next_buttons_location": "both",
}

# 表の折り返しなど、テーマの表示を調整する CSS です。
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst のソースを閲覧できないようにします。
html_copy_source = False
html_show_sourcelink = False

# -- サンプルコードの一括ダウンロード用 zip ファイルの作成 ------------------------

_SOURCE_DIR = Path(__file__).resolve().parent
_EXAMPLES_DIR = _SOURCE_DIR.parent / "examples"
_GENERATED_DIR = _SOURCE_DIR / "_generated"
EXAMPLES_ZIP = _GENERATED_DIR / "unity_introduction_examples.zip"


def _create_examples_zip() -> None:
    """examples フォルダーの内容を zip ファイルにまとめます。"""
    _GENERATED_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(EXAMPLES_ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(_EXAMPLES_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, Path("examples") / path.relative_to(_EXAMPLES_DIR))


_create_examples_zip()
