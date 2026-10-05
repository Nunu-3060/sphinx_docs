"""ガベージコレクションのシミュレーション（第 11 章）。

オブジェクトどうしの参照関係だけを持つ小さなヒープを作り、
参照カウント・マーク & スイープ・コピー GC の動きを確かめる。
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------- 参照カウント

class RefCountHeap:
    """各オブジェクトが「自分を指す参照の数」を持つヒープ。"""

    def __init__(self) -> None:
        self.refs: dict[str, list[str]] = {}  # オブジェクト → 参照先
        self.count: dict[str, int] = {}

    def new(self, name: str) -> None:
        self.refs[name] = []
        self.count[name] = 0

    def increment(self, name: str) -> None:
        self.count[name] += 1

    def decrement(self, name: str) -> None:
        self.count[name] -= 1
        if self.count[name] == 0:
            print(f"  {name} を解放")
            for child in self.refs.pop(name):
                self.decrement(child)
            del self.count[name]

    def add_ref(self, src: str, dst: str) -> None:
        self.refs[src].append(dst)
        self.increment(dst)


def demo_refcount() -> None:
    print("== 参照カウント")
    heap = RefCountHeap()
    for name in "ABCD":
        heap.new(name)
    heap.increment("A")  # ルート（局所変数）から A を指す
    heap.add_ref("A", "B")
    heap.increment("C")  # ルートから C を指す
    heap.add_ref("C", "D")
    heap.add_ref("D", "C")  # C と D は循環している
    print("ルートから A への参照を消す")
    heap.decrement("A")
    print("ルートから C への参照を消す")
    heap.decrement("C")
    print(f"  解放されずに残ったオブジェクト: {sorted(heap.refs)}")


# ---------------------------------------------------------------- マーク & スイープ

def mark_and_sweep(refs: dict[str, list[str]], roots: list[str]) -> list[str]:
    """ルートから到達できないオブジェクトを refs から取り除き、その名前を返す。"""
    marked: set[str] = set()
    stack = list(roots)
    while stack:  # マーク: ルートからたどれるものに印を付ける
        name = stack.pop()
        if name not in marked:
            marked.add(name)
            stack.extend(refs[name])
    garbage = [name for name in refs if name not in marked]
    for name in garbage:  # スイープ: 印のないものを解放する
        del refs[name]
    return garbage


def demo_mark_and_sweep() -> None:
    print("== マーク & スイープ")
    refs = {"A": ["B"], "B": [], "C": ["D"], "D": ["C"], "E": ["B"]}
    print(f"  解放: {mark_and_sweep(refs, roots=['A'])}")
    print(f"  残り: {sorted(refs)}")


# ---------------------------------------------------------------- コピー GC

@dataclass
class Cell:
    """ヒープ上のオブジェクト。fields は参照先のアドレス。"""

    name: str
    fields: list[int] = field(default_factory=list)
    forward: int | None = None  # コピー済みなら移動先のアドレス


def copying_collect(from_space: list[Cell],
                    roots: list[int]) -> tuple[list[Cell], list[int]]:
    """Cheney のアルゴリズム。生きているオブジェクトを新しい領域に詰めて写す。

    新しい領域と、書き換えたルート（新しいアドレス）を返す。
    """
    to_space: list[Cell] = []

    def copy(address: int) -> int:
        cell = from_space[address]
        if cell.forward is None:
            to_space.append(Cell(cell.name, list(cell.fields)))
            cell.forward = len(to_space) - 1
        return cell.forward

    new_roots = [copy(r) for r in roots]
    scan = 0
    while scan < len(to_space):  # 写したオブジェクトの参照先を順に写す
        cell = to_space[scan]
        cell.fields = [copy(f) for f in cell.fields]
        scan += 1
    return to_space, new_roots


def show(space: list[Cell]) -> str:
    return ", ".join(f"{i}:{c.name}->{c.fields}" for i, c in enumerate(space))


def demo_copying() -> None:
    print("== コピー GC")
    heap = [Cell("A", [3]), Cell("X"), Cell("Y", [1]), Cell("B", [4]),
            Cell("C", [0])]
    print(f"  コピー前: {show(heap)}")
    new_heap, roots = copying_collect(heap, roots=[0])
    print(f"  コピー後: {show(new_heap)}  ルート={roots}")


def main() -> None:
    demo_refcount()
    demo_mark_and_sweep()
    demo_copying()


if __name__ == "__main__":
    main()
