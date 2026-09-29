# Configuration file for the Sphinx documentation builder.

import pathlib
import zipfile

# -- Paths -------------------------------------------------------------------

SOURCE_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = SOURCE_DIR.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
GENERATED_DIR = ROOT_DIR / "build" / "generated"
EXAMPLES_ZIP = GENERATED_DIR / "unity_editor_examples.zip"

# zip に含めないファイル名とフォルダー名（OS やツールが自動で作るもの）
EXCLUDED_FILE_NAMES = {"Thumbs.db", "desktop.ini", ".DS_Store"}
EXCLUDED_DIR_NAMES = {"bin", "obj", ".vs", ".vscode", ".idea"}


def is_excluded(path):
    """zip に含めないファイルなら True を返す。"""
    relative = path.relative_to(EXAMPLES_DIR)
    if path.name in EXCLUDED_FILE_NAMES:
        return True
    return any(part in EXCLUDED_DIR_NAMES for part in relative.parts[:-1])


def make_examples_zip():
    """examples フォルダーをまとめた zip を作成する（index.rst からダウンロードリンクを張る）。

    conf.py はビルドのたびに読み込まれるため、zip も毎回作り直される。
    """
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(EXAMPLES_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(EXAMPLES_DIR.rglob("*")):
            if path.is_file() and not is_excluded(path):
                zf.write(path, pathlib.Path("examples") / path.relative_to(EXAMPLES_DIR))


make_examples_zip()

# -- Project information -----------------------------------------------------

project = "Unity エディター拡張入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- General configuration ---------------------------------------------------

language = "ja"

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.mathjax",
]

exclude_patterns = []

highlight_language = "csharp"

# Unity スクリプトリファレンスへのリンク
# 例：:unity-api:`MenuItem` → https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MenuItem.html
extlinks = {
    "unity-api": ("https://docs.unity3d.com/6000.0/Documentation/ScriptReference/%s.html", "%s"),
}

linkcheck_timeout = 30
linkcheck_retries = 2

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    "navigation_depth": 3,
}
