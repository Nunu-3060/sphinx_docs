"""ベクトルの内積、外積、三重積を NumPy で計算する.

使い方: python ch02_vector_ops.py
"""

import numpy as np
from numpy.typing import NDArray

import vc_plot


def angle_deg(a: NDArray[np.float64], b: NDArray[np.float64]) -> float:
    """2 つのベクトルのなす角を度で返す."""
    cos = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(np.degrees(np.arccos(np.clip(cos, -1.0, 1.0))))


def projection(a: NDArray[np.float64], b: NDArray[np.float64]) -> NDArray[np.float64]:
    """a の b 方向への正射影ベクトルを返す."""
    return (a @ b) / (b @ b) * b


def report() -> None:
    """内積、なす角、正射影、外積、三重積を計算して表示する."""
    a = np.array([1.0, 2.0, 2.0])
    b = np.array([3.0, 0.0, 4.0])
    c = np.array([0.0, 1.0, 1.0])
    print(f"a = {a}, b = {b}, c = {c}")
    print(f"|a| = {np.linalg.norm(a):.6f}, |b| = {np.linalg.norm(b):.6f}")
    print(f"a・b = {a @ b:.6f}")
    print(f"a と b のなす角 = {angle_deg(a, b):.6f} 度")
    print(f"a の b 方向への正射影 = {projection(a, b)}")

    axb = np.cross(a, b)
    print(f"a×b = {axb}")
    print(f"(a×b)・a = {axb @ a:.6f}, (a×b)・b = {axb @ b:.6f}")
    print(f"|a×b| = {np.linalg.norm(axb):.6f}（a と b が作る平行四辺形の面積）")
    print(f"b×a = {np.cross(b, a)}")

    triple = a @ np.cross(b, c)
    det = np.linalg.det(np.array([a, b, c]))
    print(f"a・(b×c) = {triple:.6f}, det[a; b; c] = {det:.6f}")
    left = np.cross(a, np.cross(b, c))
    right = (a @ c) * b - (a @ b) * c
    print(f"a×(b×c) = {left}, (a・c)b - (a・b)c = {right}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
