"""md-example ディレクティブ: Markdown のソースと、その表示結果を並べて出力する。

使い方::

    .. md-example::
       :github:

       - [ ] 牛乳を買う
       - [x] 部屋を掃除する

オプション:

``:github:``
    GitHub に近い表示にする（GFM の拡張、脚注、アラート、見出しの ID）。
``:math:``
    ``:github:`` に加えて数式（``$...$``、``$$...$$``）を有効にする。
``:front-matter:``
    ``:github:`` に加えてフロントマター（YAML）を有効にする。
``:breaks:``
    ``:github:`` に加えて、ソース中の改行をそのまま改行として表示する（GitHub のコメント欄の動作）。
``:file:``
    本文の代わりに、指定したファイルを Markdown のソースとして読み込む。
``:no-render:``
    表示結果を出さず、ソースだけを示す。
``:caption:``
    例の上に表示する見出し。
"""

from __future__ import annotations

import html
from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst import directives
from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.gfm import gfm_plugin
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata, OptionSpec

MATH_CLASS = "md-example-math"


def render_math(content: str, options: dict[str, Any]) -> str:
    """数式を MathJax が描画できる区切り記号で囲む。"""
    escaped = html.escape(content)
    if options.get("display_mode"):
        return f"\\[{escaped}\\]"
    return f"\\({escaped}\\)"


def create_parser(*, github: bool, math: bool, front_matter: bool, breaks: bool) -> MarkdownIt:
    """オプションに応じた Markdown パーサーを作る。"""
    md = MarkdownIt("commonmark", {"breaks": breaks})
    if github:
        md.use(gfm_plugin, front_matter=front_matter)
        md.use(anchors_plugin, min_level=1, max_level=6)
        if math:
            md.use(dollarmath_plugin, allow_blank_lines=False, renderer=render_math)
    return md


class MarkdownExample(SphinxDirective):
    """Markdown のソースと表示結果を出力するディレクティブ。"""

    has_content = True
    option_spec: ClassVar[OptionSpec] = {
        "github": directives.flag,
        "math": directives.flag,
        "front-matter": directives.flag,
        "breaks": directives.flag,
        "file": directives.path,
        "no-render": directives.flag,
        "caption": directives.unchanged,
    }

    def read_source(self) -> str:
        if "file" in self.options:
            relpath, abspath = self.env.relfn2path(self.options["file"])
            self.env.note_dependency(relpath)
            with open(abspath, encoding="utf-8") as f:
                return f.read()
        if not self.content:
            raise self.error("md-example には本文か :file: オプションが必要である。")
        return "\n".join(self.content) + "\n"

    def run(self) -> list[nodes.Node]:
        source = self.read_source()
        math = "math" in self.options
        front_matter = "front-matter" in self.options
        breaks = "breaks" in self.options
        github = "github" in self.options or math or front_matter or breaks

        container = nodes.container(classes=["md-example"])
        if "caption" in self.options:
            container += nodes.paragraph(self.options["caption"], self.options["caption"],
                                         classes=["md-example-caption"])

        container += nodes.paragraph("書き方", "書き方", classes=["md-example-label"])
        # rawsource と本文が異なると Sphinx はハイライトしないので、同じ文字列を渡す
        text = source.rstrip("\n")
        code = nodes.literal_block(text, text)
        code["language"] = "markdown"
        code["linenos"] = True
        container += code

        if "no-render" not in self.options:
            # 脚注の ID が例どうしで重複しないよう、例ごとに異なる docId を渡す
            doc_id = f"ex{self.env.new_serialno('md-example')}"
            parser = create_parser(github=github, math=math, front_matter=front_matter, breaks=breaks)
            body = parser.render(source, {"docId": doc_id})
            if breaks:
                label = "表示結果（GitHub のコメント欄）"
            elif github:
                label = "表示結果（GitHub）"
            else:
                label = "表示結果（CommonMark）"
            container += nodes.paragraph(label, label, classes=["md-example-label"])
            result = f'<div class="md-result">\n{body}</div>\n'
            container += nodes.raw("", result, format="html")
            if math:
                container["classes"].append(MATH_CLASS)
        return [container]


def enable_mathjax(app: Sphinx, pagename: str, templatename: str,
                   context: dict[str, Any], doctree: nodes.document | None) -> None:
    """数式の例を含むページで MathJax を読み込ませる。

    Sphinx は数式のノードがあるページでだけ MathJax を読み込む。表示結果の数式は
    生の HTML なので、sphinx.ext.mathjax より先にこの関数で読み込みを指示する。
    """
    if doctree is None:
        return
    for node in doctree.findall(nodes.container):
        if MATH_CLASS in node["classes"]:
            context["has_maths_elements"] = True
            return


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("md-example", MarkdownExample)
    app.connect("html-page-context", enable_mathjax, priority=400)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
