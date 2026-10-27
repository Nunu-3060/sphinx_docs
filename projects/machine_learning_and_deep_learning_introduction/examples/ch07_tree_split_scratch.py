"""第 7 章: 決定木の分割をジニ不純度で選ぶ処理を NumPy でスクラッチ実装する。

決定木の学習は「不純度が最も下がる (特徴量, しきい値) の組を探して分割する」ことの繰り返しである。
ここでは 1 回分の分割の探索だけを実装する。

実行方法:
    python ch07_tree_split_scratch.py
"""
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


def gini(y: IntArray) -> float:
    """ジニ不純度 1 - sum_k p_k^2 を計算する。"""
    if y.size == 0:
        return 0.0
    p = np.bincount(y) / y.size
    return float(1.0 - np.sum(p ** 2))


def best_split(x: FloatArray, y: IntArray) -> tuple[int, float, float]:
    """不純度の減少量が最大となる (特徴量の番号, しきい値, 減少量) を返す。"""
    n, d = x.shape
    parent = gini(y)
    best = (-1, 0.0, 0.0)
    for j in range(d):
        values = np.unique(x[:, j])
        # 隣り合う値の中点をしきい値の候補とする
        for threshold in (values[:-1] + values[1:]) / 2.0:
            left = y[x[:, j] <= threshold]
            right = y[x[:, j] > threshold]
            # 子ノードの不純度を、サンプル数で重み付けして平均する
            child = (left.size * gini(left) + right.size * gini(right)) / n
            gain = parent - child
            if gain > best[2]:
                best = (j, float(threshold), gain)
    return best


def main() -> None:
    # 特徴量 0: 年齢, 特徴量 1: 年収 (百万円), ラベル: 商品を購入したか (1: 購入)
    x = np.array([
        [25.0, 3.0], [32.0, 4.5], [47.0, 8.0], [51.0, 6.5],
        [23.0, 2.5], [38.0, 7.5], [60.0, 5.0], [44.0, 9.0],
    ])
    y = np.array([0, 0, 1, 1, 0, 1, 0, 1], dtype=np.int64)

    print(f"分割前のジニ不純度 = {gini(y):.3f}")
    feature, threshold, gain = best_split(x, y)
    names = ["年齢", "年収"]
    print(f"最良の分割: {names[feature]} <= {threshold} (不純度の減少量 = {gain:.3f})")

    mask = x[:, feature] <= threshold
    print("左の子ノードのラベル:", y[mask], " 右の子ノードのラベル:", y[~mask])


if __name__ == "__main__":
    main()
