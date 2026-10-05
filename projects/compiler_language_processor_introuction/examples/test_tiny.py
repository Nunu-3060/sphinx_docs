"""Tiny 処理系のテスト（付録 A）。

すべての実行方式（木構造インタプリタ、IR、SSA 形式の IR、最適化した IR、
SSA 形式から戻した IR、仮想マシン）が同じ出力になることを確かめる。

    python -m unittest test_tiny.py
"""

from __future__ import annotations

import io
import unittest
from collections.abc import Callable
from pathlib import Path

from tiny_bytecode import compile_source
from tiny_checker import TypeCheckError
from tiny_interp import run_source
from tiny_ir import IRInterpreter, compile_to_ir
from tiny_lexer import LexError
from tiny_opt import optimize_module
from tiny_parser import ParseError
from tiny_runtime import TinyRuntimeError
from tiny_ssa import module_from_ssa, module_to_ssa
from tiny_vm import VM

PROGRAMS = Path(__file__).parent / "programs"


def run_interp(source: str, out: io.StringIO) -> None:
    run_source(source, out)


def run_ir(source: str, out: io.StringIO) -> None:
    IRInterpreter(compile_to_ir(source), out).run()


def run_ssa(source: str, out: io.StringIO) -> None:
    IRInterpreter(module_to_ssa(compile_to_ir(source)), out).run()


def run_opt(source: str, out: io.StringIO) -> None:
    module = optimize_module(module_to_ssa(compile_to_ir(source)))
    IRInterpreter(module, out).run()


def run_from_ssa(source: str, out: io.StringIO) -> None:
    module = optimize_module(module_to_ssa(compile_to_ir(source)))
    IRInterpreter(module_from_ssa(module), out).run()


def run_vm(source: str, out: io.StringIO) -> None:
    VM(compile_source(source), out).run()


RUNNERS: dict[str, Callable[[str, io.StringIO], None]] = {
    "interp": run_interp, "ir": run_ir, "ssa": run_ssa, "opt": run_opt,
    "from_ssa": run_from_ssa, "vm": run_vm,
}


def outputs(source: str) -> dict[str, str]:
    results = {}
    for name, runner in RUNNERS.items():
        out = io.StringIO()
        runner(source, out)
        results[name] = out.getvalue()
    return results


def main_with(body: str) -> str:
    return "fn main() {\n" + body + "\n}\n"


class SameOutputTest(unittest.TestCase):
    def assert_output(self, source: str, expected: str) -> None:
        for name, result in outputs(source).items():
            with self.subTest(runner=name):
                self.assertEqual(result, expected)

    def test_programs(self) -> None:
        for path in sorted(PROGRAMS.glob("*.tiny")):
            if path.name == "type_error.tiny":
                continue
            with self.subTest(program=path.name):
                results = outputs(path.read_text(encoding="utf-8"))
                self.assertEqual(len(set(results.values())), 1, results)

    def test_integer_division(self) -> None:
        self.assert_output(main_with("print(7 / 2, -7 / 2, 7 % -2, -7 % 2);"),
                           "3 -3 1 -1\n")

    def test_short_circuit(self) -> None:
        source = ("fn t(s: str) -> bool { print(s); return true; }\n"
                  "fn f(s: str) -> bool { print(s); return false; }\n"
                  + main_with("print(f(\"a\") && t(\"b\"));"
                              "print(t(\"c\") || f(\"d\"));"))
        self.assert_output(source, "a\nfalse\nc\ntrue\n")

    def test_shadowing(self) -> None:
        self.assert_output(
            main_with("let x = 1; { let x = 2; print(x); } print(x);"),
            "2\n1\n")

    def test_strings_and_arrays(self) -> None:
        self.assert_output(
            main_with('let a = ["x", "y"]; push(a, "z\\n");'
                      'print(a, len(a), "ab" + "c", "abc"[1]);'),
            '["x", "y", "z\n"] 3 abc b\n')

    def test_constant_branch(self) -> None:
        self.assert_output(
            main_with("let a = 3 * 4; if (a > 100) { print(1); }"
                      " else { print(a + 1); }"),
            "13\n")


class ErrorTest(unittest.TestCase):
    def test_lex_error(self) -> None:
        for body in ["let x = 1 @ 2;", "let x = １;", "let 変数 = 1;"]:
            with self.subTest(body=body):
                with self.assertRaises(LexError):
                    run_source(main_with(body))

    def test_parse_errors_are_collected(self) -> None:
        source = main_with("let x = ;\nlet y = 1\nprint(x);")
        with self.assertRaises(ParseError) as cm:
            run_source(source)
        self.assertEqual(len(cm.exception.all_errors), 2)

    def test_type_errors(self) -> None:
        bad = [
            main_with('let x = 1 + "a";'),
            main_with("print(y);"),
            main_with("let a = [];"),
            main_with('let s = "abc"; s[0] = "x";'),
            "fn f() -> int { if (true) { return 1; } }\n" + main_with(""),
            "fn main(x: int) {}\n",
        ]
        for source in bad:
            with self.subTest(source=source):
                with self.assertRaises(TypeCheckError):
                    run_source(source)

    def test_runtime_errors(self) -> None:
        for body in ["let z = 0; print(1 / z);", "let a = [1]; print(a[1]);",
                     "let a = [1]; let i = 0 - 1; print(a[i]);"]:
            for name, runner in RUNNERS.items():
                with self.subTest(body=body, runner=name):
                    with self.assertRaises(TinyRuntimeError):
                        runner(main_with(body), io.StringIO())


if __name__ == "__main__":
    unittest.main()
