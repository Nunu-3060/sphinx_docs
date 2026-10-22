"""乱数の分布による「ばらつきの質」の違い。

同じ数の円を同じ位置に置き、半径だけを 3 種類の分布から選んで
描き比べる。

1. 一様分布: どの大きさも同じくらいの頻度で現れる。
2. 正規分布: 平均の近くの大きさが多く、極端な大きさは少ない。
3. べき分布（パレート分布）: 小さい円が非常に多く、大きい円はごく少ない。

あわせて、それぞれの分布から選んだ半径のヒストグラムを描く。
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# 3 つの分布で、半径の平均をそろえるための目標値（ピクセル）。
_MEAN_RADIUS: float = 6.0
# 描く半径の上限と下限（ピクセル）。
_MIN_RADIUS: float = 1.0
_MAX_RADIUS: float = 60.0


def uniform_radii(rng: np.random.Generator, count: int) -> np.ndarray:
    """一様分布から半径を選ぶ。平均が ``_MEAN_RADIUS`` になる範囲を使う。"""
    result: np.ndarray = rng.uniform(_MIN_RADIUS, 2 * _MEAN_RADIUS - _MIN_RADIUS, count)
    return result


def normal_radii(rng: np.random.Generator, count: int) -> np.ndarray:
    """正規分布から半径を選ぶ。

    正規分布は負の値も取りうるため、下限で切り詰める。標準偏差を
    平均の 1/4 にしているので、切り詰められる値はごくわずかである。
    """
    values: np.ndarray = rng.normal(_MEAN_RADIUS, _MEAN_RADIUS / 4, count)
    result: np.ndarray = np.clip(values, _MIN_RADIUS, _MAX_RADIUS)
    return result


def power_law_radii(
    rng: np.random.Generator, count: int, exponent: float = 2.5
) -> np.ndarray:
    """べき分布（パレート分布）から半径を選ぶ。

    確率密度が半径の ``-exponent`` 乗に比例する分布で、最小値
    ``x_min`` 以上の値を取る。平均は ``x_min * (a - 1) / (a - 2)``
    （``a = exponent``）なので、平均が ``_MEAN_RADIUS`` になるように
    ``x_min`` を決める。NumPy の ``pareto`` は ``x_min = 1`` から 1 を
    引いた値を返すため、1 を足してから ``x_min`` 倍する。
    """
    x_min: float = _MEAN_RADIUS * (exponent - 2) / (exponent - 1)
    values: np.ndarray = (rng.pareto(exponent - 1, count) + 1) * x_min
    result: np.ndarray = np.clip(values, _MIN_RADIUS, _MAX_RADIUS)
    return result


def render_circles(
    positions: np.ndarray, radii: np.ndarray, size: int
) -> Image.Image:
    """円を描いた画像を返す。小さい円が隠れないよう、大きい円から描く。"""
    image: Image.Image = Image.new("RGB", (size, size), (245, 241, 232))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for k in np.argsort(-radii):
        x, y = positions[k]
        r: float = float(radii[k])
        draw.ellipse(
            [x - r, y - r, x + r, y + r],
            fill=(40, 70, 110),
            outline=(245, 241, 232),
        )
    return image


def save_histograms(samples: dict[str, np.ndarray], path: str) -> None:
    """各分布の半径のヒストグラムを横に並べて保存する。"""
    fig, axes = plt.subplots(1, len(samples), figsize=(9, 2.6), sharey=True)
    bins: np.ndarray = np.linspace(0, 30, 61)
    for ax, (name, radii) in zip(axes, samples.items()):
        ax.hist(radii, bins=bins, color="#28466e")
        ax.set_title(f"{name} (mean {radii.mean():.1f})")
        ax.set_xlabel("radius [px]")
    axes[0].set_ylabel("count")
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def main() -> None:
    size: int = 400
    count: int = 600
    rng: np.random.Generator = np.random.default_rng(seed=3)
    positions: np.ndarray = rng.uniform(0, size, size=(count, 2))

    samples: dict[str, np.ndarray] = {
        "uniform": uniform_radii(rng, count),
        "normal": normal_radii(rng, count),
        "power law": power_law_radii(rng, count),
    }
    for name, radii in samples.items():
        file_name: str = "distribution_" + name.replace(" ", "_") + ".png"
        render_circles(positions, radii, size).save(file_name)
    save_histograms(samples, "distribution_histograms.png")


if __name__ == "__main__":
    main()
