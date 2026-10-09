"""散布図行列: すべての項目の組の関係を一覧する.

4 つの項目のすべての組み合わせについて散布図を描き、行列の形に並べる。
対角線のマスには、その項目のヒストグラムを描く。

使い方: python ch08_scatter_matrix.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont
from multivariate_data import FEATURES, GROUPS, make_dataset


def create_figure() -> Figure:
    """機種ごとに色分けした散布図行列を描く."""
    data, labels = make_dataset()
    size = len(FEATURES)
    fig, axes = plt.subplots(size, size, figsize=(8, 8))
    for row in range(size):
        for col in range(size):
            ax = axes[row, col]
            # 対角線のヒストグラムは縦軸の単位が違うため、別の縦軸に描く
            hist_ax = ax.twinx() if row == col else None
            for group, name in enumerate(GROUPS):
                values = data[labels == group]
                if hist_ax is not None:  # 対角線: ヒストグラム
                    hist_ax.hist(values[:, col], bins=12, alpha=0.5,
                                 color=f"C{group}")
                    hist_ax.set_yticks([])
                else:           # それ以外: 横軸が col、縦軸が row の散布図
                    ax.scatter(values[:, col], values[:, row], s=6,
                               alpha=0.6, color=f"C{group}", label=name)
            # 外周のマスにだけ目盛りと項目名を付ける
            if row == size - 1:
                ax.set_xlabel(FEATURES[col])
            else:
                ax.set_xticklabels([])
            if col == 0:
                ax.set_ylabel(FEATURES[row])
            else:
                ax.set_yticklabels([])
    # 対角線のマスの軸の範囲を、同じ行と列の散布図にそろえる
    for index in range(size):
        other = (index + 1) % size
        axes[index, index].set_xlim(axes[other, index].get_xlim())
        axes[index, index].set_ylim(axes[index, other].get_ylim())
    handles, names = axes[0, 1].get_legend_handles_labels()
    fig.legend(handles, names, loc="upper center", ncols=len(GROUPS),
               frameon=False, markerscale=2)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
