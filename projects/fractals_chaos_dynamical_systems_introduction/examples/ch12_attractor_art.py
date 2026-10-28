"""ストレンジアトラクタをジェネラティブアートとして描く.

* 密度描画: 点を打つ代わりに、各画素に入った点の数を数え、対数とガンマ補正で明るさに変換する
* パラメータの自動探索: ランダムに選んだ 2 次写像のうち、リアプノフ指数が正で発散しないものを残す
* アニメーション: パラメータを少しずつ変えながら描いた画像を GIF にする

使い方: python ch12_attractor_art.py [--save DIR]
"""

from functools import cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from PIL import Image

import plot_util
from ch06_clifford import attractor_points, clifford

Array = NDArray[np.float64]


def density(x: Array, y: Array, size: int, margin: float = 0.05) -> Array:
    """点の集まりを size × size の画素に振り分け、各画素に入った点の数を返す（上の行ほど y が大きい）."""
    x0, x1 = float(x.min()), float(x.max())
    y0, y1 = float(y.min()), float(y.max())
    span = max(x1 - x0, y1 - y0) * (1.0 + 2.0 * margin)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    edges_x = np.linspace(cx - span / 2.0, cx + span / 2.0, size + 1)
    edges_y = np.linspace(cy - span / 2.0, cy + span / 2.0, size + 1)
    hist, _, _ = np.histogram2d(y, x, bins=(edges_y, edges_x))
    result: Array = hist[::-1]
    return result


def tone_map(hist: Array, gamma: float = 2.2) -> Array:
    """点の数を 0 から 1 の明るさに変換する.

    点の数は場所によって何桁も違うので、まず対数を取って幅を縮め、
    最後にガンマ補正（1/gamma 乗）で暗い部分を持ち上げる。
    """
    level = np.log1p(hist) / np.log1p(hist.max())
    result: Array = level ** (1.0 / gamma)
    return result


def colorize(level: Array, cmap: str, background: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> Array:
    """明るさをカラーマップで色に変換し、点のない画素を背景色にした RGB 画像を返す."""
    rgb = plt.get_cmap(cmap)(level)[..., :3]
    alpha = np.clip(level * 4.0, 0.0, 1.0)[..., None]  # 点の少ない画素は背景に溶け込ませる
    result: Array = alpha * rgb + (1.0 - alpha) * np.array(background)
    return result


def quadratic_map(coef: Array, x: Array, y: Array) -> tuple[Array, Array]:
    """係数 coef（形は (12, 候補の数)）で決まる 2 次写像を、候補ごとにまとめて計算する.

    x' = a0 + a1 x + a2 x^2 + a3 x y + a4 y + a5 y^2
    y' = a6 + a7 x + a8 x^2 + a9 x y + a10 y + a11 y^2
    """
    a = coef
    nx = a[0] + a[1] * x + a[2] * x * x + a[3] * x * y + a[4] * y + a[5] * y * y
    ny = a[6] + a[7] * x + a[8] * x * x + a[9] * x * y + a[10] * y + a[11] * y * y
    return nx, ny


def search_attractors(n_candidates: int = 4000, n_found: int = 6, seed: int = 2026) -> list[tuple[Array, float]]:
    """ストレンジアトラクタを持つ 2 次写像の係数を探し、(係数, リアプノフ指数) の一覧を返す.

    係数は -1.2 から 1.2 までの 0.1 刻みの値からランダムに選ぶ（J. C. Sprott の方法）。
    候補ごとに、わずかに離れた 2 つの点を同時に動かし、距離の伸び率の対数の平均から
    リアプノフ指数を推定する。距離は毎回もとの大きさに戻す（再規格化）。
    """
    rng = np.random.default_rng(seed)
    coef = rng.integers(-12, 13, size=(12, n_candidates)) / 10.0
    x = np.full(n_candidates, 0.05)
    y = np.full(n_candidates, 0.05)
    xe, ye = x + 1e-6, y.copy()
    lyap = np.zeros(n_candidates)
    alive = np.ones(n_candidates, dtype=bool)
    xmin = np.full(n_candidates, np.inf)
    xmax = np.full(n_candidates, -np.inf)
    n_steps, transient = 3000, 500
    with np.errstate(over="ignore", invalid="ignore"):
        for n in range(n_steps):
            x, y = quadratic_map(coef, x, y)
            xe, ye = quadratic_map(coef, xe, ye)
            alive &= np.isfinite(x) & (np.abs(x) < 1e6) & (np.abs(y) < 1e6)
            d = np.hypot(xe - x, ye - y)
            d = np.where(alive & (d > 0), d, 1e-6)
            if n >= transient:
                lyap += np.log(d / 1e-6)
                xmin, xmax = np.minimum(xmin, x), np.maximum(xmax, x)
            # 2 つの点の距離を 1e-6 に戻す
            xe = x + (xe - x) * 1e-6 / d
            ye = y + (ye - y) * 1e-6 / d
            x = np.where(alive, x, 0.0)
            y = np.where(alive, y, 0.0)
    lyap /= n_steps - transient
    # 発散せず、リアプノフ指数が正で、1 点に縮まらない（ある程度の広がりを持つ）ものを残す
    good = np.nonzero(alive & (lyap > 0.05) & (xmax - xmin > 0.1))[0]
    return [(coef[:, i], float(lyap[i])) for i in good[:n_found]]


def quadratic_points(coef: Array, n_orbits: int = 1000, n_steps: int = 600) -> tuple[Array, Array]:
    """係数 coef の 2 次写像のアトラクタ上の点を、n_orbits 本の軌道をまとめて計算して返す."""
    rng = np.random.default_rng(0)
    c = np.repeat(coef[:, None], n_orbits, axis=1)
    x = 0.05 + 1e-3 * rng.standard_normal(n_orbits)
    y = 0.05 + 1e-3 * rng.standard_normal(n_orbits)
    xs, ys = [], []
    with np.errstate(over="ignore", invalid="ignore"):
        for n in range(n_steps + 200):
            x, y = quadratic_map(c, x, y)
            if n >= 200:
                xs.append(x)
                ys.append(y)
    px, py = np.concatenate(xs), np.concatenate(ys)
    ok = np.isfinite(px) & np.isfinite(py) & (np.abs(px) < 1e3) & (np.abs(py) < 1e3)
    return px[ok], py[ok]


@cache
def found_attractors() -> list[tuple[Array, float]]:
    """search_attractors() の結果を返す（2 回目以降は計算済みの値を返す）."""
    return search_attractors()


def create_figures() -> dict[str, Figure]:
    """描き方の比較（rendering）と、自動探索で見つかったアトラクタ（gallery）の図を作る."""
    params = (-1.4, 1.6, 1.0, 0.7)
    x, y = attractor_points(clifford, params, n_orbits=5000, n_steps=400)
    size = 500
    hist = density(x, y, size)
    fig1, axes1 = plt.subplots(1, 3, figsize=(14.0, 5.0))
    axes1[0].plot(x[:300000], y[:300000], ",", color="k", alpha=0.3)
    axes1[0].set_aspect("equal")
    axes1[0].set_title("点を半透明で打つ")
    axes1[1].imshow(hist / hist.max(), cmap="gray_r")
    axes1[1].set_title("点の数をそのまま濃さにする")
    axes1[2].imshow(colorize(tone_map(hist), "inferno"))
    axes1[2].set_title("対数 + ガンマ補正 + カラーマップ")
    for ax in axes1:
        ax.set_xticks([])
        ax.set_yticks([])
    fig1.tight_layout()

    found = found_attractors()
    fig2, axes2 = plt.subplots(2, 3, figsize=(12.0, 8.4))
    cmaps = ["magma", "viridis", "plasma", "cividis", "twilight", "cubehelix"]
    for ax, (coef, lyap), cmap in zip(axes2.ravel(), found, cmaps):
        px, py = quadratic_points(coef)
        ax.imshow(colorize(tone_map(density(px, py, 400)), cmap))
        ax.set_title(f"$\\lambda = {lyap:.3f}$", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig2.tight_layout()
    return {"rendering": fig1, "gallery": fig2}


def report() -> None:
    """自動探索で見つかったアトラクタの係数とリアプノフ指数を表示する."""
    for k, (coef, lyap) in enumerate(found_attractors()):
        print(f"{k + 1}: λ = {lyap:.3f}, 係数 = [{', '.join(f'{c:+.1f}' for c in coef)}]")


def create_animation(path: Path) -> None:
    """クリフォード・アトラクタのパラメータを 2 組の間で往復させる GIF アニメーションを保存する."""
    # 2 組のパラメータは、補間の途中のどのコマでもアトラクタが周期軌道につぶれないことを確かめて選んだ
    start = np.array([-1.4, 1.6, 1.0, 0.7])
    end = np.array([-1.6, 1.6, 0.7, 1.0])
    n_frames = 48
    frames = []
    for k in range(n_frames):
        s = 0.5 - 0.5 * np.cos(2.0 * np.pi * k / n_frames)  # 0 → 1 → 0 と滑らかに往復する
        p = (1.0 - s) * start + s * end
        x, y = attractor_points(clifford, (p[0], p[1], p[2], p[3]), n_orbits=2000, n_steps=150)
        rgb = colorize(tone_map(density(x, y, 240)), "magma")
        frames.append(Image.fromarray((rgb * 255).astype(np.uint8)).quantize(colors=64))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report, create_animation)


if __name__ == "__main__":
    main()
