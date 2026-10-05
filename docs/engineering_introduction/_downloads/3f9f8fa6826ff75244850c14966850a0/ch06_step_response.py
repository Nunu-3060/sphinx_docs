"""第 6 章: 1 次遅れ系と 2 次系のステップ応答を描く。

* 1 次遅れ系 τ y' + y = u: 時定数 τ で最終値の約 63.2 % に達する
* 2 次系 y'' + 2ζω_n y' + ω_n^2 y = ω_n^2 u: 減衰比 ζ によって
  振動の仕方が変わる

図は ch06_step_response.png として保存します。

実行例::

    python ch06_step_response.py --outdir output
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

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def first_order(t: NDArray[np.float64], tau: float) -> NDArray[np.float64]:
    """1 次遅れ系の単位ステップ応答 1 - exp(-t/τ) を返す。"""
    return 1.0 - np.exp(-t / tau)


def second_order(t: NDArray[np.float64], zeta: float,
                 omega_n: float) -> NDArray[np.float64]:
    """2 次系の単位ステップ応答を数値積分 (RK4) で求める。"""
    dt = float(t[1] - t[0])

    def deriv(state: NDArray[np.float64]) -> NDArray[np.float64]:
        y, v = state
        acc = omega_n ** 2 * (1.0 - y) - 2 * zeta * omega_n * v
        return np.array([v, acc])

    state = np.zeros(2)
    out = np.empty_like(t)
    out[0] = 0.0
    for i in range(1, t.size):
        k1 = deriv(state)
        k2 = deriv(state + dt / 2 * k1)
        k3 = deriv(state + dt / 2 * k2)
        k4 = deriv(state + dt * k3)
        state = state + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[i] = state[0]
    return out


def overshoot_percent(zeta: float) -> float:
    """減衰比 ζ (0 < ζ < 1) の 2 次系の最大行き過ぎ量 [%] を返す。"""
    return 100 * math.exp(-zeta * math.pi / math.sqrt(1 - zeta ** 2))


def plot(path: Path) -> None:
    """1 次遅れ系と 2 次系のステップ応答を並べて描く。"""
    fig = Figure(figsize=(9, 3.8), layout="constrained")
    ax1, ax2 = fig.subplots(1, 2)

    tau = 1.0
    t = np.linspace(0.0, 5.0, 501)
    ax1.plot(t, first_order(t, tau))
    ax1.axhline(1 - math.exp(-1), color="gray", linestyle=":")
    ax1.axvline(tau, color="gray", linestyle=":")
    ax1.annotate(r"$t = \tau$ で 63.2 %", xy=(tau, 1 - math.exp(-1)),
                 xytext=(1.6, 0.4), arrowprops={"arrowstyle": "->"})
    ax1.set_title(r"1 次遅れ系 ($\tau$ = 1 s)")
    ax1.set_xlabel("時刻 [s]")
    ax1.set_ylabel("出力 y")
    ax1.set_ylim(0, 1.1)
    ax1.grid(alpha=0.3)

    t2 = np.linspace(0.0, 15.0, 1501)
    for zeta in (0.2, 0.5, 0.7, 1.0, 2.0):
        ax2.plot(t2, second_order(t2, zeta, omega_n=1.0),
                 label=rf"$\zeta$ = {zeta}")
    ax2.set_title(r"2 次系 ($\omega_n$ = 1 rad/s)")
    ax2.set_xlabel("時刻 [s]")
    ax2.set_ylabel("出力 y")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="lower right")
    fig.savefig(path, dpi=120)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    print("減衰比 ζ と最大行き過ぎ量")
    for zeta in (0.2, 0.5, 0.7):
        print(f"  ζ = {zeta}: {overshoot_percent(zeta):5.1f} %")

    setup_font()
    plot(outdir / "ch06_step_response.png")
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
