"""第 5 章: カラーマップの明度の変化を比較する。

カラーマップ上の各色を CIE L*a*b* 色空間に変換し、明度 L* を
プロットした ch05_colormap_lightness.png と、同じデータを jet と
viridis で描いた ch05_colormap_compare.png を保存します。

実行例::

    python ch05_colormap.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib import colormaps, font_manager

FloatArray = npt.NDArray[np.float64]

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]
COLORMAPS = ["jet", "viridis", "cividis", "gray"]

# 線形 RGB から CIE XYZ (D65) への変換行列
RGB_TO_XYZ = np.array([
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505],
])


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する。"""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    available = [name for name in JAPANESE_FONTS if name in installed]
    plt.rcParams["font.family"] = available + ["sans-serif"]


def spread_labels(values: list[float], min_gap: float) -> list[float]:
    """ラベルの y 座標が min_gap 以上離れるように調整した値を返す。

    値の小さい順に見ていき、直前のラベルと近すぎる場合は上へずらす。
    戻り値の順序は引数と同じ。
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    adjusted = list(values)
    for prev, curr in zip(order, order[1:]):
        adjusted[curr] = max(adjusted[curr], adjusted[prev] + min_gap)
    return adjusted


def lightness(srgb: FloatArray) -> FloatArray:
    """(N, 3) の sRGB (0〜1) 配列から CIE L* (0〜100) を計算する。"""
    linear = np.where(srgb <= 0.04045, srgb / 12.92,
                      ((srgb + 0.055) / 1.055) ** 2.4)
    y = linear @ RGB_TO_XYZ[1]  # L* の計算には Y (輝度) だけを使う
    epsilon = (6 / 29) ** 3
    f = np.where(y > epsilon, np.cbrt(y), y / (3 * (6 / 29) ** 2) + 4 / 29)
    result: FloatArray = 116 * f - 16
    return result


def plot_lightness(path: Path) -> None:
    """カラーマップごとに、位置と明度 L* の関係をプロットする。"""
    positions = np.linspace(0, 1, 256)
    fig, ax = plt.subplots(figsize=(8, 4))
    last_values: list[float] = []
    for name in COLORMAPS:
        colors = colormaps[name](positions)[:, :3]
        values = lightness(colors)
        # 点の色をカラーマップの色にして、どの位置が何色かを示す
        ax.scatter(positions, values, c=colors, s=6)
        last_values.append(float(values[-1]))
    for name, y in zip(COLORMAPS, spread_labels(last_values, min_gap=5)):
        ax.text(1.02, y, name, va="center", fontsize=11)
    ax.set_xlabel("カラーマップ上の位置 (データの値)")
    ax.set_ylabel("明度 L*")
    ax.set_xlim(0, 1.15)
    ax.set_ylim(0, 105)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def plot_compare(path: Path) -> None:
    """2 つの山を持つデータを、jet と viridis で描き比べる。"""
    x, y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-3, 3, 200))
    z = (np.exp(-((x - 1) ** 2 + y ** 2))
         + 0.6 * np.exp(-((x + 1.2) ** 2 + (y - 1) ** 2) / 0.5))
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
    for ax, name in zip(axes, ["jet", "viridis"]):
        image = ax.imshow(z, cmap=name, origin="lower")
        ax.set_title(name)
        ax.set_xticks([])
        ax.set_yticks([])
        fig.colorbar(image, ax=ax, shrink=0.85)
    fig.tight_layout()
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    use_japanese_font()
    plot_lightness(outdir / "ch05_colormap_lightness.png")
    plot_compare(outdir / "ch05_colormap_compare.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
