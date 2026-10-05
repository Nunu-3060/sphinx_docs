"""Tiny 言語のバイトコード生成器と逆アセンブラ（第 10 章）。

意味解析済みの抽象構文木から、スタック型仮想マシン用の命令列を生成する。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from enum import IntEnum, auto

import tiny_ast as A
from tiny_checker import always_returns, check
from tiny_parser import parse
from tiny_runtime import Value, format_value


class Op(IntEnum):
    """仮想マシンの命令。引数を取る命令は、その意味をコメントに書く。"""

    CONST = auto()          # 定数表の arg 番目の値を積む
    LOAD = auto()           # 局所変数 arg の値を積む
    STORE = auto()          # 値を降ろして局所変数 arg に書き込む
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    NEG = auto()
    NOT = auto()
    JUMP = auto()           # arg 番地へ飛ぶ
    JUMP_IF_FALSE = auto()  # 値を降ろし、偽なら arg 番地へ飛ぶ
    JUMP_IF_FALSE_OR_POP = auto()  # 偽なら値を残して飛び、真なら降ろす
    JUMP_IF_TRUE_OR_POP = auto()   # 真なら値を残して飛び、偽なら降ろす
    BUILD_ARRAY = auto()    # 値を arg 個降ろして配列を作る
    INDEX = auto()          # 配列と添字を降ろし、要素を積む
    STORE_INDEX = auto()    # 配列・添字・値を降ろし、要素に書き込む
    CALL = auto()           # arg 番目の関数を呼ぶ
    PRINT = auto()          # 値を arg 個降ろして表示する
    LEN = auto()
    PUSH = auto()
    TO_STR = auto()
    POP = auto()            # 値を 1 つ降ろして捨てる
    RETURN = auto()         # 値を降ろし、呼び出し元に戻る


BINARY_OPS: dict[str, Op] = {
    "+": Op.ADD, "-": Op.SUB, "*": Op.MUL, "/": Op.DIV, "%": Op.MOD,
    "==": Op.EQ, "!=": Op.NE, "<": Op.LT, "<=": Op.LE, ">": Op.GT,
    ">=": Op.GE,
}
BUILTIN_OPS: dict[str, Op] = {
    "len": Op.LEN, "push": Op.PUSH, "to_str": Op.TO_STR,
}

Instruction = tuple[Op, int]


@dataclass
class CodeObject:
    """1 つの関数をコンパイルした結果。"""

    name: str
    num_params: int
    num_locals: int = 0
    code: list[Instruction] = field(default_factory=list)
    constants: list[Value] = field(default_factory=list)
    local_names: list[str] = field(default_factory=list)


@dataclass
class CompiledProgram:
    functions: list[CodeObject]
    main: int  # main 関数の番号


class FunctionCompiler:
    def __init__(self, func: A.FuncDef, func_index: dict[str, int]) -> None:
        self.func = func
        self.func_index = func_index
        self.code = CodeObject(func.name, len(func.params))
        self.scopes: list[dict[str, int]] = [{}]
        self.next_slot = 0

    # ------------------------------------------------ 補助

    def emit(self, op: Op, arg: int = 0) -> int:
        """命令を追加し、その番地を返す。"""
        self.code.code.append((op, arg))
        return len(self.code.code) - 1

    def patch(self, address: int) -> None:
        """address のジャンプ命令の飛び先を、次に生成する命令の番地にする。"""
        op, _ = self.code.code[address]
        self.code.code[address] = (op, len(self.code.code))

    def constant(self, value: Value) -> int:
        constants = self.code.constants
        for i, c in enumerate(constants):
            if type(c) is type(value) and c == value:
                return i
        constants.append(value)
        return len(constants) - 1

    def declare(self, name: str) -> int:
        """局所変数にスロット（番号）を割り当てる。"""
        slot = self.next_slot
        self.next_slot += 1
        self.scopes[-1][name] = slot
        self.code.num_locals = max(self.code.num_locals, self.next_slot)
        names = self.code.local_names
        if slot == len(names):
            names.append(name)
        elif name not in names[slot].split("/"):
            names[slot] += "/" + name
        return slot

    def lookup(self, name: str) -> int:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise AssertionError(name)

    # ------------------------------------------------ 関数と文

    def compile(self) -> CodeObject:
        for param in self.func.params:
            self.declare(param.name)
        self.compile_block(self.func.body)
        if self.func.return_type == A.VOID:
            # 値を返さない関数は、末尾に達したら None を返す。
            self.emit(Op.CONST, self.constant(None))
            self.emit(Op.RETURN)
        return self.code

    def compile_block(self, block: A.Block) -> None:
        # ブロックを抜けたら、そのブロックの変数のスロットを再利用する。
        self.scopes.append({})
        saved = self.next_slot
        for stmt in block.stmts:
            self.compile_stmt(stmt)
        self.next_slot = saved
        self.scopes.pop()

    def compile_stmt(self, stmt: A.Stmt) -> None:
        match stmt:
            case A.Block():
                self.compile_block(stmt)
            case A.Let(name, _, value):
                self.compile_expr(value)
                self.emit(Op.STORE, self.declare(name))
            case A.Assign(A.Name(name), value):
                self.compile_expr(value)
                self.emit(Op.STORE, self.lookup(name))
            case A.Assign(A.Index(target, index), value):
                self.compile_expr(target)
                self.compile_expr(index)
                self.compile_expr(value)
                self.emit(Op.STORE_INDEX)
            case A.If(cond, then_body, else_body):
                self.compile_expr(cond)
                to_else = self.emit(Op.JUMP_IF_FALSE)
                self.compile_block(then_body)
                if else_body is None:
                    self.patch(to_else)
                elif always_returns(then_body):
                    # then 節が必ず return するなら、飛び越す命令は不要。
                    self.patch(to_else)
                    self.compile_stmt(else_body)
                else:
                    to_end = self.emit(Op.JUMP)
                    self.patch(to_else)
                    self.compile_stmt(else_body)
                    self.patch(to_end)
            case A.While(cond, body):
                start = len(self.code.code)
                self.compile_expr(cond)
                to_end = self.emit(Op.JUMP_IF_FALSE)
                self.compile_block(body)
                self.emit(Op.JUMP, start)
                self.patch(to_end)
            case A.Return(value):
                if value is None:
                    self.emit(Op.CONST, self.constant(None))
                else:
                    self.compile_expr(value)
                self.emit(Op.RETURN)
            case A.ExprStmt(expr):
                self.compile_expr(expr)
                self.emit(Op.POP)

    # ------------------------------------------------ 式

    def compile_expr(self, expr: A.Expr) -> None:
        """式の値を計算し、スタックに 1 つ積む命令を生成する。"""
        match expr:
            case A.IntLit(value) | A.BoolLit(value) | A.StrLit(value):
                self.emit(Op.CONST, self.constant(value))
            case A.Name(name):
                self.emit(Op.LOAD, self.lookup(name))
            case A.ArrayLit(elements):
                for e in elements:
                    self.compile_expr(e)
                self.emit(Op.BUILD_ARRAY, len(elements))
            case A.Index(target, index):
                self.compile_expr(target)
                self.compile_expr(index)
                self.emit(Op.INDEX)
            case A.Unary(op, operand):
                self.compile_expr(operand)
                self.emit(Op.NEG if op == "-" else Op.NOT)
            case A.Binary("&&" | "||" as op, left, right):
                self.compile_expr(left)
                jump = Op.JUMP_IF_FALSE_OR_POP if op == "&&" \
                    else Op.JUMP_IF_TRUE_OR_POP
                to_end = self.emit(jump)
                self.compile_expr(right)
                self.patch(to_end)
            case A.Binary(op, left, right):
                self.compile_expr(left)
                self.compile_expr(right)
                self.emit(BINARY_OPS[op])
            case A.Call(callee, args):
                for arg in args:
                    self.compile_expr(arg)
                if callee == "print":
                    self.emit(Op.PRINT, len(args))
                elif callee in BUILTIN_OPS:
                    self.emit(BUILTIN_OPS[callee])
                else:
                    self.emit(Op.CALL, self.func_index[callee])
            case _:
                raise AssertionError(expr)


def compile_program(program: A.Program) -> CompiledProgram:
    """意味解析済みのプログラムをバイトコードに変換する。"""
    func_index = {f.name: i for i, f in enumerate(program.functions)}
    functions = [FunctionCompiler(f, func_index).compile()
                 for f in program.functions]
    return CompiledProgram(functions, func_index["main"])


def compile_source(source: str) -> CompiledProgram:
    return compile_program(check(parse(source)))


# ---------------------------------------------------------------- 逆アセンブラ

def disassemble(code: CodeObject, program: CompiledProgram) -> str:
    lines = [f"function {code.name}: params={code.num_params} "
             f"locals={code.num_locals}"]
    for address, (op, arg) in enumerate(code.code):
        text = f"{address:4}  {op.name:20}"
        if op is Op.CONST:
            text += f"{arg:3} ({format_value(code.constants[arg], True)})"
        elif op in (Op.LOAD, Op.STORE):
            text += f"{arg:3} ({code.local_names[arg]})"
        elif op is Op.CALL:
            text += f"{arg:3} ({program.functions[arg].name})"
        elif op.name.startswith("JUMP") or op in (Op.BUILD_ARRAY, Op.PRINT):
            text += f"{arg:3}"
        lines.append(text.rstrip())
    return "\n".join(lines)


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
    program = compile_source(source)
    print("\n\n".join(disassemble(f, program) for f in program.functions))


if __name__ == "__main__":
    main()
