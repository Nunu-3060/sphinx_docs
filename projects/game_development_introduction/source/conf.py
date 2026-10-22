# Configuration file for the Sphinx documentation builder.

from matplotlib import font_manager

# -- Project information -----------------------------------------------------

project = 'ゲーム作成入門'
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
exclude_patterns = ['_scripts']

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


_FONT = _select_font(['Noto Sans JP', 'Yu Gothic', 'Meiryo'])

graphviz_output_format = 'png'
graphviz_dot_args = [
    f'-Gfontname={_FONT}',
    f'-Nfontname={_FONT}',
    f'-Efontname={_FONT}',
    '-Gdpi=110',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = 'ゲーム作成入門'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2
# 以下のサイトは自動アクセスを 403 で拒否するため、検査対象から除外する（いずれも公式サイトのトップページ）。
linkcheck_ignore = [
    r'https://globalgamejam\.org/',
    r'https://inkscape\.org/',
    r'https://phaser\.io/',
    r'https://www\.construct\.net/',
    r'https://www\.unrealengine\.com/.*',
    # Python の requests からの接続がタイムアウトする（curl では 200 を返すことを確認済み）。
    r'https://b\.tyrano\.jp/',
]
