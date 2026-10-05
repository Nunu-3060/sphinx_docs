"""GPU のメモリアクセスの合体とバンクコンフリクトを数えるサンプル。

(1) グローバルメモリ: ワープ内の 32 スレッドがそれぞれ 4 バイトを読むとき、
    触れる 32 バイトのセクタの数をメモリトランザクションの数とみなします
    （近年の NVIDIA GPU の L1/L2 キャッシュのセクタ単位に合わせた単純な
    モデルです）。効率 = 必要なバイト数 / 実際に転送するバイト数。
(2) 共有メモリ: 4 バイト幅のバンクが 32 個あり、ワード番号 % 32 がバンク
    番号になるとします。同じバンクの異なるワードへのアクセスは順番に処理
    され（バンクコンフリクト）、同じワードへのアクセスは 1 回で配られる
    （ブロードキャスト）とします。

実行方法: python gpu_coalescing.py
"""

import random

WARP_SIZE = 32
ELEM = 4  # 1 スレッドが読むバイト数（float 1 個）
SECTOR = 32  # メモリトランザクションの単位（バイト）
NUM_BANKS = 32


def sectors(addrs: list[int]) -> int:
    """アドレスの列が触れる 32 バイトセクタの数を返す。"""
    touched: set[int] = set()
    for a in addrs:
        # 4 バイトの要素がまたぐセクタをすべて数える
        for b in (a, a + ELEM - 1):
            touched.add(b // SECTOR)
    return len(touched)


def bank_passes(word_indices: list[int]) -> int:
    """共有メモリのアクセスに必要な処理の回数（1 ならコンフリクトなし）。"""
    words_in_bank: dict[int, set[int]] = {}
    for w in word_indices:
        words_in_bank.setdefault(w % NUM_BANKS, set()).add(w)
    return max(len(ws) for ws in words_in_bank.values())


def main() -> None:
    rng = random.Random(1)  # 毎回同じ結果になるよう乱数の種を固定する
    tids = range(WARP_SIZE)
    global_cases: list[tuple[str, list[int]]] = [
        ("連続（a[tid]）", [ELEM * t for t in tids]),
        ("連続、4 バイトずれ", [ELEM * t + 4 for t in tids]),
        ("ストライド 2（a[2*tid]）", [ELEM * 2 * t for t in tids]),
        ("ストライド 4（a[4*tid]）", [ELEM * 4 * t for t in tids]),
        ("ストライド 8（a[8*tid]）", [ELEM * 8 * t for t in tids]),
        ("ランダム（1 MiB の範囲）",
         [ELEM * rng.randrange(1 << 18) for _ in tids]),
    ]
    need = WARP_SIZE * ELEM
    print(f"(1) グローバルメモリ（1 ワープで {need} バイトを読む）")
    for label, addrs in global_cases:
        n = sectors(addrs)
        eff = need / (n * SECTOR)
        print(f"  セクタ {n:>2} 個  {n * SECTOR:>5} バイト転送  "
              f"効率 {eff:6.1%}  {label}")

    shared_cases: list[tuple[str, list[int]]] = [
        ("s[tid]", list(tids)),
        ("s[2*tid]", [2 * t for t in tids]),
        ("s[0]（全員同じワード）", [0 for _ in tids]),
        ("tile[tid][0]（32 列）", [32 * t for t in tids]),
        ("tile[tid][0]（33 列）", [33 * t for t in tids]),
    ]
    print()
    print("(2) 共有メモリ（32 バンク、4 バイト幅）")
    for label, words in shared_cases:
        p = bank_passes(words)
        print(f"  処理 {p:>2} 回  コンフリクト {p - 1:>2} 回  {label}")


if __name__ == "__main__":
    main()
