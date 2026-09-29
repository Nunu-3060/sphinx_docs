# Sphinx の設定ファイル
# https://www.sphinx-doc.org/ja/master/usage/configuration.html

import shutil
from pathlib import Path

# -- プロジェクト情報 ---------------------------------------------------------

project = "GLSL 入門"
copyright = "2026, Nunu_3060"
author = "Nunu_3060"
release = "1.0"

# -- 一般設定 -----------------------------------------------------------------

extensions = [
    "sphinx.ext.mathjax",      # 数式の表示
    "sphinx.ext.githubpages",  # 出力先に .nojekyll を作成する
]

language = "ja"
templates_path = []
exclude_patterns = []

# コードブロックの既定の言語
highlight_language = "glsl"

# -- HTML 出力の設定 ----------------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_title = "GLSL 入門"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}

# rst のソースを HTML から閲覧できないようにする
html_show_sourcelink = False
html_copy_source = False

html_static_path = ["_static"]
html_css_files = ["custom.css"]

# -- linkcheck の設定 ---------------------------------------------------------
# ../examples/ へのリンクはビルド後にコピーされるファイルを指すため、linkcheck の対象外にする。
# Shadertoy は自動アクセスを拒否する（403）ため対象外にする。
linkcheck_ignore = [
    r"\.\./examples/.*",
    r"https://www\.shadertoy\.com/",
]

# -- サンプルコードの処理 -----------------------------------------------------
# (1) examples の HTML に埋め込まれたシェーダーを取り出し、examples/shaders に .vert / .frag として書き出す。
#     本文の literalinclude と、シェーダーのダウンロード用のリンクはこのファイルを参照する。
#     元のソースは HTML で、シェーダーのファイルはビルドのたびに HTML から作り直す。
#     そのため、HTML とシェーダーのファイルの内容が食い違うことはない。
# (2) examples フォルダーを build/html/examples にコピーし、HTML から直接実行できるようにする。
#     （ダウンロード用のファイルは rst の :download: ロールで _downloads に出力される）

import re

ROOT_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = ROOT_DIR / "examples"
SHADERS_DIR = EXAMPLES_DIR / "shaders"

# <script id="vertex-shader" type="x-shader/x-vertex"> や
# <script id="wave-fragment-shader" type="x-shader/x-fragment"> の形の要素を探す
SHADER_SCRIPT = re.compile(
    r'<script id="(?:(?P<prefix>[a-z0-9]+)-)?(?P<stage>vertex|fragment)-shader" '
    r'type="x-shader/x-(?:vertex|fragment)">(?P<source>.*?)</script>',
    re.S,
)
EXTENSIONS = {"vertex": ".vert", "fragment": ".frag"}


def extract_shaders(app):
    """HTML のシェーダーを、ファイル名_接頭辞.vert / .frag として書き出す"""
    SHADERS_DIR.mkdir(parents=True, exist_ok=True)
    written = set()
    for html_path in sorted(EXAMPLES_DIR.glob("*.html")):
        text = html_path.read_text(encoding="utf-8")
        matches = list(SHADER_SCRIPT.finditer(text))
        # フラグメントシェーダーを JavaScript の文字列で持つサンプル（12_shader_editor.html）は対象外
        if not any(m.group("stage") == "fragment" for m in matches):
            continue
        for match in matches:
            name = html_path.stem
            if match.group("prefix"):
                name += "_" + match.group("prefix")
            # JavaScript 側の getShaderSource() と同じく、前後の空白と改行を取り除く
            source = match.group("source").strip() + "\n"
            out_path = SHADERS_DIR / (name + EXTENSIONS[match.group("stage")])
            # 内容が変わらない場合は書き換えない（Sphinx の再ビルドの判定に使われるため）
            if not out_path.exists() or out_path.read_text(encoding="utf-8") != source:
                out_path.write_text(source, encoding="utf-8", newline="\n")
            written.add(out_path.name)
    # 対応する HTML がなくなったシェーダーのファイルを削除する
    for old_path in list(SHADERS_DIR.glob("*.vert")) + list(SHADERS_DIR.glob("*.frag")):
        if old_path.name not in written:
            old_path.unlink()


def copy_examples(app, exception):
    if exception is not None or app.builder.format != "html":
        return
    shutil.copytree(EXAMPLES_DIR, Path(app.outdir) / "examples", dirs_exist_ok=True)


def setup(app):
    app.connect("builder-inited", extract_shaders)
    app.connect("build-finished", copy_examples)
