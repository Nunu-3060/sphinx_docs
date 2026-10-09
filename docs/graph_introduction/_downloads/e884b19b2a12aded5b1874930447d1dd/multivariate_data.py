"""第 8 章のサンプルで共通に使う、多次元の架空データ.

3 機種のセンサー機器、各 50 台について、4 つの項目を測定した値を作る。
"""

import numpy as np

FEATURES = ["消費電力", "温度", "騒音", "処理速度"]
UNITS = ["W", "℃", "dB", "件/秒"]
GROUPS = ["機種 A", "機種 B", "機種 C"]
COUNT = 50  # 1 機種あたりの台数

# 機種ごとの各項目の平均と標準偏差
_MEANS = np.array([
    [40.0, 45.0, 30.0, 120.0],
    [55.0, 52.0, 38.0, 150.0],
    [48.0, 60.0, 33.0, 135.0],
])
_STDS = np.array([4.0, 3.0, 2.5, 10.0])


def make_dataset() -> tuple[np.ndarray, np.ndarray]:
    """測定値（行が機器、列が項目）と、機種の番号の配列を返す."""
    rng = np.random.default_rng(10)
    rows = []
    labels = []
    for group, means in enumerate(_MEANS):
        base = rng.normal(0, 1, (COUNT, 1))  # 項目どうしの相関を作る共通成分
        noise = rng.normal(0, 1, (COUNT, len(FEATURES)))
        weights = np.array([0.8, 0.6, 0.5, 0.7])
        values = means + _STDS * (weights * base
                                  + np.sqrt(1 - weights ** 2) * noise)
        rows.append(values)
        labels.append(np.full(COUNT, group))
    return np.vstack(rows), np.concatenate(labels)
