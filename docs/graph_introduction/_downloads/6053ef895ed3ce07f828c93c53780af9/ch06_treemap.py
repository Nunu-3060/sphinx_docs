"""ツリーマップ: 長方形の面積で構成比を表す.

架空のファイルサーバーの使用容量を、ファイルの種類ごとに描く。
配置の計算は treemap.py の squarify() で行う。

使い方: python ch06_treemap.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont
import treemap

USAGE = {  # ファイルの種類: 使用容量（GB）
    "動画": 420,
    "画像": 260,
    "文書": 120,
    "ソースコード": 60,
    "表計算": 45,
    "圧縮ファイル": 35,
    "その他": 20,
}


def create_figure() -> Figure:
    """使用容量のツリーマップを描く."""
    values = [float(value) for value in USAGE.values()]
    rects = treemap.squarify(values, (0.0, 0.0, 16.0, 9.0))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for index, ((name, value), rect) in enumerate(zip(USAGE.items(), rects)):
        treemap.draw_rect(ax, rect, f"C{index}", f"{name}\n{value} GB",
                          linewidth=2)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
