"""第 8 章: k-means 法のスクラッチ実装と、scikit-learn による主成分分析・異常検知。

実行方法:
    python ch08_unsupervised.py
"""
import numpy as np
from numpy.typing import NDArray
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def kmeans(x: FloatArray, k: int, iters: int = 100, seed: int = 0) -> tuple[FloatArray, IntArray]:
    """k-means 法。クラスタ中心と各サンプルの所属クラスタを返す。"""
    rng = np.random.default_rng(seed)
    centers = x[rng.choice(len(x), size=k, replace=False)]
    labels = np.zeros(len(x), dtype=np.int64)
    for _ in range(iters):
        # 1. 各サンプルを最も近い中心のクラスタに割り当てる
        dist = np.linalg.norm(x[:, None, :] - centers[None, :, :], axis=2)
        labels = np.argmin(dist, axis=1)
        # 2. 各クラスタの平均を新しい中心とする
        new_centers = np.array([x[labels == c].mean(axis=0) for c in range(k)])
        if np.allclose(new_centers, centers):
            break
        centers = new_centers
    return centers, labels


def main() -> None:
    rng = np.random.default_rng(0)
    true_centers = np.array([[0.0, 0.0], [4.0, 4.0], [0.0, 5.0]])
    x = np.vstack([rng.normal(c, 0.8, size=(100, 2)) for c in true_centers])

    centers, labels = kmeans(x, k=3)
    print("k-means で求めたクラスタ中心:\n", np.round(centers, 2))
    print("各クラスタのサンプル数:", np.bincount(labels))

    # 手書き数字画像 (8x8 = 64 次元) を主成分分析で 2 次元に圧縮する
    digits = load_digits()
    pca = PCA(n_components=10).fit(digits.data)
    ratio = pca.explained_variance_ratio_
    print("各主成分の寄与率:", np.round(ratio, 3))
    print(f"上位 2 成分の累積寄与率 = {ratio[:2].sum():.3f}, 上位 10 成分 = {ratio.sum():.3f}")
    z = pca.transform(digits.data)[:, :2]
    print("2 次元に圧縮したデータの形状:", z.shape)

    # 正常データから大きく外れた点を Isolation Forest で検出する
    outliers = rng.uniform(-6.0, 10.0, size=(10, 2))
    x_all = np.vstack([x, outliers])
    detector = IsolationForest(contamination=0.03, random_state=0).fit(x_all)
    flags = detector.predict(x_all)  # 1: 正常, -1: 異常
    print("異常と判定された件数:", int(np.sum(flags == -1)))
    print("追加した外れ値のうち異常と判定された件数:", int(np.sum(flags[-10:] == -1)))


if __name__ == "__main__":
    main()
