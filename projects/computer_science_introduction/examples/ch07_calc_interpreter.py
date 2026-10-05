"""四則演算と括弧の式を評価する小さなインタプリタ。

第 7 章「プログラミング言語処理系」のサンプルである。次の 3 段階で
式を処理する。

1. 字句解析: 文字列をトークンの列に分ける
2. 構文解析: 再帰下降構文解析で抽象構文木（AST）を作る
3. 評価: AST をたどって値を計算する

文法（EBNF）::

    expr   ::= term   { ("+" | "-") term }
    term   ::= factor { ("*" | "/") factor }
    factor ::= NUMBER | "(" expr ")" | "-" factor

実行方法::

    python ch07_calc_interpreter.py
"""

import operator
import re
from collections.abc import Callable
from dataclasses import dataclass

# ---- 字句解析 ----------------------------------------------------------

# 数値（整数または小数）か、それ以外の 1 文字にマッチする
TOKEN_RE = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|(.))")


@dataclass(frozen=True)
class Token:
    """トークン. kind は "NUM"、"OP"、"END" のいずれか."""

    kind: str
    text: str


def tokenize(source: str) -> list[Token]:
    """文字列をトークンの列に変換する."""
    tokens: list[Token] = []
    for number, other in TOKEN_RE.findall(source.rstrip()):
        if number:
            tokens.append(Token("NUM", number))
        elif other in "+-*/()":
            tokens.append(Token("OP", other))
        else:
            raise SyntaxError(f"不正な文字: {other!r}")
    tokens.append(Token("END", ""))  # 入力の終わりを表す
    return tokens


# ---- 抽象構文木 --------------------------------------------------------


@dataclass(frozen=True)
class Num:
    """数値リテラル."""

    value: float


@dataclass(frozen=True)
class Neg:
    """単項マイナス."""

    operand: "Node"


@dataclass(frozen=True)
class BinOp:
    """二項演算. op は "+"、"-"、"*"、"/" のいずれか."""

    op: str
    left: "Node"
    right: "Node"


Node = Num | Neg | BinOp


# ---- 構文解析（再帰下降） ----------------------------------------------


class Parser:
    """文法の非終端記号 1 つに 1 つのメソッドを対応させた構文解析器."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> str:
        """次のトークンの文字列を、読み進めずに返す."""
        return self.tokens[self.pos].text

    def advance(self) -> Token:
        """次のトークンを返し、1 つ読み進める."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self) -> Node:
        """式全体を解析し、入力が残っていればエラーにする."""
        node = self.expr()
        if self.tokens[self.pos].kind != "END":
            raise SyntaxError(f"余分なトークン: {self.peek()!r}")
        return node

    def expr(self) -> Node:
        """expr ::= term { ("+" | "-") term }."""
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.advance().text
            node = BinOp(op, node, self.term())  # 左結合になる
        return node

    def term(self) -> Node:
        """term ::= factor { ("*" | "/") factor }."""
        node = self.factor()
        while self.peek() in ("*", "/"):
            op = self.advance().text
            node = BinOp(op, node, self.factor())
        return node

    def factor(self) -> Node:
        """factor ::= NUMBER | "(" expr ")" | "-" factor."""
        token = self.advance()
        if token.kind == "NUM":
            return Num(float(token.text))
        if token.text == "(":
            node = self.expr()
            if self.advance().text != ")":
                raise SyntaxError("')' がない")
            return node
        if token.text == "-":
            return Neg(self.factor())
        raise SyntaxError(f"予期しないトークン: {token.text!r}")


# ---- 評価 --------------------------------------------------------------

OPS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def evaluate(node: Node) -> float:
    """AST を再帰的にたどって値を計算する."""
    match node:
        case Num(value):
            return value
        case Neg(operand):
            return -evaluate(operand)
        case BinOp(op, left, right):
            return OPS[op](evaluate(left), evaluate(right))


def dump(node: Node, depth: int) -> None:
    """AST を字下げした木の形で表示する."""
    pad = "  " * depth
    match node:
        case Num(value):
            print(f"{pad}Num {value}")
        case Neg(operand):
            print(f"{pad}Neg")
            dump(operand, depth + 1)
        case BinOp(op, left, right):
            print(f"{pad}BinOp {op}")
            dump(left, depth + 1)
            dump(right, depth + 1)


def main() -> None:
    """いくつかの式について、トークン列・AST・値を表示する."""
    tokens = tokenize("2 * (3 + 4) - 5")
    print("トークン:", [t.text for t in tokens if t.kind != "END"])
    tree = Parser(tokens).parse()
    print("AST:")
    dump(tree, 1)
    print("値:", evaluate(tree))

    print("その他の式:")
    for text in ["1 - 2 - 3", "1 + 2 * 3", "-(4 - 6) / 4", "(1 + 2", "3 4"]:
        try:
            value = evaluate(Parser(tokenize(text)).parse())
            print(f"  {text} = {value}")
        except SyntaxError as e:
            print(f"  {text} -> 構文エラー: {e}")


if __name__ == "__main__":
    main()
