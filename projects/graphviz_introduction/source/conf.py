"""Sphinx configuration for "Graphviz 入門"."""

import importlib.util
import os
import shutil
import sys
import zipfile
from pathlib import Path

project = "Graphviz 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 3}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# コードブロックの既定の言語
highlight_language = "dot"

# コピーボタンでプロンプト（$ や >>>）をコピー対象から除く
copybutton_prompt_text = r"\$ |>>> |> "
copybutton_prompt_is_regexp = True

# 図は拡大しても劣化しない SVG で出力する
graphviz_output_format = "svg"

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える。
# neato などほかのレイアウトエンジンもコマンド名で呼び出されるため、PATH に加える。
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "Graphviz", "bin")
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / "examples"
_EXTRA = _ROOT / "build" / "extra"
_GENERATED = _ROOT / "build" / "generated"

# Python のサンプルが生成する DOT を、本文の図として使うために書き出す。
# キーはサンプルのファイル名、値は書き出す DOT のファイル名。
_PYTHON_SAMPLES = {
    "ch03_first_graph.py": "ch03_first_graph.gv",
    "ch10_digraph_basics.py": "ch10_digraph_basics.gv",
    "ch10_subgraph.py": "ch10_subgraph.gv",
    "ch10_dot_from_string.py": "ch10_dot_from_string.gv",
    "ch11_import_graph.py": "ch11_import_graph.gv",
    "ch11_directory_tree.py": "ch11_directory_tree.gv",
}


def _write_generated_dot() -> None:
    """Python のサンプルが組み立てるグラフの DOT を書き出す.

    サンプルの build_graph()（graphviz パッケージのグラフを返す）または
    build_dot()（DOT の文字列を返す）を呼び出す。
    """
    _GENERATED.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True  # examples に __pycache__ を作らない
    for script, output in _PYTHON_SAMPLES.items():
        path = _EXAMPLES / "py" / script
        spec = importlib.util.spec_from_file_location(path.stem, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "build_graph"):
            source = module.build_graph().source
        else:
            source = module.build_dot()
        (_GENERATED / output).write_text(source, encoding="utf-8")


def _make_examples_zip() -> None:
    """examples フォルダーのサンプルファイルを ZIP にまとめる."""
    _EXTRA.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in _EXAMPLES.rglob("*")
        if p.is_file() and p.suffix in (".py", ".dot", ".cfg")
        and "__pycache__" not in p.parts and "output" not in p.parts
    )
    with zipfile.ZipFile(_EXTRA / "examples.zip", "w",
                         zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("examples") / path.relative_to(_EXAMPLES))


# 本文から :download: ロールで参照するため、文書の読み込みより前に生成する
_write_generated_dot()
_make_examples_zip()
