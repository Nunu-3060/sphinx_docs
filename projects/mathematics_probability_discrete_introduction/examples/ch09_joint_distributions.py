"""第 9 章 同時分布と確率変数の和のサンプルコード。

同時分布を「(x, y) → 確率」の dict で表し、周辺分布・共分散・相関係数を求める。
また、独立な確率変数の和の分布を numpy.convolve による畳み込みで計算する。
"""

import math
from collections.abc import Callable
from fractions import Fraction
from itertools import product

import numpy as np
import numpy.typing as npt

# 同時分布（(x, y) → 確率）
JointDistribution = dict[tuple[int, int], Fraction]


def joint_from_dice(x_of: Callable[[int, int], int], y_of: Callable[[int, int], int]) -> JointDistribution:
    """2 個のサイコロの目 (a, b) から定めた確率変数 X, Y の同時分布を作る。"""
    joint: JointDistribution = {}
    for a, b in product(range(1, 7), repeat=2):
        key = (x_of(a, b), y_of(a, b))
        joint[key] = joint.get(key, Fraction(0)) + Fraction(1, 36)
    return joint


def marginal(joint: JointDistribution, axis: int) -> dict[int, Fraction]:
    """周辺分布を返す。axis=0 なら X の分布、axis=1 なら Y の分布。"""
    result: dict[int, Fraction] = {}
    for key, p in joint.items():
        result[key[axis]] = result.get(key[axis], Fraction(0)) + p
    return dict(sorted(result.items()))


def is_independent(joint: JointDistribution) -> bool:
    """すべての (x, y) で P(X=x, Y=y) = P(X=x) P(Y=y) が成り立つかを返す。"""
    px, py = marginal(joint, 0), marginal(joint, 1)
    return all(joint.get((x, y), Fraction(0)) == px[x] * py[y] for x in px for y in py)


def covariance(joint: JointDistribution) -> Fraction:
    """共分散 Cov[X, Y] = E[XY] - E[X]E[Y] を返す。"""
    ex = sum((x * p for (x, _), p in joint.items()), Fraction(0))
    ey = sum((y * p for (_, y), p in joint.items()), Fraction(0))
    exy = sum((x * y * p for (x, y), p in joint.items()), Fraction(0))
    return exy - ex * ey


def variance_of(dist: dict[int, Fraction]) -> Fraction:
    """1 変数の分布の分散を返す。"""
    mean = sum((x * p for x, p in dist.items()), Fraction(0))
    return sum(((x - mean) ** 2 * p for x, p in dist.items()), Fraction(0))


def correlation(joint: JointDistribution) -> float:
    """相関係数 ρ = Cov[X, Y] / (σ_X σ_Y) を返す。"""
    vx = variance_of(marginal(joint, 0))
    vy = variance_of(marginal(joint, 1))
    return float(covariance(joint)) / math.sqrt(float(vx * vy))


def sum_distribution(pmf: npt.NDArray[np.float64], n: int) -> npt.NDArray[np.float64]:
    """値 0, 1, 2, ... をとる確率変数 n 個の独立和の分布を畳み込みで求める。"""
    result = np.array([1.0])
    for _ in range(n):
        result = np.convolve(result, pmf)
    return result


def main() -> None:
    print("--- X = 1 個目の目, S = 2 個の和 ---")
    joint = joint_from_dice(lambda a, b: a, lambda a, b: a + b)
    print(f"Cov[X, S] = {covariance(joint)}, ρ = {correlation(joint):.4f}, 1/√2 = {1 / math.sqrt(2):.4f}")
    print(f"独立か: {is_independent(joint)}")

    print("--- X = 1 個目の目, Y = 2 個目の目 ---")
    joint_xy = joint_from_dice(lambda a, b: a, lambda a, b: b)
    print(f"Cov[X, Y] = {covariance(joint_xy)}, 独立か: {is_independent(joint_xy)}")

    print("--- 無相関だが独立でない例 ---")
    # X は -1, 0, 1 を等確率でとり、Y = X^2 とする
    third = Fraction(1, 3)
    joint_sq: JointDistribution = {(-1, 1): third, (0, 0): third, (1, 1): third}
    print(f"Cov[X, Y] = {covariance(joint_sq)}, 独立か: {is_independent(joint_sq)}")

    print("--- サイコロ n 個の和の分布（畳み込み） ---")
    die = np.array([0.0] + [1 / 6] * 6)  # 添字 k が目 k の確率
    for n in [1, 2, 3]:
        dist = sum_distribution(die, n)
        support = np.nonzero(dist > 0)[0]
        mean = float(np.dot(np.arange(len(dist)), dist))
        print(f"n={n}: 値の範囲 {support[0]}..{support[-1]}, 最頻値 {int(np.argmax(dist))}, "
              f"期待値 {mean:.4f}, 総和 {dist.sum():.4f}")
    two = sum_distribution(die, 2)
    print("2 個の和の確率 x 36:", [round(float(v) * 36) for v in two[2:]])


if __name__ == "__main__":
    main()
