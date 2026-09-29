"""第 4 章: データの可視化。

ヒストグラム・箱ひげ図・散布図・棒グラフを作成し、PNG ファイルとして
保存する。保存先のフォルダーは --outdir で指定する（既定値は output）。

実行例::

    python ch04_visualization.py --outdir output
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面に表示せず、ファイルに保存するだけにする

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"


def plot_histogram(scores: pd.DataFrame, path: Path) -> None:
    """数学の点数のヒストグラムを保存する。

    Args:
        scores: 成績データの表
        path: 保存先のファイル
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(scores["math"], bins=range(0, 101, 10), edgecolor="black")
    ax.set_xlabel("Math score")
    ax.set_ylabel("Number of students")
    ax.set_title("Histogram of math scores")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_boxplot(scores: pd.DataFrame, path: Path) -> None:
    """クラス別の数学の点数の箱ひげ図を保存する。

    Args:
        scores: 成績データの表
        path: 保存先のファイル
    """
    labels = ["A", "B"]
    groups = [scores.loc[scores["class"] == c, "math"] for c in labels]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(groups, tick_labels=labels)
    ax.set_xlabel("Class")
    ax.set_ylabel("Math score")
    ax.set_title("Math scores by class")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_scatter(scores: pd.DataFrame, path: Path) -> None:
    """学習時間と数学の点数の散布図を保存する。

    Args:
        scores: 成績データの表
        path: 保存先のファイル
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(scores["study_hours"], scores["math"])
    ax.set_xlabel("Study hours per day")
    ax.set_ylabel("Math score")
    ax.set_title("Study hours and math scores")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_bar(scores: pd.DataFrame, path: Path) -> None:
    """部活動ごとの人数の棒グラフを保存する。

    Args:
        scores: 成績データの表
        path: 保存先のファイル
    """
    counts = scores["club"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index, counts.to_numpy())
    ax.set_xlabel("Club")
    ax.set_ylabel("Number of students")
    ax.set_title("Number of students by club")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    """4 種類のグラフを作成して保存する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("output"),
                        help="グラフの保存先のフォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(DATA_PATH)
    plot_histogram(scores, outdir / "ch04_histogram.png")
    plot_boxplot(scores, outdir / "ch04_boxplot.png")
    plot_scatter(scores, outdir / "ch04_scatter.png")
    plot_bar(scores, outdir / "ch04_bar.png")
    print(f"{outdir} にグラフを保存しました。")


if __name__ == "__main__":
    main()
