"""本書のサンプルで共通に使う、双曲平面の計算の関数（曲率 K = -1）.

点の表し方
    上半平面モデル、ポアンカレ円板モデル、クラインモデルの点は複素数 (complex) で表す。
    双曲面モデルの点は、成分 (x0, x1, x2) を持つ長さ 3 の NumPy 配列で表す。

距離
    half_plane_distance()   上半平面モデルの 2 点間の距離
    disk_distance()         ポアンカレ円板モデルの 2 点間の距離
    klein_distance()        クラインモデルの 2 点間の距離
    hyperboloid_distance()  双曲面モデルの 2 点間の距離

モデル間の変換
    half_plane_to_disk(), disk_to_half_plane()
    disk_to_klein(), klein_to_disk()
    disk_to_hyperboloid(), hyperboloid_to_disk()

円板モデルでの作図
    disk_point()      原点からの距離と向きで点を指定する
    disk_translate()  原点を点 a に移す等長変換
    disk_geodesic()   2 点を結ぶ測地線分の上の点列
    disk_line()       2 点を通る測地線全体の点列
    disk_reflect()    2 点を通る測地線に関する鏡映
    disk_angle()      測地線どうしのなす角
"""

import cmath
import math

import numpy as np
from numpy.typing import NDArray

Point3 = NDArray[np.float64]


# ---------------------------------------------------------------- 距離


def half_plane_distance(z: complex, w: complex) -> float:
    """上半平面モデルの距離. cosh d = 1 + |z - w|^2 / (2 Im z Im w)."""
    return math.acosh(1.0 + abs(z - w) ** 2 / (2.0 * z.imag * w.imag))


def disk_distance(z: complex, w: complex) -> float:
    """ポアンカレ円板モデルの距離. d = 2 artanh |(z - w) / (1 - conj(w) z)|."""
    return 2.0 * math.atanh(abs((z - w) / (1.0 - w.conjugate() * z)))


def klein_distance(k: complex, m: complex) -> float:
    """クラインモデルの距離. cosh d = (1 - k・m) / sqrt((1 - |k|^2)(1 - |m|^2))."""
    dot = k.real * m.real + k.imag * m.imag
    return math.acosh((1.0 - dot) / math.sqrt((1.0 - abs(k) ** 2) * (1.0 - abs(m) ** 2)))


def minkowski(x: Point3, y: Point3) -> float:
    """ミンコフスキーの双線形形式 B(x, y) = x0 y0 - x1 y1 - x2 y2."""
    return float(x[0] * y[0] - x[1] * y[1] - x[2] * y[2])


def hyperboloid_distance(x: Point3, y: Point3) -> float:
    """双曲面モデルの距離. cosh d = B(x, y)."""
    return math.acosh(max(minkowski(x, y), 1.0))  # 丸め誤差で 1 をわずかに下回る場合に備える


# ---------------------------------------------------------------- モデル間の変換


def half_plane_to_disk(z: complex) -> complex:
    """ケーリー変換 w = (z - i) / (z + i). 上半平面の点 i が円板の原点に移る."""
    return (z - 1j) / (z + 1j)


def disk_to_half_plane(w: complex) -> complex:
    """ケーリー変換の逆 z = i (1 + w) / (1 - w)."""
    return 1j * (1.0 + w) / (1.0 - w)


def disk_to_klein(z: complex) -> complex:
    """円板モデルからクラインモデルへ. k = 2 z / (1 + |z|^2)."""
    return 2.0 * z / (1.0 + abs(z) ** 2)


def klein_to_disk(k: complex) -> complex:
    """クラインモデルから円板モデルへ. z = k / (1 + sqrt(1 - |k|^2))."""
    return k / (1.0 + math.sqrt(1.0 - abs(k) ** 2))


def disk_to_hyperboloid(z: complex) -> Point3:
    """円板モデルから双曲面モデルへ（立体射影の逆）."""
    s = 1.0 - abs(z) ** 2
    return np.array([(1.0 + abs(z) ** 2) / s, 2.0 * z.real / s, 2.0 * z.imag / s])


def hyperboloid_to_disk(x: Point3) -> complex:
    """双曲面モデルから円板モデルへ. 点 (-1, 0, 0) からの立体射影 z = (x1 + i x2) / (1 + x0)."""
    return complex(x[1], x[2]) / (1.0 + float(x[0]))


# ---------------------------------------------------------------- 円板モデルでの作図


def disk_point(r: float, theta: float) -> complex:
    """原点からの双曲的な距離が r、偏角が theta の点. 円板上では半径 tanh(r / 2) の位置にある."""
    return math.tanh(r / 2.0) * cmath.exp(1j * theta)


def disk_translate(a: complex, z: complex) -> complex:
    """原点を点 a に移す円板の等長変換 z -> (z + a) / (1 + conj(a) z)."""
    return (z + a) / (1.0 + a.conjugate() * z)


def disk_geodesic(a: complex, b: complex, n: int = 64) -> NDArray[np.complex128]:
    """円板モデルで点 a と点 b を結ぶ測地線分の上に、双曲的な長さで等間隔に並ぶ n 個の点を返す.

    a を原点に移すと、測地線分は原点からの線分になる。その線分の上に点を取り、
    a を原点に移した変換の逆変換で元に戻す。
    """
    w = disk_translate(-a, b)  # a を原点に移したときの b の位置
    length = disk_distance(0j, w)
    direction = w / abs(w) if abs(w) > 0.0 else 1.0 + 0j
    points = np.tanh(np.linspace(0.0, length, n) / 2.0) * direction
    return (points + a) / (1.0 + a.conjugate() * points)


def disk_line(a: complex, b: complex, n: int = 200, extent: float = 12.0) -> NDArray[np.complex128]:
    """円板モデルで点 a と点 b を通る測地線全体を、a から両側に距離 extent までの n 個の点で近似して返す."""
    w = disk_translate(-a, b)
    direction = w / abs(w)
    points = np.tanh(np.linspace(-extent, extent, n) / 2.0) * direction
    return (points + a) / (1.0 + a.conjugate() * points)


def disk_reflect(z: complex, p: complex, q: complex) -> complex:
    """円板モデルで、点 p と点 q を通る測地線に関する点 z の鏡映（対称な点）."""
    w = disk_translate(-p, q)  # p を原点に移すと、測地線は原点を通る直線になる
    u = w / abs(w)
    moved = disk_translate(-p, z)
    reflected = u * u * moved.conjugate()  # 原点を通る直線に関する鏡映
    return disk_translate(p, reflected)


def disk_angle(vertex: complex, p: complex, q: complex) -> float:
    """円板モデルで、vertex から p へ向かう測地線と vertex から q へ向かう測地線のなす角（0 から pi）.

    円板モデルは角度を正しく表すので、vertex を原点に移してから直線どうしの角度を測ればよい。
    """
    u = disk_translate(-vertex, p)
    v = disk_translate(-vertex, q)
    return abs(cmath.phase(v / u))
