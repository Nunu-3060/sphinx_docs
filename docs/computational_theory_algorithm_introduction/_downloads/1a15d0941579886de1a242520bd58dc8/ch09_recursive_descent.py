"""第 9 章: 再帰下降構文解析による四則演算の電卓。

次の文法の各変数を 1 つの関数として実装する。
演算子の優先順位と左結合性は文法の形で表現されている。

    expr   -> term (("+" | "-") term)*
    term   -> factor (("*" | "/") factor)*
    factor -> NUMBER | "(" expr ")" | "-" factor

実行例::

    python ch09_recursive_descent.py
"""

from __future__ import annotations

import re

TOKEN_PATTERN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(.))")


def tokenize(text: str) -> list[str]:
    """文字列を数値と記号のトークンに分ける。"""
    tokens: list[str] = []
    for number, symbol in TOKEN_PATTERN.findall(text):
        if number:
            tokens.append(number)
        elif symbol.strip():
            tokens.append(symbol)
    return tokens


class Parser:
    """トークン列を左から読み、式の値を計算する。"""

    def __init__(self, text: str) -> None:
        self.tokens = tokenize(text)
        self.pos = 0

    def peek(self) -> str | None:
        """次のトークンを返す (読み進めない)。"""
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def take(self) -> str:
        """次のトークンを読み進めて返す。"""
        token = self.peek()
        if token is None:
            raise SyntaxError("式が途中で終わっている")
        self.pos += 1
        return token

    def parse(self) -> float:
        """式全体を解析して値を返す。"""
        value = self.expr()
        if self.peek() is not None:
            raise SyntaxError(f"余分なトークン: {self.peek()}")
        return value

    def expr(self) -> float:
        value = self.term()
        while self.peek() in ("+", "-"):
            if self.take() == "+":
                value += self.term()
            else:
                value -= self.term()
        return value

    def term(self) -> float:
        value = self.factor()
        while self.peek() in ("*", "/"):
            if self.take() == "*":
                value *= self.factor()
            else:
                value /= self.factor()
        return value

    def factor(self) -> float:
        token = self.take()
        if token == "(":
            value = self.expr()
            if self.take() != ")":
                raise SyntaxError("')' が必要")
            return value
        if token == "-":
            return -self.factor()
        try:
            return float(token)
        except ValueError:
            raise SyntaxError(f"予期しないトークン: {token}") from None


def main() -> None:
    for text in ["1 + 2 * 3", "(1 + 2) * 3", "10 - 4 - 3", "2 * -(3 + 4)",
                 "8 / 4 / 2", "1 + * 2"]:
        try:
            print(f"{text} = {Parser(text).parse()}")
        except SyntaxError as error:
            print(f"{text}: 構文エラー ({error})")


if __name__ == "__main__":
    main()
