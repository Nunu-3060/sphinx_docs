"""カオス同期（ペコラ＝キャロルの方法）: 2 つのローレンツ系を、1 つの変数を共有させて同期させる.

駆動系はふつうのローレンツ方程式である。応答系は y, z だけを持ち、x の代わりに
駆動系の x を使う。応答系の初期値が駆動系と違っていても、差は指数関数的に小さくなる。

使い方: python ch11_synchronization.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import ode
import plot_util
from ch06_lorenz import BETA, RHO, lorenz
from ode import Vector


def coupled(state: Vector) -> Vector:
    """駆動系 (x, y, z) と応答系 (y2, z2) をまとめた 5 変数の系の右辺."""
    x, y2, z2 = state[..., 0], state[..., 3], state[..., 4]
    drive = lorenz(state[..., :3])
    dy2 = x * (RHO - z2) - y2
    dz2 = x * y2 - BETA * z2
    return np.concatenate([drive, np.stack([dy2, dz2], axis=-1)], axis=-1)


def create_figures() -> dict[str, Figure]:
    """同期する場合としない場合の、2 つの系の差の時間変化を描く（sync）."""
    dt = 0.01
    n = 2000
    xs = ode.integrate(coupled, np.array([1.0, 1.0, 1.0, -5.0, 30.0]), dt, n)
    sync_error = np.abs(xs[:, 1] - xs[:, 3])
    # 比較: 結合しない 2 つのローレンツ系（初期値の差は同じ程度）
    a = ode.integrate(lorenz, np.array([1.0, 1.0, 1.0]), dt, n)
    b = ode.integrate(lorenz, np.array([1.0, -5.0, 30.0]), dt, n)
    free_error = np.abs(a[:, 1] - b[:, 1])
    t = np.arange(n + 1) * dt
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.semilogy(t, free_error + 1e-16, linewidth=0.8, color="0.5", label="結合しない場合")
    ax.semilogy(t, sync_error + 1e-16, linewidth=1.0, color="C3", label="$x$ を共有した場合")
    ax.set_xlabel("時刻 $t$")
    ax.set_ylabel("$y$ の差の絶対値")
    ax.set_ylim(1e-15, 1e3)
    ax.grid(True, color="0.9")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.tight_layout()
    return {"sync": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
