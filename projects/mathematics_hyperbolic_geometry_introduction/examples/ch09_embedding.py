"""木構造のデータを、ポアンカレ円板（2 次元）に埋め込む（Poincaré embeddings の簡易版）.

根から 3 本、その先は各頂点から 3 本ずつ枝分かれする深さ 3 の木（頂点 40 個）を使う。
祖先と子孫の組を「近いはずの組」、それ以外の組を「遠いはずの組」として、
近いはずの組の距離が、遠いはずの組の距離より小さくなるように点の位置を学習する。

使い方: python ch09_embedding.py
"""

import functools

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import hg_plot

FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]

EPS = 1e-5  # 点を円板の内側（|x| <= 1 - EPS）に留めるための余白


def make_tree(branching: int = 3, depth: int = 3) -> tuple[list[int], list[int]]:
    """頂点 0 を根とする完全 branching 分木を作り、各頂点の親と深さのリストを返す（根の親は -1）."""
    parent, level = [-1], [0]
    frontier = [0]
    for d in range(1, depth + 1):
        next_frontier = []
        for p in frontier:
            for _ in range(branching):
                parent.append(p)
                level.append(d)
                next_frontier.append(len(parent) - 1)
        frontier = next_frontier
    return parent, level


def related_matrix(parent: list[int]) -> BoolArray:
    """i が j の祖先か子孫であれば related[i, j] が True になる行列（推移閉包）."""
    n = len(parent)
    related = np.zeros((n, n), dtype=bool)
    for i in range(n):
        j = parent[i]
        while j >= 0:
            related[i, j] = related[j, i] = True
            j = parent[j]
    return related


def distances(x: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """全点の組の距離 d[i, j] と、勾配の計算に使う量を返す.

    d = arcosh(1 + 2 |x_i - x_j|^2 / ((1 - |x_i|^2)(1 - |x_j|^2)))
    """
    sq = np.sum(x**2, axis=1)
    alpha = 1.0 - sq  # 1 - |x_i|^2
    diff = x[:, None, :] - x[None, :, :]
    dist2 = np.sum(diff**2, axis=2)
    gamma = 1.0 + 2.0 * dist2 / (alpha[:, None] * alpha[None, :])
    gamma = np.maximum(gamma, 1.0 + 1e-12)
    return np.arccosh(gamma), gamma, alpha, sq


def loss_and_grad(x: FloatArray, related: BoolArray) -> tuple[float, FloatArray]:
    """損失と、各点の位置に関する（ユークリッドの）勾配を返す.

    近いはずの組 (u, v) ごとに、u から v への距離と、u から「遠いはずの点」への距離を比べる
    ソフトマックス損失 -log(exp(-d(u, v)) / sum(exp(-d(u, v')))) を足し合わせる。
    """
    n = x.shape[0]
    d, gamma, alpha, sq = distances(x)
    negative = ~related & ~np.eye(n, dtype=bool)
    # 各 u について、遠いはずの点との exp(-d) の和
    neg_sum = np.sum(np.exp(-d) * negative, axis=1)
    pairs = np.argwhere(related)
    loss = 0.0
    coef = np.zeros((n, n))  # 損失の d[u, w] による偏微分
    for u, v in pairs:
        denominator = np.exp(-d[u, v]) + neg_sum[u]
        loss += d[u, v] + np.log(denominator)
        coef[u, v] += 1.0 - np.exp(-d[u, v]) / denominator
        coef[u, negative[u]] -= np.exp(-d[u, negative[u]]) / denominator
    # d[u, w] の x_u による偏微分（Nickel と Kiela の論文の式）
    beta = alpha[None, :]
    root = np.sqrt(gamma**2 - 1.0)
    root[root < 1e-12] = np.inf  # 同じ点どうしの組は勾配に寄与させない
    xu, xw = x[:, None, :], x[None, :, :]
    inner = np.sum(xu * xw, axis=2)
    factor = 4.0 / (beta * root)
    dd_dxu = factor[:, :, None] * (((sq[None, :] - 2.0 * inner + 1.0) / alpha[:, None] ** 2)[:, :, None] * xu
                                   - xw / alpha[:, None, None])
    # d は対称なので、d[u, w] は x_u と x_w の両方に寄与する
    grad = np.sum(coef[:, :, None] * dd_dxu, axis=1) + np.sum(coef.T[:, :, None] * dd_dxu, axis=1)
    return float(loss), grad


def train(related: BoolArray, epochs: int = 300, rate: float = 0.05, seed: int = 0) -> FloatArray:
    """リーマン勾配法で点の位置を学習する.

    円板の計量は ds = 2 |dx| / (1 - |x|^2) なので、ユークリッドの勾配に (1 - |x|^2)^2 / 4 を掛けると
    リーマン多様体としての勾配になる。最初の 100 回は学習率を小さくして全体の配置を落ち着かせる。
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1e-3, 1e-3, size=(related.shape[0], 2))
    for epoch in range(epochs):
        _, grad = loss_and_grad(x, related)
        lr = rate / 10.0 if epoch < 100 else rate
        scale = (1.0 - np.sum(x**2, axis=1, keepdims=True)) ** 2 / 4.0
        x = x - lr * scale * grad
        norm = np.linalg.norm(x, axis=1, keepdims=True)
        x = np.where(norm >= 1.0 - EPS, x / norm * (1.0 - EPS), x)  # 円板の外に出た点を内側に戻す
    return x


@functools.cache
def embedding() -> FloatArray:
    """本書の木を学習した結果（図と実行結果で同じものを使うため、1 回だけ計算する）."""
    parent, _ = make_tree()
    return train(related_matrix(parent))


def create_figure() -> Figure:
    """学習した点の位置と木の辺を、円板モデルと極座標表示で描く. 色は根からの深さを表す.

    極座標表示では、原点からの双曲的な距離をそのまま半径にとる（偏角は円板モデルと同じ）。
    円板モデルでは境界の近くに集まって見える点の並びを、見やすく広げて表示できる。
    """
    parent, level = make_tree()
    x = embedding()
    z = x[:, 0] + 1j * x[:, 1]
    polar = 2.0 * np.arctanh(np.abs(z)) * np.exp(1j * np.angle(z))
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.4))
    hg_plot.setup_disk(axes[0], "ポアンカレ円板モデル")
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    axes[1].set_title("極座標表示（半径は原点からの双曲的な距離）")
    for ax, points in zip(axes, (z, polar)):
        for i, p in enumerate(parent):
            if p >= 0:
                ax.plot([points[i].real, points[p].real], [points[i].imag, points[p].imag], color="0.6",
                        linewidth=0.8)
        for d in range(max(level) + 1):
            idx = [i for i in range(len(level)) if level[i] == d]
            ax.plot(points[idx].real, points[idx].imag, "o", color=f"C{d}", markersize=6, label=f"深さ {d}")
    axes[0].legend(loc="upper center", bbox_to_anchor=(1.1, 0.02), ncol=4, frameon=False)
    fig.tight_layout()
    return fig


def report() -> None:
    """学習前後の損失と、深さごとの原点からの距離の平均を表示する."""
    parent, level = make_tree()
    related = related_matrix(parent)
    rng = np.random.default_rng(0)
    x0 = rng.uniform(-1e-3, 1e-3, size=(len(parent), 2))
    x = embedding()
    print(f"頂点の数 {len(parent)}、近いはずの組の数 {int(related.sum())}")
    print(f"損失 学習前 {loss_and_grad(x0, related)[0]:.2f} -> 学習後 {loss_and_grad(x, related)[0]:.2f}")
    origin_distance = 2.0 * np.arctanh(np.linalg.norm(x, axis=1))
    for d in range(max(level) + 1):
        mask = np.array(level) == d
        print(f"深さ {d} の頂点の、原点からの距離の平均 {origin_distance[mask].mean():.3f}")


def main() -> None:
    hg_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
