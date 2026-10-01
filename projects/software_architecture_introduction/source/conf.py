# Configuration file for the Sphinx documentation builder.

import shutil
import zipfile
from pathlib import Path

# -- Project information -----------------------------------------------------

project = 'ソフトウェア設計入門'
copyright = '2026, Nunu_3060'
author = 'Nunu_3060'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.graphviz',
    'sphinx.ext.githubpages',  # .nojekyll を出力する
]

templates_path = []
exclude_patterns = []

language = 'ja'

# -- Graphviz ----------------------------------------------------------------

# dot が PATH にない場合は、既定のインストール先を探す
_DOT_CANDIDATES = [
    Path(r'C:\Program Files\Graphviz\bin\dot.exe'),
    Path(r'C:\Program Files (x86)\Graphviz\bin\dot.exe'),
]
graphviz_dot = shutil.which('dot') or next(
    (str(path) for path in _DOT_CANDIDATES if path.exists()), 'dot')
graphviz_output_format = 'svg'
_FONT = 'Meiryo'
graphviz_dot_args = [
    f'-Gfontname={_FONT}',
    f'-Nfontname={_FONT}',
    f'-Efontname={_FONT}',
    '-Gfontsize=12',
    '-Nfontsize=12',
    '-Efontsize=10',
    '-Nshape=box',
    '-Nstyle=rounded,filled',
    '-Nfillcolor=#f5f7fa',
    '-Ncolor=#4a5568',
    '-Ecolor=#4a5568',
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']

# 出力された HTML から rst ソースを閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    'navigation_depth': 3,
}

html_search_language = 'ja'

# -- サンプルコード一式の zip ファイル --------------------------------------------

# examples フォルダーを zip ファイルにまとめる。examples.rst の :download: で参照する
_ROOT = Path(__file__).resolve().parent.parent
_ZIP_DIR = _ROOT / 'build' / 'zip'
_EXCLUDED_PARTS = {'__pycache__', '.mypy_cache', '.pytest_cache'}
# サンプルの実行で作られるファイル（inventory.json など）は含めない
_EXCLUDED_SUFFIXES = {'.json', '.pyc'}


def _make_examples_zip() -> None:
    _ZIP_DIR.mkdir(parents=True, exist_ok=True)
    examples_dir = _ROOT / 'examples'
    with zipfile.ZipFile(_ZIP_DIR / 'examples.zip', 'w',
                         zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(examples_dir.rglob('*')):
            relative = path.relative_to(_ROOT)
            if (path.is_file() and not _EXCLUDED_PARTS & set(relative.parts)
                    and path.suffix not in _EXCLUDED_SUFFIXES):
                archive.write(path, relative.as_posix())


_make_examples_zip()
