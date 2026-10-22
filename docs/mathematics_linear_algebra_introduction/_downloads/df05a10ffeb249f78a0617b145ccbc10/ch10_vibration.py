"""2 つの質点とばねの振動を、固有値と固有ベクトル（固有モード）で解く.

壁 - ばね - 質点 1 - ばね - 質点 2 - ばね - 壁 とつないだ系である。
質量 m = 1、ばね定数 k = 1 とすると、変位 x = (x1, x2) は
x'' = -K x、K = [[2, -1], [-1, 2]] を満たす。
K の固有ベクトルの方向の振動（固有モード）は、それぞれ単独の
単振動になり、角振動数は固有値の平方根である。

使い方: python ch10_vibration.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

K = np.array([[2.0, -1.0],
              [-1.0, 2.0]])
X0 = np.array([1.0, 0.0])  # 初期変位: 質点 1 だけをずらし、静かに離す


def eigen_modes() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """K の固有値（小さい順）と固有ベクトル（列）を返す.

    固有ベクトルの符号は任意なので、各列の 1 番目の成分が正になるようにそろえる。
    """
    values, vectors = np.linalg.eigh(K)  # 対称行列なので eigh を使う
    return values, vectors * np.sign(vectors[0])


def displacement(t: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """時刻 t の変位（2 行 N 列）と、各モードの座標（2 行 N 列）を返す."""
    values, vectors = eigen_modes()
    omega = np.sqrt(values)
    c = vectors.T @ X0  # 初期変位を固有ベクトルで展開する（vectors は直交行列）
    modes = c[:, np.newaxis] * np.cos(np.outer(omega, t))
    return vectors @ modes, modes


def report() -> None:
    """固有値、角振動数、固有ベクトルを表示する."""
    values, vectors = eigen_modes()
    with np.printoptions(precision=4, suppress=True):
        print("固有値 =", values)
        print("角振動数 =", np.sqrt(values))
        print("固有ベクトル（列）=")
        print(vectors)


def create_figure() -> Figure:
    """各質点の変位と、各モードの座標の時間変化を描く."""
    t = np.linspace(0.0, 30.0, 1000)
    x, modes = displacement(t)
    fig, (ax_x, ax_mode) = plt.subplots(2, 1, figsize=(10, 5.5), sharex=True)
    ax_x.plot(t, x[0], color="C0", label="質点 1")
    ax_x.plot(t, x[1], color="C1", label="質点 2")
    ax_x.set_ylabel("変位")
    ax_x.set_title("各質点の変位（エネルギーが 2 つの質点の間を行き来する）")
    ax_mode.plot(t, modes[0], color="C2", label="モード 1（同じ向き、ω = 1）")
    ax_mode.plot(t, modes[1], color="C3", label="モード 2（逆向き、ω = √3）")
    ax_mode.set_ylabel("モードの座標")
    ax_mode.set_xlabel("時刻")
    ax_mode.set_title("固有モードの座標（それぞれ単振動）")
    for ax in (ax_x, ax_mode):
        ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
        ax.grid(True, color="0.9")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
