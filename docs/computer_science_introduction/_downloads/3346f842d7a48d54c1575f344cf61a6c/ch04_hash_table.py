"""チェイン法によるハッシュ表のサンプル。

各バケットをリストとして持ち、同じバケットに入る（衝突した）キーを
そのリストにつなげて格納する。負荷率が 1 を超えたらバケット数を 2 倍に
して全要素を入れ直す（再ハッシュ）。

Python の組み込みの hash() は、文字列に対しては実行のたびに値が変わる
（ハッシュのランダム化）ため、ここでは結果を再現できるよう簡単な
ハッシュ関数を自作している。

実行方法: python ch04_hash_table.py
関連する章: 第 4 章「データ構造」
"""


def simple_hash(key: str) -> int:
    """文字列から 32 ビットの整数を計算する簡単なハッシュ関数。"""
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) % 2**32
    return h


class ChainedHashTable:
    """文字列のキーと整数の値を格納するチェイン法のハッシュ表。"""

    def __init__(self, capacity: int = 4) -> None:
        """指定した数の空のバケットを用意する。"""
        self.buckets: list[list[tuple[str, int]]] = [
            [] for _ in range(capacity)
        ]
        self.count = 0

    def _index(self, key: str) -> int:
        """キーが入るバケットの番号を求める。"""
        return simple_hash(key) % len(self.buckets)

    def load_factor(self) -> float:
        """負荷率（要素数 / バケット数）を返す。"""
        return self.count / len(self.buckets)

    def put(self, key: str, value: int) -> None:
        """キーと値を格納する。キーが既にあれば値を上書きする。"""
        bucket = self.buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1
        if self.load_factor() > 1.0:
            self._resize(2 * len(self.buckets))

    def get(self, key: str) -> int | None:
        """キーに対応する値を返す。無ければ None を返す。"""
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        return None

    def _resize(self, new_capacity: int) -> None:
        """バケット数を変えて、すべての要素を入れ直す。"""
        print(f"  -- 再ハッシュ: バケット数 {len(self.buckets)}"
              f" -> {new_capacity}")
        old_items = [item for bucket in self.buckets for item in bucket]
        self.buckets = [[] for _ in range(new_capacity)]
        for k, v in old_items:
            self.buckets[self._index(k)].append((k, v))

    def dump(self) -> None:
        """各バケットの中身を表示する。"""
        for i, bucket in enumerate(self.buckets):
            keys = [k for k, _ in bucket]
            print(f"  バケット {i}: {keys}")
        print(f"  要素数 {self.count}, 負荷率 {self.load_factor():.2f}")


def main() -> None:
    """ハッシュ表に値を格納し、内部の状態と検索結果を表示する。"""
    table = ChainedHashTable()
    stock = {"apple": 3, "banana": 5, "cherry": 7, "grape": 2,
             "lemon": 4, "melon": 1}
    for name, qty in stock.items():
        print(f"put({name!r}) ハッシュ値 {simple_hash(name)}")
        table.put(name, qty)
    print("最終状態:")
    table.dump()
    print("get('cherry') =", table.get("cherry"))
    print("get('peach') =", table.get("peach"))


if __name__ == "__main__":
    main()
