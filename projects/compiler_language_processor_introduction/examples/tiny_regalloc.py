"""線形走査法によるレジスタ割り当て（第 11 章）。

最適化した IR を SSA 形式から戻し、変数を有限個のレジスタに割り当てる。
レジスタが足りない変数はメモリ（スタック上の退避領域）に置く（スピル）。

本書の仮想的な機械では、命令のオペランドにメモリを直接書けるものとし、
関数呼び出しはレジスタの値を壊さないものとする。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

from tiny_ir import (
    Copy, Function, Operand, Store, Var, compile_to_ir, defined_var,
    format_function, format_item, map_operands, used_vars)
from tiny_opt import liveness, optimize_module
from tiny_ssa import from_ssa, module_to_ssa


@dataclass
class Interval:
    """変数の生存区間。start から end までの命令で値を保持する必要がある。"""

    var: str
    start: int
    end: int
    location: str = ""  # 割り当てたレジスタ名または退避領域


def live_intervals(func: Function) -> list[Interval]:
    """各変数の生存区間を（1 つの連続した区間として）求める。"""
    live_in, live_out = liveness(func)
    first: dict[str, int] = {}
    last: dict[str, int] = {}

    def touch(var: str, pos: int) -> None:
        first[var] = min(first.get(var, pos), pos)
        last[var] = max(last.get(var, pos), pos)

    for param in func.params:
        touch(param, 0)
    # 基本ブロックを並べた順に、命令へ通し番号 pos を付ける。
    pos = 0
    for block in func.blocks.values():
        start = pos
        for instr in block.instrs:
            for var in used_vars(instr):
                touch(var, pos)
            dst = defined_var(instr)
            if dst is not None:
                touch(dst, pos)
            pos += 1
        for var in used_vars(block.terminator):
            touch(var, pos)
        # ブロックの入口・出口で生存している変数は、区間をそこまで広げる。
        for var in live_in[block.label]:
            touch(var, start)
        for var in live_out[block.label]:
            touch(var, pos)
        pos += 1
    intervals = [Interval(v, first[v], last[v]) for v in first]
    return sorted(intervals, key=lambda i: (i.start, i.end))


def linear_scan(intervals: list[Interval], num_registers: int) -> int:
    """Poletto と Sarkar の線形走査法。使った退避領域の数を返す。"""
    free = [f"r{i}" for i in range(num_registers)]
    active: list[Interval] = []  # レジスタを持つ区間（end の昇順）
    spill_count = 0

    def spill_slot() -> str:
        nonlocal spill_count
        spill_count += 1
        return f"[fp-{spill_count}]"

    for current in intervals:
        # 終わった区間のレジスタを解放する。
        for old in list(active):
            if old.end < current.start:
                active.remove(old)
                free.append(old.location)
        if free:
            current.location = free.pop(0)
            active.append(current)
        else:
            # 最も遠くまで生きる区間をスピルする。
            victim = active[-1]
            if victim.end > current.end:
                current.location = victim.location
                victim.location = spill_slot()
                active.remove(victim)
                active.append(current)
            else:
                current.location = spill_slot()
        active.sort(key=lambda i: i.end)
    return spill_count


def assign_registers(func: Function, num_registers: int) -> str:
    """レジスタを割り当て、結果を擬似アセンブリ言語として返す。"""
    intervals = live_intervals(func)
    linear_scan(intervals, num_registers)
    location = {i.var: i.location for i in intervals}

    def rename(op: Operand) -> Operand:
        return Var(location[op.name]) if isinstance(op, Var) else op

    lines = [f"function {func.name}("
             + ", ".join(location[p] for p in func.params) + ")"]
    for block in func.blocks.values():
        lines.append(f"{block.label}:")
        for instr in block.instrs:
            map_operands(instr, rename)
            if not isinstance(instr, Store) and instr.dst is not None:
                instr.dst = location[instr.dst]
            # 同じ場所どうしのコピーは不要になる。
            if isinstance(instr, Copy) and instr.src == Var(instr.dst):
                continue
            lines.append("    " + format_item(instr))
        map_operands(block.terminator, rename)
        lines.append("    " + format_item(block.terminator))
    return "\n".join(lines)


def format_intervals(func: Function) -> str:
    return "\n".join(f"{i.var:8} [{i.start:2}, {i.end:2}]"
                     for i in live_intervals(func))


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
    num_registers = 3
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    if len(sys.argv) > 2:
        num_registers = int(sys.argv[2])
    module = optimize_module(module_to_ssa(compile_to_ir(source)))
    for func in module.values():
        from_ssa(func)
        print(format_function(func))
        print("--- 生存区間")
        print(format_intervals(func))
        print(f"--- レジスタ割り当て（レジスタ {num_registers} 個）")
        print(assign_registers(func, num_registers))
        print()


if __name__ == "__main__":
    main()
