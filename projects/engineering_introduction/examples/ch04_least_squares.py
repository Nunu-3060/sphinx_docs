"""第 4 章: 最小二乗法で直線を当てはめ、傾きの不確かさを求める。

ばねにおもりを吊るし、荷重 F [N] と伸び x [mm] を測定した、という
想定の模擬データに直線 x = a + bF を当てはめます。

* 切片 a と傾き b、それぞれの標準不確かさを計算する
* 傾きからばね定数 k = 1/b を求め、不確かさを伝播させる
* 測定値・当てはめた直線・残差を図にする (ch04_least_squares.png)

実行例::

    python ch04_least_squares.py --outdir output
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

TRUE_SPRING_CONSTANT = 0.5  # 模擬データを作るときのばね定数 [N/mm]
NOISE_MM = 0.15  # 伸びの測定に含まれる偶然誤差の標準偏差 [mm]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


@dataclass(frozen=True)
class LineFit:
    """直線 y = a + b x の当てはめ結果。"""

    a: float  # 切片
    b: float  # 傾き
    u_a: float  # 切片の標準不確かさ
    u_b: float  # 傾きの標準不確かさ
    residual_std: float  # 残差の標準偏差


def fit_line(x: NDArray[np.float64], y: NDArray[np.float64]) -> LineFit:
    """最小二乗法で直線を当てはめる。"""
    n = len(x)
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))
    sxx = float(np.sum((x - x_mean) ** 2))
    sxy = float(np.sum((x - x_mean) * (y - y_mean)))

    b = sxy / sxx
    a = y_mean - b * x_mean

    # 残差の標準偏差 (自由度は n - 2)
    residuals = y - (a + b * x)
    s = math.sqrt(float(np.sum(residuals ** 2)) / (n - 2))

    u_b = s / math.sqrt(sxx)
    u_a = s * math.sqrt(1 / n + x_mean ** 2 / sxx)
    return LineFit(a, b, u_a, u_b, s)


def make_data(seed: int) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """荷重と伸びの模擬測定データを作る。"""
    rng = np.random.default_rng(seed)
    force = np.arange(0.5, 5.01, 0.5)  # 荷重 0.5〜5.0 N
    elongation = force / TRUE_SPRING_CONSTANT
    elongation = elongation + rng.normal(0.0, NOISE_MM, size=force.size)
    return force, elongation


def plot(force: NDArray[np.float64], elongation: NDArray[np.float64],
         fit: LineFit, path: Path) -> None:
    """測定値と当てはめた直線、残差を描く。"""
    fig = Figure(figsize=(7, 5), layout="constrained")
    ax_fit, ax_res = fig.subplots(2, 1, sharex=True,
                                  height_ratios=[3, 1.3])

    line_x = np.linspace(0.0, 5.5, 50)
    ax_fit.plot(force, elongation, "o", label="測定値")
    ax_fit.plot(line_x, fit.a + fit.b * line_x, "-",
                label=f"当てはめ: x = {fit.a:.3f} + {fit.b:.3f} F")
    ax_fit.set_ylabel("伸び x [mm]")
    ax_fit.set_title("荷重と伸びの関係")
    ax_fit.grid(alpha=0.3)
    ax_fit.legend(loc="upper left")

    residuals = elongation - (fit.a + fit.b * force)
    ax_res.axhline(0.0, color="gray", linewidth=1)
    ax_res.plot(force, residuals, "o")
    ax_res.set_xlabel("荷重 F [N]")
    ax_res.set_ylabel("残差 [mm]")
    ax_res.grid(alpha=0.3)
    fig.savefig(path, dpi=120)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--seed", type=int, default=1,
                        help="模擬データを作る乱数のシード")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    force, elongation = make_data(args.seed)
    fit = fit_line(force, elongation)
    print(f"切片 a = {fit.a:.3f} ± {fit.u_a:.3f} mm")
    print(f"傾き b = {fit.b:.4f} ± {fit.u_b:.4f} mm/N")
    print(f"残差の標準偏差 s = {fit.residual_std:.3f} mm")

    # k = 1/b なので、相対不確かさは b と同じ大きさになる
    k = 1 / fit.b
    u_k = k * (fit.u_b / fit.b)
    print(f"ばね定数 k = {k:.4f} ± {u_k:.4f} N/mm "
          f"(模擬データの真値 {TRUE_SPRING_CONSTANT} N/mm)")

    setup_font()
    plot(force, elongation, fit, outdir / "ch04_least_squares.png")
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
