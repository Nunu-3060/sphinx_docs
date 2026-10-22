"""ベクトルの組が線形独立かを、ランクで判定する.

ベクトルを列に並べた行列のランクが、ベクトルの本数に等しければ線形独立である。

使い方: python ch07_independence.py
"""

import numpy as np


def report() -> None:
    """2 組のベクトルについて、線形独立かを判定する."""
    sets = {
        "組 1": [[1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1.0, 1.0, 0.0]],
        "組 2": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
    }
    for name, vectors in sets.items():
        a = np.column_stack(vectors)  # ベクトルを列に並べる
        rank = np.linalg.matrix_rank(a)
        result = "線形独立" if rank == len(vectors) else "線形従属"
        print(f"{name}: ランク {rank}、{result}")

    v1, v2, v3 = (np.array(v) for v in sets["組 2"])
    print("組 2 の v1 - 2 v2 + v3 =", v1 - 2 * v2 + v3)


def main() -> None:
    report()


if __name__ == "__main__":
    main()
