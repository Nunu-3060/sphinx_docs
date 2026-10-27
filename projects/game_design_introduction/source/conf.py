# Configuration file for the Sphinx documentation builder.

import subprocess
import sys
import zipfile
from pathlib import Path

from matplotlib import font_manager

# -- Project information -----------------------------------------------------

project = 'ゲームデザイン・レベルデザイン入門'
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
exclude_patterns = ['_scripts', '_generated', 'Thumbs.db', '.DS_Store']

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


_FONT = _select_font(['Yu Gothic', 'Meiryo', 'MS Gothic'])

graphviz_output_format = 'png'
graphviz_dot_args = [
    f'-Gfontname={_FONT}',
    f'-Nfontname={_FONT}',
    f'-Efontname={_FONT}',
    '-Nfontsize=12',
    '-Efontsize=11',
    '-Gdpi=110',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = project
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

# -- Build-time generation ---------------------------------------------------

_SOURCE_DIR = Path(__file__).resolve().parent
_GENERATED_DIR = _SOURCE_DIR / '_generated'
_EXAMPLES_DIR = _SOURCE_DIR.parent / 'examples'
_ZIP_EXCLUDED_DIRS = {'__pycache__', '.mypy_cache'}
_ZIP_EXCLUDED_FILES = {'playlog.csv'}


def _make_figures() -> None:
    """本文で使う図を _generated に出力する。"""
    script = _SOURCE_DIR / '_scripts' / 'make_figures.py'
    subprocess.run([sys.executable, str(script), str(_GENERATED_DIR)], check=True)


def _make_final_project_zip() -> None:
    """総合演習のサンプル一式を zip にまとめる。"""
    project_dir = _EXAMPLES_DIR / 'final_project'
    archive = _GENERATED_DIR / 'final_project.zip'
    _GENERATED_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(project_dir.rglob('*')):
            relative = path.relative_to(project_dir)
            if path.is_dir() or _ZIP_EXCLUDED_DIRS & set(relative.parts) or path.name in _ZIP_EXCLUDED_FILES:
                continue
            zf.write(path, Path('final_project') / relative)
        # ヒートマップを描くスクリプトと検査用の設定も同梱する。
        zf.write(_EXAMPLES_DIR / 'playtest_heatmap.py', 'playtest_heatmap.py')
        zf.write(_EXAMPLES_DIR / 'setup.cfg', 'setup.cfg')


def _on_builder_inited(app) -> None:
    _make_figures()
    _make_final_project_zip()


def setup(app):
    app.connect('builder-inited', _on_builder_inited)
