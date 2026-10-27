# Configuration file for the Sphinx documentation builder.
#
# ビルド開始時（builder-inited）に次の処理を行う。
#
# * examples/ と source/_figures/ のスクリプトを呼び出し、本文で使う図を source/_generated/ に出力する。
# * パストレーサーの画像は生成に時間がかかるため、画像が存在し、かつ path_tracer.py より新しい場合は再生成しない。
# * examples/ のサンプルコード一式を ZIP にまとめ、一括ダウンロードできるようにする。

import os
import sys
import zipfile
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import logging

SOURCE_DIR = Path(__file__).resolve().parent
ROOT_DIR = SOURCE_DIR.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
FIGURES_DIR = SOURCE_DIR / "_figures"
GENERATED_DIR = SOURCE_DIR / "_generated"
EXAMPLES_ZIP = GENERATED_DIR / "pbr_examples.zip"

os.environ.setdefault("MPLBACKEND", "Agg")
sys.dont_write_bytecode = True  # examples/ に __pycache__ を作らない
sys.path.insert(0, str(EXAMPLES_DIR))
sys.path.insert(0, str(FIGURES_DIR))

logger = logging.getLogger(__name__)

# -- Project information -----------------------------------------------------

project = "物理ベースレンダリング入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.graphviz",
    "sphinx.ext.githubpages",  # .nojekyll を出力する
]

language = "ja"
exclude_patterns = ["_figures", "_generated"]
numfig = True
math_numfig = True
graphviz_output_format = "svg"
graphviz_dot_args = ["-Nfontname=Meiryo", "-Efontname=Meiryo", "-Gfontname=Meiryo"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = project
html_copy_source = False      # rst ソースを出力しない
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_theme_options = {
    "navigation_depth": 3,
}
html_static_path = ["_static"]
html_css_files = ["custom.css"]


# -- Build-time generation ---------------------------------------------------

def _needs_update(target: Path, *sources: Path) -> bool:
    """target が存在しないか、sources のいずれかより古ければ True を返す。"""
    if not target.exists():
        return True
    return any(target.stat().st_mtime < source.stat().st_mtime for source in sources)


def generate_figures() -> None:
    """本文で使う図を生成する。"""
    import brdf_plot
    import diagrams
    import fresnel_plot
    import monte_carlo
    import tone_mapping

    GENERATED_DIR.mkdir(exist_ok=True)
    out = GENERATED_DIR
    tone_mapping.plot_srgb_curve(out / "srgb_curve.png")
    tone_mapping.plot_tone_curves(out / "tone_curves.png")
    tone_mapping.plot_tone_mapping_comparison(out / "tone_mapping_comparison.png")
    fresnel_plot.plot_fresnel(out / "fresnel.png")
    brdf_plot.plot_lobes(out / "brdf_lobes.png")
    brdf_plot.plot_ggx(out / "ggx_distribution.png")
    brdf_plot.plot_spheres(out / "roughness_spheres.png")
    monte_carlo.plot_convergence(out / "mc_convergence.png")
    monte_carlo.plot_importance(out / "mc_importance.png")
    diagrams.plot_solid_angle(out / "solid_angle.png")
    diagrams.plot_snell(out / "snell.png")
    diagrams.plot_microfacets(out / "microfacets.png")
    diagrams.plot_rendering_equation(out / "rendering_equation.png")


def generate_renders() -> None:
    """パストレーサーで画像を描画する。最新の画像が既にあれば再生成しない。"""
    import path_tracer

    scene = path_tracer.cornell_box_scene()
    jobs: list[tuple[str, int, int, bool]] = [
        # (ファイル名, 画像の一辺の画素数, spp, 次イベント推定を使うか)
        ("render_main.png", 256, 128, True),
        ("render_spp1.png", 160, 1, True),
        ("render_spp4.png", 160, 4, True),
        ("render_spp16.png", 160, 16, True),
        ("render_spp64.png", 160, 64, True),
        ("render_no_nee16.png", 160, 16, False),
    ]
    source = EXAMPLES_DIR / "path_tracer.py"
    for name, size, spp, use_nee in jobs:
        target = GENERATED_DIR / name
        if not _needs_update(target, source):
            continue
        logger.info(f"rendering {name} ({size} x {size}, {spp} spp) ...")
        image = path_tracer.render(scene, size, size, spp, use_nee=use_nee, seed=1)
        path_tracer.save_image(image, target)

    make_montage(GENERATED_DIR / "render_spp_series.png",
                 [("render_spp1.png", "1 spp"), ("render_spp4.png", "4 spp"),
                  ("render_spp16.png", "16 spp"), ("render_spp64.png", "64 spp")])
    make_montage(GENERATED_DIR / "render_nee_comparison.png",
                 [("render_no_nee16.png", "without NEE (16 spp)"), ("render_spp16.png", "with NEE (16 spp)")])


def make_montage(output: Path, items: list[tuple[str, str]]) -> None:
    """複数の画像を横に並べ、それぞれの下にラベルを付けた 1 枚の画像を作る。"""
    from PIL import Image, ImageDraw, ImageFont

    images = [Image.open(GENERATED_DIR / name).convert("RGB") for name, _ in items]
    width, height = images[0].size
    gap, label_height = 8, 28
    montage = Image.new("RGB", (len(images) * (width + gap) - gap, height + label_height), "white")
    draw = ImageDraw.Draw(montage)
    font = ImageFont.load_default(size=15)
    for index, (image, (_, label)) in enumerate(zip(images, items)):
        x = index * (width + gap)
        montage.paste(image, (x, 0))
        text_width = draw.textlength(label, font=font)
        draw.text((x + (width - text_width) / 2, height + 6), label, fill="black", font=font)
    montage.save(output)


def make_examples_zip() -> None:
    """examples/ のファイルを ZIP にまとめる。"""
    files = sorted(p for p in EXAMPLES_DIR.iterdir()
                   if p.is_file() and p.suffix in {".py", ".cfg", ".txt"})
    with zipfile.ZipFile(EXAMPLES_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, arcname=f"examples/{path.name}")


def on_builder_inited(app: Sphinx) -> None:
    generate_figures()
    generate_renders()
    make_examples_zip()


def on_build_finished(app: Sphinx, exception: Exception | None) -> None:
    # html_copy_source = False でも空の _sources フォルダが作られるため削除する
    sources_dir = Path(app.outdir) / "_sources"
    if exception is None and sources_dir.is_dir() and not any(sources_dir.iterdir()):
        sources_dir.rmdir()


def setup(app: Sphinx) -> None:
    app.connect("builder-inited", on_builder_inited)
    app.connect("build-finished", on_build_finished)
