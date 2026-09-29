"""第 10 章: 相関と回帰。

学習時間と数学の点数について、共分散・相関係数を計算し、単回帰分析を
行う。回帰直線と残差のグラフを保存する。保存先のフォルダーは --outdir
で指定する（既定値は output）。
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # 画面に表示せず、ファイルに保存するだけにする

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import numpy.typing as npt  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

DATA_PATH = Path(__file__).parent / "data" / "scores.csv"

FloatArray = npt.NDArray[np.float64]


def least_squares(x: FloatArray, y: FloatArray) -> tuple[float, float]:
    """最小二乗法で回帰直線 y = a + b x の切片 a と傾き b を求める。

    Args:
        x: 説明変数
        y: 目的変数

    Returns:
        切片と傾き
    """
    x_dev = x - x.mean()
    y_dev = y - y.mean()
    slope = float(np.sum(x_dev * y_dev) / np.sum(x_dev ** 2))
    intercept = float(y.mean() - slope * x.mean())
    return intercept, slope


def r_squared(y: FloatArray, predicted: FloatArray) -> float:
    """決定係数を計算する。

    Args:
        y: 目的変数の実測値
        predicted: 回帰直線による予測値

    Returns:
        決定係数
    """
    residual_ss = np.sum((y - predicted) ** 2)
    total_ss = np.sum((y - y.mean()) ** 2)
    return float(1 - residual_ss / total_ss)


def plot_regression(x: FloatArray, y: FloatArray, intercept: float,
                    slope: float, path: Path) -> None:
    """散布図と回帰直線、および残差のグラフを保存する。

    Args:
        x: 説明変数
        y: 目的変数
        intercept: 回帰直線の切片
        slope: 回帰直線の傾き
        path: 保存先のファイル
    """
    predicted = intercept + slope * x
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.scatter(x, y)
    line_x = np.array([x.min(), x.max()])
    ax1.plot(line_x, intercept + slope * line_x, color="red")
    ax1.set_xlabel("Study hours per day")
    ax1.set_ylabel("Math score")
    ax1.set_title("Regression line")

    ax2.scatter(predicted, y - predicted)
    ax2.axhline(0, color="red")
    ax2.set_xlabel("Predicted math score")
    ax2.set_ylabel("Residual")
    ax2.set_title("Residuals")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    """第 10 章のサンプルをすべて実行する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=Path("output"),
                        help="グラフの保存先のフォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(DATA_PATH)
    x: FloatArray = scores["study_hours"].to_numpy(dtype=np.float64)
    y: FloatArray = scores["math"].to_numpy(dtype=np.float64)

    print("--- 相関 ---")
    covariance = np.mean((x - x.mean()) * (y - y.mean()))
    print(f"共分散: {covariance:.3f}")
    r = covariance / (x.std() * y.std())
    print(f"ピアソンの相関係数（定義どおり）: {r:.3f}")
    print(f"ピアソンの相関係数（NumPy）: {np.corrcoef(x, y)[0, 1]:.3f}")
    pearson = stats.pearsonr(x, y)
    print(f"無相関の検定の p 値: {pearson.pvalue:.3g}")
    spearman = stats.spearmanr(x, y)
    print(f"スピアマンの順位相関係数: {spearman.statistic:.3f}")
    print()

    print("--- 単回帰分析 ---")
    intercept, slope = least_squares(x, y)
    print(f"切片（定義どおり）: {intercept:.3f}、"
          f"傾き（定義どおり）: {slope:.3f}")
    fit = stats.linregress(x, y)
    print(f"切片（scipy）: {fit.intercept:.3f}、傾き（scipy）: {fit.slope:.3f}")
    predicted = intercept + slope * x
    print(f"決定係数: {r_squared(y, predicted):.3f}")
    print(f"相関係数の 2 乗: {r ** 2:.3f}")
    print(f"学習時間 4 時間の予測値: {intercept + slope * 4:.1f} 点")

    plot_regression(x, y, intercept, slope, outdir / "ch10_regression.png")


if __name__ == "__main__":
    main()
