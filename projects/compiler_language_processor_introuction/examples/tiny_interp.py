"""Tiny 言語の木構造インタプリタ（第 7 章）。

意味解析済みの抽象構文木を再帰的にたどり、そのまま実行する。
"""

from __future__ import annotations

import sys
from typing import TextIO

from tiny_ast import (
    ArrayLit, Assign, Binary, Block, BoolLit, Call, Expr, ExprStmt, FuncDef,
    If, Index, IntLit, Let, Name, Program, Return, Stmt, StrLit, Unary, While)
from tiny_checker import check
from tiny_lexer import TinyError
from tiny_parser import parse
from tiny_runtime import (
    BUILTINS, TinyRuntimeError, Value, binary_op, call_builtin, index_value,
    store_index, unary_op)


class Environment:
    """変数の値を保持する環境。ブロックごとに 1 つ作る。"""

    def __init__(self, parent: Environment | None = None) -> None:
        self.parent = parent
        self.values: dict[str, Value] = {}

    def define(self, name: str, value: Value) -> None:
        self.values[name] = value

    def find(self, name: str) -> Environment:
        env: Environment | None = self
        while env is not None:
            if name in env.values:
                return env
            env = env.parent
        raise TinyRuntimeError(f"変数 {name} が見つかりません")

    def get(self, name: str) -> Value:
        return self.find(name).values[name]

    def set(self, name: str, value: Value) -> None:
        self.find(name).values[name] = value


class ReturnSignal(Exception):
    """return 文の実行を関数呼び出し元まで伝える。"""

    def __init__(self, value: Value) -> None:
        super().__init__()
        self.value = value


class Interpreter:
    def __init__(self, program: Program, out: TextIO = sys.stdout) -> None:
        self.functions = {f.name: f for f in program.functions}
        self.out = out

    def run(self) -> None:
        self.call_function(self.functions["main"], [])

    def call_function(self, func: FuncDef, args: list[Value]) -> Value:
        env = Environment()
        for param, arg in zip(func.params, args):
            env.define(param.name, arg)
        try:
            self.exec_block(func.body, Environment(env))
        except ReturnSignal as signal:
            return signal.value
        return None

    # ------------------------------------------------ 文の実行

    def exec_block(self, block: Block, env: Environment) -> None:
        for stmt in block.stmts:
            self.exec_stmt(stmt, env)

    def exec_stmt(self, stmt: Stmt, env: Environment) -> None:
        match stmt:
            case Block():
                self.exec_block(stmt, Environment(env))
            case Let(name, _, value):
                env.define(name, self.eval(value, env))
            case Assign(Name(name), value):
                env.set(name, self.eval(value, env))
            case Assign(Index(target, index), value):
                base = self.eval(target, env)
                i = self.eval(index, env)
                store_index(base, i, self.eval(value, env))
            case If(cond, then_body, else_body):
                if self.eval(cond, env):
                    self.exec_block(then_body, Environment(env))
                elif else_body is not None:
                    self.exec_stmt(else_body, env)
            case While(cond, body):
                while self.eval(cond, env):
                    self.exec_block(body, Environment(env))
            case Return(value):
                result = None if value is None else self.eval(value, env)
                raise ReturnSignal(result)
            case ExprStmt(expr):
                self.eval(expr, env)
            case _:
                raise AssertionError(stmt)

    # ------------------------------------------------ 式の評価

    def eval(self, expr: Expr, env: Environment) -> Value:
        match expr:
            case IntLit(value) | BoolLit(value) | StrLit(value):
                return value
            case ArrayLit(elements):
                return [self.eval(e, env) for e in elements]
            case Name(name):
                return env.get(name)
            case Index(target, index):
                return index_value(self.eval(target, env),
                                   self.eval(index, env))
            case Unary(op, operand):
                return unary_op(op, self.eval(operand, env))
            case Binary("&&", left, right):
                return bool(self.eval(left, env)) and \
                    bool(self.eval(right, env))
            case Binary("||", left, right):
                return bool(self.eval(left, env)) or \
                    bool(self.eval(right, env))
            case Binary(op, left, right):
                return binary_op(op, self.eval(left, env),
                                 self.eval(right, env))
            case Call(callee, args):
                values = [self.eval(a, env) for a in args]
                if callee in BUILTINS:
                    return call_builtin(callee, values, self.out)
                return self.call_function(self.functions[callee], values)
        raise AssertionError(expr)


def run_source(source: str, out: TextIO = sys.stdout) -> None:
    """ソースコードを解析し、インタプリタで実行する。"""
    Interpreter(check(parse(source)), out).run()


def main() -> None:
    source = ('fn fact(n: int) -> int {\n'
              '    if (n <= 1) { return 1; }\n'
              '    return n * fact(n - 1);\n'
              '}\n'
              'fn main() {\n'
              '    print("10! =", fact(10));\n'
              '}\n')
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    try:
        run_source(source)
    except TinyError as e:
        print(f"エラー: {e}")


if __name__ == "__main__":
    main()
