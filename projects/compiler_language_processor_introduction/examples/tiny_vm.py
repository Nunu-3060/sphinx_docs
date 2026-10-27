"""Tiny 言語のスタック型仮想マシン（第 10 章）。

すべての関数呼び出しで 1 本の値スタックを共有する。各フレームは
「局所変数の先頭位置（ベースポインタ）」と「次に実行する番地」を持つ。

    値スタック: [ ... | 引数・局所変数 | 計算途中の値 ... ]
                      ^ bp
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import TextIO

from tiny_bytecode import CodeObject, CompiledProgram, Op, compile_source
from tiny_runtime import (
    TinyRuntimeError, Value, binary_op, call_builtin, index_value,
    store_index, unary_op)

BINARY_SYMBOLS: dict[Op, str] = {
    Op.ADD: "+", Op.SUB: "-", Op.MUL: "*", Op.DIV: "/", Op.MOD: "%",
    Op.EQ: "==", Op.NE: "!=", Op.LT: "<", Op.LE: "<=", Op.GT: ">",
    Op.GE: ">=",
}
MAX_FRAMES = 10000


@dataclass
class Frame:
    """関数呼び出し 1 回分の情報（スタックフレーム）。"""

    code: CodeObject
    pc: int  # 次に実行する命令の番地
    bp: int  # 局所変数 0 番の値スタック上の位置


class VM:
    def __init__(self, program: CompiledProgram,
                 out: TextIO = sys.stdout) -> None:
        self.program = program
        self.out = out
        self.stack: list[Value] = []
        self.frames: list[Frame] = []
        self.steps = 0  # 実行した命令の数

    def run(self) -> None:
        self.call(self.program.functions[self.program.main])
        self.execute()

    def call(self, code: CodeObject) -> None:
        """引数は値スタックに積まれている。残りの局所変数の領域を確保する。"""
        if len(self.frames) >= MAX_FRAMES:
            raise TinyRuntimeError("関数呼び出しが深すぎます")
        bp = len(self.stack) - code.num_params
        self.stack.extend([None] * (code.num_locals - code.num_params))
        self.frames.append(Frame(code, 0, bp))

    def execute(self) -> None:
        stack = self.stack
        frame = self.frames[-1]
        code, constants = frame.code.code, frame.code.constants
        while True:
            op, arg = code[frame.pc]
            frame.pc += 1
            self.steps += 1
            match op:
                case Op.CONST:
                    stack.append(constants[arg])
                case Op.LOAD:
                    stack.append(stack[frame.bp + arg])
                case Op.STORE:
                    stack[frame.bp + arg] = stack.pop()
                case Op.ADD | Op.SUB | Op.MUL | Op.DIV | Op.MOD | Op.EQ \
                        | Op.NE | Op.LT | Op.LE | Op.GT | Op.GE:
                    right = stack.pop()
                    stack[-1] = binary_op(BINARY_SYMBOLS[op], stack[-1], right)
                case Op.NEG:
                    stack[-1] = unary_op("-", stack[-1])
                case Op.NOT:
                    stack[-1] = unary_op("!", stack[-1])
                case Op.JUMP:
                    frame.pc = arg
                case Op.JUMP_IF_FALSE:
                    if not stack.pop():
                        frame.pc = arg
                case Op.JUMP_IF_FALSE_OR_POP:
                    if stack[-1]:
                        stack.pop()
                    else:
                        frame.pc = arg
                case Op.JUMP_IF_TRUE_OR_POP:
                    if stack[-1]:
                        frame.pc = arg
                    else:
                        stack.pop()
                case Op.BUILD_ARRAY:
                    elements = stack[len(stack) - arg:]
                    del stack[len(stack) - arg:]
                    stack.append(elements)
                case Op.INDEX:
                    index = stack.pop()
                    stack[-1] = index_value(stack[-1], index)
                case Op.STORE_INDEX:
                    value = stack.pop()
                    index = stack.pop()
                    store_index(stack.pop(), index, value)
                case Op.PRINT | Op.LEN | Op.PUSH | Op.TO_STR:
                    self.builtin(op, arg)
                case Op.POP:
                    stack.pop()
                case Op.CALL:
                    self.call(self.program.functions[arg])
                    frame = self.frames[-1]
                    code, constants = frame.code.code, frame.code.constants
                case Op.RETURN:
                    result = stack.pop()
                    del stack[frame.bp:]  # 引数と局所変数を捨てる
                    self.frames.pop()
                    if not self.frames:
                        return
                    stack.append(result)
                    frame = self.frames[-1]
                    code, constants = frame.code.code, frame.code.constants

    def builtin(self, op: Op, arg: int) -> None:
        count = {Op.PRINT: arg, Op.LEN: 1, Op.PUSH: 2, Op.TO_STR: 1}[op]
        args = self.stack[len(self.stack) - count:]
        del self.stack[len(self.stack) - count:]
        name = op.name.lower()
        self.stack.append(call_builtin(name, args, self.out))


def main() -> None:
    from tiny_checker import check
    from tiny_interp import Interpreter
    from tiny_parser import parse

    source = ('fn fib(n: int) -> int {\n'
              '    if (n < 2) { return n; }\n'
              '    return fib(n - 1) + fib(n - 2);\n'
              '}\n'
              'fn main() {\n'
              '    print(fib(22));\n'
              '}\n')
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
        VM(compile_source(source)).run()
        return
    start = time.perf_counter()
    Interpreter(check(parse(source))).run()
    print(f"木構造インタプリタ: {time.perf_counter() - start:.2f} 秒")
    start = time.perf_counter()
    VM(compile_source(source)).run()
    print(f"仮想マシン:         {time.perf_counter() - start:.2f} 秒")


if __name__ == "__main__":
    main()
