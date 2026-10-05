"""第 6 章: バックトラッキングによる N クイーン問題。

n x n の盤面に、互いに取り合わないように n 個のクイーンを置く方法を数える。
1 行ずつクイーンを置き、矛盾が生じた時点でその先の探索を打ち切る (枝刈り)。

実行例::

    python ch06_backtracking.py
"""

from __future__ import annotations


def count_n_queens(n: int) -> int:
    """n クイーン問題の解の個数を返す。"""
    cols: set[int] = set()
    diag1: set[int] = set()  # row + col が等しいマスは同じ斜線上にある
    diag2: set[int] = set()  # row - col が等しいマスは同じ斜線上にある

    def place(row: int) -> int:
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in cols or row + col in diag1 or row - col in diag2:
                continue  # 枝刈り: この先を調べても解は無い
            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            count += place(row + 1)
            cols.remove(col)  # 状態を元に戻して次の候補を試す
            diag1.remove(row + col)
            diag2.remove(row - col)
        return count

    return place(0)


def main() -> None:
    for n in range(1, 9):
        print(f"n = {n}: {count_n_queens(n)} 通り")


if __name__ == "__main__":
    main()
