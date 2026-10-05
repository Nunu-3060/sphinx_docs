"""Pratt 構文解析（演算子順位構文解析）による算術式の解析（第 4 章）。

演算子ごとに「結合力」を表で与え、1 つの関数で任意の優先順位の式を解析する。
結果は構造が分かるように括弧付きの S 式の文字列で返す。
"""

from __future__ import annotations

from tiny_lexer import Token, TinyError, TokenKind, tokenize

# 二項演算子の結合力（左、右）。数が大きいほど強く結び付く。
# 左結合の演算子は 右 = 左 + 1 とする。
BINARY_POWER: dict[TokenKind, tuple[int, int]] = {
    TokenKind.OR: (1, 2),
    TokenKind.AND: (3, 4),
    TokenKind.EQ: (5, 6),
    TokenKind.NE: (5, 6),
    TokenKind.LT: (7, 8),
    TokenKind.LE: (7, 8),
    TokenKind.GT: (7, 8),
    TokenKind.GE: (7, 8),
    TokenKind.PLUS: (9, 10),
    TokenKind.MINUS: (9, 10),
    TokenKind.STAR: (11, 12),
    TokenKind.SLASH: (11, 12),
    TokenKind.PERCENT: (11, 12),
}

PREFIX_POWER = 13  # 単項演算子 - と ! の結合力


class PrattParser:
    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self) -> str:
        result = self.expr(0)
        token = self.peek()
        if token.kind is not TokenKind.EOF:
            raise TinyError(f"余分な字句 {token.text!r} があります",
                            token.line, token.column)
        return result

    def expr(self, min_power: int) -> str:
        """結合力が min_power 以上の演算子だけを取り込んで式を解析する。"""
        left = self.prefix()
        while True:
            op = self.peek()
            power = BINARY_POWER.get(op.kind)
            if power is None or power[0] < min_power:
                return left
            self.advance()
            right = self.expr(power[1])
            left = f"({op.text} {left} {right})"

    def prefix(self) -> str:
        token = self.advance()
        if token.kind in (TokenKind.MINUS, TokenKind.NOT):
            operand = self.expr(PREFIX_POWER)
            return f"({token.text} {operand})"
        if token.kind in (TokenKind.INT, TokenKind.IDENT):
            return token.text
        if token.kind is TokenKind.LPAREN:
            inner = self.expr(0)
            if self.advance().kind is not TokenKind.RPAREN:
                raise TinyError(") が必要です", token.line, token.column)
            return inner
        raise TinyError(f"式が必要ですが {token.text!r} があります",
                        token.line, token.column)


def main() -> None:
    for source in ["1 + 2 * 3", "a - b - c", "-x * y",
                   "a < b && b < c || !d", "(1 + 2) * 3"]:
        print(f"{source:22} => {PrattParser(source).parse()}")


if __name__ == "__main__":
    main()
