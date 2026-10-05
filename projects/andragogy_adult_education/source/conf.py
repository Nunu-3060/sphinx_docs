# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import pathlib
import zipfile

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------

project = 'アンドラゴジー・成人教育'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',      # 数式を MathJax で表示する
    'sphinx.ext.githubpages',  # 出力先に .nojekyll を作成する
    'sphinx_copybutton',       # コード例にコピーボタンを付ける
]

exclude_patterns: list[str] = []
language = 'ja'

# 図・表・コードに番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': 'コード %s',
    'section': '%s 節',
}

# コピーボタンで行番号をコピーしないようにする。
copybutton_exclude = '.linenos, .gp'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_title = f'{project} {release}'
html_search_language = 'ja'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力した HTML から rst ソースを閲覧できないようにする。
html_copy_source = False
html_show_sourcelink = False

html_theme_options = {
    'navigation_depth': 3,
}

# -- Options for linkcheck ---------------------------------------------------

linkcheck_timeout = 30
linkcheck_retries = 2

# 次の出版社は、ボット対策のため linkcheck のアクセスに 403 を返す。
# DOI は、Crossref に登録された書誌情報（題名、巻号、ページ）と一致する
# ことを確認済み。
linkcheck_ignore = [
    r'https://doi\.org/10\.1177/',
    r'https://doi\.org/10\.1111/',
    r'https://doi\.org/10\.1073/',
    r'https://doi\.org/10\.2307/',
]

# -- Build examples.zip for download -----------------------------------------


def generate_examples_zip(app: Sphinx) -> None:
    """examples/ 以下のファイルを _static/downloads/examples.zip にまとめる。"""
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / 'examples'
    output_dir = src_dir / '_static' / 'downloads'
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_dir / 'examples.zip', 'w',
                         zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(examples_dir.iterdir()):
            if path.is_file() and path.suffix in {'.py', '.md', '.csv'}:
                zf.write(path, arcname=f'examples/{path.name}')


def setup(app: Sphinx) -> None:
    app.connect('builder-inited', generate_examples_zip)
