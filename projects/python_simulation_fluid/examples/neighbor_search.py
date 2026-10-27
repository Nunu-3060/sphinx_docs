"""近傍探索: 総当たり法とセル分割法の比較。

距離が radius 未満の粒子の組をすべて求める処理を、総当たり法と
セル分割法(セルリスト法)の 2 通りで実装し、結果が一致することと
計算時間の違いを確かめる。セル分割法の関数は SPH のサンプル
(sph_dam_break.py)からも利用する。

実行方法::

    python neighbor_search.py
"""
import time

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int64]


def brute_force_pairs(pos: FloatArray, radius: float) -> tuple[IntArray, IntArray]:
    """すべての組の距離を計算し、距離が radius 未満の組 (i, j) (i < j) を返す。"""
    i, j = np.triu_indices(len(pos), k=1)
    dist2 = np.sum((pos[j] - pos[i]) ** 2, axis=1)
    close = dist2 < radius**2
    return i[close].astype(np.int64), j[close].astype(np.int64)


def cell_list_pairs(pos: FloatArray, radius: float) -> tuple[IntArray, IntArray]:
    """セル分割法で、距離が radius 未満の組 (i, j) (i < j) を返す。

    一辺 radius の正方形のセルに空間を分割すると、距離 radius 未満の相手は
    自分のセルとその周囲 8 セルの中にしか存在しない。そこで、各粒子について
    9 セル分の粒子だけを距離計算の候補にする。
    """
    n = len(pos)
    # 1. 各粒子が属するセルの番号を求める
    cell = np.floor((pos - pos.min(axis=0)) / radius).astype(np.int64)
    n_cx, n_cy = (cell.max(axis=0) + 1).tolist()
    cell_id = cell[:, 0] * n_cy + cell[:, 1]

    # 2. 粒子をセル番号順に並べ、各セルの粒子が並び替え後の配列のどこにあるかを求める
    order = np.argsort(cell_id, kind="stable")
    counts = np.bincount(cell_id, minlength=n_cx * n_cy)  # セルごとの粒子数
    starts = np.cumsum(counts) - counts  # セルごとの先頭位置

    # 3. 周囲 9 セルのそれぞれについて候補の組を作り、距離で絞り込む
    found_i: list[IntArray] = []
    found_j: list[IntArray] = []
    particles = np.arange(n)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            cx = cell[:, 0] + dx
            cy = cell[:, 1] + dy
            inside = (cx >= 0) & (cx < n_cx) & (cy >= 0) & (cy < n_cy)
            nbr = cx[inside] * n_cy + cy[inside]  # 隣のセルの番号
            c = counts[nbr]
            # 粒子 i を、隣のセルにいる粒子の数だけ繰り返す
            cand_i = np.repeat(particles[inside], c)
            # 隣のセルにいる粒子を、並び替え後の配列から順に取り出す
            offset = np.arange(c.sum()) - np.repeat(np.cumsum(c) - c, c)
            cand_j = order[np.repeat(starts[nbr], c) + offset]
            keep = cand_i < cand_j  # 同じ組を 2 回数えないようにする
            cand_i, cand_j = cand_i[keep], cand_j[keep]
            close = np.sum((pos[cand_j] - pos[cand_i]) ** 2, axis=1) < radius**2
            found_i.append(cand_i[close])
            found_j.append(cand_j[close])
    return np.concatenate(found_i), np.concatenate(found_j)


def sorted_pairs(i: IntArray, j: IntArray) -> IntArray:
    """比較しやすいように、組の一覧を (i, j) の辞書順に並べた配列にして返す。"""
    order = np.lexsort((j, i))
    return np.stack([i[order], j[order]], axis=1)


def random_positions(n: int, radius: float, seed: int = 0) -> FloatArray:
    """1 個の粒子の近傍に平均 10 個程度の粒子があるように、一様乱数で配置する。"""
    density = 10.0 / (np.pi * radius**2)
    side = np.sqrt(n / density)
    return np.random.default_rng(seed).uniform(0.0, side, (n, 2))


def measure(n: int, radius: float = 1.0, repeat: int = 3) -> tuple[float, float]:
    """n 個の粒子について、総当たり法とセル分割法の計算時間 [s] を返す。"""
    pos = random_positions(n, radius)
    times = []
    for search in (brute_force_pairs, cell_list_pairs):
        start = time.perf_counter()
        for _ in range(repeat):
            search(pos, radius)
        times.append((time.perf_counter() - start) / repeat)
    return times[0], times[1]


def main() -> None:
    pos = random_positions(2000, 1.0)
    a = sorted_pairs(*brute_force_pairs(pos, 1.0))
    b = sorted_pairs(*cell_list_pairs(pos, 1.0))
    print(f"見つかった組の数: 総当たり法 {len(a)}, セル分割法 {len(b)}, 一致: {np.array_equal(a, b)}")

    sizes = [250, 500, 1000, 2000, 4000]
    results = [measure(n) for n in sizes]
    for n, (t_brute, t_cell) in zip(sizes, results):
        print(f"N = {n:>5}: 総当たり法 {t_brute * 1e3:8.2f} ms, セル分割法 {t_cell * 1e3:6.2f} ms")

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(sizes, [r[0] * 1e3 for r in results], "o-", label="総当たり法")
    ax.loglog(sizes, [r[1] * 1e3 for r in results], "s-", label="セル分割法")
    ax.set_xlabel("粒子数 N")
    ax.set_ylabel("計算時間 [ms]")
    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
