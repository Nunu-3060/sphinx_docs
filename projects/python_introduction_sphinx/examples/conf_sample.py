# よく使う設定をまとめた conf.py のサンプルです。
#
# conf.py は Sphinx の起動時に Python のコードとして実行されます。
# モジュールの変数として定義した値が、そのまま設定値になります。

import sys
from pathlib import Path

# autodoc で読み込むモジュールの場所を import パスに追加します。
# ここでは conf.py の 1 つ上のディレクトリにある src を追加しています。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# -- プロジェクト情報 --------------------------------------------------------

project: str = "sample"          # ドキュメントの名前
author: str = "author"           # 著者名
copyright: str = "2026, author"  # フッターに表示される著作権表示
release: str = "1.0.0"           # バージョン（完全な表記）

# -- 一般設定 ----------------------------------------------------------------

# 有効にする拡張機能のモジュール名
extensions: list[str] = [
    "sphinx.ext.autodoc",      # docstring からドキュメントを生成
    "sphinx.ext.napoleon",     # Google 形式・NumPy 形式の docstring に対応
    "sphinx.ext.viewcode",     # ソースコードのページへのリンクを追加
    "sphinx.ext.intersphinx",  # 他のドキュメントへの相互参照
    "sphinx.ext.githubpages",  # GitHub Pages 用に .nojekyll を出力
]

# ソースディレクトリの中で、ビルドの対象外にするパターン
exclude_patterns: list[str] = ["drafts/*"]

# ドキュメントの言語（UI の文言や検索の単語分割に影響する）
language: str = "ja"

# 図・表・コードに番号を付けて :numref: で参照できるようにする
numfig: bool = True

# -- 拡張機能の設定 ----------------------------------------------------------

# 型ヒントをシグネチャではなく説明文の中に表示する
autodoc_typehints: str = "description"

# intersphinx で参照するドキュメント
intersphinx_mapping: dict[str, tuple[str, str | None]] = {
    "python": ("https://docs.python.org/3", None),
}

# -- HTML 出力の設定 ---------------------------------------------------------

html_theme: str = "sphinx_rtd_theme"  # テーマ
html_title: str = "sample ドキュメント"  # ページのタイトル
html_static_path: list[str] = ["_static"]  # CSS や画像を置くディレクトリ
html_css_files: list[str] = ["custom.css"]  # 追加で読み込む CSS

html_show_sourcelink: bool = False  # 「ソースを表示」リンクを出さない
html_copy_source: bool = False      # rst ソースを出力先にコピーしない
