"""上半平面の 2 点を 4 つのモデルに移し、それぞれの公式で求めた距離が一致することを確かめる.

使い方: python ch03_conversion.py
"""

import hg


def report() -> None:
    """2 点の各モデルでの座標と、各モデルの公式で求めた距離を表示する."""
    z, w = 1j, 2.0 + 3.0j  # 上半平面の 2 点

    dz, dw = hg.half_plane_to_disk(z), hg.half_plane_to_disk(w)
    kz, kw = hg.disk_to_klein(dz), hg.disk_to_klein(dw)
    xz, xw = hg.disk_to_hyperboloid(dz), hg.disk_to_hyperboloid(dw)

    print("モデル      点 1                        点 2")
    print(f"上半平面    {z:<27.6f} {w:.6f}")
    print(f"円板        {dz:<27.6f} {dw:.6f}")
    print(f"クライン    {kz:<27.6f} {kw:.6f}")
    print(f"双曲面      {str(xz.round(6)):<27} {xw.round(6)}")
    print()
    print(f"上半平面の公式による距離 {hg.half_plane_distance(z, w):.12f}")
    print(f"円板の公式による距離     {hg.disk_distance(dz, dw):.12f}")
    print(f"クラインの公式による距離 {hg.klein_distance(kz, kw):.12f}")
    print(f"双曲面の公式による距離   {hg.hyperboloid_distance(xz, xw):.12f}")


if __name__ == "__main__":
    report()
