"""主成分分析（PCA）: 共分散行列の固有ベクトルで、データの主な方向を求める.

2 次元の架空のデータ（200 点）を中心化し、共分散行列の固有値と
固有ベクトルを求める。固有値の大きい固有ベクトル（第 1 主成分）の方向に
データは最も大きく広がっている。

使い方: python ch14_pca.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

Matrix = NDArray[np.float64]


def make_data() -> Matrix:
    """相関のある 2 次元の架空のデータを、200 行 2 列の配列で返す."""
    rng = np.random.default_rng(seed=3)
    cov = np.array([[3.0, 1.8],
                    [1.8, 1.5]])
    return rng.multivariate_normal([2.0, 1.0], cov, size=200)


def pca(data: Matrix) -> tuple[Matrix, Matrix, Matrix]:
    """平均、固有値（大きい順）、固有ベクトル（列、同じ順）を返す."""
    mean = data.mean(axis=0)
    centered = data - mean
    cov = centered.T @ centered / (len(data) - 1)  # 共分散行列
    values, vectors = np.linalg.eigh(cov)
    order = np.argsort(values)[::-1]  # 大きい順に並べ替える
    values, vectors = values[order], vectors[:, order]
    # 固有ベクトルの符号は任意なので、各列の絶対値が最大の成分が正になるようにそろえる
    signs = np.sign(vectors[np.argmax(np.abs(vectors), axis=0), np.arange(vectors.shape[1])])
    return mean, values, vectors * signs


def report() -> None:
    """共分散行列、固有値、寄与率を表示し、特異値分解の結果と比べる."""
    data = make_data()
    mean, values, vectors = pca(data)
    with np.printoptions(precision=4, suppress=True):
        print("平均 =", mean)
        print("共分散行列 =")
        print(np.cov(data.T))
        print("固有値（主成分の分散）=", values)
        print("寄与率 =", values / values.sum())
        print("主成分の方向（列）=")
        print(vectors)
        s = np.linalg.svd(data - mean, compute_uv=False)
        print("特異値の 2 乗 / (n - 1) =", s**2 / (len(data) - 1))


def create_figure() -> Figure:
    """データと主成分の方向、第 1 主成分への射影を描く."""
    data = make_data()
    mean, values, vectors = pca(data)
    fig, (ax_data, ax_proj) = plt.subplots(1, 2, figsize=(10, 4.4))

    for ax in (ax_data, ax_proj):
        la_plot.setup_plane(ax, (-4, 8), (-3.5, 5))

    ax_data.scatter(data[:, 0], data[:, 1], s=8, color="C0", alpha=0.5)
    for i, (color, offset) in enumerate((("C3", (0.1, 0.1)), ("C2", (-2.6, 0.2)))):
        length = 2 * np.sqrt(values[i])  # 標準偏差の 2 倍の長さで描く
        la_plot.draw_vector(ax_data, length * vectors[:, i], origin=mean, color=color,
                            label=f"第 {i + 1} 主成分", offset=offset)
    ax_data.set_title("データと主成分の方向")

    w = vectors[:, 0]
    scores = (data - mean) @ w  # 第 1 主成分の座標（主成分得点）
    projected = mean + np.outer(scores, w)
    for p, q in zip(data[::4], projected[::4]):
        ax_proj.plot([p[0], q[0]], [p[1], q[1]], color="0.7", linewidth=0.6)
    ax_proj.scatter(data[:, 0], data[:, 1], s=8, color="C0", alpha=0.3)
    ax_proj.scatter(projected[:, 0], projected[:, 1], s=8, color="C3")
    ax_proj.set_title("第 1 主成分への射影（2 次元 → 1 次元）")

    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
