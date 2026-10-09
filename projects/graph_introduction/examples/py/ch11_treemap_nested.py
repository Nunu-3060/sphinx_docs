"""入れ子のツリーマップ: 階層構造と量を同時に描く.

架空のファイルサーバーの使用容量を、部署（1 段目）とフォルダー（2 段目）
の 2 段の階層で描く。部署の長方形の中を、さらにフォルダーで分割する。

使い方: python ch11_treemap_nested.py
"""

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, to_rgb
from matplotlib.figure import Figure

import jpfont
import treemap

# 部署: {フォルダー: 使用容量（GB）}
TREE = {
    "開発部": {"ビルド成果物": 150, "ソースコード": 80, "設計書": 70,
            "テスト結果": 50},
    "営業部": {"提案書": 120, "契約書": 60, "見積書": 40},
    "広報部": {"画像": 110, "動画": 90},
    "総務部": {"議事録": 30, "規程": 20},
}
PADDING = 0.12  # 部署の枠とフォルダーの間の余白
HEADER = 0.45   # 部署名を書く帯の高さ


def create_figure() -> Figure:
    """2 段の入れ子のツリーマップを描く."""
    totals = [float(sum(children.values())) for children in TREE.values()]
    outer_rects = treemap.squarify(totals, (0.0, 0.0, 16.0, 9.0))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for index, ((department, children), outer) in enumerate(
            zip(TREE.items(), outer_rects)):
        color = f"C{index}"
        # フォルダーは、部署の色を白に近づけた薄い色で塗る
        red, green, blue = to_rgb(color)
        light_color = to_hex((1 - 0.5 * (1 - red), 1 - 0.5 * (1 - green),
                              1 - 0.5 * (1 - blue)))
        treemap.draw_rect(ax, outer, color, linewidth=3)
        x, y, width, height = outer
        ax.text(x + 0.1, y + height - 0.08, department, va="top",
                color="white", fontweight="bold")
        # 部署名の帯と余白を除いた領域を、フォルダーで分割する
        inner = (x + PADDING, y + PADDING, width - 2 * PADDING,
                 height - 2 * PADDING - HEADER)
        values = [float(value) for value in children.values()]
        for (name, value), rect in zip(children.items(),
                                       treemap.squarify(values, inner)):
            treemap.draw_rect(ax, rect, light_color, f"{name}\n{value} GB")
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
