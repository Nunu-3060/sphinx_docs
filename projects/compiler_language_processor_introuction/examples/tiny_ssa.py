"""支配関係の計算と SSA 形式への変換（第 8 章）。

* 支配木: Cooper, Harvey, Kennedy の反復アルゴリズムで求める。
* SSA 形式: Cytron らの方法（支配辺境に φ 関数を置き、支配木をたどって
  変数の名前を付け替える）で構築する。
* SSA 形式からの復帰: φ 関数を先行ブロックでのコピーに置き換える。
"""

from __future__ import annotations

import sys

from tiny_ir import (
    Const, Copy, Function, IRInterpreter, Module, Operand, Phi, Store, Var,
    compile_to_ir, defined_var, format_function, map_operands)


def reverse_postorder(func: Function) -> list[str]:
    """入口から深さ優先探索したときの帰りがけ順の逆順。"""
    order: list[str] = []
    visited: set[str] = set()

    def visit(label: str) -> None:
        visited.add(label)
        for succ in func.blocks[label].successors():
            if succ not in visited:
                visit(succ)
        order.append(label)

    visit(func.entry)
    return order[::-1]


def immediate_dominators(func: Function) -> dict[str, str]:
    """各基本ブロックの直接支配ブロックを返す（入口は自分自身）。"""
    rpo = reverse_postorder(func)
    index = {label: i for i, label in enumerate(rpo)}
    preds = func.predecessors()
    idom: dict[str, str] = {func.entry: func.entry}

    def intersect(a: str, b: str) -> str:
        # 支配木を上にたどり、a と b の共通の祖先を探す。
        while a != b:
            while index[a] > index[b]:
                a = idom[a]
            while index[b] > index[a]:
                b = idom[b]
        return a

    changed = True
    while changed:
        changed = False
        for label in rpo[1:]:
            done = [p for p in preds[label] if p in idom]
            new_idom = done[0]
            for p in done[1:]:
                new_idom = intersect(p, new_idom)
            if idom.get(label) != new_idom:
                idom[label] = new_idom
                changed = True
    return idom


def dominator_tree(func: Function,
                   idom: dict[str, str]) -> dict[str, list[str]]:
    """支配木の子の一覧を返す。"""
    children: dict[str, list[str]] = {label: [] for label in func.blocks}
    for label in reverse_postorder(func):
        if label != func.entry:
            children[idom[label]].append(label)
    return children


def dominance_frontiers(func: Function,
                        idom: dict[str, str]) -> dict[str, set[str]]:
    """各基本ブロックの支配辺境を返す。"""
    frontier: dict[str, set[str]] = {label: set() for label in func.blocks}
    for label, preds in func.predecessors().items():
        if len(preds) < 2:
            continue
        for p in preds:
            runner = p
            while runner != idom[label]:
                frontier[runner].add(label)
                runner = idom[runner]
    return frontier


def to_ssa(func: Function) -> Function:
    """関数を SSA 形式に変換する（func を直接書き換える）。"""
    idom = immediate_dominators(func)
    frontier = dominance_frontiers(func, idom)
    children = dominator_tree(func, idom)
    preds = func.predecessors()

    # 1. 変数ごとに、定義している基本ブロックと定義の数を数える。
    def_blocks: dict[str, set[str]] = {p: {func.entry} for p in func.params}
    def_count: dict[str, int] = {p: 1 for p in func.params}
    for block in func.blocks.values():
        for instr in block.instrs:
            dst = defined_var(instr)
            if dst is not None:
                def_blocks.setdefault(dst, set()).add(block.label)
                def_count[dst] = def_count.get(dst, 0) + 1
    # 定義が 1 つだけの変数は、定義がすべての使用を支配するので名前を変えない。
    targets = {v for v, n in def_count.items() if n >= 2}

    # 2. 支配辺境に φ 関数を置く。
    phi_var: dict[int, str] = {}  # φ 関数（の id）→ 元の変数名
    for var in sorted(targets):
        worklist = list(def_blocks[var])
        has_phi: set[str] = set()
        while worklist:
            x = worklist.pop()
            for y in frontier[x]:
                if y in has_phi:
                    continue
                phi = Phi(var, {p: Var(var) for p in preds[y]})
                func.blocks[y].instrs.insert(0, phi)
                phi_var[id(phi)] = var
                has_phi.add(y)
                if y not in def_blocks[var]:
                    def_blocks[var].add(y)
                    worklist.append(y)

    # 3. 支配木をたどりながら名前を付け替える。
    counter: dict[str, int] = {v: 0 for v in targets}
    stacks: dict[str, list[str]] = {
        v: [v] if v in func.params else [] for v in targets}

    def current(op: Operand) -> Operand:
        if isinstance(op, Var) and op.name in targets:
            stack = stacks[op.name]
            return Var(stack[-1]) if stack else Const(None)
        return op

    def rename(label: str) -> None:
        block = func.blocks[label]
        pushed: list[str] = []
        for instr in block.instrs:
            if not isinstance(instr, Phi):
                map_operands(instr, current)
            if isinstance(instr, Store) or instr.dst not in targets:
                continue
            dst = instr.dst
            counter[dst] += 1
            new_name = f"{dst}.{counter[dst]}"
            stacks[dst].append(new_name)
            pushed.append(dst)
            instr.dst = new_name
        map_operands(block.terminator, current)
        for succ in block.successors():
            for phi in func.blocks[succ].phis():
                phi.args[label] = current(Var(phi_var[id(phi)]))
        for child in children[label]:
            rename(child)
        for var in pushed:
            stacks[var].pop()

    rename(func.entry)
    return func


def from_ssa(func: Function) -> Function:
    """φ 関数をコピー命令に置き換えて SSA 形式から戻す（直接書き換える）。

    x = phi(B1: a, B2: b) を、B1 の末尾の x' = a と B2 の末尾の x' = b、
    そして元の位置の x = x' に置き換える。新しい変数 x' を経由するので、
    φ 関数どうしが互いの値を参照していても正しく動く。
    """
    for block in list(func.blocks.values()):
        for i, phi in enumerate(block.phis()):
            temp = phi.dst + "'"
            for pred, value in phi.args.items():
                func.blocks[pred].instrs.append(Copy(temp, value))
            block.instrs[i] = Copy(phi.dst, Var(temp))
    return func


def module_to_ssa(module: Module) -> Module:
    for func in module.values():
        to_ssa(func)
    return module


def module_from_ssa(module: Module) -> Module:
    for func in module.values():
        from_ssa(func)
    return module


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
    for func in module.values():
        idom = immediate_dominators(func)
        frontier = dominance_frontiers(func, idom)
        print(f"function {func.name}")
        for label in func.blocks:
            print(f"  {label:12} idom={idom[label]:12} "
                  f"DF={sorted(frontier[label])}")
    module_to_ssa(module)
    print("--- SSA 形式")
    for func in module.values():
        print(format_function(func))
    IRInterpreter(module).run()
    module_from_ssa(module)
    print("--- SSA 形式から戻した結果")
    for func in module.values():
        print(format_function(func))
    IRInterpreter(module).run()


if __name__ == "__main__":
    main()
