"""固有値と固有ベクトルを求め、対角化と行列のべき乗を確かめる.

使い方: python ch10_eigen.py
"""

import numpy as np


def report() -> None:
    """固有値、固有ベクトル、対角化、べき乗の結果を表示する."""
    a = np.array([[4.0, 1.0],
                  [2.0, 3.0]])
    values, vectors = np.linalg.eig(a)  # vectors の各列が固有ベクトル
    # 結果は複素数の配列で返るので、虚部が 0 なら実数の配列にする
    values, vectors = np.real_if_close(values), np.real_if_close(vectors)
    with np.printoptions(precision=4, suppress=True):
        print("固有値 =", values)
        print("固有ベクトル（列）=")
        print(vectors)
        for i in range(len(values)):
            v = vectors[:, i]
            print(f"A v{i + 1} == λ{i + 1} v{i + 1}:", np.allclose(a @ v, values[i] * v))

        p = np.array([[1.0, 1.0],
                      [1.0, -2.0]])  # 固有ベクトル (1, 1) と (1, -2) を列に並べる
        d = np.diag([5.0, 2.0])
        p_inv = np.linalg.inv(p)
        print("P^-1 A P =")
        print(p_inv @ a @ p)
        a10 = p @ np.diag([5.0**10, 2.0**10]) @ p_inv
        print("P D^10 P^-1 =")
        print(a10)
        print("np.linalg.matrix_power(A, 10) =")
        print(np.linalg.matrix_power(a, 10))
        print("P D P^-1 == A:", np.allclose(p @ d @ p_inv, a))

    rotation = np.array([[0.0, -1.0],
                         [1.0, 0.0]])  # 90 度の回転
    print("90 度の回転の固有値 =", np.linalg.eigvals(rotation))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
