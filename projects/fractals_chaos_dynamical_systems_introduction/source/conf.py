"""Sphinx configuration for "フラクタル・カオス・力学系入門"."""

import os
import shutil
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

project = "フラクタル・カオス・力学系入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"

language = "ja"

extensions = [
    "sphinx.ext.githubpages",  # .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
]

templates_path: list[str] = []
exclude_patterns: list[str] = ["_figures"]

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

# 数式は MathJax 3 で表示する。Sphinx 9 の既定の MathJax 4 では、インライン数式が途中で改行されたり、
# 数式用のフォントの読み込みに失敗して文字が欠けたりすることがあるため
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"

# Graphviz の図は拡大しても劣化しない SVG で出力する
graphviz_output_format = "svg"

# dot コマンドが PATH にない場合は、Windows の既定のインストール先を PATH に加える
if shutil.which("dot") is None:
    _GRAPHVIZ_BIN = Path(os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin")
    if (_GRAPHVIZ_BIN / "dot.exe").exists():
        os.environ["PATH"] = f"{_GRAPHVIZ_BIN}{os.pathsep}{os.environ['PATH']}"

_ROOT = Path(__file__).resolve().parent.parent
_EXAMPLES = _ROOT / "examples"
_GENERATED = _ROOT / "build" / "generated"
_MAKE_FIGURES = Path(__file__).resolve().parent / "_figures" / "make_figures.py"


def _build_sample(sample: Path) -> tuple[Path, int, str]:
    """1 つのサンプルの図と実行結果を、別のプロセスで生成する."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    result = subprocess.run([sys.executable, str(_MAKE_FIGURES), str(sample), str(_GENERATED)],
                            capture_output=True, text=True, encoding="utf-8", env=env)
    return sample, result.returncode, result.stderr


def _generate_figures() -> None:
    """すべてのサンプルの図と実行結果を、並列に生成する（時間のかかるサンプルから始める）."""
    samples = sorted(_EXAMPLES.glob("ch*.py"), key=lambda p: p.stat().st_size, reverse=True)
    workers = max(1, min(len(samples), os.cpu_count() or 1))
    failed = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for sample, code, stderr in pool.map(_build_sample, samples):
            if code != 0:
                failed.append(f"{sample.name}:\n{stderr}")
    if failed:
        raise RuntimeError("図の生成に失敗したサンプルがある:\n" + "\n".join(failed))


def _make_examples_zip() -> None:
    """examples フォルダーのサンプルファイルを ZIP にまとめる."""
    _GENERATED.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in _EXAMPLES.iterdir() if p.is_file() and p.suffix in (".py", ".cfg"))
    with zipfile.ZipFile(_GENERATED / "examples.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, Path("examples") / path.name)


# 本文から図、実行結果、:download: で参照するため、文書の読み込みより前に生成する
_generate_figures()
_make_examples_zip()


def _remove_empty_sources(app: object, exception: Exception | None) -> None:
    """html_copy_source = False でも作られる空の _sources フォルダーを消す."""
    sources = Path(app.outdir) / "_sources"  # type: ignore[attr-defined]
    if exception is None and sources.is_dir() and not any(sources.iterdir()):
        sources.rmdir()


def setup(app: object) -> None:
    """Sphinx の拡張機能として、ビルド後の処理を登録する."""
    app.connect("build-finished", _remove_empty_sources)  # type: ignore[attr-defined]
