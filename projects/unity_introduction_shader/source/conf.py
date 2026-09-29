# Sphinx の設定ファイル。
# 設定項目の詳細: https://www.sphinx-doc.org/ja/master/usage/configuration.html

import zipfile
from pathlib import Path

# -- プロジェクト情報 ---------------------------------------------------------

project = "Unity シェーダー・グラフィックス入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    # 数式を MathJax で表示する。
    "sphinx.ext.mathjax",
    # GitHub Pages で公開できるように .nojekyll を出力する。
    "sphinx.ext.githubpages",
]

# 数式の表示に使う MathJax のバージョンを 3 に固定する。
# Sphinx 9 の既定の MathJax 4 では、表のセルの中の数式の上下が欠けて表示されるため。
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

language = "ja"
templates_path: list[str] = []
exclude_patterns: list[str] = []

# コードブロックの既定の言語を HLSL にする。
# ShaderLab 用の字句解析器は Pygments にないため、.shader ファイルも HLSL として色分けする。
highlight_language = "hlsl"

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "Unity シェーダー・グラフィック入門"
html_theme_options = {
    "navigation_depth": 3,
    "prev_next_buttons_location": "both",
}

# 表の折り返しなど、テーマの表示を調整する CSS。
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# 出力した HTML から rst のソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

# -- サンプルコードの一括ダウンロード用 zip ファイルの作成 ------------------------

_SOURCE_DIR = Path(__file__).resolve().parent
_EXAMPLES_DIR = _SOURCE_DIR.parent / "examples"
_GENERATED_DIR = _SOURCE_DIR / "_generated"
EXAMPLES_ZIP = _GENERATED_DIR / "unity_introduction_shader_examples.zip"


def _create_examples_zip() -> None:
    """examples フォルダーの内容を zip ファイルにまとめる。"""
    _GENERATED_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(EXAMPLES_ZIP, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(_EXAMPLES_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, Path("examples") / path.relative_to(_EXAMPLES_DIR))


_create_examples_zip()


# -- ビルド後の処理 -----------------------------------------------------------


def _remove_empty_sources_dir(app, exception) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダーを削除する。"""
    if exception is not None or app.builder.format != "html":
        return
    sources_dir = Path(app.outdir) / "_sources"
    if sources_dir.is_dir() and not any(sources_dir.iterdir()):
        sources_dir.rmdir()


def setup(app):
    app.connect("build-finished", _remove_empty_sources_dir)
