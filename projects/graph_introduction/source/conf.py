"""Sphinx configuration for "グラフによる可視化入門"."""

import importlib.util
import os
import shutil
import sys
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面を持たないバックエンドで描画する

import matplotlib.pyplot as plt  # noqa: E402

project = "グラフによる可視化入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
]

templates_path: list[str] = []
exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 3}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# 図に番号を付け、:numref: で参照できるようにする
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
}

# コードブロックの既定の言語
highlight_language = "python"

# コピーボタンでプロンプト（$ や >>>）をコピー対象から除く
copybutton_prompt_text = r"\$ |>>> |> "
copybutton_prompt_is_regexp = True

# Graphviz の図は拡大しても劣化しない SVG で出力する
graphviz_output_format = "svg"

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(os.environ.get("ProgramFiles", r"C:\Program Files"),
                         "Graphviz", "bin")
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / "examples"
_SAMPLES = _EXAMPLES / "py"
_FIGURES = _ROOT / "build" / "figures"
_EXTRA = _ROOT / "build" / "extra"


def _load_sample(path: Path) -> object:
    """サンプルのファイルをモジュールとして読み込む."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_figures() -> None:
    """サンプルを実行し、本文で使う図を build/figures に書き出す.

    サンプルが create_figure()（matplotlib の Figure を返す）を持つ場合は
    SVG 画像を、create_graph()（graphviz パッケージのグラフを返す）を持つ
    場合は DOT のファイルを書き出す。
    """
    _FIGURES.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True  # examples に __pycache__ を作らない
    sys.path.insert(0, str(_SAMPLES))  # サンプル間の import を解決する
    jpfont = _load_sample(_SAMPLES / "jpfont.py")
    jpfont.setup()  # type: ignore[attr-defined]
    plt.rcParams["svg.hashsalt"] = "graph_introduction"  # 出力を毎回同じにする
    for path in sorted(_SAMPLES.glob("ch*.py")):
        module = _load_sample(path)
        if hasattr(module, "create_figure"):
            fig = module.create_figure()
            fig.savefig(_FIGURES / f"{path.stem}.svg", bbox_inches="tight")
            plt.close(fig)
        if hasattr(module, "create_graph"):
            source = module.create_graph().source
            (_FIGURES / f"{path.stem}.gv").write_text(source, encoding="utf-8")


def _make_examples_zip() -> None:
    """examples フォルダーのサンプルファイルを ZIP にまとめる."""
    _EXTRA.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in _EXAMPLES.rglob("*")
        if p.is_file() and p.suffix in (".py", ".dot", ".cfg")
        and "__pycache__" not in p.parts
    )
    with zipfile.ZipFile(_EXTRA / "examples.zip", "w",
                         zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("examples") / path.relative_to(_EXAMPLES))


# 本文から図と :download: で参照するため、文書の読み込みより前に生成する
_make_figures()
_make_examples_zip()


def _remove_empty_sources(app: object, exception: Exception | None) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダーを消す."""
    sources = Path(app.outdir) / "_sources"  # type: ignore[attr-defined]
    if exception is None and sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: object) -> None:
    """Sphinx の拡張機能として、ビルド後の処理を登録する."""
    app.connect("build-finished", _remove_empty_sources)  # type: ignore
