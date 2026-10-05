"""Tiny 言語の意味解析器（第 6 章）。

名前解決（変数・関数が宣言されているか）と型検査を行い、
各式の ty 属性に型を書き込む。
"""

from __future__ import annotations

import sys

from tiny_ast import (
    BOOL, INT, STR, VOID, ArrayLit, ArrayType, Assign, Binary, Block, BoolLit,
    Call, Expr, ExprStmt, FuncDef, If, Index, IntLit, Let, Name, Program,
    Return, Stmt, StrLit, Type, Unary, While)
from tiny_lexer import TinyError
from tiny_parser import parse
from tiny_runtime import BUILTINS


class TypeCheckError(TinyError):
    """意味解析で見つかったエラー。"""


class Scope:
    """記号表。ブロックごとに 1 つ作り、外側のスコープへの参照を持つ。"""

    def __init__(self, parent: Scope | None = None) -> None:
        self.parent = parent
        self.symbols: dict[str, Type] = {}

    def declare(self, name: str, ty: Type, line: int) -> None:
        if name in self.symbols:
            raise TypeCheckError(f"変数 {name} はこのスコープで宣言済みです", line)
        self.symbols[name] = ty

    def lookup(self, name: str) -> Type | None:
        scope: Scope | None = self
        while scope is not None:
            if name in scope.symbols:
                return scope.symbols[name]
            scope = scope.parent
        return None


ARITHMETIC_OPS = ("-", "*", "/", "%")
COMPARISON_OPS = ("<", "<=", ">", ">=")
EQUALITY_OPS = ("==", "!=")
LOGICAL_OPS = ("&&", "||")


def always_returns(stmt: Stmt) -> bool:
    """文の実行が必ず return で終わるかを（保守的に）判定する。"""
    if isinstance(stmt, Return):
        return True
    if isinstance(stmt, Block):
        return any(always_returns(s) for s in stmt.stmts)
    if isinstance(stmt, If):
        return (stmt.else_body is not None and always_returns(stmt.then_body)
                and always_returns(stmt.else_body))
    return False


class Checker:
    def __init__(self, program: Program) -> None:
        self.program = program
        self.functions: dict[str, FuncDef] = {}
        self.current: FuncDef | None = None

    def check(self) -> None:
        for func in self.program.functions:
            if func.name in self.functions or func.name in BUILTINS:
                raise TypeCheckError(f"関数 {func.name} は定義済みです",
                                     func.line)
            self.functions[func.name] = func
        main = self.functions.get("main")
        if main is None:
            raise TypeCheckError("関数 main がありません")
        if main.params or main.return_type != VOID:
            raise TypeCheckError("main は引数も戻り値も持てません", main.line)
        for func in self.program.functions:
            self.check_function(func)

    def check_function(self, func: FuncDef) -> None:
        self.current = func
        scope = Scope()
        for param in func.params:
            scope.declare(param.name, param.ty, param.line)
        self.check_block(func.body, Scope(scope))
        if func.return_type != VOID and not always_returns(func.body):
            raise TypeCheckError(
                f"関数 {func.name} の末尾に return がありません", func.line)

    # ------------------------------------------------ 文

    def check_block(self, block: Block, scope: Scope) -> None:
        for stmt in block.stmts:
            self.check_stmt(stmt, scope)

    def check_stmt(self, stmt: Stmt, scope: Scope) -> None:
        match stmt:
            case Block():
                self.check_block(stmt, Scope(scope))
            case Let(name, declared, value):
                ty = self.check_expr(value, scope, declared)
                if ty == VOID:
                    raise TypeCheckError("値を持たない式は代入できません",
                                         stmt.line)
                scope.declare(name, ty, stmt.line)
            case Assign(target, value):
                if isinstance(target, Index) and \
                        self.check_expr(target.target, scope) == STR:
                    raise TypeCheckError("文字列の要素には代入できません",
                                         stmt.line)
                target_type = self.check_expr(target, scope)
                self.check_expr(value, scope, target_type)
            case If(cond, then_body, else_body):
                self.check_expr(cond, scope, BOOL)
                self.check_block(then_body, Scope(scope))
                if else_body is not None:
                    self.check_stmt(else_body, scope)
            case While(cond, body):
                self.check_expr(cond, scope, BOOL)
                self.check_block(body, Scope(scope))
            case Return(value):
                assert self.current is not None
                expected = self.current.return_type
                if value is None:
                    if expected != VOID:
                        raise TypeCheckError("戻り値が必要です", stmt.line)
                elif expected == VOID:
                    raise TypeCheckError(
                        f"関数 {self.current.name} は値を返せません",
                        stmt.line)
                else:
                    self.check_expr(value, scope, expected)
            case ExprStmt(expr):
                self.check_expr(expr, scope)

    # ------------------------------------------------ 式

    def check_expr(self, expr: Expr, scope: Scope,
                   expected: Type | None = None) -> Type:
        """式の型を求めて expr.ty に記録する。

        expected が与えられたら、式の型がそれと一致することを確かめる。
        空の配列リテラル [] の要素型は expected から決める。
        """
        if isinstance(expr, ArrayLit) and not expr.elements:
            if not isinstance(expected, ArrayType):
                raise TypeCheckError("空の配列の型を決められません",
                                     expr.line)
            ty: Type = expected
        else:
            ty = self.infer(expr, scope, expected)
        if expected is not None and ty != expected:
            raise TypeCheckError(
                f"型 {expected} が必要ですが、型 {ty} の式があります",
                expr.line)
        expr.ty = ty
        return ty

    def infer(self, expr: Expr, scope: Scope, expected: Type | None) -> Type:
        match expr:
            case IntLit():
                return INT
            case BoolLit():
                return BOOL
            case StrLit():
                return STR
            case Name(name):
                ty = scope.lookup(name)
                if ty is None:
                    raise TypeCheckError(f"変数 {name} は宣言されていません",
                                         expr.line)
                return ty
            case ArrayLit(elements):
                hint = expected.element \
                    if isinstance(expected, ArrayType) else None
                first = self.check_expr(elements[0], scope, hint)
                for element in elements[1:]:
                    self.check_expr(element, scope, first)
                return ArrayType(first)
            case Index(target, index):
                target_type = self.check_expr(target, scope)
                self.check_expr(index, scope, INT)
                if isinstance(target_type, ArrayType):
                    return target_type.element
                if target_type == STR:
                    return STR
                raise TypeCheckError(f"型 {target_type} の値は添字で参照できません",
                                     expr.line)
            case Unary(op, operand):
                return self.check_expr(operand, scope,
                                       INT if op == "-" else BOOL)
            case Binary(op, left, right):
                return self.check_binary(op, left, right, scope)
            case Call():
                return self.check_call(expr, scope)
        raise AssertionError(expr)

    def check_binary(self, op: str, left: Expr, right: Expr,
                     scope: Scope) -> Type:
        if op in LOGICAL_OPS:
            self.check_expr(left, scope, BOOL)
            self.check_expr(right, scope, BOOL)
            return BOOL
        left_type = self.check_expr(left, scope)
        if op in EQUALITY_OPS:
            if left_type == VOID:
                raise TypeCheckError("値を持たない式は比較できません",
                                     left.line)
            self.check_expr(right, scope, left_type)
            return BOOL
        if op == "+" and left_type == STR:
            self.check_expr(right, scope, STR)
            return STR
        if left_type != INT:
            raise TypeCheckError(
                f"演算子 {op} は型 {left_type} に使えません", left.line)
        self.check_expr(right, scope, INT)
        return BOOL if op in COMPARISON_OPS else INT

    def check_call(self, call: Call, scope: Scope) -> Type:
        name, args = call.callee, call.args
        if name in BUILTINS:
            return self.check_builtin(call, scope)
        func = self.functions.get(name)
        if func is None:
            raise TypeCheckError(f"関数 {name} は定義されていません",
                                 call.line)
        if len(args) != len(func.params):
            raise TypeCheckError(
                f"関数 {name} の引数は {len(func.params)} 個です", call.line)
        for arg, param in zip(args, func.params):
            self.check_expr(arg, scope, param.ty)
        return func.return_type

    def check_builtin(self, call: Call, scope: Scope) -> Type:
        name, args = call.callee, call.args
        if name == "print":
            for arg in args:
                if self.check_expr(arg, scope) == VOID:
                    raise TypeCheckError("値を持たない式は表示できません",
                                         arg.line)
            return VOID
        arity = 2 if name == "push" else 1
        if len(args) != arity:
            raise TypeCheckError(f"関数 {name} の引数は {arity} 個です",
                                 call.line)
        ty = self.check_expr(args[0], scope)
        if name == "len":
            if not isinstance(ty, ArrayType) and ty != STR:
                raise TypeCheckError("len の引数は配列か文字列です",
                                     call.line)
            return INT
        if name == "push":
            if not isinstance(ty, ArrayType):
                raise TypeCheckError("push の第 1 引数は配列です", call.line)
            self.check_expr(args[1], scope, ty.element)
            return VOID
        # to_str
        if ty not in (INT, BOOL, STR):
            raise TypeCheckError(f"型 {ty} は to_str で変換できません",
                                 call.line)
        return STR


def check(program: Program) -> Program:
    """意味解析を行い、型情報を書き込んだ構文木を返す。"""
    Checker(program).check()
    return program


def main() -> None:
    source = 'fn main() {\n    let x = 1 + "a";\n}\n'
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    try:
        check(parse(source))
        print("エラーはありません")
    except TinyError as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
