"""Tiny 言語の字句解析器（第 3 章）。

ソースコードの文字列を先頭から 1 文字ずつ読み進め、トークンの列に変換する。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum, auto


class TinyError(Exception):
    """Tiny 処理系が報告するエラーの基底クラス。"""

    def __init__(self, message: str, line: int = 0, column: int = 0) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        if self.column > 0:
            return f"{self.line}:{self.column}: {self.message}"
        if self.line > 0:
            return f"{self.line}: {self.message}"
        return self.message


class LexError(TinyError):
    """字句解析で見つかったエラー。"""


class TokenKind(Enum):
    """トークンの種類。"""

    INT = auto()
    STRING = auto()
    IDENT = auto()
    # キーワード
    LET = auto()
    FN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    # 演算子と区切り記号
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    ASSIGN = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    ARROW = auto()
    EOF = auto()


KEYWORDS: dict[str, TokenKind] = {
    "let": TokenKind.LET,
    "fn": TokenKind.FN,
    "if": TokenKind.IF,
    "else": TokenKind.ELSE,
    "while": TokenKind.WHILE,
    "return": TokenKind.RETURN,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
}

# 2 文字の記号は 1 文字の記号より先に調べる（最長一致）。
TWO_CHAR_SYMBOLS: dict[str, TokenKind] = {
    "==": TokenKind.EQ,
    "!=": TokenKind.NE,
    "<=": TokenKind.LE,
    ">=": TokenKind.GE,
    "&&": TokenKind.AND,
    "||": TokenKind.OR,
    "->": TokenKind.ARROW,
}

ONE_CHAR_SYMBOLS: dict[str, TokenKind] = {
    "+": TokenKind.PLUS,
    "-": TokenKind.MINUS,
    "*": TokenKind.STAR,
    "/": TokenKind.SLASH,
    "%": TokenKind.PERCENT,
    "<": TokenKind.LT,
    ">": TokenKind.GT,
    "!": TokenKind.NOT,
    "=": TokenKind.ASSIGN,
    "(": TokenKind.LPAREN,
    ")": TokenKind.RPAREN,
    "{": TokenKind.LBRACE,
    "}": TokenKind.RBRACE,
    "[": TokenKind.LBRACKET,
    "]": TokenKind.RBRACKET,
    ",": TokenKind.COMMA,
    ";": TokenKind.SEMICOLON,
    ":": TokenKind.COLON,
}

ESCAPES: dict[str, str] = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}


def is_digit(ch: str) -> bool:
    """ch が ASCII の数字か（str.isdigit は全角数字なども真になる）。"""
    return ch.isascii() and ch.isdigit()


def is_ident_start(ch: str) -> bool:
    """ch が識別子の先頭に使える文字（ASCII の英字か _）か。"""
    return ch == "_" or (ch.isascii() and ch.isalpha())


def is_ident_char(ch: str) -> bool:
    """ch が識別子の 2 文字目以降に使える文字か。"""
    return is_ident_start(ch) or is_digit(ch)


@dataclass(frozen=True)
class Token:
    """トークン。text はソースコード上の字句そのもの。"""

    kind: TokenKind
    text: str
    line: int
    column: int
    value: int | str | None = None  # 整数・文字列リテラルの値


class Lexer:
    """ソースコードをトークン列に変換する。"""

    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def peek(self, offset: int = 0) -> str:
        """現在位置から offset 文字先の文字を返す（末尾なら空文字列）。"""
        index = self.pos + offset
        return self.source[index] if index < len(self.source) else ""

    def advance(self) -> str:
        """1 文字読み進め、読んだ文字を返す。"""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace_and_comments(self) -> None:
        while True:
            ch = self.peek()
            if ch in (" ", "\t", "\r", "\n"):
                self.advance()
            elif ch == "/" and self.peek(1) == "/":
                while self.peek() not in ("", "\n"):
                    self.advance()
            else:
                return

    def next_token(self) -> Token:
        """次のトークンを 1 つ切り出す。"""
        self.skip_whitespace_and_comments()
        line, column = self.line, self.column
        start = self.pos
        ch = self.peek()

        if ch == "":
            return Token(TokenKind.EOF, "", line, column)

        if is_digit(ch):
            while is_digit(self.peek()):
                self.advance()
            text = self.source[start:self.pos]
            return Token(TokenKind.INT, text, line, column, int(text))

        if is_ident_start(ch):
            while is_ident_char(self.peek()):
                self.advance()
            text = self.source[start:self.pos]
            kind = KEYWORDS.get(text, TokenKind.IDENT)
            return Token(kind, text, line, column)

        if ch == '"':
            return self.read_string(line, column)

        two = ch + self.peek(1)
        if two in TWO_CHAR_SYMBOLS:
            self.advance()
            self.advance()
            return Token(TWO_CHAR_SYMBOLS[two], two, line, column)

        if ch in ONE_CHAR_SYMBOLS:
            self.advance()
            return Token(ONE_CHAR_SYMBOLS[ch], ch, line, column)

        raise LexError(f"不正な文字 {ch!r} です", line, column)

    def read_string(self, line: int, column: int) -> Token:
        """文字列リテラルを読む。エスケープシーケンスを解釈する。"""
        start = self.pos
        self.advance()  # 開始の "
        chars: list[str] = []
        while True:
            ch = self.peek()
            if ch in ("", "\n"):
                raise LexError("文字列リテラルが閉じていません", line, column)
            self.advance()
            if ch == '"':
                break
            if ch == "\\":
                esc = self.peek()
                if esc not in ESCAPES:
                    raise LexError(
                        f"不正なエスケープシーケンス \\{esc} です",
                        self.line, self.column)
                self.advance()
                chars.append(ESCAPES[esc])
            else:
                chars.append(ch)
        text = self.source[start:self.pos]
        return Token(TokenKind.STRING, text, line, column, "".join(chars))

    def tokenize(self) -> list[Token]:
        """すべてのトークンを切り出す。末尾は必ず EOF トークンになる。"""
        tokens: list[Token] = []
        while True:
            token = self.next_token()
            tokens.append(token)
            if token.kind is TokenKind.EOF:
                return tokens


def tokenize(source: str) -> list[Token]:
    """ソースコードをトークン列に変換する。"""
    return Lexer(source).tokenize()


def main() -> None:
    source = 'let x = 10 * (y + 2); // コメント\nprint("x=", x >= 3);'
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    for token in tokenize(source):
        print(f"{token.line:3}:{token.column:<3} {token.kind.name:10} "
              f"{token.text}")


if __name__ == "__main__":
    main()
