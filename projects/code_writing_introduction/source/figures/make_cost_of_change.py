"""第 2 章の図「変更にかかる手間の推移（概念図）」を生成する。

このスクリプトと同じフォルダに cost_of_change.png を出力する。
"""

from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUTPUT_PATH = Path(__file__).with_name("cost_of_change.png")


def main() -> None:
    plt.rcParams["font.family"] = "Yu Gothic"

    elapsed = np.linspace(0.0, 10.0, 200)
    bad_code_cost = 1.0 + 0.04 * np.exp(0.45 * elapsed)
    good_code_cost = 1.3 + 0.08 * elapsed

    fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=120)
    ax.plot(elapsed, bad_code_cost, color="#d62728", linewidth=2.5, label="悪いコード")
    ax.plot(elapsed, good_code_cost, color="#1f77b4", linewidth=2.5, label="良いコード")

    ax.set_xlabel("開発を始めてからの時間")
    ax.set_ylabel("機能を 1 つ追加する手間")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 4.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper left", frameon=False)
    ax.text(9.9, 0.15, "※ 説明のための概念図であり、実測値ではない", ha="right", fontsize=9, color="#555555")

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    main()
