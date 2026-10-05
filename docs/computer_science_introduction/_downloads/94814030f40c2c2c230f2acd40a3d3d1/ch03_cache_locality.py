"""直接写像キャッシュのシミュレータで、アクセス順序とヒット率の関係を見る。

2 次元配列（行優先で連続したメモリに配置）を、行優先と列優先の
2 通りの順序で走査し、そのときのアドレス列を直接写像キャッシュに
与えてヒット率を比較する。Python のリストは実際の CPU キャッシュの
効果が見えにくいため、ここでは時間ではなくシミュレーションで比較する。

実行方法: python ch03_cache_locality.py
関連する章: 第 3 章「コンピュータの構成」
"""

from collections.abc import Iterator


class DirectMappedCache:
    """直接写像方式のキャッシュ（ヒット・ミスの回数だけを数える）。"""

    def __init__(self, num_lines: int, line_size: int) -> None:
        """ライン数 num_lines、ラインの大きさ line_size バイトで初期化する。"""
        self.num_lines = num_lines
        self.line_size = line_size
        # 各ラインに格納されているブロックのタグ（None は空）
        self.tags: list[int | None] = [None] * num_lines
        self.hits = 0
        self.misses = 0

    def access(self, address: int) -> None:
        """バイトアドレス address を読み出す。"""
        block = address // self.line_size  # 何番目のブロックか
        index = block % self.num_lines     # どのラインに入るか
        tag = block // self.num_lines      # ラインを共有するブロックの区別
        if self.tags[index] == tag:
            self.hits += 1
        else:
            self.misses += 1
            self.tags[index] = tag  # 主記憶から読み込んで置き換える

    def hit_rate(self) -> float:
        """これまでのアクセスのヒット率を返す。"""
        return self.hits / (self.hits + self.misses)


def row_major(rows: int, cols: int, elem: int) -> Iterator[int]:
    """行ごとに走査したときのアドレス列（a[0][0], a[0][1], ...）。"""
    for i in range(rows):
        for j in range(cols):
            yield (i * cols + j) * elem


def column_major(
    rows: int, cols: int, elem: int, pad: int = 0
) -> Iterator[int]:
    """列ごとに走査したときのアドレス列（a[0][0], a[1][0], ...）。

    pad は各行の末尾に置く詰め物の要素数で、行の先頭どうしの間隔が
    (cols + pad) 要素になる。
    """
    stride = cols + pad
    for j in range(cols):
        for i in range(rows):
            yield (i * stride + j) * elem


def simulate(addresses: Iterator[int]) -> DirectMappedCache:
    """32 KiB（64 バイト × 512 ライン）のキャッシュでアドレス列を処理する。"""
    cache = DirectMappedCache(num_lines=512, line_size=64)
    for address in addresses:
        cache.access(address)
    return cache


def main() -> None:
    """行優先と列優先のヒット率を比較して表示する。"""
    rows, cols, elem = 512, 512, 8  # 8 バイトの要素が 512 × 512 個（2 MiB）
    print(f"配列: {rows} x {cols}、要素 {elem} バイト、"
          "キャッシュ: 64 バイト x 512 ライン")
    for name, addresses in [
        ("行優先", row_major(rows, cols, elem)),
        ("列優先", column_major(rows, cols, elem)),
        ("列優先（詰め物あり）", column_major(rows, cols, elem, pad=8)),
    ]:
        cache = simulate(addresses)
        print(f"{name}: ヒット {cache.hits:6d} 回、ミス {cache.misses:6d} 回、"
              f"ヒット率 {cache.hit_rate():.1%}")


if __name__ == "__main__":
    main()
