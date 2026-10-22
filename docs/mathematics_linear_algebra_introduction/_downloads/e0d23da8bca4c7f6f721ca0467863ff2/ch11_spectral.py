"""対称行列の固有値分解（スペクトル分解）と正定値の判定.

対称行列 a は、直交行列 Q と対角行列 Λ で a = Q Λ Q^T と分解できる。
固有値がすべて正なら正定値であり、コレスキー分解 a = L L^T ができる。

使い方: python ch11_spectral.py
"""

import numpy as np


def report() -> None:
    """固有値分解とコレスキー分解の結果を表示する."""
    a = np.array([[2.0, -1.0, 0.0],
                  [-1.0, 2.0, -1.0],
                  [0.0, -1.0, 2.0]])
    values, q = np.linalg.eigh(a)  # 固有値は小さい順に並ぶ
    with np.printoptions(precision=4, suppress=True):
        print("固有値 =", values)
        print("2 - √2, 2, 2 + √2 =", np.array([2 - np.sqrt(2), 2.0, 2 + np.sqrt(2)]))
        print("Q =")
        print(q)
        print("Q.T @ Q == I:", np.allclose(q.T @ q, np.eye(3)))
        print("Q Λ Q.T == a:", np.allclose(q @ np.diag(values) @ q.T, a))

        lower = np.linalg.cholesky(a)
        print("コレスキー分解の L =")
        print(lower)
        print("L @ L.T == a:", np.allclose(lower @ lower.T, a))

    indefinite = np.array([[1.0, 2.0],
                           [2.0, 1.0]])
    print("不定値の行列の固有値 =", np.linalg.eigvalsh(indefinite))
    try:
        np.linalg.cholesky(indefinite)
    except np.linalg.LinAlgError as error:
        print("不定値の行列のコレスキー分解:", error)


def main() -> None:
    report()


if __name__ == "__main__":
    main()
