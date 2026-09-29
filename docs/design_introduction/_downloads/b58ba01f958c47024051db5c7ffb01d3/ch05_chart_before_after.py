"""第 5 章: matplotlib の折れ線グラフを、伝えたいことが伝わる形に改善する。

pandas で作成した製品別の月次売上データを使い、次の 2 枚を保存します。

* ch05_chart_before.png: 装飾が多く、要点が分かりにくいグラフ
* ch05_chart_after.png: 要点の系列だけを強調し、直接ラベルを付けたグラフ

実行例::

    python ch05_chart_before_after.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

HIGHLIGHT = "#1f5fbf"  # 強調する系列の色
MUTED = "#949494"  # 強調しない系列の色 (白地とのコントラスト比 3 : 1)
TEXT_SUB = "#555555"


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する。"""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    available = [name for name in JAPANESE_FONTS if name in installed]
    plt.rcParams["font.family"] = available + ["sans-serif"]


def spread_labels(values: list[float], min_gap: float) -> list[float]:
    """ラベルの y 座標が min_gap 以上離れるように調整した値を返す。

    値の小さい順に見ていき、直前のラベルと近すぎる場合は上へずらす。
    戻り値の順序は引数と同じ。
    """
    order = sorted(range(len(values)), key=lambda i: values[i])
    adjusted = list(values)
    for prev, curr in zip(order, order[1:]):
        adjusted[curr] = max(adjusted[curr], adjusted[prev] + min_gap)
    return adjusted


def make_sales_data(seed: int = 0) -> pd.DataFrame:
    """製品 A〜D の月次売上 (百万円) を作成する。製品 A だけが 7 月から伸びる。"""
    rng = np.random.default_rng(seed)
    months = [f"{m} 月" for m in range(1, 13)]
    trend = np.linspace(0, 1, 12)
    data = {
        "製品 A": 40 + 60 * np.clip(trend - 0.5, 0, None),
        "製品 B": 55 - 5 * trend,
        "製品 C": 35 + 0 * trend,
        "製品 D": 48 - 2 * trend,
    }
    frame = pd.DataFrame(data, index=months)
    noise = rng.normal(0, 1.5, frame.shape)
    return (frame + noise).round(1)


def plot_before(sales: pd.DataFrame, path: Path) -> None:
    """よくある「初期設定のまま + 装飾過多」のグラフ。"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for column in sales.columns:
        ax.plot(sales.index, sales[column], marker="o", linewidth=2,
                label=column)
    ax.set_title("製品別売上推移")
    ax.set_ylabel("売上")
    ax.grid(True, which="both", linestyle="-", linewidth=1)
    ax.legend(loc="upper left", shadow=True, frameon=True)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def plot_after(sales: pd.DataFrame, path: Path, focus: str) -> None:
    """focus の系列だけを強調し、結論をタイトルにしたグラフ。"""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(sales.index))

    # 強調しない系列を先に描き、強調する系列を最前面に描く
    others = [column for column in sales.columns if column != focus]
    for column in others:
        ax.plot(x, sales[column], color=MUTED, linewidth=1.5)
    ax.plot(x, sales[focus], color=HIGHLIGHT, linewidth=3)

    # 凡例の代わりに、線の右端へ系列名を直接書く (重ならないように調整)
    last_values = [float(sales[column].iloc[-1]) for column in sales.columns]
    label_y = spread_labels(last_values, min_gap=2.5)
    for column, y in zip(sales.columns, label_y):
        is_focus = column == focus
        ax.text(x[-1] + 0.3, y, column,
                va="center", fontsize=11,
                color=HIGHLIGHT if is_focus else TEXT_SUB,
                fontweight="bold" if is_focus else "normal")

    # タイトルで結論を述べ、単位は軸ラベルで示す
    ax.set_title(f"{focus} だけが 7 月以降に売上を伸ばした", loc="left",
                 fontsize=15, fontweight="bold")
    ax.set_ylabel("売上 (百万円)", color=TEXT_SUB)
    ax.set_xticks(x[::2], sales.index[::2])
    ax.set_xlim(-0.3, len(x) + 0.7)

    # 上・右・左の枠線と目盛りの線を消し、補助線は横方向だけ薄く表示する
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TEXT_SUB, length=0)
    fig.tight_layout()
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    use_japanese_font()
    sales = make_sales_data()
    print(sales)
    plot_before(sales, outdir / "ch05_chart_before.png")
    plot_after(sales, outdir / "ch05_chart_after.png", focus="製品 A")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
