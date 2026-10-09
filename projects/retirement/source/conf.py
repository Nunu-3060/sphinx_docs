# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.util
import pathlib
import zipfile

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------

project = '退職'
author = 'Nunu_3060'
copyright = '2026, Nunu_3060'
version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',      # 数式を MathJax で表示する
    'sphinx.ext.githubpages',  # 出力先に .nojekyll を作成する
]

exclude_patterns: list[str] = []
language = 'ja'

# 表とコードに番号を付け、:numref: で参照できるようにする。
numfig = True
numfig_format = {
    'figure': '図 %s',
    'table': '表 %s',
    'code-block': '例 %s',
    'section': '%s 節',
}

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

# 次のサイトは、Python の TLS ライブラリーとのハンドシェイクに失敗するため
# linkcheck では確認できない。ブラウザーと curl では閲覧できることを確認済み。
linkcheck_ignore = [
    r'https://www\.ideco-koushiki\.jp/',
]

# -- Figures and examples.zip ------------------------------------------------

EXAMPLES_SUFFIXES = {'.py', '.dot'}


def generate_figures(app: Sphinx) -> None:
    """examples/make_figures.py を使って、source/figures に図を作成する。"""
    src_dir = pathlib.Path(app.srcdir)
    script = src_dir.parent / 'examples' / 'make_figures.py'
    spec = importlib.util.spec_from_file_location('make_figures', script)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'{script} を読み込めません。')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.make_all(src_dir / 'figures')


def generate_examples_zip(app: Sphinx) -> None:
    """examples/ 以下のファイルを _static/downloads/examples.zip にまとめる。"""
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / 'examples'
    output_dir = src_dir / '_static' / 'downloads'
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_dir / 'examples.zip', 'w',
                         zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(examples_dir.iterdir()):
            if path.is_file() and path.suffix in EXAMPLES_SUFFIXES:
                zf.write(path, arcname=f'examples/{path.name}')


def setup(app: Sphinx) -> None:
    app.connect('builder-inited', generate_figures)
    app.connect('builder-inited', generate_examples_zip)
