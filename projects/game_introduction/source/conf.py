# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

from matplotlib import font_manager

# -- Project information -----------------------------------------------------

project = 'ゲーム入門'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
release = '1.0'
version = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.githubpages',  # GitHub Pages 用に .nojekyll を出力する
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
    'sphinx_rtd_theme',
]

language = 'ja'
exclude_patterns = ['_scripts', '_generated']

numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'リスト %s',
    'section': '%s 節',
}

# -- Graphviz ----------------------------------------------------------------


def _select_font(candidates: list[str]) -> str:
    """インストール済みのフォントから候補順に最初に見つかったものを返す。"""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return candidates[-1]


_FONT = _select_font(['Meiryo', 'Yu Gothic', 'Noto Sans JP'])

graphviz_output_format = 'png'
graphviz_dot_args = [
    f'-Gfontname={_FONT}',
    f'-Nfontname={_FONT}',
    f'-Efontname={_FONT}',
    '-Gdpi=100',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = 'ゲーム入門'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- 図と配布ファイルの生成 ----------------------------------------------------
# 本文の図（source/_generated/*.png）と Godot サンプルの zip は _scripts/make_figures.py で生成する。
# 図はサンプルコード（examples/py）の関数を使って計算するので、ビルドのたびに作り直してコードと一致させる。


def _make_figures(app: object) -> None:
    sys.path.insert(0, str(Path(__file__).parent / '_scripts'))
    import make_figures
    make_figures.main()


def setup(app):  # type: ignore[no-untyped-def]
    # Pygments に付属する GDScript の字句解析器は Godot 3 の文法を前提にしているので、Godot 4 に対応したものに置き換える
    sys.path.insert(0, str(Path(__file__).parent / '_scripts'))
    from gdscript4_lexer import GDScript4Lexer
    app.add_lexer('gdscript', GDScript4Lexer)
    app.connect('builder-inited', _make_figures)
