"""第 10 章の数値実験：格子点による数値積分とモンテカルロ積分の比較。

d 次元の単位立方体 [0, 1]^d 上で f(x) = exp(-|x|^2) を積分する。
厳密値は (∫_0^1 exp(-t^2) dt)^d = (sqrt(pi)/2 * erf(1))^d である。

1. 標本点の総数 N を固定し、次元 d を変えたときの誤差を比べる。
   格子点（中点則）では 1 軸あたり n = N^(1/d) 点しか取れない。
2. d = 6 のモンテカルロ積分で、N と誤差の関係（N^(-1/2) に比例）を調べる。

実行方法:
    python ch10_monte_carlo.py
"""

import math

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]

# 乱数の種（結果を再現できるように固定する）
SEED = 0


def integrand(points: FloatArray) -> FloatArray:
    """被積分関数 f(x) = exp(-|x|^2) を、各行が 1 点を表す配列に対して評価する。"""
    result: FloatArray = np.exp(-np.sum(points**2, axis=1))
    return result


def exact_value(d: int) -> float:
    """[0, 1]^d 上の積分の厳密値を返す。"""
    return (math.sqrt(math.pi) / 2.0 * math.erf(1.0)) ** d


def midpoint_rule(d: int, n: int) -> float:
    """各軸を n 等分した格子（小立方体の中心 n^d 点）による中点則の値を返す。"""
    centers = (np.arange(n) + 0.5) / n
    grids = np.meshgrid(*([centers] * d), indexing="ij")
    points = np.stack(grids, axis=-1).reshape(-1, d)
    # 各点の重みは小立方体の体積 1/n^d
    return float(np.mean(integrand(points)))


def monte_carlo(d: int, num_samples: int, rng: np.random.Generator) -> float:
    """[0, 1]^d 上の一様乱数 num_samples 点による推定値を返す。"""
    points = rng.random((num_samples, d))
    return float(np.mean(integrand(points)))


def compare_dimensions(total_points: int, dims: list[int]) -> list[tuple[int, int, float, float]]:
    """点の総数を total_points に固定し、各次元 d での相対誤差を (d, n, 格子, MC) の形で返す。"""
    rng = np.random.default_rng(SEED)
    rows = []
    for d in dims:
        n = round(total_points ** (1.0 / d))
        exact = exact_value(d)
        grid_error = abs(midpoint_rule(d, n) - exact) / exact
        mc_error = abs(monte_carlo(d, total_points, rng) - exact) / exact
        rows.append((d, n, grid_error, mc_error))
    return rows


def rms_error(d: int, num_samples: int, num_trials: int, rng: np.random.Generator) -> float:
    """モンテカルロ積分を num_trials 回繰り返したときの相対誤差の二乗平均平方根を返す。"""
    exact = exact_value(d)
    errors = [(monte_carlo(d, num_samples, rng) - exact) / exact for _ in range(num_trials)]
    return math.sqrt(sum(e * e for e in errors) / num_trials)


def main() -> None:
    """2 種類の実験を行い、結果を表として表示する。"""
    total_points = 4096
    print(f"[1] 点の総数 N = {total_points} を固定したときの相対誤差")
    print("d    n/軸   格子点（中点則）  モンテカルロ")
    for d, n, grid_error, mc_error in compare_dimensions(total_points, [1, 2, 3, 4, 6, 12]):
        print(f"{d:<4d} {n:<6d} {grid_error:<17.2e} {mc_error:.2e}")
    print()

    d = 6
    num_trials = 50
    rng = np.random.default_rng(SEED)
    print(f"[2] d = {d} のモンテカルロ積分（{num_trials} 回の試行の二乗平均平方根）")
    print("N          相対誤差   相対誤差 * sqrt(N)")
    for num_samples in [10**2, 10**3, 10**4, 10**5]:
        error = rms_error(d, num_samples, num_trials, rng)
        print(f"{num_samples:<10d} {error:<10.2e} {error * math.sqrt(num_samples):.3f}")


if __name__ == "__main__":
    main()
