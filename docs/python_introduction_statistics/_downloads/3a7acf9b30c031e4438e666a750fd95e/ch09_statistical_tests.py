"""第 9 章: 代表的な検定手法。

成績データを使い、t 検定・カイ二乗検定・一元配置分散分析・
マン・ホイットニーの U 検定を行う。有意水準はすべて 5 % とする。
"""

from pathlib import Path

import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"
ALPHA = 0.05


def report(name: str, statistic: float, pvalue: float) -> None:
    """検定統計量と p 値、有意水準 5 % での判定を表示する。

    Args:
        name: 検定の名前
        statistic: 検定統計量
        pvalue: p 値
    """
    decision = "棄却する" if pvalue < ALPHA else "棄却しない"
    print(f"{name}: 統計量 = {statistic:.3f}、p 値 = {pvalue:.3g}"
          f" -> 帰無仮説を{decision}")


def main() -> None:
    """成績データに対して各種の検定を行う。"""
    scores = pd.read_csv(DATA_PATH)
    math_a = scores.loc[scores["class"] == "A", "math"]
    math_b = scores.loc[scores["class"] == "B", "math"]

    # 1 標本 t 検定: 全体の数学の平均点は 60 点と言えるか
    result = stats.ttest_1samp(scores["math"], popmean=60)
    report("1 標本 t 検定", result.statistic, result.pvalue)

    # 対応のある t 検定: 同じ生徒の数学と英語の点数に差があるか
    result = stats.ttest_rel(scores["math"], scores["english"])
    report("対応のある t 検定", result.statistic, result.pvalue)

    # Welch の t 検定: A クラスと B クラスで数学の平均点に差があるか
    result = stats.ttest_ind(math_a, math_b, equal_var=False)
    report("Welch の t 検定", result.statistic, result.pvalue)

    # カイ二乗検定: クラスと部活動は独立か
    table = pd.crosstab(scores["class"], scores["club"])
    print()
    print("クラスと部活動の分割表:")
    print(table)
    chi2 = stats.chi2_contingency(table)
    report("カイ二乗検定", chi2.statistic, chi2.pvalue)
    print(f"自由度: {chi2.dof}")
    print()

    # 一元配置分散分析: 部活動によって数学の平均点に差があるか
    groups = [group["math"] for _, group in scores.groupby("club")]
    result = stats.f_oneway(*groups)
    report("一元配置分散分析", result.statistic, result.pvalue)

    # マン・ホイットニーの U 検定: A クラスと B クラスで数学の点数の
    # 分布に差があるか
    result = stats.mannwhitneyu(math_a, math_b, alternative="two-sided")
    report("マン・ホイットニーの U 検定", result.statistic, result.pvalue)


if __name__ == "__main__":
    main()
