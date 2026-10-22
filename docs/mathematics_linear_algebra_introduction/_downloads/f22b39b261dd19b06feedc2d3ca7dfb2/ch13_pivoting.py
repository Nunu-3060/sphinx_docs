"""ピボット選択の効果: ピボットが非常に小さいと、消去法の結果が大きく狂う.

    1e-20 x + y = 1
          x + y = 2

の解はほぼ x = 1、y = 1 である。ピボット選択をしないと、1 行目の
1e-20 をピボットにして消去するため、丸め誤差で x が失われる。

使い方: python ch13_pivoting.py
"""

import numpy as np

from ch05_gauss import gaussian_elimination


def report() -> None:
    """ピボット選択の有無で、消去法の解を比べる."""
    a = [[1e-20, 1.0],
         [1.0, 1.0]]
    b = [1.0, 2.0]
    print("ピボット選択なし:", gaussian_elimination(a, b, pivoting=False))
    print("ピボット選択あり:", gaussian_elimination(a, b, pivoting=True))
    print("np.linalg.solve: ", np.linalg.solve(a, b))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
