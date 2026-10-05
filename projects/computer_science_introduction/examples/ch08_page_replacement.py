"""ページ置換アルゴリズム（FIFO・LRU・OPT）を比較するサンプル。

同じページ参照列に対して、ページフレーム数を固定したときの
ページフォールト回数を 3 つのアルゴリズムで数える。
最後に、FIFO でフレームを増やすとフォールトが増える
Belady の異常の例も示す。乱数は使わないので出力は毎回同じになる。

実行方法: python ch08_page_replacement.py
関連する章: 第 8 章「オペレーティングシステム」
"""

from collections import OrderedDict, deque

REFERENCES = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
BELADY_REFERENCES = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]


def fifo(refs: list[int], frames: int) -> int:
    """最も早く読み込んだページを追い出す。フォールト回数を返す。"""
    resident: set[int] = set()
    order: deque[int] = deque()  # 読み込んだ順
    faults = 0
    for page in refs:
        if page in resident:
            continue  # 命中しても順序は変えない
        faults += 1
        if len(resident) == frames:
            resident.remove(order.popleft())
        resident.add(page)
        order.append(page)
    return faults


def lru(refs: list[int], frames: int) -> int:
    """最も長く使われていないページを追い出す。フォールト回数を返す。"""
    resident: OrderedDict[int, None] = OrderedDict()  # 先頭が最も古い
    faults = 0
    for page in refs:
        if page in resident:
            resident.move_to_end(page)  # 使ったので最新にする
            continue
        faults += 1
        if len(resident) == frames:
            resident.popitem(last=False)
        resident[page] = None
    return faults


def opt(refs: list[int], frames: int) -> int:
    """次に使われるのが最も遠いページを追い出す。フォールト回数を返す。"""
    resident: set[int] = set()
    faults = 0
    for i, page in enumerate(refs):
        if page in resident:
            continue
        faults += 1
        if len(resident) == frames:
            future = refs[i + 1:]

            def next_use(p: int) -> int:
                """p が次に参照される位置（参照されなければ無限大扱い）。"""
                return future.index(p) if p in future else len(future)

            resident.remove(max(sorted(resident), key=next_use))
        resident.add(page)
    return faults


def main() -> None:
    """3 つのアルゴリズムの比較と Belady の異常を表示する。"""
    print("参照列:", " ".join(map(str, REFERENCES)))
    for frames in (3, 4):
        print(f"フレーム数 {frames}: FIFO {fifo(REFERENCES, frames)} 回, "
              f"LRU {lru(REFERENCES, frames)} 回, "
              f"OPT {opt(REFERENCES, frames)} 回")
    print("Belady の異常の参照列:", " ".join(map(str, BELADY_REFERENCES)))
    for frames in (3, 4):
        print(f"  FIFO, フレーム数 {frames}: "
              f"{fifo(BELADY_REFERENCES, frames)} 回")


if __name__ == "__main__":
    main()
