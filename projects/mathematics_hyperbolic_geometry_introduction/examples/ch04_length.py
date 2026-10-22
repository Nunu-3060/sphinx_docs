"""上半平面モデルで、曲線の長さを計量 ds = |dz| / y の数値積分で求め、距離の公式と比べる.

使い方: python ch04_length.py
"""

import math

import numpy as np
from numpy.typing import ArrayLike

import hg


def curve_length(points: ArrayLike) -> float:
    """上半平面の折れ線 points の双曲的な長さ. 各区間の |dz| / y を足し合わせる."""
    path = np.asarray(points, dtype=np.complex128)
    dz = np.abs(np.diff(path))
    y_mid = (path[1:].imag + path[:-1].imag) / 2.0
    return float(np.sum(dz / y_mid))


def report() -> None:
    """3 本の曲線の長さと、端点間の距離を表示する."""
    n = 200_001

    # 1. i から 2i への垂直な線分（測地線）
    vertical = 1j * np.linspace(1.0, 2.0, n)
    print("i から 2i への垂直な線分")
    print(f"  数値積分による長さ {curve_length(vertical):.9f}")
    print(f"  ln 2               {math.log(2.0):.9f}")
    print(f"  距離の公式         {hg.half_plane_distance(1j, 2j):.9f}")

    # 2. -1 + i から 1 + i への水平な線分（測地線ではない）
    z, w = -1.0 + 1j, 1.0 + 1j
    horizontal = np.linspace(-1.0, 1.0, n) + 1j
    print("-1 + i から 1 + i への水平な線分")
    print(f"  数値積分による長さ {curve_length(horizontal):.9f}")

    # 3. 同じ 2 点を結ぶ、中心 0、半径 sqrt(2) の半円の弧（測地線）
    theta = np.linspace(3.0 * math.pi / 4.0, math.pi / 4.0, n)
    arc = math.sqrt(2.0) * np.exp(1j * theta)
    print("-1 + i から 1 + i への半円の弧")
    print(f"  数値積分による長さ {curve_length(arc):.9f}")
    print(f"  距離の公式         {hg.half_plane_distance(z, w):.9f}")


if __name__ == "__main__":
    report()
