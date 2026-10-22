"""ベクトルの演算: 和、スカラー倍、内積、ノルム、なす角、正射影、外積.

使い方: python ch02_vector_ops.py
"""

import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]


def angle_between(u: Vector, v: Vector) -> float:
    """2 つのベクトルのなす角を度で返す."""
    cos_theta = (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))
    # 丸め誤差で cos が [-1, 1] をわずかに超えると arccos が nan になるので、範囲内に収める
    return float(np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0))))


def project(u: Vector, v: Vector) -> Vector:
    """u の v 方向への正射影を返す."""
    return (u @ v) / (v @ v) * v


def report() -> None:
    """2 次元と 3 次元のベクトルの演算の結果を表示する."""
    u = np.array([3.0, 1.0])
    v = np.array([1.0, 2.0])
    print("u + v =", u + v)
    print("2 * u =", 2 * u)
    print("u @ v =", u @ v)  # 内積（np.dot(u, v) と同じ）
    print(f"|u| = {np.linalg.norm(u):.4f}")
    print(f"|v| = {np.linalg.norm(v):.4f}")
    print(f"なす角 = {angle_between(u, v):.1f} 度")
    p = project(u, v)
    print("u の v 方向への正射影 p =", p)
    print("(u - p) @ v =", (u - p) @ v)  # 残りの成分は v と直交する

    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    c = np.cross(a, b)  # 外積
    print("a x b =", c)
    print("(a x b) @ a =", c @ a, " (a x b) @ b =", c @ b)
    print("b x a =", np.cross(b, a))  # 順序を入れ替えると向きが逆になる


def main() -> None:
    report()


if __name__ == "__main__":
    main()
