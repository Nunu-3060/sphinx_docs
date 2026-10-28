"""マンデルブロ集合とジュリア集合を、脱出時間アルゴリズムで描く.

複素数の写像 z -> z^2 + c を反復する。

* ジュリア集合: c を固定し、初期値 z0 を平面上で動かす
* マンデルブロ集合: 初期値を z0 = 0 に固定し、c を平面上で動かす

|z| が 2 を超えると、その後は必ず無限大に発散する。そこで、|z| が 2 を超えるまでの
反復回数（脱出時間）で色を付ける。

使い方: python ch09_mandelbrot_julia.py [--save DIR]
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util
from ch04_logistic import bifurcation_points

Complex = NDArray[np.complex128]
Real = NDArray[np.float64]
Step = Callable[[Complex, Complex], Complex]


def square_step(z: Complex, c: Complex) -> Complex:
    """標準の写像 z -> z^2 + c."""
    return z * z + c


def complex_grid(center: complex, width: float, nx: int, ny: int) -> Complex:
    """中心 center、横幅 width の長方形を nx × ny の格子に分けた複素数の配列を返す（上の行ほど虚部が大きい）."""
    height = width * ny / nx
    x = np.linspace(center.real - width / 2, center.real + width / 2, nx)
    y = np.linspace(center.imag + height / 2, center.imag - height / 2, ny)
    grid: Complex = x[None, :] + 1j * y[:, None]
    return grid


def escape_time(z0: Complex, c: Complex, max_iter: int, step: Step = square_step,
                radius: float = 2.0) -> tuple[Real, Complex]:
    """各点の脱出時間と、脱出した直後の z を返す.

    max_iter 回反復しても |z| <= radius のままの点（集合に属するとみなす点）の脱出時間は
    max_iter にする。計算が済んだ点は配列から除き、残った点だけを反復して速くする。
    """
    z = z0.astype(np.complex128).ravel()
    c = np.broadcast_to(c, z0.shape).astype(np.complex128).ravel()
    count = np.full(z.shape, float(max_iter))
    last = np.zeros_like(z)
    active = np.arange(z.size)
    for n in range(max_iter):
        z_act = step(z[active], c[active])
        escaped = np.abs(z_act) > radius
        idx = active[escaped]
        count[idx] = n + 1
        last[idx] = z_act[escaped]
        z[active] = z_act
        active = active[~escaped]
        if active.size == 0:
            break
    return count.reshape(z0.shape), last.reshape(z0.shape)


def smooth_count(count: Real, last: Complex, max_iter: int, degree: int = 2) -> Real:
    """連続的な脱出時間 ν = n + 1 - log(log|z|) / log(d) を返す（集合内の点は NaN）.

    整数の脱出時間で色を付けると、色の境目が等高線のような帯（バンド）になる。
    脱出した直後の |z| の大きさを使って、帯の間を滑らかにつなぐ。d は写像の次数
    （z^2 + c なら 2）である。
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        nu: Real = count + 1.0 - np.log(np.log(np.abs(last))) / np.log(degree)
    nu[count >= max_iter] = np.nan
    return nu


def show(ax: Axes, values: Real, center: complex, width: float, cmap: str = "magma",
         title: str = "", log: bool = True) -> None:
    """脱出時間の配列を画像として表示する（NaN の点、つまり集合内の点は黒）.

    脱出時間は境界の近くで急に大きくなるので、log が True なら対数を取ってから色に変換する。
    """
    ny, nx = values.shape
    height = width * ny / nx
    extent = (center.real - width / 2, center.real + width / 2, center.imag - height / 2, center.imag + height / 2)
    colormap = plt.get_cmap(cmap).with_extremes(bad="k")
    if log:
        values = np.log(np.maximum(values, 1.0))
    ax.imshow(np.ma.masked_invalid(values), extent=extent, cmap=colormap, interpolation="nearest")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])


def mandelbrot(center: complex, width: float, nx: int, ny: int, max_iter: int,
               step: Step = square_step, degree: int = 2) -> Real:
    """マンデルブロ集合（の仲間）の、滑らかな脱出時間の配列を返す（degree は写像 step の次数）."""
    c = complex_grid(center, width, nx, ny)
    count, last = escape_time(np.zeros_like(c), c, max_iter, step, radius=1000.0)
    return smooth_count(count, last, max_iter, degree)


def julia(c: complex, nx: int, ny: int, max_iter: int, width: float = 3.2) -> Real:
    """パラメータ c のジュリア集合の、滑らかな脱出時間の配列を返す."""
    z0 = complex_grid(0.0, width, nx, ny)
    count, last = escape_time(z0, np.full(z0.shape, c), max_iter, radius=1000.0)
    return smooth_count(count, last, max_iter)


def format_complex(c: complex) -> str:
    """図の見出し用に、複素数を a + bi の形の文字列にする（0 の部分は省く）."""
    re, im = c.real, c.imag
    if im == 0.0:
        return f"{re:g}"
    imag = "i" if abs(im) == 1.0 else f"{abs(im):g}i"
    if re == 0.0:
        return imag if im > 0 else "-" + imag
    return f"{re:g} {'+' if im > 0 else '-'} {imag}"


JULIA_EXAMPLES: list[tuple[complex, str]] = [
    (0.0, "円板"),
    (-1.0, "サンマルコ"),
    (-0.123 + 0.745j, "ドゥアディのウサギ"),
    (1j, "樹状"),
    (-0.8 + 0.156j, "渦巻き（非連結）"),
    (0.3, "カントールの塵（非連結）"),
]


def create_figures() -> dict[str, Figure]:
    """マンデルブロ集合（mandelbrot）、ジュリア集合（julia）、滑らかな着色（smooth）、
    分岐図との対応（bifurcation_link）、変種（variants）の図を作る."""
    figures: dict[str, Figure] = {}
    fig = plt.figure(figsize=(13.0, 7.6))
    grid = fig.add_gridspec(2, 2, width_ratios=[1.4, 1])
    ax1 = fig.add_subplot(grid[:, 0])
    show(ax1, mandelbrot(-0.75 + 0j, 3.0, 600, 600, 200), -0.75 + 0j, 3.0, title="全体（中心 $-0.75$、幅 3）")
    zooms = [(-0.7453 + 0.1127j, 0.01, "A"), (-1.7676 + 0j, 0.045, "B")]
    for row, (center, width, name) in enumerate(zooms):
        ax1.annotate(name, (center.real, center.imag), xytext=(center.real - 0.25, center.imag + 0.35),
                     color="w", fontsize=12, arrowprops={"arrowstyle": "->", "color": "w"})
        ax = fig.add_subplot(grid[row, 1])
        show(ax, mandelbrot(center, width, 400, 400, 800), center, width,
             title=f"{name} の拡大（中心 ${format_complex(center)}$、幅 {width}）")
    fig.tight_layout()
    figures["mandelbrot"] = fig

    fig, axes = plt.subplots(2, 3, figsize=(12.0, 8.0))
    for ax, (c, name) in zip(axes.ravel(), JULIA_EXAMPLES):
        show(ax, julia(c, 400, 400, 300), 0.0, 3.2, cmap="viridis", title=f"$c = {format_complex(c)}$\n{name}")
    fig.tight_layout()
    figures["julia"] = fig

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.6))
    center, width, max_iter = -0.7453 + 0.1127j, 0.01, 800
    c_grid = complex_grid(center, width, 450, 380)
    count, last = escape_time(np.zeros_like(c_grid), c_grid, max_iter, radius=1000.0)
    banded = count.copy()
    banded[count >= max_iter] = np.nan
    smooth = smooth_count(count, last, max_iter)
    # 色が周期的に変わるカラーマップを使い、脱出時間の対数の変化を何周も色に割り当てる
    show(ax1, np.log(banded) * 4.0 % 1.0, center, width, cmap="twilight_shifted", title="整数の脱出時間", log=False)
    show(ax2, np.log(smooth) * 4.0 % 1.0, center, width, cmap="twilight_shifted", title="滑らかな脱出時間", log=False)
    fig.tight_layout()
    figures["smooth"] = fig

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.0, 7.0), sharex=True)
    show(ax1, mandelbrot(-0.875 + 0j, 2.25, 900, 260, 200), -0.875 + 0j, 2.25, title="マンデルブロ集合（実軸の付近）")
    ax1.set_xticks(np.arange(-2.0, 0.5, 0.25))
    # 実数の c に対する x -> x^2 + c の分岐図（初期値 0 から出発）
    cs, xs = bifurcation_c(-2.0, 0.25)
    ax2.plot(cs, xs, ",", color="k", alpha=0.3)
    ax2.set_xlim(-2.0, 0.25)
    ax2.set_ylim(-2.0, 2.0)
    ax2.set_xlabel("$c$（実数）")
    ax2.set_ylabel("$x$")
    ax2.set_title("$x_{n+1} = x_n^2 + c$ の分岐図", fontsize=10)
    fig.tight_layout()
    figures["bifurcation_link"] = fig

    variants: list[tuple[str, Step, complex, float, int]] = [
        # バーニング・シップは、船の形に見えるよう虚軸を上下反転した向き（c の代わりに共役の c）で描くことが多い
        ("バーニング・シップ（上下反転）\n$z \\to (|\\mathrm{Re}\\,z| + i|\\mathrm{Im}\\,z|)^2 + c$",
         lambda z, c: (np.abs(z.real) + 1j * np.abs(z.imag)) ** 2 + np.conj(c), -0.4 + 0.55j, 3.4, 2),
        ("トリコーン\n$z \\to \\bar{z}^2 + c$", lambda z, c: np.conj(z) ** 2 + c, -0.3 + 0j, 4.0, 2),
        ("マルチブロ集合\n$z \\to z^3 + c$", lambda z, c: z**3 + c, 0.0, 3.2, 3),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.6))
    for ax, (title, step, center, width, degree) in zip(axes, variants):
        show(ax, mandelbrot(center, width, 420, 420, 150, step, degree), center, width, cmap="inferno", title=title)
    fig.tight_layout()
    figures["variants"] = fig
    return figures


def bifurcation_c(c_min: float, c_max: float) -> tuple[Real, Real]:
    """実数の c に対する写像 x -> x^2 + c の分岐図の点を返す.

    x = r (1/2 - y) と置くと、ロジスティック写像 y -> r y (1 - y) は x -> x^2 + c
    （c = r/2 - r^2/4）に変換できる。そこで、ロジスティック写像の分岐図の点を変換して使う。
    """
    r_min = 1.0 + np.sqrt(1.0 - 4.0 * c_max)
    r_max = 1.0 + np.sqrt(1.0 - 4.0 * c_min)
    rs, ys = bifurcation_points(r_min, r_max, n_r=2000, keep=200)
    cs: Real = rs / 2.0 - rs**2 / 4.0
    xs: Real = rs * (0.5 - ys)
    return cs, xs


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
