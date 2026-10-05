"""Tiny 言語の中間表現（第 8 章）。

三番地コードと基本ブロックからなる中間表現（IR）を定義し、
抽象構文木から IR への変換、IR の表示、Graphviz 形式の出力、
IR を直接実行するインタプリタを提供する。
"""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import TextIO, Union

import tiny_ast as A
from tiny_checker import check
from tiny_parser import parse
from tiny_runtime import (
    BUILTINS, Value, binary_op, call_builtin, index_value, store_index,
    unary_op)


# ---------------------------------------------------------------- オペランド

@dataclass(frozen=True)
class Var:
    """変数（ソースコードの変数、または一時変数 %1, %2, ...）。"""

    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Const:
    """定数。value が None のときは未定義値 undef を表す。"""

    value: int | bool | str | None

    def __str__(self) -> str:
        if self.value is None:
            return "undef"
        if isinstance(self.value, bool):
            return "true" if self.value else "false"
        if isinstance(self.value, str):
            return json.dumps(self.value, ensure_ascii=False)
        return str(self.value)


Operand = Union[Var, Const]


# ---------------------------------------------------------------- 命令

@dataclass
class Copy:
    dst: str
    src: Operand


@dataclass
class BinOp:
    dst: str
    op: str
    left: Operand
    right: Operand


@dataclass
class UnOp:
    dst: str
    op: str
    operand: Operand


@dataclass
class Call:
    dst: str | None  # 戻り値を使わないときは None
    func: str
    args: list[Operand]


@dataclass
class NewArray:
    dst: str
    elements: list[Operand]


@dataclass
class Load:
    dst: str
    base: Operand
    index: Operand


@dataclass
class Store:
    base: Operand
    index: Operand
    value: Operand


@dataclass
class Phi:
    """φ 関数。args は「直前に実行した基本ブロックのラベル → 値」の対応。"""

    dst: str
    args: dict[str, Operand]


Instr = Union[Copy, BinOp, UnOp, Call, NewArray, Load, Store, Phi]


# ---------------------------------------------------------------- 終端命令

@dataclass
class Jump:
    target: str


@dataclass
class Branch:
    cond: Operand
    if_true: str
    if_false: str


@dataclass
class Return:
    value: Operand | None


Terminator = Union[Jump, Branch, Return]


@dataclass
class BasicBlock:
    label: str
    instrs: list[Instr]
    terminator: Terminator

    def successors(self) -> list[str]:
        term = self.terminator
        if isinstance(term, Jump):
            return [term.target]
        if isinstance(term, Branch):
            return [term.if_true, term.if_false]
        return []

    def phis(self) -> list[Phi]:
        return [i for i in self.instrs if isinstance(i, Phi)]


@dataclass
class Function:
    name: str
    params: list[str]
    blocks: dict[str, BasicBlock]  # 先頭の基本ブロックが入口

    @property
    def entry(self) -> str:
        return next(iter(self.blocks))

    def predecessors(self) -> dict[str, list[str]]:
        preds: dict[str, list[str]] = {label: [] for label in self.blocks}
        for block in self.blocks.values():
            for succ in block.successors():
                preds[succ].append(block.label)
        return preds


Module = dict[str, Function]


# ---------------------------------------------------------------- 命令の操作

def defined_var(instr: Instr) -> str | None:
    """命令が値を書き込む変数の名前を返す。"""
    if isinstance(instr, Store):
        return None
    return instr.dst


def used_operands(item: Instr | Terminator) -> list[Operand]:
    """命令が読むオペランドを返す。"""
    match item:
        case Copy(_, src):
            return [src]
        case BinOp(_, _, left, right):
            return [left, right]
        case UnOp(_, _, operand):
            return [operand]
        case Call(_, _, args) | NewArray(_, args):
            return list(args)
        case Load(_, base, index):
            return [base, index]
        case Store(base, index, value):
            return [base, index, value]
        case Phi(_, args):
            return list(args.values())
        case Branch(cond, _, _):
            return [cond]
        case Return(value):
            return [] if value is None else [value]
    return []


def used_vars(item: Instr | Terminator) -> list[str]:
    return [op.name for op in used_operands(item) if isinstance(op, Var)]


def map_operands(item: Instr | Terminator,
                 f: Callable[[Operand], Operand]) -> None:
    """命令が読むオペランドを f で置き換える（命令を直接書き換える）。"""
    match item:
        case Copy():
            item.src = f(item.src)
        case BinOp():
            item.left, item.right = f(item.left), f(item.right)
        case UnOp():
            item.operand = f(item.operand)
        case Call():
            item.args = [f(a) for a in item.args]
        case NewArray():
            item.elements = [f(e) for e in item.elements]
        case Load():
            item.base, item.index = f(item.base), f(item.index)
        case Store():
            item.base, item.index = f(item.base), f(item.index)
            item.value = f(item.value)
        case Phi():
            item.args = {label: f(v) for label, v in item.args.items()}
        case Branch():
            item.cond = f(item.cond)
        case Return():
            if item.value is not None:
                item.value = f(item.value)


# ---------------------------------------------------------------- 表示

def format_item(item: Instr | Terminator) -> str:
    match item:
        case Copy(dst, src):
            return f"{dst} = {src}"
        case BinOp(dst, op, left, right):
            return f"{dst} = {left} {op} {right}"
        case UnOp(dst, op, operand):
            return f"{dst} = {op} {operand}"
        case Call(dst, func, args):
            text = f"call {func}({', '.join(map(str, args))})"
            return text if dst is None else f"{dst} = {text}"
        case NewArray(dst, elements):
            return f"{dst} = [{', '.join(map(str, elements))}]"
        case Load(dst, base, index):
            return f"{dst} = {base}[{index}]"
        case Store(base, index, value):
            return f"{base}[{index}] = {value}"
        case Phi(dst, args):
            pairs = ", ".join(f"{label}: {v}" for label, v in args.items())
            return f"{dst} = phi({pairs})"
        case Jump(target):
            return f"jump {target}"
        case Branch(cond, if_true, if_false):
            return f"branch {cond}, {if_true}, {if_false}"
        case Return(value):
            return "return" if value is None else f"return {value}"
    raise AssertionError(item)


def block_lines(block: BasicBlock) -> list[str]:
    lines = [f"{block.label}:"]
    lines += ["    " + format_item(i) for i in block.instrs]
    lines.append("    " + format_item(block.terminator))
    return lines


def format_function(func: Function) -> str:
    lines = [f"function {func.name}({', '.join(func.params)})"]
    for block in func.blocks.values():
        lines += block_lines(block)
    return "\n".join(lines)


def format_module(module: Module) -> str:
    return "\n\n".join(format_function(f) for f in module.values())


def to_dot(func: Function) -> str:
    """制御フローグラフを Graphviz の DOT 言語で表す。"""
    def escape(text: str) -> str:
        return text.replace("\\", "\\\\").replace('"', '\\"')

    lines = [f'digraph "{func.name}" {{',
             '  node [shape=box, fontname="monospace"];']
    for block in func.blocks.values():
        label = "".join(escape(line) + "\\l" for line in block_lines(block))
        lines.append(f'  "{block.label}" [label="{label}"];')
    for block in func.blocks.values():
        term = block.terminator
        if isinstance(term, Branch):
            lines.append(f'  "{block.label}" -> "{term.if_true}" '
                         '[label="true"];')
            lines.append(f'  "{block.label}" -> "{term.if_false}" '
                         '[label="false"];')
        elif isinstance(term, Jump):
            lines.append(f'  "{block.label}" -> "{term.target}";')
    lines.append("}")
    return "\n".join(lines)


# ------------------------------------------------------------ AST から IR への変換

class Lowering:
    """1 つの関数の構文木を IR に変換する。"""

    def __init__(self, func: A.FuncDef) -> None:
        self.func = func
        self.blocks: dict[str, BasicBlock] = {}
        self.label: str | None = "entry"  # 組み立て中の基本ブロック
        self.instrs: list[Instr] = []
        self.label_count = 0
        self.temp_count = 0
        self.scopes: list[dict[str, str]] = [{}]
        self.used_names: set[str] = set()

    # ------------------------------------------------ 組み立ての補助

    def new_id(self) -> int:
        """ラベルの番号を作る。1 つの構文から作るラベルには同じ番号を使う。"""
        self.label_count += 1
        return self.label_count

    def new_temp(self) -> str:
        self.temp_count += 1
        return f"%{self.temp_count}"

    def emit(self, instr: Instr) -> None:
        if self.label is None:  # return の後ろの到達不能なコード
            self.start_block(f"dead{self.new_id()}")
        self.instrs.append(instr)

    def terminate(self, term: Terminator) -> None:
        """組み立て中の基本ブロックを終端命令で閉じる。"""
        if self.label is None:
            self.start_block(f"dead{self.new_id()}")
        assert self.label is not None
        self.blocks[self.label] = BasicBlock(self.label, self.instrs, term)
        self.label = None

    def start_block(self, label: str) -> None:
        if self.label is not None:  # 前のブロックから流れ込む
            self.terminate(Jump(label))
        self.label = label
        self.instrs = []

    def declare(self, name: str) -> str:
        """変数を宣言し、IR 上の名前を返す。同名の変数は名前を変える。"""
        ir_name = name
        n = 1
        while ir_name in self.used_names:
            n += 1
            ir_name = f"{name}#{n}"
        self.used_names.add(ir_name)
        self.scopes[-1][name] = ir_name
        return ir_name

    def lookup(self, name: str) -> str:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise AssertionError(name)

    # ------------------------------------------------ 関数と文

    def lower(self) -> Function:
        params = [self.declare(p.name) for p in self.func.params]
        self.lower_block(self.func.body)
        if self.label is not None:
            self.terminate(Return(None))
        return Function(self.func.name, params,
                        remove_unreachable(self.blocks, "entry"))

    def lower_block(self, block: A.Block) -> None:
        self.scopes.append({})
        for stmt in block.stmts:
            self.lower_stmt(stmt)
        self.scopes.pop()

    def lower_stmt(self, stmt: A.Stmt) -> None:
        match stmt:
            case A.Block():
                self.lower_block(stmt)
            case A.Let(name, _, value):
                src = self.lower_expr(value)
                self.emit(Copy(self.declare(name), src))
            case A.Assign(A.Name(name), value):
                self.emit(Copy(self.lookup(name), self.lower_expr(value)))
            case A.Assign(A.Index(target, index), value):
                base = self.lower_expr(target)
                i = self.lower_expr(index)
                self.emit(Store(base, i, self.lower_expr(value)))
            case A.If(cond, then_body, else_body):
                n = self.new_id()
                then_label, end_label = f"then{n}", f"endif{n}"
                else_label = end_label if else_body is None else f"else{n}"
                c = self.lower_expr(cond)
                self.terminate(Branch(c, then_label, else_label))
                self.start_block(then_label)
                self.lower_block(then_body)
                if else_body is not None:
                    self.goto(end_label)
                    self.start_block(else_label)
                    self.lower_stmt(else_body)
                self.goto(end_label)
                self.start_block(end_label)
            case A.While(cond, body):
                n = self.new_id()
                cond_label, body_label = f"cond{n}", f"body{n}"
                end_label = f"endwhile{n}"
                self.start_block(cond_label)
                c = self.lower_expr(cond)
                self.terminate(Branch(c, body_label, end_label))
                self.start_block(body_label)
                self.lower_block(body)
                self.goto(cond_label)
                self.start_block(end_label)
            case A.Return(value):
                result = None if value is None else self.lower_expr(value)
                self.terminate(Return(result))
            case A.ExprStmt(expr):
                self.lower_expr(expr)

    def goto(self, label: str) -> None:
        """組み立て中のブロックがあれば label へのジャンプで閉じる。"""
        if self.label is not None:
            self.terminate(Jump(label))

    # ------------------------------------------------ 式

    def lower_expr(self, expr: A.Expr) -> Operand:
        match expr:
            case A.IntLit(value) | A.BoolLit(value) | A.StrLit(value):
                return Const(value)
            case A.Name(name):
                return Var(self.lookup(name))
            case A.ArrayLit(elements):
                values = [self.lower_expr(e) for e in elements]
                dst = self.new_temp()
                self.emit(NewArray(dst, values))
                return Var(dst)
            case A.Index(target, index):
                base = self.lower_expr(target)
                i = self.lower_expr(index)
                dst = self.new_temp()
                self.emit(Load(dst, base, i))
                return Var(dst)
            case A.Unary(op, operand):
                src = self.lower_expr(operand)
                dst = self.new_temp()
                self.emit(UnOp(dst, op, src))
                return Var(dst)
            case A.Binary("&&" | "||" as op, left, right):
                return self.lower_logical(op, left, right)
            case A.Binary(op, left, right):
                lhs = self.lower_expr(left)
                rhs = self.lower_expr(right)
                dst = self.new_temp()
                self.emit(BinOp(dst, op, lhs, rhs))
                return Var(dst)
            case A.Call(callee, args):
                values = [self.lower_expr(a) for a in args]
                if expr.ty == A.VOID:
                    self.emit(Call(None, callee, values))
                    return Const(None)
                dst = self.new_temp()
                self.emit(Call(dst, callee, values))
                return Var(dst)
        raise AssertionError(expr)

    def lower_logical(self, op: str, left: A.Expr, right: A.Expr) -> Operand:
        """短絡評価: 左辺だけで結果が決まれば右辺を評価しない。"""
        result = self.new_temp()
        n = self.new_id()
        rhs_label, end_label = f"rhs{n}", f"endlogic{n}"
        lhs = self.lower_expr(left)
        self.emit(Copy(result, lhs))
        if op == "&&":
            self.terminate(Branch(lhs, rhs_label, end_label))
        else:
            self.terminate(Branch(lhs, end_label, rhs_label))
        self.start_block(rhs_label)
        self.emit(Copy(result, self.lower_expr(right)))
        self.start_block(end_label)
        return Var(result)


def remove_unreachable(blocks: dict[str, BasicBlock],
                       entry: str) -> dict[str, BasicBlock]:
    """入口から到達できない基本ブロックを取り除く（順序は保つ）。"""
    reachable: set[str] = set()
    stack = [entry]
    while stack:
        label = stack.pop()
        if label not in reachable:
            reachable.add(label)
            stack.extend(blocks[label].successors())
    return {k: b for k, b in blocks.items() if k in reachable}


def lower_program(program: A.Program) -> Module:
    """意味解析済みのプログラムを IR に変換する。"""
    return {f.name: Lowering(f).lower() for f in program.functions}


def compile_to_ir(source: str) -> Module:
    return lower_program(check(parse(source)))


# ---------------------------------------------------------------- IR インタプリタ

class IRInterpreter:
    """IR を直接実行する。steps は実行した命令の数。"""

    def __init__(self, module: Module, out: TextIO = sys.stdout) -> None:
        self.module = module
        self.out = out
        self.steps = 0

    def run(self) -> None:
        self.call("main", [])

    def call(self, name: str, args: list[Value]) -> Value:
        func = self.module[name]
        env: dict[str, Value] = dict(zip(func.params, args))

        def value(op: Operand) -> Value:
            return op.value if isinstance(op, Const) else env[op.name]

        label, previous = func.entry, ""
        while True:
            block = func.blocks[label]
            # φ 関数はすべて同時に評価する（先に値を集めてから書き込む）。
            phis = block.phis()
            incoming = [value(phi.args[previous]) for phi in phis]
            for phi, v in zip(phis, incoming):
                env[phi.dst] = v
            self.steps += len(phis)
            for instr in block.instrs[len(phis):]:
                self.steps += 1
                self.execute(instr, env, value)
            self.steps += 1
            term = block.terminator
            if isinstance(term, Return):
                return None if term.value is None else value(term.value)
            previous = label
            if isinstance(term, Jump):
                label = term.target
            else:
                label = term.if_true if value(term.cond) else term.if_false

    def execute(self, instr: Instr, env: dict[str, Value],
                value: Callable[[Operand], Value]) -> None:
        match instr:
            case Copy(dst, src):
                env[dst] = value(src)
            case BinOp(dst, op, left, right):
                env[dst] = binary_op(op, value(left), value(right))
            case UnOp(dst, op, operand):
                env[dst] = unary_op(op, value(operand))
            case Call(dst, func, args):
                values = [value(a) for a in args]
                if func in BUILTINS:
                    result = call_builtin(func, values, self.out)
                else:
                    result = self.call(func, values)
                if dst is not None:
                    env[dst] = result
            case NewArray(dst, elements):
                env[dst] = [value(e) for e in elements]
            case Load(dst, base, index):
                env[dst] = index_value(value(base), value(index))
            case Store(base, index, v):
                store_index(value(base), value(index), value(v))
            case Phi():
                raise AssertionError("φ 関数は基本ブロックの先頭に置きます")


def main() -> None:
    source = ('fn sum(n: int) -> int {\n'
              '    let s = 0;\n'
              '    let i = 1;\n'
              '    while (i <= n) {\n'
              '        s = s + i;\n'
              '        i = i + 1;\n'
              '    }\n'
              '    return s;\n'
              '}\n'
              'fn main() {\n'
              '    print(sum(10));\n'
              '}\n')
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    module = compile_to_ir(source)
    print(format_module(module))
    print("--- 実行結果")
    IRInterpreter(module).run()


if __name__ == "__main__":
    main()
