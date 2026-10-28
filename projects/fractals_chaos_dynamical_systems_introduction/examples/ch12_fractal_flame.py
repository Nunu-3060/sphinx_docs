"""フラクタル・フレーム（の簡易版）: IFS に非線形の変形と色を加えて描く.

カオスゲーム（第 8 章）と同じく、毎回 1 つの写像を選んで点を動かす。ただし、

1. 写像は「アフィン変換」の後に「バリエーション」（非線形の変形）を施したものにする
2. 各写像に色の番号 c_k を割り当て、点の色 c を (c + c_k) / 2 で更新する
3. 画素ごとに点の数と色の合計を記録し、対数の密度で明るさを、色の平均で色合いを決める

使い方: python ch12_fractal_flame.py [--save DIR]
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Array = NDArray[np.float64]
Variation = Callable[[Array, Array], tuple[Array, Array]]


def linear(x: Array, y: Array) -> tuple[Array, Array]:
    """変形しない."""
    return x, y


def sinusoidal(x: Array, y: Array) -> tuple[Array, Array]:
    """各座標を sin で折り返す."""
    return np.sin(x), np.sin(y)


def horseshoe(x: Array, y: Array) -> tuple[Array, Array]:
    """極座標の角度を 2 倍にし、距離はそのままにする（馬蹄形に折り曲げる）."""
    r = np.sqrt(x * x + y * y) + 1e-9
    return (x - y) * (x + y) / r, 2.0 * x * y / r


def swirl(x: Array, y: Array) -> tuple[Array, Array]:
    """原点からの距離に応じて回転させる（渦巻き）."""
    r2 = x * x + y * y
    s, c = np.sin(r2), np.cos(r2)
    return x * s - y * c, x * c + y * s


VARIATIONS: dict[str, Variation] = {"linear": linear, "sinusoidal": sinusoidal, "horseshoe": horseshoe, "swirl": swirl}

# アフィン変換の係数 (a, b, c, d, e, f): x' = a x + b y + e, y' = c x + d y + f
AFFINES = np.array([
    [0.56, -0.38, 0.38, 0.56, 0.20, 0.10],
    [0.45, 0.30, -0.30, 0.45, -0.55, 0.25],
    [-0.40, 0.25, 0.20, 0.50, 0.15, -0.60],
])
COLORS = np.array([0.0, 0.5, 1.0])  # 各写像の色の番号（カラーマップ上の位置）


def flame(variation: Variation, n_points: int = 1_500_000, n_walkers: int = 5000, size: int = 400,
          span: float = 4.0, seed: int = 1) -> tuple[Array, Array]:
    """画素ごとの点の数と、色の番号の平均を返す（span は描く範囲の一辺の長さ）."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.0, 1.0, n_walkers)
    y = rng.uniform(-1.0, 1.0, n_walkers)
    c = rng.random(n_walkers)
    hist = np.zeros(size * size)
    color_sum = np.zeros(size * size)
    for n in range(n_points // n_walkers + 20):
        k = rng.integers(0, len(AFFINES), n_walkers)
        a, b, cc, d, e, f = AFFINES[k].T
        x, y = variation(a * x + b * y + e, cc * x + d * y + f)
        c = (c + COLORS[k]) / 2.0
        if n < 20:
            continue  # 最初の 20 回は、アトラクタに近づくまでの過渡状態として捨てる
        col = np.floor((x / span + 0.5) * size).astype(np.int64)
        row = np.floor((0.5 - y / span) * size).astype(np.int64)
        ok = (col >= 0) & (col < size) & (row >= 0) & (row < size)
        idx = row[ok] * size + col[ok]
        hist += np.bincount(idx, minlength=size * size)
        color_sum += np.bincount(idx, weights=c[ok], minlength=size * size)
    with np.errstate(invalid="ignore"):
        mean_color = np.where(hist > 0, color_sum / hist, 0.0)
    return hist.reshape(size, size), mean_color.reshape(size, size)


def render(hist: Array, mean_color: Array, cmap: str = "plasma", gamma: float = 2.5) -> Array:
    """点の数の対数で明るさを、色の番号の平均で色合いを決めた RGB 画像を返す（背景は黒）."""
    alpha = (np.log1p(hist) / np.log1p(hist.max())) ** (1.0 / gamma)
    rgb = plt.get_cmap(cmap)(mean_color)[..., :3]
    result: Array = rgb * alpha[..., None]
    return result


def create_figures() -> dict[str, Figure]:
    """同じアフィン変換に 4 種類のバリエーションを組み合わせた画像を並べる（variations）."""
    fig, axes = plt.subplots(1, 4, figsize=(14.0, 3.9))
    for ax, (name, variation) in zip(axes, VARIATIONS.items()):
        span = 2.4 if name == "sinusoidal" else 3.0
        hist, mean_color = flame(variation, span=span)
        ax.imshow(render(hist, mean_color))
        ax.set_title(name)
        ax.axis("off")
    fig.tight_layout()
    return {"variations": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
