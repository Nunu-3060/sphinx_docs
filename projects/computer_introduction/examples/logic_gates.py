"""論理ゲートのサンプル。

NAND ゲートだけを使って NOT、AND、OR、XOR を組み立て、
それぞれの真理値表を表示します。

実行方法::

    python logic_gates.py
"""

from collections.abc import Callable
from itertools import product

# 2 入力 1 出力の論理ゲートを表す型 (入力・出力は 0 または 1)
Gate = Callable[[int, int], int]


def nand(a: int, b: int) -> int:
    """NAND: 両方が 1 のときだけ 0、それ以外は 1。"""
    return 0 if a == 1 and b == 1 else 1


def not_(a: int) -> int:
    """NOT: 同じ信号を NAND の 2 つの入力に入れる。"""
    return nand(a, a)


def and_(a: int, b: int) -> int:
    """AND: NAND の出力を反転する。"""
    return not_(nand(a, b))


def or_(a: int, b: int) -> int:
    """OR: ド・モルガンの法則 A + B = NOT(NOT A ・ NOT B) を使う。"""
    return nand(not_(a), not_(b))


def xor(a: int, b: int) -> int:
    """XOR: NAND 4 個で作る標準的な回路。"""
    c = nand(a, b)
    return nand(nand(a, c), nand(b, c))


def print_truth_table(name: str, gate: Gate) -> None:
    """2 入力ゲートの真理値表を表示する。"""
    print(f"{name}:  A B | 出力")
    for a, b in product([0, 1], repeat=2):
        print(f"{'':>{len(name)}}   {a} {b} |  {gate(a, b)}")


def main() -> None:
    """NOT と 2 入力ゲートの真理値表を表示する。"""
    print("NOT:  A | 出力")
    for a in [0, 1]:
        print(f"      {a} |  {not_(a)}")

    gates: dict[str, Gate] = {
        "NAND": nand,
        "AND": and_,
        "OR": or_,
        "XOR": xor,
    }
    for name, gate in gates.items():
        print_truth_table(name, gate)


if __name__ == "__main__":
    main()
