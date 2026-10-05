"""連続アクセスとストライドアクセスの速さを比べるサンプル。

大きな bytearray を、隣のバイトを順に読む連続アクセスと、一定の間隔
（ストライド）をあけて読むアクセスで、同じ回数だけ読み、実行時間を
比較します。読む位置の列はあらかじめ作っておき、時間の測定には含め
ません。結果は環境によって変わります。

実行方法: python cache_effect.py
"""

import time

SIZE = 64 * 1024 * 1024  # 配列の大きさ（64 MiB。キャッシュより十分大きい）
COUNT = 1_000_000  # 読む回数


def read_all(buf: bytearray, positions: list[int]) -> tuple[int, float]:
    """buf の positions の位置を順に読み、合計と経過時間（秒）を返す。"""
    total = 0
    start = time.perf_counter()
    for p in positions:
        total += buf[p]
    return total, time.perf_counter() - start


def main() -> None:
    """ストライドを変えて、1 回の読み出しあたりの時間を表示する。"""
    buf = bytearray(SIZE)
    for i in range(0, SIZE, 4096):  # 各ページに書き込んで実際に確保させる
        buf[i] = 1
    print(f"配列 {SIZE // 2**20} MiB を {COUNT:,} 回読む")
    print("ストライド（バイト）  時間（ミリ秒）  1 回あたり（ナノ秒）")
    for stride in (1, 16, 64, 256, 4096 + 64):
        # 配列の末尾を越えたら先頭に戻る位置の列を作る
        positions = [(k * stride) % SIZE for k in range(COUNT)]
        best = min(read_all(buf, positions)[1] for _ in range(3))
        print(f"{stride:>20}{best * 1e3:>16.1f}{best / COUNT * 1e9:>22.1f}")


if __name__ == "__main__":
    main()
