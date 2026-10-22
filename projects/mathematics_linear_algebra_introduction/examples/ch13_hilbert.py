"""悪条件の行列: ヒルベルト行列の条件数と、連立一次方程式の誤差.

ヒルベルト行列 H の (i, j) 成分は 1 / (i + j - 1) である（i、j は 1 から数える）。
真の解をすべて 1 のベクトルとし、b = H x を作ってから H x = b を解き直す。
条件数が大きいほど、解の誤差が大きくなる。

使い方: python ch13_hilbert.py
"""

import numpy as np
from numpy.typing import NDArray


def hilbert(n: int) -> NDArray[np.float64]:
    """n 次のヒルベルト行列を返す."""
    i = np.arange(1, n + 1)
    return 1.0 / (i[:, np.newaxis] + i[np.newaxis, :] - 1)


def report() -> None:
    """次数ごとの条件数と、解の相対誤差を表示する."""
    print(" n   条件数        解の相対誤差")
    for n in (2, 4, 6, 8, 10, 12):
        h = hilbert(n)
        x_true = np.ones(n)
        b = h @ x_true
        x = np.linalg.solve(h, b)
        error = np.linalg.norm(x - x_true) / np.linalg.norm(x_true)
        print(f"{n:2d}   {np.linalg.cond(h):10.2e}   {error:10.2e}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
