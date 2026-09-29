"""第 3 章: 記述統計。

代表値（平均値・中央値・最頻値）と散布度（範囲・分散・標準偏差・
四分位範囲）を計算する。定義どおりに計算した値と、NumPy・pandas の
関数で計算した値が一致することも確認する。
"""

from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"

FloatArray = npt.NDArray[np.float64]


def mean(values: FloatArray) -> float:
    """平均値を定義どおりに計算する。

    Args:
        values: データ

    Returns:
        データの合計をデータの個数で割った値
    """
    return float(sum(values) / len(values))


def variance(values: FloatArray, ddof: int = 0) -> float:
    """分散を定義どおりに計算する。

    Args:
        values: データ
        ddof: 偏差の 2 乗和を割る数を「データの個数 - ddof」にする。
            0 のとき標本分散、1 のとき不偏分散になる。

    Returns:
        分散
    """
    m = mean(values)
    squared_deviations = [(x - m) ** 2 for x in values]
    return float(sum(squared_deviations) / (len(values) - ddof))


def z_scores(values: FloatArray) -> FloatArray:
    """データを標準化した値（z 得点）を計算する。

    Args:
        values: データ

    Returns:
        平均値が 0、標準偏差が 1 になるように変換したデータ
    """
    result: FloatArray = (values - values.mean()) / values.std()
    return result


def main() -> None:
    """数学の点数について、代表値と散布度を計算する。"""
    scores = pd.read_csv(DATA_PATH)
    math: FloatArray = scores["math"].to_numpy(dtype=np.float64)

    print("--- 代表値 ---")
    print(f"平均値（定義どおり）: {mean(math):.2f}")
    print(f"平均値（NumPy）: {np.mean(math):.2f}")
    print(f"中央値: {np.median(math):.2f}")
    print(f"最頻値: {scores['math'].mode().tolist()}")
    print()

    print("--- 散布度 ---")
    print(f"範囲: {np.max(math) - np.min(math):.2f}")
    print(f"標本分散（定義どおり）: {variance(math, ddof=0):.2f}")
    print(f"標本分散（NumPy）: {np.var(math, ddof=0):.2f}")
    print(f"不偏分散（定義どおり）: {variance(math, ddof=1):.2f}")
    print(f"不偏分散（NumPy）: {np.var(math, ddof=1):.2f}")
    print(f"標準偏差（ddof=1）: {np.std(math, ddof=1):.2f}")
    q1, q3 = np.percentile(math, [25, 75])
    print(f"第 1 四分位数: {q1:.2f}")
    print(f"第 3 四分位数: {q3:.2f}")
    print(f"四分位範囲: {q3 - q1:.2f}")
    print()

    print("--- pandas の describe() ---")
    print(scores[["study_hours", "math", "english"]].describe().round(2))
    print()

    print("--- 標準化（先頭の 5 人） ---")
    z = z_scores(math)
    for point, z_value in zip(math[:5], z[:5]):
        print(f"{point:5.1f} 点 -> z 得点 {z_value:6.2f}")
    print(f"z 得点の平均値: {z.mean():.2f}、標準偏差: {z.std():.2f}")


if __name__ == "__main__":
    main()
