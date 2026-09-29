# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import json
import pathlib
import subprocess
import sys
import zipfile

from sphinx.application import Sphinx

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Python で作る\nジェネラティブアート"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"

version = "1.0"
release = "1.0"

# -- General configuration ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

language = "ja"

# -- Options for HTML output ---------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_copy_source = False
html_show_sourcelink = False
html_css_files = ["custom.css"]

# -- Generate gallery images from examples/ -----------------------------------

# 他のスクリプトが生成する画像を読み込むスクリプトは、その画像を作る
# スクリプトより後に実行する必要がある。依存関係のあるものだけを先頭に
# 明示し、それ以外は名前順で後ろに続ける。
_GALLERY_SCRIPT_ORDER = [
    "perlin_noise.py",  # image_effects.py が perlin_noise.png を読む
    "mandelbrot.py",  # palette.py が julia.png を読む
    "reaction_diffusion.py",  # image_effects.py が coral 画像を読む
    "image_effects.py",
    "stippling.py",  # perlin_noise.png を読む
    "palette.py",
]

# ギャラリーに集める画像の拡張子。
_GALLERY_IMAGE_PATTERNS = ["*.png", "*.gif"]


def _list_images(directory: pathlib.Path) -> set[str]:
    """directory 直下にあるギャラリー対象の画像ファイル名を返す。"""
    return {
        path.name
        for pattern in _GALLERY_IMAGE_PATTERNS
        for path in directory.glob(pattern)
    }


def generate_gallery_images(app: Sphinx) -> None:
    """examples/ 以下の各スクリプトを実行し、生成された画像を
    _static/gallery に集める。

    スクリプトはそれぞれ画像をカレントディレクトリ（プロジェクト直下）
    に相対パスで保存するため、実行後にプロジェクト直下へ新たに現れた
    画像(.png と、アニメーションの .gif)だけをギャラリーへ移動する。スクリプトのソースが前回のビルド
    から変わっていなければ再実行をスキップし、ビルドのたびに全スクリプト
    (反応拡散系や進化的アルゴリズムなど、実行に時間がかかるものを含む)
    を走らせる無駄を避ける。
    """
    src_dir = pathlib.Path(app.srcdir)
    project_root = src_dir.parent
    examples_dir = project_root / "examples"
    gallery_dir = src_dir / "_static" / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)

    cache_path = project_root / ".gallery_cache.json"
    cache: dict[str, float] = {}
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))

    ordered_names = list(_GALLERY_SCRIPT_ORDER)
    ordered_names += sorted(
        path.name
        for path in examples_dir.glob("*.py")
        if path.name not in ordered_names
    )

    for name in ordered_names:
        script_path = examples_dir / name
        if not script_path.is_file():
            continue

        mtime = script_path.stat().st_mtime
        if cache.get(name) == mtime:
            continue

        before = _list_images(project_root)
        subprocess.run(
            [sys.executable, str(script_path)],
            cwd=project_root,
            check=True,
        )
        after = _list_images(project_root)
        for image_name in after - before:
            (project_root / image_name).replace(gallery_dir / image_name)

        cache[name] = mtime

    cache_path.write_text(json.dumps(cache), encoding="utf-8")


# -- Build examples.zip for download ------------------------------------------


def generate_examples_zip(app: Sphinx) -> None:
    """examples/ 以下の .py ファイルをまとめて _static/downloads/examples.zip に固める。"""
    src_dir = pathlib.Path(app.srcdir)
    examples_dir = src_dir.parent / "examples"
    output_dir = src_dir / "_static" / "downloads"
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / "examples.zip"

    py_files = sorted(examples_dir.glob("*.py"))

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for py_file in py_files:
            zf.write(py_file, arcname=f"examples/{py_file.name}")


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", generate_gallery_images)
    app.connect("builder-inited", generate_examples_zip)
