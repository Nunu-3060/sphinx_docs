"""第 2 章: 色覚の違いによる見え方をシミュレーションする。

Machado ら (2009) の変換行列を使い、P 型 (1 型) と D 型 (2 型) の
2 色覚での見え方を近似します。赤と緑の配色と、色覚の多様性に配慮した
配色 (Okabe & Ito) を比較する画像 ch02_color_vision.png を保存します。

実行例::

    python ch02_color_vision.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib import font_manager

FloatArray = npt.NDArray[np.float64]

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

# 線形 RGB に掛ける変換行列 (Machado et al. 2009, 重症度 1.0)
SIMULATION_MATRICES: dict[str, FloatArray] = {
    "P 型": np.array([
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ]),
    "D 型": np.array([
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ]),
}

PALETTES: dict[str, list[str]] = {
    "赤と緑": ["#d62728", "#2ca02c", "#ff7f0e", "#8c564b"],
    "Okabe & Ito": ["#e69f00", "#56b4e9", "#009e73", "#d55e00"],
}


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する。"""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    available = [name for name in JAPANESE_FONTS if name in installed]
    plt.rcParams["font.family"] = available + ["sans-serif"]


def hex_to_array(colors: list[str]) -> FloatArray:
    """'#rrggbb' のリストを、0〜1 の値を持つ (N, 3) 配列に変換する。"""
    values = [[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in colors]
    return np.array(values, dtype=np.float64) / 255


def srgb_to_linear(srgb: FloatArray) -> FloatArray:
    """sRGB (0〜1) のガンマ補正を外して線形 RGB にする。"""
    return np.where(srgb <= 0.04045, srgb / 12.92,
                    ((srgb + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(linear: FloatArray) -> FloatArray:
    """線形 RGB を sRGB (0〜1) に戻す。範囲外の値は 0〜1 に切り詰める。"""
    linear = np.clip(linear, 0.0, 1.0)
    return np.where(linear <= 0.0031308, linear * 12.92,
                    1.055 * linear ** (1 / 2.4) - 0.055)


def simulate(srgb: FloatArray, matrix: FloatArray) -> FloatArray:
    """(N, 3) の sRGB 配列に色覚シミュレーションを適用する。"""
    linear = srgb_to_linear(srgb)
    return linear_to_srgb(linear @ matrix.T)


def draw_comparison(path: Path) -> None:
    """パレットごとに、一般的な色覚と 2 種類のシミュレーション結果を並べる。"""
    views = ["一般的な色覚", *SIMULATION_MATRICES]
    fig, axes = plt.subplots(len(PALETTES), len(views), figsize=(8, 3.2))
    for row, (name, colors) in enumerate(PALETTES.items()):
        srgb = hex_to_array(colors)
        for col, view in enumerate(views):
            if view in SIMULATION_MATRICES:
                shown = simulate(srgb, SIMULATION_MATRICES[view])
            else:
                shown = srgb
            ax = axes[row, col]
            ax.imshow(shown[np.newaxis, :, :], aspect="auto")
            ax.set_xticks([])
            ax.set_yticks([])
            if row == 0:
                ax.set_title(view, fontsize=12)
            if col == 0:
                ax.set_ylabel(name, fontsize=11, rotation=0, ha="right",
                              va="center")
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
    draw_comparison(outdir / "ch02_color_vision.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
