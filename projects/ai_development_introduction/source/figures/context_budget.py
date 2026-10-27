"""コンテキストウィンドウの内訳を示す図を生成する（conf.py から呼び出す）。"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CATEGORIES = [
    "システムプロンプト",
    "ツール定義",
    "規約ファイル",
    "読み込んだファイル",
    "会話履歴",
    "ツールの実行結果",
]
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
FREE_COLOR = "#e4e3df"
# 濃い色の区画では、数値を白で表示して読みやすくする
DARK_COLORS = {"#2a78d6", "#008300"}

# コンテキストウィンドウに占める割合（%）。説明のための例であり、実測値ではない。
BARS = {
    "整理前": [3, 12, 4, 30, 25, 22],
    "整理後": [3, 6, 4, 12, 8, 7],
}


def make(out_path: Path) -> None:
    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]
    fig, ax = plt.subplots(figsize=(9, 3.0), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    labels = list(BARS)[::-1]
    for y, name in enumerate(labels):
        left = 0
        for value, color, cat in zip(BARS[name], COLORS, CATEGORIES):
            ax.barh(y, value, left=left, color=color, edgecolor="#ffffff", linewidth=2, height=0.6,
                    label=cat if y == 0 else None)
            if value >= 6:
                ax.text(left + value / 2, y, f"{value}%", ha="center", va="center", fontsize=9,
                        color="#ffffff" if color in DARK_COLORS else "#0b0b0b")
            left += value
        free = 100 - left
        ax.barh(y, free, left=left, color=FREE_COLOR, edgecolor="#ffffff", linewidth=2, height=0.6,
                label="空き（応答と以降の作業に使える）" if y == 0 else None)
        if free >= 10:
            ax.text(left + free / 2, y, f"空き {free}%", ha="center", va="center", fontsize=9, color="#52514e")
    ax.set_yticks(range(len(labels)), labels, fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_xlabel("コンテキストウィンドウに占める割合（%）", fontsize=9, color="#52514e")
    ax.tick_params(colors="#52514e", labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#b5b4ae")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4, fontsize=8.5, frameon=False)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    make(Path(__file__).resolve().parent.parent / "_generated" / "context_budget.png")
