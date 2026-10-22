"""フィボナッチ数列を、行列のべき乗と固有値で求める.

(F_{n+1}, F_n) = A (F_n, F_{n-1})、A = [[1, 1], [1, 0]] なので、
A^n を求めれば F_n が分かる。A の固有値は (1 ± √5) / 2 であり、
対角化すると一般項（ビネの公式）が得られる。

使い方: python ch10_fibonacci.py
"""

import numpy as np


def fibonacci_matrix(n: int) -> int:
    """行列のべき乗で F_n を求める（F_0 = 0、F_1 = 1）."""
    a = np.array([[1, 1], [1, 0]], dtype=np.int64)
    return int(np.linalg.matrix_power(a, n)[0, 1])


def fibonacci_binet(n: int) -> float:
    """固有値を使った一般項（ビネの公式）で F_n を求める."""
    phi = (1 + np.sqrt(5)) / 2
    psi = (1 - np.sqrt(5)) / 2
    return float((phi**n - psi**n) / np.sqrt(5))


def report() -> None:
    """2 つの方法で求めたフィボナッチ数を表示する."""
    a = np.array([[1.0, 1.0], [1.0, 0.0]])
    print("A の固有値 =", np.sort(np.real_if_close(np.linalg.eigvals(a))))
    print("F_0 から F_10 =", [fibonacci_matrix(n) for n in range(11)])
    for n in (10, 50, 80):
        print(f"F_{n}: 行列のべき乗 {fibonacci_matrix(n)}、ビネの公式 {fibonacci_binet(n):.1f}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
