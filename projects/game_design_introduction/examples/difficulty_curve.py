"""難易度曲線の 3 つの型を比較する。

* 単調増加型 : 時間とともに一定の割合で難しくなる
* のこぎり型 : レベルの中で難しくなり、次のレベルの最初で少し易しくなる
* 波型       : 山と谷を繰り返しながら、全体として難しくなる

横軸はゲームの進行度（0 が開始、1 が終了）、縦軸は相対的な難易度（0〜1）である。

実行例:
    python difficulty_curve.py                      # グラフを画面に表示する
    python difficulty_curve.py --output curve.png   # グラフを画像として保存する
"""

from __future__ import annotations

import argparse
import math

import matplotlib.pyplot as plt

LEVELS = 5  # のこぎり型で使うレベル数


def linear(progress: float) -> float:
    return 0.1 + 0.8 * progress


def sawtooth(progress: float) -> float:
    """レベルの中では難易度が上がり、レベルが変わると上がった分の半分だけ下がる。"""
    position = min(progress * LEVELS, LEVELS - 1e-9)
    level = int(position)
    within = position - level  # レベル内の進行度（0〜1）
    rise = 0.8 / (LEVELS + 1)  # 1 レベルの中で上がる量
    start = 0.1 + level * rise
    return start + 2.0 * rise * within


def wave(progress: float) -> float:
    """全体の上昇に、緊張と緩和を表す正弦波を重ねる。"""
    return 0.1 + 0.7 * progress + 0.1 * math.sin(progress * 2.0 * math.pi * 4)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", help="グラフを保存するファイル名（省略時は画面に表示する）")
    args = parser.parse_args()

    xs = [i / 500 for i in range(501)]
    curves = {"単調増加型": linear, "のこぎり型": sawtooth, "波型": wave}

    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, (label, curve) in zip(axes, curves.items()):
        ax.plot(xs, [curve(x) for x in xs], linewidth=2)
        ax.set_title(label)
        ax.set_xlabel("ゲームの進行度")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("難易度")
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=110)
    else:
        plt.show()


if __name__ == "__main__":
    main()
