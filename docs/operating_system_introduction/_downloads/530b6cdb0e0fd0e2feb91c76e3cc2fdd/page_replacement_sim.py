"""ページ置換アルゴリズムのシミュレーター。

プログラムが参照するページ番号の列 (参照列) と、使える物理メモリの
枠 (フレーム) の数を与え、次のアルゴリズムでページフォールトが
何回起きるかを比べます。

* FIFO: 最も古くに読み込んだページを追い出す
* LRU: 最も長く参照されていないページを追い出す
* クロック: 参照ビットを使って LRU を近似する
* OPT: 今後最も長く参照されないページを追い出す (理論上の最適解)

実行方法::

    python page_replacement_sim.py
"""

from collections import OrderedDict, deque
from collections.abc import Callable

# 参照列とフレーム数を受け取り、ページフォールトの回数を返す関数の型
Algorithm = Callable[[list[int], int], int]


def fifo(references: list[int], frames: int) -> int:
    """FIFO でのページフォールトの回数を返す。"""
    memory: deque[int] = deque()
    faults = 0
    for page in references:
        if page in memory:
            continue
        faults += 1
        if len(memory) == frames:
            memory.popleft()  # 最も古くに読み込んだページを追い出す
        memory.append(page)
    return faults


def lru(references: list[int], frames: int) -> int:
    """LRU でのページフォールトの回数を返す。"""
    # 参照された順に並べ、先頭が最も長く参照されていないページになる
    memory: OrderedDict[int, None] = OrderedDict()
    faults = 0
    for page in references:
        if page in memory:
            memory.move_to_end(page)  # 最近参照されたので末尾へ
            continue
        faults += 1
        if len(memory) == frames:
            memory.popitem(last=False)
        memory[page] = None
    return faults


def clock(references: list[int], frames: int) -> int:
    """クロックアルゴリズムでのページフォールトの回数を返す。"""
    pages: list[int | None] = [None] * frames  # 各フレームのページ
    referenced = [False] * frames  # 各フレームの参照ビット
    hand = 0  # 時計の針 (次に調べるフレーム)
    faults = 0
    for page in references:
        if page in pages:
            referenced[pages.index(page)] = True
            continue
        faults += 1
        # 参照ビットが 0 のフレームが見つかるまで針を進める
        while referenced[hand]:
            referenced[hand] = False  # 1 なら 0 にして猶予を与える
            hand = (hand + 1) % frames
        pages[hand] = page
        referenced[hand] = True
        hand = (hand + 1) % frames
    return faults


def optimal(references: list[int], frames: int) -> int:
    """OPT でのページフォールトの回数を返す。"""
    memory: list[int] = []
    faults = 0
    for i, page in enumerate(references):
        if page in memory:
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(page)
            continue
        future = references[i + 1:]

        def next_use(p: int) -> int:
            """次に参照される位置を返す。参照されないなら無限大とみなす。"""
            return future.index(p) if p in future else len(future)

        memory.remove(max(memory, key=next_use))
        memory.append(page)
    return faults


ALGORITHMS: dict[str, Algorithm] = {
    "FIFO": fifo,
    "LRU": lru,
    "クロック": clock,
    "OPT": optimal,
}


def main() -> None:
    references = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    print(f"参照列: {references}")
    for frames in (3, 4):
        print(f"フレーム数 {frames}:")
        for name, algorithm in ALGORITHMS.items():
            faults = algorithm(references, frames)
            print(f"  ページフォールト {faults:>2} 回: {name}")

    # FIFO でフレームを増やすとかえってページフォールトが増える例
    belady = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    print()
    print(f"参照列: {belady}")
    for frames in (3, 4):
        print(f"  FIFO, フレーム数 {frames}: {fifo(belady, frames)} 回")


if __name__ == "__main__":
    main()
