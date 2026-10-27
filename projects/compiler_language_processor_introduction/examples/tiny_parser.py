"""Tiny 言語の構文解析器（第 5 章）。

文は再帰下降構文解析で、式は Pratt 構文解析で解析し、抽象構文木を作る。
文の途中で構文エラーを見つけたら、次の文の先頭まで読み飛ばして解析を続け
（パニックモードのエラー回復）、見つかったエラーをまとめて報告する。
"""

from __future__ import annotations

import sys

from tiny_ast import (
    BOOL, INT, STR, VOID, ArrayLit, ArrayType, Assign, Binary, Block, BoolLit,
    Call, Expr, ExprStmt, FuncDef, If, Index, IntLit, Let, Name, Param,
    Program, Return, Stmt, StrLit, Type, Unary, While, dump)
from tiny_lexer import Token, TinyError, TokenKind, tokenize


class ParseError(TinyError):
    """構文エラー。all_errors に見つかったすべてのエラーを持つ。"""

    def __init__(self, message: str, line: int = 0, column: int = 0) -> None:
        super().__init__(message, line, column)
        self.all_errors: list[ParseError] = [self]


# 二項演算子の結合力（左、右）。すべて左結合。
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
PREFIX_POWER = 13
POSTFIX_POWER = 15  # 関数呼び出し f(...) と添字 a[...]

TYPE_NAMES: dict[str, Type] = {"int": INT, "bool": BOOL, "str": STR}

# エラー回復で読み飛ばしを止める、文の先頭になるキーワード
STATEMENT_START = (TokenKind.LET, TokenKind.IF, TokenKind.WHILE,
                   TokenKind.RETURN, TokenKind.FN)

# 式の先頭になり得る字句
PREFIX_START = (TokenKind.INT, TokenKind.STRING, TokenKind.TRUE,
                TokenKind.FALSE, TokenKind.IDENT, TokenKind.MINUS,
                TokenKind.NOT, TokenKind.LPAREN, TokenKind.LBRACKET)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0
        self.errors: list[ParseError] = []

    # ------------------------------------------------ 字句の操作

    def peek(self, offset: int = 0) -> Token:
        index = min(self.pos + offset, len(self.tokens) - 1)
        return self.tokens[index]

    def at(self, kind: TokenKind) -> bool:
        return self.peek().kind is kind

    def advance(self) -> Token:
        token = self.peek()
        if token.kind is not TokenKind.EOF:
            self.pos += 1
        return token

    def accept(self, kind: TokenKind) -> bool:
        """次の字句が kind なら読み進めて True を返す。"""
        if self.at(kind):
            self.advance()
            return True
        return False

    def expect(self, kind: TokenKind, what: str) -> Token:
        if not self.at(kind):
            raise self.error(f"{what} が必要です")
        return self.advance()

    def error(self, message: str) -> ParseError:
        token = self.peek()
        found = "ファイルの終わり" if token.kind is TokenKind.EOF \
            else f"{token.text!r}"
        return ParseError(f"{message}（{found} があります）",
                          token.line, token.column)

    def synchronize(self) -> None:
        """エラー回復: 文の区切りまで字句を読み飛ばす。"""
        while not self.at(TokenKind.EOF):
            if self.accept(TokenKind.SEMICOLON):
                return
            if self.peek().kind in (*STATEMENT_START, TokenKind.RBRACE):
                return
            self.advance()

    # ------------------------------------------------ プログラムと関数

    def parse_program(self) -> Program:
        functions: list[FuncDef] = []
        while not self.at(TokenKind.EOF):
            try:
                functions.append(self.parse_function())
            except ParseError as e:
                self.errors.append(e)
                self.advance()
                while not self.at(TokenKind.EOF) and not self.at(TokenKind.FN):
                    self.advance()
        if self.errors:
            first = self.errors[0]
            first.all_errors = self.errors
            raise first
        return Program(functions, line=1)

    def parse_function(self) -> FuncDef:
        # function = "fn" IDENT "(" [ param { "," param } ] ")"
        #            [ "->" type ] block
        line = self.expect(TokenKind.FN, "関数定義 fn").line
        name = self.expect(TokenKind.IDENT, "関数名").text
        self.expect(TokenKind.LPAREN, "(")
        params: list[Param] = []
        if not self.at(TokenKind.RPAREN):
            while True:
                token = self.expect(TokenKind.IDENT, "引数名")
                self.expect(TokenKind.COLON, ":")
                params.append(Param(token.text, self.parse_type(),
                                    line=token.line))
                if not self.accept(TokenKind.COMMA):
                    break
        self.expect(TokenKind.RPAREN, ")")
        return_type: Type = VOID
        if self.accept(TokenKind.ARROW):
            return_type = self.parse_type()
        body = self.parse_block()
        return FuncDef(name, params, return_type, body, line=line)

    def parse_type(self) -> Type:
        # type = "int" | "bool" | "str" | "[" type "]"
        if self.accept(TokenKind.LBRACKET):
            element = self.parse_type()
            self.expect(TokenKind.RBRACKET, "]")
            return ArrayType(element)
        token = self.expect(TokenKind.IDENT, "型名")
        if token.text not in TYPE_NAMES:
            raise ParseError(f"未知の型 {token.text} です",
                             token.line, token.column)
        return TYPE_NAMES[token.text]

    # ------------------------------------------------ 文

    def parse_block(self) -> Block:
        # block = "{" { statement } "}"
        line = self.expect(TokenKind.LBRACE, "{").line
        stmts: list[Stmt] = []
        while not self.at(TokenKind.RBRACE) and not self.at(TokenKind.EOF):
            start = self.pos
            try:
                stmts.append(self.parse_statement())
            except ParseError as e:
                self.errors.append(e)
                self.synchronize()
                if self.pos == start:  # 1 字句も進まなければ強制的に進める
                    self.advance()
        self.expect(TokenKind.RBRACE, "}")
        return Block(stmts, line=line)

    def parse_statement(self) -> Stmt:
        token = self.peek()
        line = token.line
        match token.kind:
            case TokenKind.LBRACE:
                return self.parse_block()
            case TokenKind.LET:
                # "let" IDENT [ ":" type ] "=" expr ";"
                self.advance()
                name = self.expect(TokenKind.IDENT, "変数名").text
                declared: Type | None = None
                if self.accept(TokenKind.COLON):
                    declared = self.parse_type()
                self.expect(TokenKind.ASSIGN, "=")
                value = self.parse_expr()
                self.expect(TokenKind.SEMICOLON, ";")
                return Let(name, declared, value, line=line)
            case TokenKind.IF:
                return self.parse_if()
            case TokenKind.WHILE:
                # "while" "(" expr ")" block
                self.advance()
                self.expect(TokenKind.LPAREN, "(")
                cond = self.parse_expr()
                self.expect(TokenKind.RPAREN, ")")
                return While(cond, self.parse_block(), line=line)
            case TokenKind.RETURN:
                # "return" [ expr ] ";"
                self.advance()
                result = None
                if not self.at(TokenKind.SEMICOLON):
                    result = self.parse_expr()
                self.expect(TokenKind.SEMICOLON, ";")
                return Return(result, line=line)
        # 代入文または式文: expr [ "=" expr ] ";"
        expr = self.parse_expr()
        if self.accept(TokenKind.ASSIGN):
            if not isinstance(expr, (Name, Index)):
                raise ParseError("代入の左辺が不正です", token.line,
                                 token.column)
            value = self.parse_expr()
            self.expect(TokenKind.SEMICOLON, ";")
            return Assign(expr, value, line=line)
        self.expect(TokenKind.SEMICOLON, ";")
        return ExprStmt(expr, line=line)

    def parse_if(self) -> If:
        # "if" "(" expr ")" block [ "else" ( block | if ) ]
        line = self.expect(TokenKind.IF, "if").line
        self.expect(TokenKind.LPAREN, "(")
        cond = self.parse_expr()
        self.expect(TokenKind.RPAREN, ")")
        then_body = self.parse_block()
        else_body: Stmt | None = None
        if self.accept(TokenKind.ELSE):
            else_body = (self.parse_if() if self.at(TokenKind.IF)
                         else self.parse_block())
        return If(cond, then_body, else_body, line=line)

    # ------------------------------------------------ 式（Pratt 構文解析）

    def parse_expr(self, min_power: int = 0) -> Expr:
        left = self.parse_prefix()
        while True:
            token = self.peek()
            if token.kind in (TokenKind.LPAREN, TokenKind.LBRACKET):
                if POSTFIX_POWER < min_power:
                    return left
                left = self.parse_postfix(left)
                continue
            power = BINARY_POWER.get(token.kind)
            if power is None or power[0] < min_power:
                return left
            self.advance()
            right = self.parse_expr(power[1])
            left = Binary(token.text, left, right, line=token.line)

    def parse_postfix(self, left: Expr) -> Expr:
        token = self.advance()
        if token.kind is TokenKind.LBRACKET:
            index = self.parse_expr()
            self.expect(TokenKind.RBRACKET, "]")
            return Index(left, index, line=token.line)
        if not isinstance(left, Name):
            raise ParseError("関数名以外は呼び出せません", token.line,
                             token.column)
        args = self.parse_list(TokenKind.RPAREN, ")")
        return Call(left.name, args, line=left.line)

    def parse_list(self, close: TokenKind, what: str) -> list[Expr]:
        """「式 , 式 , ...」を閉じ括弧まで読む（開き括弧は読み済み）。"""
        items: list[Expr] = []
        if not self.at(close):
            items.append(self.parse_expr())
            while self.accept(TokenKind.COMMA):
                items.append(self.parse_expr())
        self.expect(close, what)
        return items

    def parse_prefix(self) -> Expr:
        token = self.peek()
        if token.kind not in PREFIX_START:
            raise self.error("式が必要です")
        self.advance()
        line = token.line
        match token.kind:
            case TokenKind.INT:
                assert isinstance(token.value, int)
                return IntLit(token.value, line=line)
            case TokenKind.STRING:
                assert isinstance(token.value, str)
                return StrLit(token.value, line=line)
            case TokenKind.TRUE:
                return BoolLit(True, line=line)
            case TokenKind.FALSE:
                return BoolLit(False, line=line)
            case TokenKind.IDENT:
                return Name(token.text, line=line)
            case TokenKind.MINUS | TokenKind.NOT:
                operand = self.parse_expr(PREFIX_POWER)
                return Unary(token.text, operand, line=line)
            case TokenKind.LPAREN:
                inner = self.parse_expr()
                self.expect(TokenKind.RPAREN, ")")
                return inner
            case TokenKind.LBRACKET:
                elements = self.parse_list(TokenKind.RBRACKET, "]")
                return ArrayLit(elements, line=line)
        raise AssertionError(token.kind)


def parse(source: str) -> Program:
    """ソースコードを構文解析して抽象構文木を返す。"""
    return Parser(tokenize(source)).parse_program()


def main() -> None:
    source = "fn main() {\n    let x = 1 + 2 * 3;\n    print(x);\n}\n"
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    try:
        print(dump(parse(source)))
    except ParseError as e:
        for error in e.all_errors:
            print(f"構文エラー: {error}")


if __name__ == "__main__":
    main()
