"""第 2 章: データの読み込みと確認。

data/scores.csv を pandas で読み込み、データの大きさ・列の型・
質的変数の度数を確認する。また、欠損値の確認と処理の方法を示す。
"""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"


def load_scores(path: Path = DATA_PATH) -> pd.DataFrame:
    """成績データを CSV ファイルから読み込む。

    Args:
        path: CSV ファイルのパス

    Returns:
        成績データの表
    """
    return pd.read_csv(path)


def show_overview(scores: pd.DataFrame) -> None:
    """データの大きさ、先頭の数行、各列の型を表示する。

    Args:
        scores: 成績データの表
    """
    print("行数と列数:", scores.shape)
    print()
    print("先頭の 5 行:")
    print(scores.head())
    print()
    print("各列の型:")
    print(scores.dtypes)


def show_frequency(scores: pd.DataFrame) -> None:
    """質的変数（クラスと部活動）の度数を表示する。

    Args:
        scores: 成績データの表
    """
    print("クラスごとの人数:")
    print(scores["class"].value_counts())
    print()
    print("部活動ごとの人数:")
    print(scores["club"].value_counts())


def show_missing_values() -> None:
    """欠損値を含む小さな表を使い、欠損値の確認と処理を示す。"""
    data = pd.DataFrame({
        "math": [70.0, np.nan, 55.0, 80.0],
        "english": [65.0, 72.0, np.nan, 90.0],
    })
    print("欠損値を含む表:")
    print(data)
    print()
    print("列ごとの欠損値の個数:")
    print(data.isna().sum())
    print()
    print("欠損値を含む行を削除した表:")
    print(data.dropna())
    print()
    print("欠損値を無視して計算した平均値:")
    print(data.mean())


def main() -> None:
    """第 2 章のサンプルをすべて実行する。"""
    scores = load_scores()
    show_overview(scores)
    print()
    show_frequency(scores)
    print()
    show_missing_values()


if __name__ == "__main__":
    main()
