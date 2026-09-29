"""第 7 章: 推定。

A クラスの数学の点数を標本とみなし、母平均の 95 % 信頼区間を求める。
また、シミュレーションで信頼区間の意味を確かめる。
"""

from pathlib import Path

import numpy as np
import numpy.typing as npt
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"
SEED = 7
CONFIDENCE = 0.95

FloatArray = npt.NDArray[np.float64]


def t_interval(sample: FloatArray,
               confidence: float = CONFIDENCE) -> tuple[float, float]:
    """母分散が未知のときの母平均の信頼区間を、t 分布を使って計算する。

    Args:
        sample: 標本
        confidence: 信頼係数（0.95 なら 95 % 信頼区間）

    Returns:
        信頼区間の下限と上限
    """
    n = len(sample)
    mean = float(sample.mean())
    se = float(sample.std(ddof=1)) / np.sqrt(n)  # 標準誤差の推定値
    t_crit = float(stats.t.ppf((1 + confidence) / 2, df=n - 1))
    return mean - t_crit * se, mean + t_crit * se


def z_interval(sample: FloatArray, sigma: float,
               confidence: float = CONFIDENCE) -> tuple[float, float]:
    """母標準偏差 sigma が既知のときの母平均の信頼区間を計算する。

    Args:
        sample: 標本
        sigma: 母標準偏差
        confidence: 信頼係数

    Returns:
        信頼区間の下限と上限
    """
    n = len(sample)
    mean = float(sample.mean())
    z_crit = float(stats.norm.ppf((1 + confidence) / 2))
    half_width = z_crit * sigma / np.sqrt(n)
    return mean - half_width, mean + half_width


def coverage_rate(rng: np.random.Generator, repetitions: int = 1_000,
                  sample_size: int = 20) -> float:
    """母平均が 50 の正規母集団から標本を繰り返し取り出し、
    信頼区間が母平均を含む割合を求める。

    Args:
        rng: 乱数生成器
        repetitions: 標本を取り出す回数
        sample_size: 標本の大きさ

    Returns:
        信頼区間が母平均を含んだ割合
    """
    true_mean = 50.0
    hits = 0
    for _ in range(repetitions):
        sample = rng.normal(true_mean, 10.0, size=sample_size)
        lower, upper = t_interval(sample)
        if lower <= true_mean <= upper:
            hits += 1
    return hits / repetitions


def main() -> None:
    """第 7 章のサンプルをすべて実行する。"""
    scores = pd.read_csv(DATA_PATH)
    sample = scores.loc[scores["class"] == "A", "math"].to_numpy(
        dtype=np.float64)

    print("--- A クラスの数学の点数 ---")
    print(f"標本の大きさ: {len(sample)}")
    print(f"標本平均: {sample.mean():.2f}")
    print(f"不偏分散から求めた標準偏差: {sample.std(ddof=1):.2f}")
    print()

    lower, upper = t_interval(sample)
    print(f"95 % 信頼区間（t 分布）: [{lower:.2f}, {upper:.2f}]")
    lower, upper = stats.t.interval(
        CONFIDENCE, df=len(sample) - 1, loc=sample.mean(),
        scale=stats.sem(sample))
    print(f"95 % 信頼区間（scipy）: [{lower:.2f}, {upper:.2f}]")
    lower, upper = z_interval(sample, sigma=15.0)
    print(f"95 % 信頼区間（母標準偏差 15 が既知の場合）: "
          f"[{lower:.2f}, {upper:.2f}]")
    print()

    rng = np.random.default_rng(SEED)
    rate = coverage_rate(rng)
    print(f"信頼区間が母平均を含んだ割合: {rate:.3f}")


if __name__ == "__main__":
    main()
