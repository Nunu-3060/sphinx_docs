"""3D サーフェス: 2 変数関数を立体的に描く.

ch09_contour.py と同じ関数を、視点を変えた 2 つの 3D サーフェスで描く。
視点によって、手前の山に隠れる部分が変わる。

使い方: python ch09_surface.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont
from ch09_contour import make_field


def create_figure() -> Figure:
    """視点の異なる 2 つの 3D サーフェスを描く."""
    xx, yy, zz = make_field()
    fig = plt.figure(figsize=(10, 4))
    for index, (elevation, azimuth) in enumerate([(30, -60), (30, 120)]):
        ax = fig.add_subplot(1, 2, index + 1, projection="3d")
        ax.plot_surface(xx, yy, zz, cmap="RdBu_r", vmin=-1, vmax=1,
                        rstride=2, cstride=2, linewidth=0)
        ax.view_init(elev=elevation, azim=azimuth)  # 視点の高さと方位
        ax.set_title(f"視点の方位: {azimuth} 度")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
