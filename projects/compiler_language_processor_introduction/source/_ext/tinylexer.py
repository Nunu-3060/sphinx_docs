"""Tiny 言語用の Pygments レキサー（コード例の構文の強調表示）。"""

from pygments.lexer import RegexLexer, words
from pygments.token import (
    Comment, Keyword, Name, Number, Operator, Punctuation, String, Text)


class TinyLexer(RegexLexer):
    name = "Tiny"
    aliases = ["tiny"]
    filenames = ["*.tiny"]

    tokens = {
        "root": [
            (r"\s+", Text),
            (r"//.*?$", Comment.Single),
            (words(("let", "fn", "if", "else", "while", "return"),
                   suffix=r"\b"), Keyword),
            (words(("true", "false"), suffix=r"\b"), Keyword.Constant),
            (words(("int", "bool", "str"), suffix=r"\b"), Keyword.Type),
            (words(("print", "len", "push", "to_str"), suffix=r"\b"),
             Name.Builtin),
            (r'"(\\.|[^"\\])*"', String),
            (r"[0-9]+", Number.Integer),
            (r"[A-Za-z_][A-Za-z0-9_]*", Name),
            (r"->|==|!=|<=|>=|&&|\|\||[-+*/%<>!=]", Operator),
            (r"[()\[\]{},;:]", Punctuation),
        ],
    }


def setup(app):
    app.add_lexer("tiny", TinyLexer)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
