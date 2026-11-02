"""第 3 章「ノイズ」: ノイズを重ねる手法（fBm・乱流・リッジ）と周波数の図を作る。

* fbm_octaves.png: オクターブ数 1・2・4・8 の fBm
* fbm_variants.png: fBm・乱流・リッジノイズの比較
* fbm_params.png: lacunarity と gain を変えた fBm の一覧
* spectrum.png: 白色雑音・1 オクターブのノイズ・fBm のパワースペクトル
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2, ridged, turbulence
from texture import show_panels

SIZE = 256


def to_unit(values: FloatArray) -> FloatArray:
    """-1〜1 のノイズの値を、表示用に 0〜1 へ写す。"""
    return np.clip(values * 0.5 + 0.5, 0.0, 1.0)


def draw_octaves(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=3.0)
    counts = (1, 2, 4, 8)
    images = []
    for n in counts:
        # fbm は振幅の合計で割って返すので、合計を掛け戻し、オクターブを足すほど細部が加わる様子を見せる。
        norm = sum(0.5 ** k for k in range(n))
        images.append(to_unit(fbm(perlin2, x, y, octaves=n, seed=4) * norm))
    titles = [f"オクターブ数 {n}" for n in counts]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_variants(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=3.0)
    images = [
        to_unit(fbm(perlin2, x, y, octaves=6, seed=4) * 1.4),
        np.clip(turbulence(perlin2, x, y, octaves=6, seed=4) * 2.0, 0, 1),
        np.clip((ridged(perlin2, x, y, octaves=6, seed=4) - 0.3) * 1.6, 0, 1),
    ]
    titles = ["fBm", "乱流（絶対値を重ねる）", "リッジノイズ（反転して 2 乗）"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_params(file_name: str) -> None:
    """lacunarity（周波数の倍率）と gain（振幅の倍率）を変えた 3 × 3 の一覧。"""
    import matplotlib.pyplot as plt

    x, y = grid(192, 192, scale=3.0)
    lacunarities = (1.5, 2.0, 3.0)
    gains = (0.3, 0.5, 0.7)
    figure, axes = plt.subplots(3, 3, figsize=(8, 8.4))
    for row, gain in enumerate(gains):
        for column, lacunarity in enumerate(lacunarities):
            image = to_unit(fbm(perlin2, x, y, octaves=6, lacunarity=lacunarity, gain=gain, seed=4) * 1.4)
            ax = axes[row, column]
            ax.imshow(image, cmap="gray", vmin=0, vmax=1)
            ax.set_xticks([])
            ax.set_yticks([])
            if row == 0:
                ax.set_title(f"lacunarity = {lacunarity:g}", fontsize=10)
            if column == 0:
                ax.set_ylabel(f"gain = {gain:g}", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def radial_spectrum(image: FloatArray) -> tuple[FloatArray, FloatArray]:
    """画像のパワースペクトルを、周波数の大きさ（原点からの距離）ごとに平均する。

    戻り値は (周波数 [1 画像あたりの周期数], パワー)。直流成分（平均値）は除く。
    """
    size = image.shape[0]
    power = np.abs(np.fft.fftshift(np.fft.fft2(image - image.mean()))) ** 2
    k = np.fft.fftshift(np.fft.fftfreq(size)) * size
    kx, ky = np.meshgrid(k, k)
    radius = np.rint(np.hypot(kx, ky)).astype(np.int64)
    sums = np.bincount(radius.ravel(), weights=power.ravel())
    counts = np.bincount(radius.ravel())
    frequencies = np.arange(1, size // 2)
    return frequencies.astype(np.float64), sums[1:size // 2] / counts[1:size // 2]


def draw_spectrum(file_name: str) -> None:
    import matplotlib.pyplot as plt

    size = 512
    x, y = grid(size, size, scale=4.0)  # 基本の周波数は 1 画像あたり 4 格子
    white = np.random.default_rng(0).uniform(-1.0, 1.0, (size, size))
    single = perlin2(x, y, seed=4)
    fractal = fbm(perlin2, x, y, octaves=6, seed=4)

    figure = plt.figure(figsize=(10, 7.6))
    layout = figure.add_gridspec(2, 3, height_ratios=[1, 1.35])
    panels = [("白色雑音", white), ("1 オクターブ", single), ("fBm（6 オクターブ）", fractal)]
    for index, (title, image) in enumerate(panels):
        ax = figure.add_subplot(layout[0, index])
        ax.imshow(to_unit(image * 1.2)[:128, :128], cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    ax = figure.add_subplot(layout[1, :])
    colors = ["#999999", "#4c72b0", "#dd8452"]
    for (title, image), color in zip(panels, colors):
        frequencies, power = radial_spectrum(image / np.sqrt(np.mean(image ** 2)))  # 分散をそろえて比べる
        ax.loglog(frequencies, power, label=title, color=color)
    for octave in range(6):
        ax.axvline(4.0 * 2 ** octave, color="#dd8452", linewidth=0.6, linestyle=":")
    ax.set_xlabel("周波数（画像 1 枚あたりの周期数）")
    ax.set_ylabel("パワー（周波数ごとの平均）")
    ax.set_title("パワースペクトル（点線は各オクターブの基本の周波数 4, 8, 16, ...）", fontsize=10)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_octaves("fbm_octaves.png")
    draw_variants("fbm_variants.png")
    draw_params("fbm_params.png")
    draw_spectrum("spectrum.png")


if __name__ == "__main__":
    main()
