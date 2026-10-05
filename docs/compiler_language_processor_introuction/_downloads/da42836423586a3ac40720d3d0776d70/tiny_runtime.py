"""Tiny 言語の実行時ライブラリ（第 7 章）。

演算の意味と組み込み関数をまとめる。インタプリタ・IR インタプリタ・
仮想マシン・最適化器（定数畳み込み）がすべてこのモジュールを使うため、
どの実行方式でも同じ結果になる。
"""

from __future__ import annotations

from typing import TextIO, Union

from tiny_lexer import TinyError

# Tiny の値。配列は Python のリストで表す。None は「値なし」を表す。
Value = Union[int, bool, str, list["Value"], None]

BUILTINS = ("print", "len", "push", "to_str")


class TinyRuntimeError(TinyError):
    """実行時エラー（ゼロ除算・範囲外アクセスなど）。"""


def int_div(a: int, b: int) -> int:
    """0 に向かって切り捨てる整数除算（C 言語と同じ）。"""
    if b == 0:
        raise TinyRuntimeError("0 で除算しました")
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q


def int_mod(a: int, b: int) -> int:
    """int_div と組になる剰余。a == int_div(a, b) * b + int_mod(a, b) となる。"""
    return a - int_div(a, b) * b


def binary_op(op: str, left: Value, right: Value) -> Value:
    """二項演算を実行する（&& と || は短絡評価のため含めない）。"""
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    if op == "+":
        if isinstance(left, str) and isinstance(right, str):
            return left + right
    if not isinstance(left, int) or not isinstance(right, int):
        raise TinyRuntimeError(f"演算 {op} の型が不正です")
    match op:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return int_div(left, right)
        case "%":
            return int_mod(left, right)
        case "<":
            return left < right
        case "<=":
            return left <= right
        case ">":
            return left > right
        case ">=":
            return left >= right
    raise TinyRuntimeError(f"未知の演算子 {op} です")


def unary_op(op: str, operand: Value) -> Value:
    """単項演算を実行する。"""
    if op == "-" and isinstance(operand, int):
        return -operand
    if op == "!" and isinstance(operand, bool):
        return not operand
    raise TinyRuntimeError(f"演算 {op} の型が不正です")


def index_value(base: Value, index: Value) -> Value:
    """base[index] を返す。範囲外ならエラー。"""
    if not isinstance(index, int) or not isinstance(base, (list, str)):
        raise TinyRuntimeError("添字演算の型が不正です")
    if not 0 <= index < len(base):
        raise TinyRuntimeError(f"添字 {index} が範囲外です")
    return base[index]


def store_index(base: Value, index: Value, value: Value) -> None:
    """base[index] = value を実行する。範囲外ならエラー。"""
    if not isinstance(index, int) or not isinstance(base, list):
        raise TinyRuntimeError("添字への代入の型が不正です")
    if not 0 <= index < len(base):
        raise TinyRuntimeError(f"添字 {index} が範囲外です")
    base[index] = value


def format_value(value: Value, nested: bool = False) -> str:
    """値を print 用の文字列に変換する。"""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return f'"{value}"' if nested else value
    if isinstance(value, list):
        return "[" + ", ".join(format_value(v, True) for v in value) + "]"
    return str(value)


def call_builtin(name: str, args: list[Value], out: TextIO) -> Value:
    """組み込み関数を呼び出す。"""
    match name:
        case "print":
            out.write(" ".join(format_value(a) for a in args) + "\n")
            return None
        case "len":
            target = args[0]
            if not isinstance(target, (list, str)):
                raise TinyRuntimeError("len の引数が不正です")
            return len(target)
        case "push":
            array = args[0]
            if not isinstance(array, list):
                raise TinyRuntimeError("push の引数が不正です")
            array.append(args[1])
            return None
        case "to_str":
            return format_value(args[0])
    raise TinyRuntimeError(f"未知の組み込み関数 {name} です")
