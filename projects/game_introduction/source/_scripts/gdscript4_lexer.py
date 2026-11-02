"""Godot 4 の GDScript に対応させた Pygments の字句解析器。

Pygments に付属する GDScriptLexer は Godot 3 の文法を前提にしており、
@export などのアノテーションを解析できない。そこで不足する規則を追加する。
"""

from __future__ import annotations

from pygments.lexer import inherit, words
from pygments.lexers.gdscript import GDScriptLexer
from pygments.token import Keyword, Name


class GDScript4Lexer(GDScriptLexer):
    """アノテーション、ノードの参照（$Node、%Node）、Godot 4 の型とキーワードに対応した字句解析器。"""

    name = "GDScript 4"
    aliases = ["gdscript4"]

    tokens = {
        "root": [
            # @export、@onready などのアノテーション
            (r"@[a-zA-Z_]\w*", Name.Decorator),
            # $Sprite2D、$Coins/Coin1 のようなノードの参照
            (r"\$[a-zA-Z_][\w/]*", Name.Variable),
            # %HealthBar のようなシーン固有名による参照（剰余演算子の % とは前の文字で区別する）
            (r"(?<=[\s(\[,])%[a-zA-Z_]\w*", Name.Variable),
            (words(("await", "super", "when", "void"), suffix=r"\b"), Keyword),
            (
                words(
                    (
                        "Vector2i", "Vector3i", "Vector4", "Vector4i", "Rect2i", "Transform3D", "Quaternion",
                        "AABB", "Projection", "Callable", "Signal", "StringName",
                    ),
                    prefix=r"(?<!\.)",
                    suffix=r"\b",
                ),
                Name.Builtin.Type,
            ),
            inherit,
        ],
    }
