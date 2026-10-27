"""Sphinx configuration for "フーリエ解析・デジタル信号処理入門"."""

import contextlib
import importlib.util
import io
import os
import shutil
import sys
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面を持たないバックエンドで描画する

import matplotlib.pyplot as plt  # noqa: E402

project = "フーリエ解析・デジタル信号処理入門"
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
exclude_patterns: list[str] = ["_scripts"]

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 3}
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = project

# 出力された HTML から rst ソースを閲覧できないようにする
html_copy_source = False
html_show_sourcelink = False

# 図、表、コードに番号を付け、:numref: で参照できるようにする
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
graphviz_dot_args = ["-Gfontname=Meiryo", "-Nfontname=Meiryo", "-Efontname=Meiryo"]

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin")
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

_SOURCE = Path(__file__).resolve().parent
_ROOT = _SOURCE.parent
_SCRIPTS = _SOURCE / "_scripts"
_IMAGES = _SOURCE / "images"
_EXAMPLES = _ROOT / "examples"
_OUTPUTS = _ROOT / "build" / "outputs"
_EXTRA = _ROOT / "build" / "extra"

# サンプルのうち、本文の図や実行結果を作らない補助モジュール
_HELPER_MODULES = {"dsp_plot"}


def _load_module(path: Path) -> object:
    """Python のファイルをモジュールとして読み込む."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _save_figure(module: object, name: str) -> None:
    """create_figure() を持つモジュールの図を SVG で source/images に保存する."""
    if hasattr(module, "create_figure"):
        fig = module.create_figure()
        fig.savefig(_IMAGES / f"{name}.svg", bbox_inches="tight")
        plt.close(fig)


def _generate() -> None:
    """図生成スクリプトとサンプルを実行し、本文で使う図と実行結果を書き出す.

    * source/_scripts/fig_*.py の create_figure() の図を source/images に保存する。
    * examples/*.py の create_figure() の図を source/images に保存し、
      report() の標準出力を build/outputs にテキストで保存する。
    """
    _IMAGES.mkdir(parents=True, exist_ok=True)
    _OUTPUTS.mkdir(parents=True, exist_ok=True)
    sys.dont_write_bytecode = True  # __pycache__ を作らない
    plt.rcParams["svg.hashsalt"] = "fourier_dsp_introduction"  # 出力を毎回同じにする

    sys.path.insert(0, str(_SCRIPTS))
    fig_common = _load_module(_SCRIPTS / "fig_common.py")
    fig_common.setup_font()  # type: ignore[attr-defined]
    for path in sorted(_SCRIPTS.glob("fig_ch*.py")):
        _save_figure(_load_module(path), path.stem)
    sys.path.remove(str(_SCRIPTS))

    sys.path.insert(0, str(_EXAMPLES))
    for path in sorted(_EXAMPLES.glob("*.py")):
        if path.stem in _HELPER_MODULES:
            continue
        module = _load_module(path)
        _save_figure(module, path.stem)
        if hasattr(module, "report"):
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                module.report()
            (_OUTPUTS / f"{path.stem}.txt").write_text(buffer.getvalue(), encoding="utf-8")
    sys.path.remove(str(_EXAMPLES))


def _make_examples_zip() -> None:
    """examples フォルダのサンプルファイルを ZIP にまとめる."""
    _EXTRA.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in _EXAMPLES.iterdir() if p.is_file() and p.suffix in (".py", ".cfg"))
    with zipfile.ZipFile(_EXTRA / "examples.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("examples") / path.name)


# 本文から図、実行結果、:download: で参照するため、文書の読み込みより前に生成する
_generate()
_make_examples_zip()


def _remove_empty_sources(app: object, exception: Exception | None) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダを消す."""
    sources = Path(app.outdir) / "_sources"  # type: ignore[attr-defined]
    if exception is None and sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: object) -> None:
    """Sphinx の拡張機能として、ビルド後の処理を登録する."""
    app.connect("build-finished", _remove_empty_sources)  # type: ignore[attr-defined]
