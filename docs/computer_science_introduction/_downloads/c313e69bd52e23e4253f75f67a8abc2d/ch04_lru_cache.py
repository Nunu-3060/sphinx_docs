"""OrderedDict による LRU キャッシュのサンプル。

容量を超えたら、最も長い間使われていない（Least Recently Used）
キーを追い出すキャッシュを collections.OrderedDict で実装し、
追加・参照のたびに内部の順序と追い出しの様子を表示する。
後半では functools.lru_cache の統計情報も表示する。

実行方法: python ch04_lru_cache.py
関連する章: 第 4 章「データ構造」
"""

from collections import OrderedDict
from functools import lru_cache


class LRUCache:
    """文字列のキーと整数の値を格納する LRU キャッシュ。"""

    def __init__(self, capacity: int) -> None:
        """容量（格納できる最大のキーの数）を指定して空のキャッシュを作る。"""
        self.capacity = capacity
        # 先頭が最も古く使われたキー、末尾が最も新しく使われたキー
        self.data: OrderedDict[str, int] = OrderedDict()

    def get(self, key: str) -> int | None:
        """キーの値を返す。無ければ None を返す。"""
        if key not in self.data:
            return None
        self.data.move_to_end(key)  # 使われたので末尾（最新）へ: O(1)
        return self.data[key]

    def put(self, key: str, value: int) -> str | None:
        """値を格納し、追い出したキーがあればそれを返す。"""
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            evicted, _ = self.data.popitem(last=False)  # 先頭を削除: O(1)
            return evicted
        return None

    def keys(self) -> list[str]:
        """古い順にキーの一覧を返す。"""
        return list(self.data)


@lru_cache(maxsize=2)
def square(x: int) -> int:
    """引数の 2 乗を返す（キャッシュの動作確認用）。"""
    return x * x


def main() -> None:
    """LRU キャッシュに対する一連の操作を実行し、様子を表示する。"""
    cache = LRUCache(capacity=3)
    operations: list[tuple[str, str, int]] = [
        ("put", "A", 1),
        ("put", "B", 2),
        ("put", "C", 3),
        ("get", "A", 0),
        ("put", "D", 4),
        ("get", "B", 0),
        ("put", "E", 5),
        ("get", "C", 0),
    ]
    for op, key, value in operations:
        if op == "put":
            evicted = cache.put(key, value)
            note = f"  {evicted} を追い出し" if evicted else ""
            print(f"put({key}, {value}) 古い順: {cache.keys()}{note}")
        else:
            result = cache.get(key)
            print(f"get({key}) = {result} 古い順: {cache.keys()}")

    for x in [1, 2, 1, 3, 2]:
        square(x)
    print(square.cache_info())


if __name__ == "__main__":
    main()
