"""第 11 章 マルコフ連鎖入門のサンプルコード。

天気のマルコフ連鎖について遷移行列のべき乗と定常分布を求め、
ギャンブラーの破産問題を理論値とシミュレーションで比較する。
"""

import numpy as np
import numpy.typing as npt

STATES = ["晴れ", "曇り", "雨"]

# 遷移行列: P[i, j] は状態 i の翌日に状態 j になる確率（各行の和は 1）
P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.4, 0.4],
])


def distribution_after(p0: npt.NDArray[np.float64], n: int) -> npt.NDArray[np.float64]:
    """初期分布 p0 から n ステップ後の分布 p0 P^n を返す。"""
    result: npt.NDArray[np.float64] = p0 @ np.linalg.matrix_power(P, n)
    return result


def stationary_distribution(p: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """π P = π, Σ π_i = 1 を連立一次方程式として解き、定常分布 π を返す。"""
    k = p.shape[0]
    # (P^T - I) π^T = 0 の 1 本を Σ π_i = 1 で置き換える
    a = p.T - np.eye(k)
    a[-1, :] = 1.0
    b = np.zeros(k)
    b[-1] = 1.0
    result: npt.NDArray[np.float64] = np.linalg.solve(a, b)
    return result


def simulate_chain(start: int, steps: int, rng: np.random.Generator) -> npt.NDArray[np.int64]:
    """マルコフ連鎖を steps ステップ動かし、各状態に滞在した回数を返す。"""
    counts = np.zeros(len(STATES), dtype=np.int64)
    state = start
    for _ in range(steps):
        state = int(rng.choice(len(STATES), p=P[state]))
        counts[state] += 1
    return counts


def ruin_win_probability(i: int, target: int, p: float) -> float:
    """所持金 i から 1 ずつ賭けて、0 になる前に target に到達する確率の理論値を返す。"""
    if p == 0.5:
        return i / target
    r = (1 - p) / p
    return float((1 - r ** i) / (1 - r ** target))


def ruin_simulation(i: int, target: int, p: float, trials: int, rng: np.random.Generator) -> float:
    """ギャンブラーの破産問題をシミュレーションし、target に到達した割合を返す。"""
    wins = 0
    for _ in range(trials):
        money = i
        while 0 < money < target:
            money += 1 if rng.random() < p else -1
        wins += money == target
    return wins / trials


def main() -> None:
    rng = np.random.default_rng(2026)
    np.set_printoptions(precision=4, suppress=True)

    print("--- 晴れから始めたときの n 日後の分布 ---")
    p0 = np.array([1.0, 0.0, 0.0])
    for n in [1, 2, 5, 10, 20]:
        print(f"n={n:>2}: {distribution_after(p0, n)}")

    print("--- 雨から始めたときの n 日後の分布 ---")
    p0 = np.array([0.0, 0.0, 1.0])
    for n in [1, 2, 5, 10, 20]:
        print(f"n={n:>2}: {distribution_after(p0, n)}")

    print("--- 定常分布 ---")
    pi = stationary_distribution(P)
    print(f"π = {pi}, π P = {pi @ P}")
    counts = simulate_chain(0, 100000, rng)
    print(f"100000 日のシミュレーションでの滞在割合: {counts / counts.sum()}")

    print("--- ギャンブラーの破産問題 (所持金 10, 目標 20) ---")
    for p in [0.5, 0.49, 0.45]:
        theory = ruin_win_probability(10, 20, p)
        sim = ruin_simulation(10, 20, p, 5000, rng)
        print(f"p={p:.2f}: 目標到達確率 理論値={theory:.4f}  シミュレーション={sim:.4f}")


if __name__ == "__main__":
    main()
