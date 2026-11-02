"""茶外茶と茶・コーヒーのカフェイン量を比較する棒グラフを生成する。"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# 浸出液 100 mL あたりのカフェイン量（mg）
# 出典：文部科学省「日本食品標準成分表」、厚生労働省「食品に含まれるカフェインの過剰摂取についてQ&A」
DRINKS: list[tuple[str, float]] = [
    ("玉露", 160),
    ("コーヒー", 60),
    ("紅茶", 30),
    ("煎茶", 20),
    ("ほうじ茶", 20),
    ("ウーロン茶", 20),
    ("麦茶", 0),
]

TEA_COLOR = "#8a6d3b"
TISANE_COLOR = "#3b8a5a"


def make(output: Path) -> None:
    """棒グラフを PNG で output に保存する。"""
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "sans-serif"]

    names = [name for name, _ in DRINKS]
    values = [value for _, value in DRINKS]
    colors = [TISANE_COLOR if name == "麦茶" else TEA_COLOR for name in names]

    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=100)
    bars = ax.barh(names, values, color=colors)
    ax.invert_yaxis()
    ax.set_xlabel("カフェイン量（mg／浸出液 100 mL）")
    ax.set_xlim(0, 180)
    ax.spines[["top", "right"]].set_visible(False)
    for bar, value in zip(bars, values):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height() / 2, f"{value:g}", va="center")
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)
