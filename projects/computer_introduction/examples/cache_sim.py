"""ダイレクトマップ方式キャッシュのシミュレータ。

メモリアクセスの並び (アクセスパターン) によって
キャッシュのヒット率が大きく変わることを確かめます。

実行方法::

    python cache_sim.py
"""

from collections.abc import Iterable

# キャッシュのライン数とブロックの大きさ (1 ブロックに入るワード数)
NUM_LINES = 8
BLOCK_SIZE = 4


class DirectMappedCache:
    """ダイレクトマップ方式のキャッシュ。

    アドレスからブロック番号を求め、ブロック番号をライン数で割った
    余り (インデックス) で格納先のラインを 1 つに決めます。
    商 (タグ) を記録しておき、次のアクセスで一致すればヒットです。
    """

    def __init__(self, num_lines: int, block_size: int) -> None:
        self.num_lines = num_lines
        self.block_size = block_size
        # 各ラインに入っているブロックのタグ (None は空)
        self.tags: list[int | None] = [None] * num_lines
        self.hits = 0
        self.misses = 0

    def access(self, address: int) -> bool:
        """address を読み、ヒットしたら True を返す。"""
        block = address // self.block_size
        index = block % self.num_lines
        tag = block // self.num_lines
        if self.tags[index] == tag:
            self.hits += 1
            return True
        # ミスしたら主記憶からブロックを読み込み、ラインを置き換える
        self.tags[index] = tag
        self.misses += 1
        return False

    @property
    def hit_rate(self) -> float:
        """これまでのアクセスのヒット率。"""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def measure(addresses: Iterable[int]) -> DirectMappedCache:
    """空のキャッシュで addresses を順にアクセスした結果を返す。"""
    cache = DirectMappedCache(NUM_LINES, BLOCK_SIZE)
    for address in addresses:
        cache.access(address)
    return cache


def main() -> None:
    """アクセスパターンごとのヒット率を表示する。"""
    capacity = NUM_LINES * BLOCK_SIZE
    print(f"キャッシュ: {NUM_LINES} ライン x {BLOCK_SIZE} ワード"
          f" = {capacity} ワード")

    patterns: dict[str, list[int]] = {
        # 配列を先頭から順に読む (空間的局所性)
        "連続アクセス": list(range(256)),
        # 小さな範囲を何度も読む (時間的局所性)
        "同じ範囲の繰り返し": list(range(16)) * 10,
        # 同じラインに割り当てられる 2 つのアドレスを交互に読む
        "競合するアドレスの交互": [0, capacity] * 50,
        # 別のラインに割り当てられる 2 つのアドレスを交互に読む
        "競合しないアドレスの交互": [0, BLOCK_SIZE] * 50,
    }
    for name, addresses in patterns.items():
        cache = measure(addresses)
        print(
            f"  {name}: ヒット {cache.hits:>3} / ミス {cache.misses:>3}"
            f"  ヒット率 {cache.hit_rate:6.1%}"
        )


if __name__ == "__main__":
    main()
