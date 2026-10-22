"""特殊相対論の速度の空間が双曲空間であることを数値で確かめる（光速 c = 1 とする）.

速度 v（|v| < 1）に 4 元速度 u = gamma (1, v) を対応させると、u は双曲面 x0^2 - x1^2 - x2^2 = 1 の上にある。
2 つの速度の 4 元速度の双曲的な距離は、一方から見た他方の速さのラピディティに等しい。

使い方: python ch09_relativity.py
"""

import math

import numpy as np
from numpy.typing import NDArray

import hg

Vector = NDArray[np.float64]


def four_velocity(v: Vector) -> Vector:
    """速度 v（2 次元）の 4 元速度 gamma (1, v)（ここでは空間 2 次元なので成分は 3 つ）."""
    gamma = 1.0 / math.sqrt(1.0 - float(v @ v))
    return gamma * np.array([1.0, v[0], v[1]])


def boost(v: Vector) -> NDArray[np.float64]:
    """速度 v で動く観測者の座標系に移るローレンツ変換（ブースト）の 3 行 3 列の行列."""
    speed2 = float(v @ v)
    gamma = 1.0 / math.sqrt(1.0 - speed2)
    matrix = np.eye(3)
    matrix[0, 0] = gamma
    matrix[0, 1:] = matrix[1:, 0] = -gamma * v
    matrix[1:, 1:] += (gamma - 1.0) * np.outer(v, v) / speed2
    return matrix


def relative_speed(v: Vector, w: Vector) -> float:
    """速度 v で動く観測者から見た、速度 w で動く物体の速さ.

    w の 4 元速度をブーストで観測者の座標系に移し、空間成分を時間成分で割って速度を求める。
    """
    u = boost(v) @ four_velocity(w)
    return float(np.linalg.norm(u[1:]) / u[0])


def report() -> None:
    """一直線上の速度の合成と、向きの異なる 2 つの速度について確かめる."""
    print("一直線上の速度の合成: ラピディティ phi = artanh v は足し算になる")
    v1, v2 = 0.6, 0.7
    composed = (v1 + v2) / (1.0 + v1 * v2)
    print(f"  (v1 + v2) / (1 + v1 v2)        = {composed:.10f}")
    print(f"  tanh(artanh v1 + artanh v2)    = {math.tanh(math.atanh(v1) + math.atanh(v2)):.10f}")

    print("向きの異なる 2 つの速度")
    v = np.array([0.6, 0.0])
    w = np.array([0.3, 0.7])
    speed = relative_speed(v, w)
    print(f"  相対速度の大きさ                = {speed:.10f}")
    print(f"  そのラピディティ artanh         = {math.atanh(speed):.10f}")
    print(f"  4 元速度の双曲的な距離          = {hg.hyperboloid_distance(four_velocity(v), four_velocity(w)):.10f}")
    print(f"  速度をクラインモデルの点とみた距離 = {hg.klein_distance(complex(*v), complex(*w)):.10f}")
    x, y = four_velocity(np.array([0.1, -0.5])), four_velocity(np.array([-0.4, 0.2]))
    print("ブーストは双曲面の等長変換である")
    print(f"  変換前の距離 {hg.hyperboloid_distance(x, y):.10f}")
    print(f"  変換後の距離 {hg.hyperboloid_distance(boost(v) @ x, boost(v) @ y):.10f}")


if __name__ == "__main__":
    report()
