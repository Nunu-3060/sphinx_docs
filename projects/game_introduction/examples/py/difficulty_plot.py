"""Godot のサンプル dodge_lab の記録（CSV）から難易度曲線を描く（8 章 演習 7）。

横軸にブロックの出現間隔、縦軸に生存時間をとる。出現間隔が短いほど難しい。

実行方法:
    py difficulty_plot.py                          同じフォルダーの difficulty_sample.csv を使う
    py difficulty_plot.py dodge_lab_log.csv        自分の記録を使う
    py difficulty_plot.py dodge_lab_log.csv a.png  図をファイルに保存する
"""

import csv
import statistics
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

SAMPLE = Path(__file__).with_name("difficulty_sample.csv")
JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "MS Gothic", "Hiragino Sans", "Noto Sans CJK JP", "Noto Sans JP"]


def use_japanese_font() -> None:
    """インストール済みの日本語フォントを探して、図の文字に使う。"""
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in installed:
            plt.rcParams["font.family"] = name
            return


def load(path: Path) -> dict[float, list[float]]:
    """出現間隔ごとに生存時間の一覧をまとめて返す。"""
    data: dict[float, list[float]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            data.setdefault(float(row["spawn_interval"]), []).append(float(row["survival_time"]))
    return data


def plot(data: dict[float, list[float]], output: Path | None = None) -> None:
    """難易度曲線を描く。output を指定すると表示せずにファイルに保存する。"""
    use_japanese_font()
    intervals = sorted(data, reverse=True)  # 左ほど易しく、右ほど難しく並べる
    labels = [f"{x:g}" for x in intervals]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for i, x in enumerate(intervals):
        ax.scatter([i] * len(data[x]), data[x], color="#9db4d0", s=18, zorder=2)
    means = [statistics.mean(data[x]) for x in intervals]
    ax.plot(range(len(intervals)), means, marker="o", color="#1f5f99", zorder=3, label="平均")
    ax.set_xticks(range(len(intervals)), labels)
    ax.set_xlabel("ブロックの出現間隔 [秒]（右ほど難しい）")
    ax.set_ylabel("生存時間 [秒]")
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    if output is None:
        plt.show()
    else:
        fig.savefig(output, dpi=110)
    plt.close(fig)


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else SAMPLE
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    data = load(path)
    for x in sorted(data, reverse=True):
        print(f"出現間隔 {x:g} 秒: 平均 {statistics.mean(data[x]):5.1f} 秒（{len(data[x])} 回）")
    plot(data, output)


if __name__ == "__main__":
    main()
