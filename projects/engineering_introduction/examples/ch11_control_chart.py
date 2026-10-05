"""第 11 章: 管理図 (X̄ 管理図) で工程の変化を検出する。

製品の寸法を 1 時間ごとに 5 個ずつ測定した、という想定の模擬データを
作ります。21 番目の群から、工程の平均がわずかにずれる (標準偏差の
0.5 倍) ようにしてあります。

* 最初の 20 群から管理限界を決める
* 次の 2 つの判定ルールで異常を検出する
  - ルール 1: 点が管理限界の外に出る
  - ルール 2: 9 点が続けて中心線の同じ側に並ぶ

図は ch11_control_chart.png として保存します。

実行例::

    python ch11_control_chart.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

NOMINAL = 10.00  # 寸法の狙い値 [mm]
SIGMA = 0.02  # 工程の標準偏差 [mm]
SUBGROUP = 5  # 1 群のサンプル数
GROUPS = 40  # 群の数
SHIFT_AT = 20  # この番号 (0 始まり) の群から平均がずれる
SHIFT = 0.5  # 平均のずれの大きさ (工程の標準偏差の何倍か)
A2 = 0.577  # 群の大きさ 5 のときの管理限界の係数
RUN_LENGTH = 9  # ルール 2 で数える連続点数


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def make_data(seed: int) -> NDArray[np.float64]:
    """群ごとの測定値 (GROUPS × SUBGROUP の配列) を作る。"""
    rng = np.random.default_rng(seed)
    data = rng.normal(NOMINAL, SIGMA, size=(GROUPS, SUBGROUP))
    data[SHIFT_AT:] += SHIFT * SIGMA  # 工程の平均がずれる
    return data


def run_rule(means: NDArray[np.float64], center: float) -> list[int]:
    """9 点が続けて中心線の同じ側にあるとき、その 9 点目の番号を返す。"""
    alarms = []
    run, side = 0, 0
    for i, mean in enumerate(means):
        current = 1 if mean > center else -1
        run = run + 1 if current == side else 1
        side = current
        if run >= RUN_LENGTH:
            alarms.append(i)
    return alarms


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    data = make_data(seed=3)
    means = data.mean(axis=1)
    ranges = data.max(axis=1) - data.min(axis=1)

    # 管理限界は、工程が安定していた最初の 20 群から決める
    center = float(means[:SHIFT_AT].mean())
    r_bar = float(ranges[:SHIFT_AT].mean())
    ucl = center + A2 * r_bar
    lcl = center - A2 * r_bar
    print(f"中心線 {center:.4f} mm, 上方管理限界 {ucl:.4f} mm, "
          f"下方管理限界 {lcl:.4f} mm")

    outside = [i for i, m in enumerate(means) if not lcl <= m <= ucl]
    runs = run_rule(means, center)
    print(f"ルール 1 (管理限界の外) の群: {[i + 1 for i in outside]}")
    print(f"ルール 2 (9 点連続で同じ側) の群: {[i + 1 for i in runs]}")
    print(f"(工程の平均は {SHIFT_AT + 1} 番目の群からずれています)")

    setup_font()
    fig = Figure(figsize=(8, 4), layout="constrained")
    ax = fig.add_subplot()
    groups = np.arange(1, GROUPS + 1)
    ax.plot(groups, means, "o-", color="tab:blue", markersize=4,
            label="群の平均")
    ax.axhline(center, color="black", linewidth=1, label="中心線")
    ax.axhline(ucl, color="tab:red", linestyle="--", label="管理限界")
    ax.axhline(lcl, color="tab:red", linestyle="--")
    alarms = sorted(set(outside) | set(runs))
    ax.plot(groups[alarms], means[alarms], "o", color="tab:red",
            markersize=9, fillstyle="none", label="異常の判定")
    ax.axvline(SHIFT_AT + 0.5, color="gray", linestyle=":")
    ax.text(SHIFT_AT + 1, lcl, "ここから平均がずれる", va="bottom")
    ax.set_xlabel("群の番号")
    ax.set_ylabel("寸法 [mm]")
    ax.set_title(r"$\bar{X}$ 管理図")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=8)
    fig.savefig(outdir / "ch11_control_chart.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
