"""サンキー図: 量の流れを帯の太さで描く.

架空の Web サイトの訪問者の流れ（流入元 → 閲覧したページ → 結果）を、
人数に比例した太さの帯で描く。帯は 3 次ベジェ曲線で滑らかにつなぐ。

使い方: python ch12_sankey.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path

import jpfont

# ノード: 列の番号（左から 0, 1, 2）
NODES = {
    "検索": 0, "SNS": 0, "広告": 0, "直接": 0,
    "製品ページ": 1, "ブログ": 1,
    "購入": 2, "離脱": 2,
}
# 流れ: (流れの元, 流れの先, 人数)
FLOWS = [
    ("検索", "製品ページ", 300), ("検索", "ブログ", 200),
    ("SNS", "製品ページ", 50), ("SNS", "ブログ", 250),
    ("広告", "製品ページ", 150), ("直接", "製品ページ", 100),
    ("製品ページ", "購入", 180), ("製品ページ", "離脱", 420),
    ("ブログ", "購入", 30), ("ブログ", "離脱", 420),
]
NODE_WIDTH = 0.03
GAP = 0.04         # 同じ列のノードの間隔
COLUMN_STEP = 0.5  # 列の間隔


def node_sizes() -> dict[str, float]:
    """各ノードの大きさ（流入と流出の多い方の人数）を返す."""
    inflow = {name: 0.0 for name in NODES}
    outflow = {name: 0.0 for name in NODES}
    for source, target, value in FLOWS:
        outflow[source] += value
        inflow[target] += value
    return {name: max(inflow[name], outflow[name]) for name in NODES}


def band(x0: float, y0: tuple[float, float], x1: float,
         y1: tuple[float, float]) -> Path:
    """左端の上下 y0 と右端の上下 y1 を結ぶ帯の輪郭を返す."""
    middle = (x0 + x1) / 2
    vertices = [
        (x0, y0[0]),                                       # 左上
        (middle, y0[0]), (middle, y1[0]), (x1, y1[0]),     # 右上へ
        (x1, y1[1]),                                       # 右下
        (middle, y1[1]), (middle, y0[1]), (x0, y0[1]),     # 左下へ
        (x0, y0[0]),
    ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CLOSEPOLY]
    return Path(vertices, codes)


def create_figure() -> Figure:
    """訪問者の流れのサンキー図を描く."""
    sizes = node_sizes()
    columns = max(NODES.values()) + 1
    largest = max(sum(sizes[n] for n in NODES if NODES[n] == column)
                  for column in range(columns))
    scale = 0.8 / largest  # 1 人あたりの高さ

    # 各ノードの上端の y 座標。列ごとに上から積む
    tops: dict[str, float] = {}
    for column in range(columns):
        y = 1.0
        for name in (n for n in NODES if NODES[n] == column):
            tops[name] = y
            y -= sizes[name] * scale + GAP

    # 帯の交差を減らすため、各ノードの流出口は流れの先が上にあるものから、
    # 流入口は流れの元が上にあるものから順に、上から割り当てる
    out_offset: dict[tuple[str, str], float] = {}
    in_offset: dict[tuple[str, str], float] = {}
    for name in NODES:
        outgoing = [f for f in FLOWS if f[0] == name]
        used = 0.0
        for source, target, value in sorted(outgoing,
                                            key=lambda f: -tops[f[1]]):
            out_offset[(source, target)] = used
            used += value * scale
        incoming = [f for f in FLOWS if f[1] == name]
        used = 0.0
        for source, target, value in sorted(incoming,
                                            key=lambda f: -tops[f[0]]):
            in_offset[(source, target)] = used
            used += value * scale

    fig, ax = plt.subplots(figsize=(8, 4.5))
    sources = [name for name in NODES if NODES[name] == 0]
    for source, target, value in FLOWS:
        height = value * scale
        y0_top = tops[source] - out_offset[(source, target)]
        y1_top = tops[target] - in_offset[(source, target)]
        x0 = NODES[source] * COLUMN_STEP + NODE_WIDTH
        x1 = NODES[target] * COLUMN_STEP
        # 帯の色は、左端の流入元の色に合わせる（2 列目以降は灰色）
        color = (f"C{sources.index(source)}" if source in sources
                 else "gray")
        ax.add_patch(PathPatch(band(x0, (y0_top, y0_top - height),
                                    x1, (y1_top, y1_top - height)),
                               facecolor=color, alpha=0.35, linewidth=0))
    for name, column in NODES.items():
        x = column * COLUMN_STEP
        height = sizes[name] * scale
        ax.add_patch(Rectangle((x, tops[name] - height), NODE_WIDTH, height,
                               color="black"))
        # 最後の列はラベルを右に、それ以外は左に書く。帯に重なっても
        # 読めるよう、ラベルの背景を白くする
        label = f"{name}\n{sizes[name]:.0f} 人"
        background = {"facecolor": "white", "alpha": 0.8, "linewidth": 0}
        if column == columns - 1:
            ax.text(x + NODE_WIDTH + 0.01, tops[name] - height / 2, label,
                    va="center", bbox=background)
        else:
            ax.text(x - 0.01, tops[name] - height / 2, label, va="center",
                    ha="right", bbox=background)
    ax.set_xlim(-0.2, (columns - 1) * COLUMN_STEP + 0.2)
    ax.set_ylim(min(tops[n] - sizes[n] * scale for n in NODES) - 0.02, 1.02)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
