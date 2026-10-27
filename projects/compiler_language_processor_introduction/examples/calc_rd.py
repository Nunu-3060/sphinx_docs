"""再帰下降構文解析による電卓（第 4 章）。

次の文法に従って算術式を構文解析し、解析しながら値を計算する。

    expr   = term { ("+" | "-") term } ;
    term   = factor { ("*" | "/" | "%") factor } ;
    factor = "-" factor | INT | "(" expr ")" ;
"""

from __future__ import annotations

from tiny_lexer import Token, TinyError, TokenKind, tokenize
from tiny_runtime import int_div, int_mod


class CalcParser:
    """非終端記号ごとに 1 つのメソッドを持つ再帰下降構文解析器。"""

    def __init__(self, source: str) -> None:
        self.tokens = tokenize(source)
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, kind: TokenKind) -> Token:
        token = self.peek()
        if token.kind is not kind:
            raise TinyError(f"{kind.name} が必要ですが {token.text!r} があります",
                            token.line, token.column)
        return self.advance()

    def parse(self) -> int:
        value = self.expr()
        self.expect(TokenKind.EOF)
        return value

    def expr(self) -> int:
        # expr = term { ("+" | "-") term }
        value = self.term()
        while self.peek().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self.advance().kind
            right = self.term()
            value = value + right if op is TokenKind.PLUS else value - right
        return value

    def term(self) -> int:
        # term = factor { ("*" | "/" | "%") factor }
        value = self.factor()
        while self.peek().kind in (TokenKind.STAR, TokenKind.SLASH,
                                   TokenKind.PERCENT):
            op = self.advance().kind
            right = self.factor()
            if op is TokenKind.STAR:
                value = value * right
            elif op is TokenKind.SLASH:
                value = int_div(value, right)
            else:
                value = int_mod(value, right)
        return value

    def factor(self) -> int:
        # factor = "-" factor | INT | "(" expr ")"
        token = self.peek()
        if token.kind is TokenKind.MINUS:
            self.advance()
            return -self.factor()
        if token.kind is TokenKind.INT:
            self.advance()
            assert isinstance(token.value, int)
            return token.value
        if token.kind is TokenKind.LPAREN:
            self.advance()
            value = self.expr()
            self.expect(TokenKind.RPAREN)
            return value
        raise TinyError(f"式が必要ですが {token.text!r} があります",
                        token.line, token.column)


def calculate(source: str) -> int:
    return CalcParser(source).parse()


def main() -> None:
    for source in ["1 + 2 * 3", "(1 + 2) * 3", "10 - 4 - 3", "-7 / 2",
                   "2 * (3 + 4) % 5"]:
        print(f"{source} = {calculate(source)}")


if __name__ == "__main__":
    main()
