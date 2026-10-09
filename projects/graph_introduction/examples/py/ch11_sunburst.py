"""サンバースト図: 階層構造を同心円で描く.

ch11_treemap_nested.py と同じ使用容量のデータを、内側の輪に部署、
外側の輪にフォルダーを置いた同心円で描く。matplotlib の円グラフを、
幅を指定した輪として 2 つ重ねて作る。

使い方: python ch11_sunburst.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont
from ch11_treemap_nested import TREE

RING_WIDTH = 0.35  # 輪の幅


def create_figure() -> Figure:
    """部署とフォルダーの 2 段のサンバースト図を描く."""
    departments = list(TREE)
    totals = [sum(children.values()) for children in TREE.values()]
    names = [name for children in TREE.values() for name in children]
    values = [value for children in TREE.values()
              for value in children.values()]
    colors = [f"C{index}" for index, children in enumerate(TREE.values())
              for _ in children]

    fig, ax = plt.subplots(figsize=(6, 6))
    # 内側の輪: 部署
    ax.pie(totals, radius=1 - RING_WIDTH, labels=departments,
           labeldistance=0.55, colors=[f"C{i}" for i in range(len(TREE))],
           wedgeprops={"width": RING_WIDTH, "edgecolor": "white"},
           textprops={"fontweight": "bold"}, startangle=90,
           counterclock=False)
    # 外側の輪: フォルダー（親の部署と同じ色を薄くして塗る）
    ax.pie(values, radius=1, labels=names, labeldistance=1.05, colors=colors,
           wedgeprops={"width": RING_WIDTH, "edgecolor": "white",
                       "alpha": 0.55},
           textprops={"fontsize": 9}, startangle=90, counterclock=False)
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
