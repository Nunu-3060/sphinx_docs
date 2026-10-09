"""レーダーチャート: 複数の評価項目をまとめて比較する.

架空の 2 つのデータベース製品を、5 つの観点の評価（5 段階）で比較する。

使い方: python ch03_radar.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.projections.polar import PolarAxes

import jpfont

AXES = ["性能", "運用のしやすさ", "拡張性", "費用の安さ", "情報の多さ"]
SCORES = {
    "製品 P": [4, 3, 5, 2, 4],
    "製品 Q": [3, 5, 3, 4, 3],
}


def create_figure() -> Figure:
    """2 製品の評価をレーダーチャートで描く."""
    # 各評価項目の角度。多角形を閉じるため、最初の角度を末尾に加える
    angles = np.linspace(0, 2 * np.pi, len(AXES), endpoint=False)
    closed_angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(4.8, 4.8))
    ax = fig.add_subplot(projection="polar")
    assert isinstance(ax, PolarAxes)  # 極座標専用のメソッドを使うため
    for name, scores in SCORES.items():
        values = scores + scores[:1]
        ax.plot(closed_angles, values, label=name)
        ax.fill(closed_angles, values, alpha=0.2)
    ax.set_theta_offset(np.pi / 2)   # 最初の項目を真上に置く
    ax.set_theta_direction(-1)       # 時計回りに並べる
    ax.set_xticks(angles, AXES)
    # 項目名が円に重ならないよう、右側の項目は左揃え、左側の項目は右揃えにする
    for label, angle in zip(ax.get_xticklabels(), angles):
        x = np.sin(angle)
        label.set_horizontalalignment(
            "left" if x > 0.1 else "right" if x < -0.1 else "center")
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_rlabel_position(36)  # 目盛りの数値を項目の間に置く
    ax.legend(loc="upper left", bbox_to_anchor=(1.05, 1.1))
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
