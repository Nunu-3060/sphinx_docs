"""SSA 形式の IR に対する最適化と生存変数解析（第 9 章）。

* 定数伝播・定数畳み込み・コピー伝播・条件分岐の畳み込み
* 共通部分式除去（支配木に沿った値番号付け）
* 不要コード除去
* 制御フローグラフの単純化
* 生存変数解析（データフロー解析）
"""

from __future__ import annotations

import io
import sys

from tiny_ir import (
    BinOp, Branch, Call, Const, Copy, Function, Instr, IRInterpreter, Jump,
    Load, Module, Operand, Phi, Store, UnOp, Var, compile_to_ir, defined_var,
    format_function, map_operands, remove_unreachable, used_vars)
from tiny_runtime import TinyRuntimeError, binary_op, unary_op
from tiny_ssa import (
    dominator_tree, immediate_dominators, module_to_ssa, reverse_postorder)


# ---------------------------------------------------------------- 定数伝播

def fold(instr: BinOp | UnOp) -> Const | None:
    """オペランドがすべて定数なら、コンパイル時に計算した結果を返す。"""
    try:
        if isinstance(instr, UnOp):
            if isinstance(instr.operand, Const):
                result = unary_op(instr.op, instr.operand.value)
                assert not isinstance(result, list)
                return Const(result)
        elif isinstance(instr.left, Const) and isinstance(instr.right, Const):
            result = binary_op(instr.op, instr.left.value, instr.right.value)
            assert not isinstance(result, list)
            return Const(result)
    except TinyRuntimeError:
        pass  # 0 除算などは実行時に任せる
    return None


def simplify_algebra(instr: BinOp) -> Operand | None:
    """x + 0 や x * 1 などの恒等式を使って簡単にする。"""
    left, right, op = instr.left, instr.right, instr.op
    if op in ("+", "-") and right == Const(0):
        return left
    if op == "+" and left == Const(0):
        return right
    if op == "*" and right == Const(1):
        return left
    if op == "*" and left == Const(1):
        return right
    if op == "*" and Const(0) in (left, right):
        return Const(0)
    return None


def propagate_constants(func: Function) -> bool:
    """定数伝播・コピー伝播・畳み込みを行う。変更があれば True を返す。"""
    changed = False
    subst: dict[str, Operand] = {}  # 変数 → 置き換え先

    def resolve(op: Operand) -> Operand:
        while isinstance(op, Var) and op.name in subst:
            op = subst[op.name]
        return op

    for label in reverse_postorder(func):
        block = func.blocks[label]
        for i, instr in enumerate(block.instrs):
            before = repr(instr)
            map_operands(instr, resolve)
            replacement: Operand | None = None
            match instr:
                case Copy(dst, src):
                    subst[dst] = src
                case BinOp() | UnOp():
                    replacement = fold(instr)
                    if replacement is None and isinstance(instr, BinOp):
                        replacement = simplify_algebra(instr)
                case Phi(dst, args):
                    # 自分自身と未定義値を除いた値が 1 種類なら、その値と同じ。
                    values = {v for v in args.values()
                              if v != Var(dst) and v != Const(None)}
                    if len(values) <= 1:
                        replacement = values.pop() if values else Const(None)
            if replacement is not None:
                assert not isinstance(instr, Store)
                assert instr.dst is not None
                block.instrs[i] = Copy(instr.dst, replacement)
                subst[instr.dst] = replacement
            changed |= before != repr(block.instrs[i])
        term = block.terminator
        map_operands(term, resolve)
        if isinstance(term, Branch) and isinstance(term.cond, Const):
            # 条件が定数の分岐は無条件ジャンプにする。
            taken = term.if_true if term.cond.value else term.if_false
            other = term.if_false if term.cond.value else term.if_true
            block.terminator = Jump(taken)
            if other != taken:
                for phi in func.blocks[other].phis():
                    phi.args.pop(label, None)
            changed = True
    # ループの back edge から来る φ 関数の引数は、後から分かった置き換えを適用する。
    for block in func.blocks.values():
        for phi in block.phis():
            before = repr(phi)
            map_operands(phi, resolve)
            changed |= before != repr(phi)
    if changed:
        remove_dead_blocks(func)
    return changed


def remove_dead_blocks(func: Function) -> None:
    """到達できない基本ブロックを除き、φ 関数の引数を整理する。"""
    func.blocks = remove_unreachable(func.blocks, func.entry)
    preds = func.predecessors()
    for block in func.blocks.values():
        for phi in block.phis():
            phi.args = {p: v for p, v in phi.args.items()
                        if p in preds[block.label]}


# ---------------------------------------------------------------- 共通部分式除去

COMMUTATIVE = ("*", "==", "!=")


def eliminate_common_subexpressions(func: Function) -> bool:
    """支配木を上からたどり、同じ計算を 2 度目以降はコピーに置き換える。"""
    children = dominator_tree(func, immediate_dominators(func))
    changed = False

    def visit(label: str, available: dict[tuple[str, ...], str]) -> None:
        nonlocal changed
        table = dict(available)  # 支配ブロックで計算済みの式 → 変数
        block = func.blocks[label]
        for i, instr in enumerate(block.instrs):
            if isinstance(instr, BinOp):
                operands = [str(instr.left), str(instr.right)]
                if instr.op in COMMUTATIVE:
                    operands.sort()
                key = (instr.op, *operands)
            elif isinstance(instr, UnOp):
                key = (instr.op, str(instr.operand))
            else:
                continue
            if key in table:
                block.instrs[i] = Copy(instr.dst, Var(table[key]))
                changed = True
            else:
                table[key] = instr.dst
        for child in children[label]:
            visit(child, table)

    visit(func.entry, {})
    return changed


# ---------------------------------------------------------------- 不要コード除去

def has_side_effect(instr: Instr) -> bool:
    """結果を使わなくても削除できない命令か。"""
    if isinstance(instr, (Call, Store, Load)):  # Load は範囲外エラーがある
        return True
    if isinstance(instr, BinOp) and instr.op in ("/", "%"):
        # 0 除算の可能性があるものは残す。
        return not (isinstance(instr.right, Const) and instr.right.value != 0)
    return False


def eliminate_dead_code(func: Function) -> bool:
    """値が使われない命令を削除する。"""
    definition: dict[str, Instr] = {}
    for block in func.blocks.values():
        for instr in block.instrs:
            dst = defined_var(instr)
            if dst is not None:
                definition[dst] = instr

    # 副作用のある命令と終端命令から、使われている変数をたどって印を付ける。
    live: set[int] = set()
    worklist: list[str] = []
    for block in func.blocks.values():
        for instr in block.instrs:
            if has_side_effect(instr):
                live.add(id(instr))
                worklist += used_vars(instr)
        worklist += used_vars(block.terminator)
    while worklist:
        name = worklist.pop()
        found = definition.get(name)
        if found is not None and id(found) not in live:
            live.add(id(found))
            worklist += used_vars(found)

    changed = False
    for block in func.blocks.values():
        kept = [i for i in block.instrs if id(i) in live]
        changed |= len(kept) != len(block.instrs)
        block.instrs = kept
    return changed


# ---------------------------------------------------------------- 制御フローの単純化

def simplify_cfg(func: Function) -> bool:
    """引数が 1 つの φ 関数をコピーにし、一直線につながるブロックを併合する。"""
    changed = False
    for block in func.blocks.values():
        for i, phi in enumerate(block.phis()):
            if len(phi.args) == 1:
                block.instrs[i] = Copy(phi.dst, next(iter(phi.args.values())))
                changed = True

    merged = True
    while merged:
        merged = False
        preds = func.predecessors()
        for block in func.blocks.values():
            term = block.terminator
            if not isinstance(term, Jump):
                continue
            succ = func.blocks[term.target]
            if succ.label == func.entry or preds[succ.label] != [block.label] \
                    or succ.phis():
                continue
            # succ を block の後ろにつなげる。
            block.instrs += succ.instrs
            block.terminator = succ.terminator
            del func.blocks[succ.label]
            for after in block.successors():
                for phi in func.blocks[after].phis():
                    phi.args = {block.label if p == succ.label else p: v
                                for p, v in phi.args.items()}
            merged = changed = True
            break
    return changed


def optimize_function(func: Function) -> Function:
    """SSA 形式の関数を、変化がなくなるまで繰り返し最適化する。"""
    while True:
        changed = propagate_constants(func)
        changed |= eliminate_common_subexpressions(func)
        changed |= eliminate_dead_code(func)
        changed |= simplify_cfg(func)
        if not changed:
            return func


def optimize_module(module: Module) -> Module:
    for func in module.values():
        optimize_function(func)
    return module


# ---------------------------------------------------------------- 生存変数解析

def liveness(func: Function) -> tuple[dict[str, set[str]],
                                      dict[str, set[str]]]:
    """各基本ブロックの入口と出口で生存している変数を求める。

    live_out[B] = ∪ live_in[S]  （S は B の後続ブロック）
    live_in[B]  = use[B] ∪ (live_out[B] - def[B])
    を、値が変化しなくなるまで繰り返し計算する。
    """
    use: dict[str, set[str]] = {}
    defs: dict[str, set[str]] = {}
    for block in func.blocks.values():
        u: set[str] = set()  # 定義より前に使われる変数
        d: set[str] = {phi.dst for phi in block.phis()}  # 定義される変数
        for instr in block.instrs[len(block.phis()):]:
            u |= {v for v in used_vars(instr) if v not in d}
            dst = defined_var(instr)
            if dst is not None:
                d.add(dst)
        u |= {v for v in used_vars(block.terminator) if v not in d}
        use[block.label], defs[block.label] = u, d

    live_in: dict[str, set[str]] = {b: set() for b in func.blocks}
    live_out: dict[str, set[str]] = {b: set() for b in func.blocks}
    order = reverse_postorder(func)[::-1]  # 後ろ向きの解析なので逆順に回す
    changed = True
    while changed:
        changed = False
        for label in order:
            out: set[str] = set()
            for succ in func.blocks[label].successors():
                block = func.blocks[succ]
                out |= live_in[succ] - {phi.dst for phi in block.phis()}
                for phi in block.phis():  # φ 関数の引数は先行ブロックの出口で使う
                    arg = phi.args.get(label)
                    if isinstance(arg, Var):
                        out.add(arg.name)
            new_in = use[label] | (out - defs[label])
            if out != live_out[label] or new_in != live_in[label]:
                live_out[label], live_in[label] = out, new_in
                changed = True
    return live_in, live_out


def main() -> None:
    source = ('fn calc(n: int) -> int {\n'
              '    let a = 3 * 4;\n'
              '    let b = a + 2;\n'
              '    let unused = n * 100;\n'
              '    let x = n * b + n * b;\n'
              '    if (a > 100) {\n'
              '        print("never");\n'
              '    }\n'
              '    return x;\n'
              '}\n'
              'fn main() {\n'
              '    print(calc(5));\n'
              '}\n')
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    module = module_to_ssa(compile_to_ir(source))
    before = IRInterpreter(module, io.StringIO())
    before.run()
    optimize_module(module)
    for func in module.values():
        print(format_function(func))
    after = IRInterpreter(module)
    after.run()
    print(f"実行した命令数: 最適化前 {before.steps}、最適化後 {after.steps}")


if __name__ == "__main__":
    main()
