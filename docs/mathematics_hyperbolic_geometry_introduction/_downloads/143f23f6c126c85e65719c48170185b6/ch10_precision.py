"""双曲平面の数値計算で起こる丸め誤差の例.

1. 円板モデルでは、原点から遠い点ほど |z| が 1 に近づき、倍精度の浮動小数点数で表せなくなる。
2. 近い 2 点の距離を arcosh(1 + 小さな数) で計算すると、桁落ちで精度が落ちる。

使い方: python ch10_precision.py
"""

import math

import hg


def report() -> None:
    """2 つの例の計算結果を表示する."""
    print("1. 原点から距離 d の点を円板モデルで表し、距離を計算し直す")
    print("     d      |z| = tanh(d / 2)       計算し直した距離")
    for d in (5.0, 10.0, 20.0, 30.0, 36.0, 38.0, 40.0):
        z = hg.disk_point(d, 0.0)
        try:
            back = f"{hg.disk_distance(0j, z):.6f}"
        except ValueError:
            back = "計算できない（|z| = 1 になった）"
        print(f"  {d:5.1f}   {abs(z):.17f}   {back}")

    print("2. 円板の原点と、そこから距離 h の点の距離を 2 通りの公式で計算する")
    print("     h         arcosh の公式         artanh の公式")
    for h in (1e-3, 1e-6, 1e-8, 1e-10):
        z = hg.disk_point(h, 0.0)
        cosh_d = 1.0 + 2.0 * abs(z) ** 2 / (1.0 - abs(z) ** 2)
        print(f"  {h:.0e}   {math.acosh(cosh_d):.15e}   {hg.disk_distance(0j, z):.15e}")


if __name__ == "__main__":
    report()
