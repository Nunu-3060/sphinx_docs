"""円板モデルの三角形で、双曲余弦定理、正弦定理、ガウス・ボネの定理を数値で確かめる.

使い方: python ch06_trig.py
"""

import math

import numpy as np

import hg


def klein_area(a: complex, b: complex, c: complex, n: int = 1000) -> float:
    """円板モデルの三角形 abc の面積を、クラインモデルで数値積分して求める.

    クラインモデルでは三角形の辺が線分になり、面積要素は dx dy / (1 - x^2 - y^2)^(3/2) である。
    三角形を n^2 個の小さな三角形に分け、それぞれの重心での値に面積を掛けて足し合わせる。
    """
    p, q, r = (hg.disk_to_klein(v) for v in (a, b, c))
    # 小三角形の重心を重心座標 (i + 1/3, j + 1/3) と (i + 2/3, j + 2/3) で表す
    i, j = np.meshgrid(np.arange(n), np.arange(n))
    mask = i + j < n
    centers = [((i + 1.0 / 3.0) / n, (j + 1.0 / 3.0) / n, mask),
               ((i + 2.0 / 3.0) / n, (j + 2.0 / 3.0) / n, i + j < n - 1)]
    small_area = abs(((q - p).conjugate() * (r - p)).imag) / 2.0 / n**2  # 小三角形のユークリッドの面積
    total = 0.0
    for s, t, valid in centers:
        k = p + s[valid] * (q - p) + t[valid] * (r - p)
        total += float(np.sum((1.0 - np.abs(k) ** 2) ** -1.5)) * small_area
    return total


def report() -> None:
    """三角形の辺と角を測り、各定理の両辺を表示する."""
    a, b, c = hg.disk_point(1.0, 0.3), hg.disk_point(1.8, 2.2), hg.disk_point(1.4, 4.0)  # 頂点 A, B, C
    side_a, side_b, side_c = hg.disk_distance(b, c), hg.disk_distance(c, a), hg.disk_distance(a, b)
    alpha, beta, gamma = hg.disk_angle(a, b, c), hg.disk_angle(b, c, a), hg.disk_angle(c, a, b)
    print(f"辺  a = {side_a:.6f}, b = {side_b:.6f}, c = {side_c:.6f}")
    print(f"角  alpha = {alpha:.6f}, beta = {beta:.6f}, gamma = {gamma:.6f}")

    rhs = math.cosh(side_a) * math.cosh(side_b) - math.sinh(side_a) * math.sinh(side_b) * math.cos(gamma)
    print("双曲余弦定理")
    print(f"  cosh c                                   = {math.cosh(side_c):.10f}")
    print(f"  cosh a cosh b - sinh a sinh b cos(gamma) = {rhs:.10f}")

    print("正弦定理")
    for name, angle, side in (("a", alpha, side_a), ("b", beta, side_b), ("c", gamma, side_c)):
        print(f"  sin(角) / sinh {name} = {math.sin(angle) / math.sinh(side):.10f}")

    angle_sum = alpha + beta + gamma
    print("ガウス・ボネの定理")
    print(f"  内角の和            = {angle_sum:.6f}（{math.degrees(angle_sum):.2f} 度）")
    print(f"  pi - 内角の和       = {math.pi - angle_sum:.6f}")
    print(f"  数値積分による面積  = {klein_area(a, b, c):.6f}")

    print("頂点の原点からの距離を scale 倍した三角形の内角の和")
    for scale in (1.0, 0.3, 0.1, 0.03):
        vs = [hg.disk_point(r * scale, t) for r, t in ((1.0, 0.3), (1.8, 2.2), (1.4, 4.0))]
        s = hg.disk_angle(vs[0], vs[1], vs[2]) + hg.disk_angle(vs[1], vs[2], vs[0]) + hg.disk_angle(vs[2], vs[0], vs[1])
        print(f"  scale = {scale:<5} 内角の和 = {math.degrees(s):8.4f} 度")


if __name__ == "__main__":
    report()
