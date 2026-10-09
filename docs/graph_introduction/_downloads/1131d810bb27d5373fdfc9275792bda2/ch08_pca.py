"""主成分分析（PCA）: 多次元のデータを 2 次元に落として描く.

4 つの項目を標準化し、共分散行列の固有ベクトルを求めて、分散の大きい
2 つの方向（第 1 主成分と第 2 主成分）に射影する。

使い方: python ch08_pca.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from multivariate_data import GROUPS, make_dataset


def pca(data: np.ndarray, components: int) -> tuple[np.ndarray, np.ndarray]:
    """主成分得点と、各主成分の寄与率を返す."""
    # 項目ごとに平均 0、標準偏差 1 にそろえる（標準化）
    standardized = (data - data.mean(axis=0)) / data.std(axis=0)
    covariance = np.cov(standardized, rowvar=False)
    # eigh は対称行列の固有値を小さい順に返すので、大きい順に並べ替える
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1][:components]
    scores = standardized @ eigenvectors[:, order]
    ratios = eigenvalues[order] / eigenvalues.sum()
    return scores, ratios


def create_figure() -> Figure:
    """第 1 主成分と第 2 主成分の散布図を描く."""
    data, labels = make_dataset()
    scores, ratios = pca(data, 2)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    for group, name in enumerate(GROUPS):
        points = scores[labels == group]
        ax.scatter(points[:, 0], points[:, 1], s=15, alpha=0.7,
                   color=f"C{group}", label=name)
    ax.set_xlabel(f"第 1 主成分（寄与率 {ratios[0]:.0%}）")
    ax.set_ylabel(f"第 2 主成分（寄与率 {ratios[1]:.0%}）")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
