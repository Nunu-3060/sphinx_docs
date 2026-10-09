"""ベクトル場: 矢印図と流線図.

平面上の各点に向きと大きさを持つ量（ベクトル場）を、矢印図（quiver）と
流線図（streamplot）で描く。例として、渦と一様な流れを重ねた流れを使う。

使い方: python ch09_vector_field.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def velocity(xx: np.ndarray,
             yy: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """各点の流れの速度（x 成分、y 成分）を返す."""
    r2 = xx ** 2 + yy ** 2 + 0.3
    u = -yy / r2 + 0.3  # 原点の周りの渦 + 右向きの一様な流れ
    v = xx / r2
    return u, v


def create_figure() -> Figure:
    """同じベクトル場を矢印図と流線図で描く."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 4.2))

    # 矢印図: 格子点ごとに 1 本の矢印を描く。間隔を粗くする
    x = np.linspace(-2, 2, 13)
    xx, yy = np.meshgrid(x, x)
    u, v = velocity(xx, yy)
    # scale_units="xy" と scale=4 で、速さ 1 の矢印を長さ 0.25 で描く
    ax_left.quiver(xx, yy, u, v, np.hypot(u, v), cmap="viridis",
                   angles="xy", scale_units="xy", scale=4)
    ax_left.set_title("矢印図（quiver）")

    # 流線図: 流れに沿った線を描く。線の色で速さを表す
    x = np.linspace(-2, 2, 100)
    xx, yy = np.meshgrid(x, x)
    u, v = velocity(xx, yy)
    stream = ax_right.streamplot(xx, yy, u, v, color=np.hypot(u, v),
                                 cmap="viridis", density=1.2)
    fig.colorbar(stream.lines, ax=ax_right, label="速さ")
    ax_right.set_title("流線図（streamplot）")

    for ax in (ax_left, ax_right):
        ax.set_aspect("equal")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
