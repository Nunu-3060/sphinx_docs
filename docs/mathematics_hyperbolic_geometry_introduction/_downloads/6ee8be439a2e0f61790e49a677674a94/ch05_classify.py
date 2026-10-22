"""SL(2, R) の行列が表すメビウス変換を、トレースで分類し、距離を保つことを確かめる.

使い方: python ch05_classify.py
"""

import math

import numpy as np
from numpy.typing import NDArray

import hg

Matrix = NDArray[np.float64]


def mobius(m: Matrix, z: complex) -> complex:
    """行列 m = [[a, b], [c, d]] が表すメビウス変換 (a z + b) / (c z + d)."""
    return complex((m[0, 0] * z + m[0, 1]) / (m[1, 0] * z + m[1, 1]))


def classify(m: Matrix) -> str:
    """トレースの絶対値と 2 の大小で、等長変換の型を判定する（m は恒等変換でないとする）."""
    trace = abs(float(np.trace(m)))
    if math.isclose(trace, 2.0):
        return "放物型"
    return "楕円型" if trace < 2.0 else "双曲型"


def report() -> None:
    """いくつかの行列について、型と、距離が保たれていることを表示する."""
    c, s = math.cos(0.5), math.sin(0.5)
    matrices = {
        "[[cos 0.5, sin 0.5], [-sin 0.5, cos 0.5]]": np.array([[c, s], [-s, c]]),
        "[[1, 1], [0, 1]]": np.array([[1.0, 1.0], [0.0, 1.0]]),
        "[[2, 0], [0, 1/2]]": np.array([[2.0, 0.0], [0.0, 0.5]]),
        "[[2, 1], [1, 1]]": np.array([[2.0, 1.0], [1.0, 1.0]]),
    }
    rng = np.random.default_rng(1)
    for name, m in matrices.items():
        print(f"{name}: det = {np.linalg.det(m):.3f}, |tr| = {abs(np.trace(m)):.4f}, {classify(m)}")
        worst = 0.0
        for _ in range(1000):  # ランダムな 2 点の距離と、変換後の距離の差の最大値
            z = complex(rng.uniform(-3.0, 3.0), rng.uniform(0.1, 3.0))
            w = complex(rng.uniform(-3.0, 3.0), rng.uniform(0.1, 3.0))
            diff = hg.half_plane_distance(mobius(m, z), mobius(m, w)) - hg.half_plane_distance(z, w)
            worst = max(worst, abs(diff))
        print(f"  距離の差の最大値 {worst:.2e}")

    # 双曲型の変換 z -> 4z は、軸（虚軸）上の点を距離 2 arcosh(|tr| / 2) だけ動かす
    m = matrices["[[2, 0], [0, 1/2]]"]
    print(f"2 arcosh(|tr| / 2) = {2.0 * math.acosh(abs(np.trace(m)) / 2.0):.6f}")
    print(f"d(i, 4i)           = {hg.half_plane_distance(1j, mobius(m, 1j)):.6f}")
    print(f"d(1 + i, 4 + 4i)   = {hg.half_plane_distance(1.0 + 1j, mobius(m, 1.0 + 1j)):.6f}")


if __name__ == "__main__":
    report()
