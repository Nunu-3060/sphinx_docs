"""3 次元の距離関数（SDF）と、その組み合わせ方。

点の座標は、最後の軸が (x, y, z) の 3 成分を持つ配列 p (..., 3) で表す。
どの関数も、p の各点について、形の表面までの符号付き距離（内側で負、外側で正）を
返す。式は Inigo Quilez の解説にある GLSL の関数を NumPy に書き直したものである。
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from common import FloatArray

# 点の配列 (..., 3) を受け取り、距離の配列 (...) を返す関数の型
Sdf = Callable[[FloatArray], FloatArray]


def length(v: FloatArray) -> FloatArray:
    """ベクトルの長さ（最後の軸について）。"""
    result: FloatArray = np.sqrt(np.sum(v * v, axis=-1))
    return result


def sd_sphere(p: FloatArray, radius: float) -> FloatArray:
    """原点を中心とする半径 radius の球。"""
    return length(p) - radius


def sd_box(p: FloatArray, half_size: tuple[float, float, float]) -> FloatArray:
    """原点を中心とし、各軸の半分の大きさが half_size の直方体。"""
    q = np.abs(p) - np.asarray(half_size)
    outside = length(np.maximum(q, 0.0))  # 外側の点: 最も近い面・辺・角までの距離
    inside = np.minimum(np.max(q, axis=-1), 0.0)  # 内側の点: 最も近い面までの距離（負）
    return outside + inside


def sd_torus(p: FloatArray, major: float, minor: float) -> FloatArray:
    """z 軸を中心軸とし、xy 平面に置いたトーラス（ドーナツ）。major は輪の半径、minor は管の半径。"""
    ring = np.hypot(p[..., 0], p[..., 1]) - major
    return np.hypot(ring, p[..., 2]) - minor


def sd_plane(p: FloatArray, height: float = 0.0) -> FloatArray:
    """高さ height の水平な平面（z が height より下が内側）。"""
    return p[..., 2] - height


def op_union(a: FloatArray, b: FloatArray) -> FloatArray:
    """和集合: どちらかの内側なら内側。"""
    return np.minimum(a, b)


def op_intersection(a: FloatArray, b: FloatArray) -> FloatArray:
    """共通部分: 両方の内側だけが内側。"""
    return np.maximum(a, b)


def op_subtraction(a: FloatArray, b: FloatArray) -> FloatArray:
    """差集合: a の内側から b の内側を取り除く。"""
    return np.maximum(a, -b)


def smooth_min(a: FloatArray, b: FloatArray, k: float) -> FloatArray:
    """多項式によるスムーズな最小値（smooth min）。

    a と b の差が k より大きい所では min(a, b) と一致し、差が k 未満の所でだけ
    min より小さい値を返して、2 つの形の継ぎ目を丸く埋める。k が丸みの幅になる。
    """
    if k <= 0.0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def smooth_max(a: FloatArray, b: FloatArray, k: float) -> FloatArray:
    """スムーズな最大値。共通部分・差集合の角を丸めるのに使う。"""
    return -smooth_min(-a, -b, k)


def gradient(sdf: Sdf, p: FloatArray, eps: float = 1e-3) -> FloatArray:
    """中心差分で距離関数の勾配を求め、正規化して返す（表面の法線になる）。"""
    offsets = np.eye(3) * eps
    components = [sdf(p + offsets[axis]) - sdf(p - offsets[axis]) for axis in range(3)]
    g = np.stack(components, axis=-1)
    result: FloatArray = g / np.maximum(length(g), 1e-12)[..., None]
    return result


def grid3(
    low: tuple[float, float, float], high: tuple[float, float, float], counts: tuple[int, int, int]
) -> FloatArray:
    """直方体 low〜high を counts 個ずつの格子点に分けた座標 (nx, ny, nz, 3) を返す。"""
    axes = [np.linspace(low[i], high[i], counts[i]) for i in range(3)]
    x, y, z = np.meshgrid(*axes, indexing="ij")
    return np.stack([x, y, z], axis=-1)
