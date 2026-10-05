"""第 5 章: 常微分方程式の数値解法を比較する。

オイラー法、ホイン法 (2 次のルンゲ・クッタ法)、4 次のルンゲ・クッタ法
(RK4) の 3 つを、厳密解が分かっている問題に適用して比べます。

* 誤差と刻み幅の関係: dy/dt = -y, y(0) = 1 を t = 1 まで解き、
  刻み幅を変えたときの誤差を両対数グラフにする (ch05_ode_error.png)
* 長時間の安定性: 単振動 x'' = -x を解き、オイラー法では振幅が
  増えていくことを図にする (ch05_ode_oscillator.png)

実行例::

    python ch05_ode.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from collections.abc import Callable
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

Vector = NDArray[np.float64]
# 微分方程式 dy/dt = f(t, y) の右辺
RightHandSide = Callable[[float, Vector], Vector]
# 1 ステップ進める関数 (f, t, y, h) -> 次の y
Stepper = Callable[[RightHandSide, float, Vector, float], Vector]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def euler_step(f: RightHandSide, t: float, y: Vector, h: float) -> Vector:
    """オイラー法で 1 ステップ進める (1 次精度)。"""
    return y + h * f(t, y)


def heun_step(f: RightHandSide, t: float, y: Vector, h: float) -> Vector:
    """ホイン法で 1 ステップ進める (2 次精度)。"""
    k1 = f(t, y)
    k2 = f(t + h, y + h * k1)
    return y + h / 2 * (k1 + k2)


def rk4_step(f: RightHandSide, t: float, y: Vector, h: float) -> Vector:
    """4 次のルンゲ・クッタ法で 1 ステップ進める (4 次精度)。"""
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h / 2 * k1)
    k3 = f(t + h / 2, y + h / 2 * k2)
    k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


METHODS: dict[str, Stepper] = {
    "オイラー法": euler_step,
    "ホイン法": heun_step,
    "RK4": rk4_step,
}


def solve(f: RightHandSide, y0: Vector, t_end: float, steps: int,
          stepper: Stepper) -> Vector:
    """t = 0 から t_end まで steps 回に分けて解き、全時刻の y を返す。"""
    h = t_end / steps
    history = np.empty((steps + 1, y0.size))
    history[0] = y0
    y = y0
    for i in range(steps):
        y = stepper(f, i * h, y, h)
        history[i + 1] = y
    return history


def decay(t: float, y: Vector) -> Vector:
    """指数減衰 dy/dt = -y。"""
    return -y


def oscillator(t: float, y: Vector) -> Vector:
    """単振動 x'' = -x を、状態 (x, v) の 1 階の方程式に直したもの。"""
    x, v = y
    return np.array([v, -x])


def plot_error(path: Path) -> None:
    """刻み幅と誤差の関係を両対数グラフに描く。"""
    step_counts = [5, 10, 20, 40, 80, 160, 320]
    exact = math.exp(-1.0)
    fig = Figure(figsize=(6.5, 4.5), layout="constrained")
    ax = fig.add_subplot()
    print("刻み幅 h   " + "  ".join(f"{name:>10}" for name in METHODS))
    errors: dict[str, list[float]] = {name: [] for name in METHODS}
    for n in step_counts:
        for name, stepper in METHODS.items():
            y_end = solve(decay, np.array([1.0]), 1.0, n, stepper)[-1, 0]
            errors[name].append(abs(y_end - exact))
        print(f"{1 / n:8.5f}  " + "  ".join(
            f"{errors[name][-1]:10.2e}" for name in METHODS))

    sizes = [1 / n for n in step_counts]
    for name, marker in zip(METHODS, ["o", "s", "^"]):
        ax.loglog(sizes, errors[name], marker=marker, label=name)
    ax.set_xlabel("刻み幅 h")
    ax.set_ylabel("t = 1 での誤差の絶対値")
    ax.set_title("刻み幅を半分にすると誤差は 1/2、1/4、1/16 になる")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    fig.savefig(path, dpi=120)


def plot_oscillator(path: Path) -> None:
    """単振動をオイラー法と RK4 で解き、位相平面に描く。"""
    t_end, steps = 20.0, 200  # 刻み幅 0.1
    y0 = np.array([1.0, 0.0])
    fig = Figure(figsize=(6.5, 4.5), layout="constrained")
    ax = fig.add_subplot()
    angle = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(angle), np.sin(angle), color="gray", linewidth=3,
            alpha=0.5, label="厳密解")
    for name in ("オイラー法", "RK4"):
        history = solve(oscillator, y0, t_end, steps, METHODS[name])
        ax.plot(history[:, 0], history[:, 1], label=name)
        energy = 0.5 * (history[-1, 0] ** 2 + history[-1, 1] ** 2)
        print(f"{name}: t = {t_end} でのエネルギー {energy:.4f} "
              "(厳密解は 0.5)")
    ax.set_aspect("equal")
    ax.set_xlabel("位置 x")
    ax.set_ylabel("速度 v")
    ax.set_title("単振動 (h = 0.1, t = 0〜20)")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")
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
    plot_error(outdir / "ch05_ode_error.png")
    plot_oscillator(outdir / "ch05_ode_oscillator.png")
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
