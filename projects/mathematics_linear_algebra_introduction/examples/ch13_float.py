"""浮動小数点数の誤差: 丸め誤差、桁落ち、計算機イプシロン.

使い方: python ch13_float.py
"""

import numpy as np


def report() -> None:
    """浮動小数点数の誤差の例を表示する."""
    print("0.1 + 0.2 =", 0.1 + 0.2)
    print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)
    print("np.isclose(0.1 + 0.2, 0.3):", np.isclose(0.1 + 0.2, 0.3))
    eps = np.finfo(np.float64).eps
    print("計算機イプシロン =", eps)
    print("(1 + eps) - 1 =", (1.0 + eps) - 1.0)
    print("(1 + eps / 2) - 1 =", (1.0 + eps / 2) - 1.0)  # 1 に比べて小さすぎて消える

    # 桁落ち: 近い値どうしの引き算で、有効数字が失われる
    x = 1e-8
    naive = (1.0 - np.cos(x)) / x**2  # 正しい値は約 0.5
    stable = 2.0 * np.sin(x / 2) ** 2 / x**2  # 1 - cos x = 2 sin^2(x/2) を使う
    print("(1 - cos x) / x^2 =", naive)
    print("2 sin^2(x/2) / x^2 =", stable)

    # 行列式が「ほぼ 0」かどうかは、行列式の値だけでは判断できない
    a = 1e-3 * np.eye(10)  # 対角成分が 0.001 の 10 次の対角行列
    print("det(0.001 I_10) =", np.linalg.det(a), " 条件数 =", np.linalg.cond(a))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
