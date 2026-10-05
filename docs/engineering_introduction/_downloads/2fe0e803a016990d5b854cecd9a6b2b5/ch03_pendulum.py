"""第 3 章: 振り子の非線形モデルと線形近似モデルを比較する。

振り子の運動方程式 θ'' = -(g/L) sin θ を、sin θ ≈ θ と近似した
線形モデルと比べ、振れ幅が大きくなると近似がどれだけ外れるかを
確かめます。

* 周期: 振れ幅ごとに、厳密な周期と線形モデルの周期を表で比較する
* 波形: 振れ幅 60° のときの角度の時間変化を図にする (ch03_pendulum.png)

実行例::

    python ch03_pendulum.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

G = 9.80665  # 標準重力加速度 [m/s^2]
LENGTH = 1.0  # 振り子の長さ [m]

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def agm(a: float, b: float) -> float:
    """算術幾何平均 (AGM) を返す。"""
    while abs(a - b) > 1e-15 * a:
        a, b = (a + b) / 2, math.sqrt(a * b)
    return a


def linear_period() -> float:
    """線形モデルの周期 2π√(L/g) を返す。振れ幅によらない。"""
    return 2 * math.pi * math.sqrt(LENGTH / G)


def exact_period(theta0: float) -> float:
    """振れ幅 theta0 [rad] のときの厳密な周期を返す。

    厳密な周期は第 1 種完全楕円積分で表され、算術幾何平均を使うと
    T = 2π√(L/g) / AGM(1, cos(θ0/2)) で計算できます。
    """
    return linear_period() / agm(1.0, math.cos(theta0 / 2))


def simulate(theta0: float, t_end: float,
             dt: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """非線形モデルを 4 次のルンゲ・クッタ法で解き、時刻と角度を返す。"""

    def deriv(state: NDArray[np.float64]) -> NDArray[np.float64]:
        theta, omega = state
        return np.array([omega, -(G / LENGTH) * math.sin(theta)])

    steps = int(round(t_end / dt))
    times = np.linspace(0.0, steps * dt, steps + 1)
    angles = np.empty(steps + 1)
    state = np.array([theta0, 0.0])
    angles[0] = theta0
    for i in range(steps):
        k1 = deriv(state)
        k2 = deriv(state + dt / 2 * k1)
        k3 = deriv(state + dt / 2 * k2)
        k4 = deriv(state + dt * k3)
        state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        angles[i + 1] = state[0]
    return times, angles


def print_period_table() -> None:
    """振れ幅ごとの周期の比較表を表示する。"""
    print("振れ幅[°]  厳密な周期[s]  線形モデル[s]  誤差[%]")
    for degree in (5, 10, 20, 30, 45, 60, 90):
        exact = exact_period(math.radians(degree))
        linear = linear_period()
        error = (linear - exact) / exact * 100
        print(f"{degree:8d}  {exact:13.4f}  {linear:13.4f}  {error:7.2f}")


def plot_waveform(path: Path) -> None:
    """振れ幅 60° のときの角度の時間変化を、2 つのモデルで比較する。"""
    theta0 = math.radians(60)
    times, angles = simulate(theta0, t_end=6.0, dt=0.001)
    omega0 = math.sqrt(G / LENGTH)
    linear = theta0 * np.cos(omega0 * times)

    fig = Figure(figsize=(7, 4), layout="constrained")
    ax = fig.add_subplot()
    ax.plot(times, np.degrees(angles), label=r"非線形モデル ($\sin\theta$)")
    ax.plot(times, np.degrees(linear), "--", label=r"線形モデル ($\theta$)")
    ax.set_xlabel("時刻 [s]")
    ax.set_ylabel("角度 [度]")
    ax.set_title("振れ幅 60 度では、線形モデルの位相が次第に進む")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncols=2)
    fig.savefig(path, dpi=120)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    setup_font()
    print_period_table()
    plot_waveform(outdir / "ch03_pendulum.png")
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
