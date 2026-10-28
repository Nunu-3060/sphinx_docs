"""浮動小数点数の丸め誤差がカオスの計算に与える影響を調べる.

ロジスティック写像 x_{n+1} = 4 x_n (1 - x_n) を、同じ初期値から
float32（約 7 桁）、float64（約 16 桁）、decimal（100 桁）で計算し、結果を比べる。
また、テント写像を float64 で計算すると、軌道が 0 に吸い込まれることを示す。

使い方: python ch05_precision.py
"""

from decimal import Decimal, getcontext

import numpy as np

import plot_util


def first_divergence(a: list[float], b: list[float], tol: float = 0.1) -> int:
    """2 つの列の差が初めて tol を超える番号を返す（超えなければ -1）."""
    for n, (x, y) in enumerate(zip(a, b)):
        if abs(x - y) > tol:
            return n
    return -1


def report() -> None:
    """3 種類の精度の結果と、差が 0.1 を超えるステップ、テント写像の結果を表示する."""
    n = 100
    getcontext().prec = 100
    x_dec = Decimal("0.2")
    x64 = np.float64(0.2)
    x32 = np.float32(0.2)
    four64, one64 = np.float64(4.0), np.float64(1.0)
    four32, one32 = np.float32(4.0), np.float32(1.0)
    ref, f64, f32 = [float(x_dec)], [float(x64)], [float(x32)]
    for _ in range(n):
        x_dec = 4 * x_dec * (1 - x_dec)
        x64 = four64 * x64 * (one64 - x64)
        x32 = four32 * x32 * (one32 - x32)
        ref.append(float(x_dec))
        f64.append(float(x64))
        f32.append(float(x32))
    print(" n    decimal(100 桁)  float64   float32")
    for i in (0, 10, 20, 30, 40, 50, 60):
        print(f"{i:2d}    {ref[i]:.6f}         {f64[i]:.6f}  {f32[i]:.6f}")
    print(f"decimal との差が 0.1 を超える最初のステップ: float32 は {first_divergence(ref, f32)}、"
          f"float64 は {first_divergence(ref, f64)}")

    x = 0.3
    steps = 0
    while x != 0.0 and steps < 100:
        x = 1.0 - abs(1.0 - 2.0 * x)
        steps += 1
    print(f"テント写像を float64 で計算すると、x0 = 0.3 の軌道は {steps} 回で 0 になる")


def main() -> None:
    plot_util.run_sample(__doc__ or "", report=report)


if __name__ == "__main__":
    main()
