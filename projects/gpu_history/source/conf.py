# Configuration file for the Sphinx documentation builder.

from matplotlib import font_manager

# -- Project information -----------------------------------------------------

project = 'GPU の歴史'
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
html_title = 'GPU の歴史'
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
# DOI のリンク先（ACM, IEEE, Wiley）は自動アクセスを 403 で拒否するため検査対象から除外する。
# DOI 自体の有効性は Crossref API で確認済み。
linkcheck_ignore = [r'https://doi\.org/.*']
