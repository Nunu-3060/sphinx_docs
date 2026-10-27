"""Tiny 言語の型と抽象構文木（第 5 章）。"""

from __future__ import annotations

from dataclasses import dataclass, field, fields


# ---------------------------------------------------------------- 型

@dataclass(frozen=True)
class Type:
    """Tiny の型の基底クラス。"""


@dataclass(frozen=True)
class IntType(Type):
    def __str__(self) -> str:
        return "int"


@dataclass(frozen=True)
class BoolType(Type):
    def __str__(self) -> str:
        return "bool"


@dataclass(frozen=True)
class StrType(Type):
    def __str__(self) -> str:
        return "str"


@dataclass(frozen=True)
class VoidType(Type):
    """値を返さない関数の戻り値の型。"""

    def __str__(self) -> str:
        return "void"


@dataclass(frozen=True)
class ArrayType(Type):
    element: Type

    def __str__(self) -> str:
        return f"[{self.element}]"


INT = IntType()
BOOL = BoolType()
STR = StrType()
VOID = VoidType()


# ---------------------------------------------------------------- 式

@dataclass
class Node:
    """構文木のノードの基底クラス。line はソースコード上の行番号。"""

    line: int = field(default=0, kw_only=True, compare=False)


@dataclass
class Expr(Node):
    # 意味解析（第 6 章）で式の型を書き込む。
    ty: Type | None = field(default=None, kw_only=True, compare=False)


@dataclass
class IntLit(Expr):
    value: int


@dataclass
class BoolLit(Expr):
    value: bool


@dataclass
class StrLit(Expr):
    value: str


@dataclass
class ArrayLit(Expr):
    elements: list[Expr]


@dataclass
class Name(Expr):
    name: str


@dataclass
class Index(Expr):
    target: Expr
    index: Expr


@dataclass
class Call(Expr):
    callee: str
    args: list[Expr]


@dataclass
class Unary(Expr):
    op: str
    operand: Expr


@dataclass
class Binary(Expr):
    op: str
    left: Expr
    right: Expr


# ---------------------------------------------------------------- 文

@dataclass
class Stmt(Node):
    pass


@dataclass
class Block(Stmt):
    stmts: list[Stmt]


@dataclass
class Let(Stmt):
    name: str
    declared_type: Type | None
    value: Expr


@dataclass
class Assign(Stmt):
    target: Expr  # Name または Index
    value: Expr


@dataclass
class If(Stmt):
    cond: Expr
    then_body: Block
    else_body: Stmt | None  # Block、If、None のいずれか


@dataclass
class While(Stmt):
    cond: Expr
    body: Block


@dataclass
class Return(Stmt):
    value: Expr | None


@dataclass
class ExprStmt(Stmt):
    expr: Expr


# ---------------------------------------------------------------- 関数とプログラム

@dataclass
class Param(Node):
    name: str
    ty: Type


@dataclass
class FuncDef(Node):
    name: str
    params: list[Param]
    return_type: Type
    body: Block


@dataclass
class Program(Node):
    functions: list[FuncDef]


# ---------------------------------------------------------------- 表示

def dump(node: object, indent: int = 0) -> str:
    """構文木を字下げ付きの文字列に変換する。"""
    pad = "  " * indent
    if isinstance(node, list):
        if not node:
            return pad + "[]"
        return "\n".join(dump(item, indent) for item in node)
    if not isinstance(node, Node):
        return pad + (str(node) if isinstance(node, Type) else repr(node))
    lines = [pad + type(node).__name__]
    for f in fields(node):
        if f.name in ("line", "ty"):
            continue
        value = getattr(node, f.name)
        if isinstance(value, (Node, list)) and value:
            lines.append(f"{pad}  {f.name}:")
            lines.append(dump(value, indent + 2))
        else:
            shown = str(value) if isinstance(value, Type) else repr(value)
            lines.append(f"{pad}  {f.name}: {shown}")
    return "\n".join(lines)
