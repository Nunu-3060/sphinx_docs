# Sphinx 設定ファイル
# 詳細: https://www.sphinx-doc.org/ja/master/usage/configuration.html

import sys
from pathlib import Path

from sphinx.application import Sphinx
from sphinx.config import Config

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

# -- プロジェクト情報 ---------------------------------------------------------
project = "Markdown 入門"
author = "Nunu_3060"
copyright = "2026, Nunu_3060"
release = "1.0"
version = "1.0"

# -- 一般設定 -----------------------------------------------------------------
extensions = [
    "sphinx.ext.githubpages",  # GitHub Pages 用に .nojekyll を出力する
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "md_example",  # Markdown のソースと表示結果を並べる独自ディレクティブ
]

language = "ja"
exclude_patterns: list[str] = []
numfig = True
numfig_format = {
    "figure": "図 %s",
    "table": "表 %s",
    "code-block": "リスト %s",
    "section": "%s 章",
}

# -- Graphviz -----------------------------------------------------------------
graphviz_output_format = "svg"
graphviz_dot_args = [
    "-Gfontname=Meiryo",
    "-Nfontname=Meiryo",
    "-Efontname=Meiryo",
]

# -- HTML 出力 ----------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_title = f"{project} {release}"
html_static_path = ["_static"]
html_extra_path = ["_extra"]  # 表示結果の中で参照するサンプル画像
html_css_files = ["custom.css"]
html_show_sourcelink = False  # 「ソースを表示」リンクを出さない
html_copy_source = False  # rst ソースを _sources に複製しない
html_search_language = "ja"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# -- linkcheck ----------------------------------------------------------------
linkcheck_timeout = 30
linkcheck_retries = 2


# -- ビルド時に生成するファイル -----------------------------------------------
def make_sample_image(app: Sphinx, config: Config) -> None:
    """第 8 章の画像の例で表示するサンプル画像を作る。

    html_extra_path の存在確認より前に作るため、config-inited で呼び出す。
    """
    from PIL import Image, ImageDraw

    path = Path(app.srcdir) / "_extra" / "images" / "sample.png"
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 240, 120
    image = Image.new("RGB", (width, height), "#e8f0fe")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width - 1, height - 1), outline="#1a73e8", width=4)
    draw.ellipse((30, 25, 100, 95), fill="#1a73e8")
    draw.polygon([(130, 95), (170, 25), (210, 95)], fill="#34a853")
    image.save(path)


def setup(app: Sphinx) -> None:
    app.connect("config-inited", make_sample_image)
