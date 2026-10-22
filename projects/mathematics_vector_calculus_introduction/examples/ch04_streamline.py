"""ベクトル場 F(x, y) = (-y, x) の流線を、常微分方程式を解いて求める.

使い方: python ch04_streamline.py
"""

import numpy as np
from numpy.typing import NDArray
from scipy import integrate

import vc_plot


def field(s: float, p: NDArray[np.float64]) -> NDArray[np.float64]:
    """流線の方程式 dr/ds = F(r) の右辺 F(x, y) = (-y, x) を返す."""
    return np.array([-p[1], p[0]])


def report() -> None:
    """点 (1, 0) を通る流線を数値的に求め、原点からの距離が一定（円）であることを確かめる."""
    s_end = 2.0 * np.pi
    sol = integrate.solve_ivp(field, (0.0, s_end), [1.0, 0.0], rtol=1e-10, atol=1e-12,
                              t_eval=np.linspace(0.0, s_end, 9))
    print("      s          x          y   原点からの距離")
    for s, x, y in zip(sol.t, sol.y[0], sol.y[1]):
        # round() で丸めてから 0.0 を足し、-0.000000 と表示されないようにする
        print(f"{s:7.4f} {round(x, 6) + 0.0:10.6f} {round(y, 6) + 0.0:10.6f} {np.hypot(x, y):14.8f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
