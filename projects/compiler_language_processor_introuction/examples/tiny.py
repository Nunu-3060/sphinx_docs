"""Tiny 言語処理系のコマンドラインツール（付録 A）。

使用例:
    python tiny.py run programs/fib.tiny       # インタプリタで実行
    python tiny.py vm programs/fib.tiny        # 仮想マシンで実行
    python tiny.py ir --opt programs/fib.tiny  # 最適化した IR を表示
"""

from __future__ import annotations

import argparse
import sys

from tiny_ast import dump
from tiny_bytecode import compile_source, disassemble
from tiny_checker import check
from tiny_interp import run_source
from tiny_ir import (
    IRInterpreter, compile_to_ir, format_function, format_module, to_dot)
from tiny_lexer import TinyError, tokenize
from tiny_opt import optimize_module
from tiny_parser import ParseError, parse
from tiny_regalloc import assign_registers
from tiny_ssa import from_ssa, module_to_ssa
from tiny_vm import VM


def command(args: argparse.Namespace, source: str) -> None:
    match args.command:
        case "tokens":
            for token in tokenize(source):
                print(f"{token.line:3}:{token.column:<3} "
                      f"{token.kind.name:10} {token.text}")
        case "ast":
            print(dump(parse(source)))
        case "check":
            check(parse(source))
            print("エラーはありません")
        case "run":
            run_source(source)
        case "ir":
            module = compile_to_ir(source)
            if args.ssa or args.opt:
                module_to_ssa(module)
            if args.opt:
                optimize_module(module)
            if args.dot:
                print(to_dot(module[args.dot]))
            elif args.exec:
                IRInterpreter(module).run()
            else:
                print(format_module(module))
        case "bytecode":
            program = compile_source(source)
            print("\n\n".join(disassemble(f, program)
                              for f in program.functions))
        case "vm":
            VM(compile_source(source)).run()
        case "regalloc":
            module = optimize_module(module_to_ssa(compile_to_ir(source)))
            for func in module.values():
                from_ssa(func)
                print(format_function(func))
                print("--- レジスタ割り当て後")
                print(assign_registers(func, args.registers))
                print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Tiny 言語処理系")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, text in [("tokens", "トークン列を表示する"),
                       ("ast", "抽象構文木を表示する"),
                       ("check", "意味解析だけを行う"),
                       ("run", "木構造インタプリタで実行する"),
                       ("bytecode", "バイトコードを表示する"),
                       ("vm", "仮想マシンで実行する")]:
        sub.add_parser(name, help=text).add_argument("file")
    ir = sub.add_parser("ir", help="中間表現を表示する")
    ir.add_argument("file")
    ir.add_argument("--ssa", action="store_true", help="SSA 形式にする")
    ir.add_argument("--opt", action="store_true", help="最適化する")
    ir.add_argument("--dot", metavar="FUNC",
                    help="関数 FUNC の制御フローグラフを DOT 言語で出力する")
    ir.add_argument("--exec", action="store_true", help="IR を実行する")
    reg = sub.add_parser("regalloc", help="レジスタ割り当ての結果を表示する")
    reg.add_argument("file")
    reg.add_argument("-k", "--registers", type=int, default=4,
                     help="レジスタの数（既定値 4）")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as f:
        source = f.read()
    try:
        command(args, source)
    except ParseError as e:
        for error in e.all_errors:
            print(f"{args.file}:{error}", file=sys.stderr)
        return 1
    except TinyError as e:
        print(f"{args.file}:{e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
