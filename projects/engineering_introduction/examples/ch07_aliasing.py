"""第 7 章: エイリアシング (折り返し) を確かめる。

サンプリング周波数 10 Hz で、9 Hz の余弦波をサンプリングします。
ナイキスト周波数 (5 Hz) を超える 9 Hz の信号は、サンプリングすると
1 Hz の信号と区別できなくなります。

図は ch07_aliasing.png として保存します。

実行例::

    python ch07_aliasing.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

FS = 10.0  # サンプリング周波数 [Hz]
F_SIGNAL = 9.0  # 元の信号の周波数 [Hz]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def alias_frequency(f: float, fs: float) -> float:
    """周波数 f の信号を fs でサンプリングしたときに見える周波数を返す。"""
    folded = f % fs
    return min(folded, fs - folded)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    f_alias = alias_frequency(F_SIGNAL, FS)
    print(f"{F_SIGNAL} Hz の信号を {FS} Hz でサンプリングすると、"
          f"{f_alias} Hz に見えます。")
    for f in (3.0, 6.0, 11.0, 50.0):
        print(f"  {f:5.1f} Hz -> {alias_frequency(f, FS):4.1f} Hz")

    t = np.linspace(0.0, 1.0, 2001)
    n = np.arange(int(FS) + 1)
    t_samples = n / FS

    setup_font()
    fig = Figure(figsize=(8, 3.6), layout="constrained")
    ax = fig.add_subplot()
    ax.plot(t, np.cos(2 * np.pi * F_SIGNAL * t), color="tab:blue",
            linewidth=1, label=f"元の信号 ({F_SIGNAL:g} Hz)")
    ax.plot(t, np.cos(2 * np.pi * f_alias * t), "--", color="tab:orange",
            label=f"サンプル値から見える信号 ({f_alias:g} Hz)")
    ax.plot(t_samples, np.cos(2 * np.pi * F_SIGNAL * t_samples), "o",
            color="black", label=f"サンプル値 ({FS:g} Hz でサンプリング)")
    ax.set_xlabel("時刻 [s]")
    ax.set_ylabel("振幅")
    ax.set_title("ナイキスト周波数を超える信号は低い周波数に折り返される")
    ax.set_ylim(-1.3, 1.6)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right", ncols=3, fontsize=8)
    fig.savefig(outdir / "ch07_aliasing.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
