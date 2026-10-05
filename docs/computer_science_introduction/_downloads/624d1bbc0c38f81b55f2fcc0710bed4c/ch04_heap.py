"""二分ヒープ（最小ヒープ）のサンプル。

配列で表した二分ヒープを自作し、標準ライブラリの heapq と同じ順序で
値を取り出せることを確かめる。後半では heapq を優先度付きキューとして
使う。

実行方法: python ch04_heap.py
関連する章: 第 4 章「データ構造」
"""

import heapq
import random


class MinHeap:
    """最小の値を常に先頭（添字 0）に置く二分ヒープ。

    添字 i のノードの子は 2i+1 と 2i+2、親は (i-1)//2 である。
    """

    def __init__(self) -> None:
        """空のヒープを作る。"""
        self.data: list[int] = []

    def push(self, value: int) -> None:
        """値を末尾に追加し、親より小さい間は親と交換する（上方移動）。"""
        self.data.append(value)
        i = len(self.data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self.data[parent] <= self.data[i]:
                break
            self.data[parent], self.data[i] = self.data[i], self.data[parent]
            i = parent

    def pop(self) -> int:
        """最小値を取り出す。末尾の値を根に移し、下方移動で整える。"""
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def _sift_down(self, i: int) -> None:
        """添字 i の値を、子のうち小さい方より大きい間は下へ移す。"""
        n = len(self.data)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self.data[child] < self.data[smallest]:
                    smallest = child
            if smallest == i:
                return
            self.data[i], self.data[smallest] = (
                self.data[smallest], self.data[i])
            i = smallest

    def __len__(self) -> int:
        """格納している値の数を返す。"""
        return len(self.data)


def main() -> None:
    """自作のヒープと heapq を比較し、優先度付きキューの例を示す。"""
    random.seed(4)
    values = [random.randint(1, 99) for _ in range(10)]
    print("入力:", values)

    mine = MinHeap()
    std: list[int] = []
    for v in values:
        mine.push(v)
        heapq.heappush(std, v)
    print("自作ヒープの内部配列:", mine.data)
    print("heapq の内部配列:    ", std)

    out_mine = [mine.pop() for _ in range(len(mine))]
    out_std = [heapq.heappop(std) for _ in range(len(std))]
    print("自作ヒープの取り出し順:", out_mine)
    print("heapq と一致するか:", out_mine == out_std)

    # (優先度, 内容) のタプルを入れると、優先度の小さい順に取り出せる
    tasks: list[tuple[int, str]] = []
    heapq.heappush(tasks, (3, "ログの整理"))
    heapq.heappush(tasks, (1, "障害対応"))
    heapq.heappush(tasks, (2, "コードレビュー"))
    while tasks:
        priority, name = heapq.heappop(tasks)
        print(f"優先度 {priority}: {name}")


if __name__ == "__main__":
    main()
