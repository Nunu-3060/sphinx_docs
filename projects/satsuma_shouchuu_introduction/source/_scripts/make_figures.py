"""本文で使用する matplotlib の図を生成する。"""

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

JP_FONTS = ["Yu Gothic", "Meiryo", "MS Gothic", "Noto Sans CJK JP", "IPAexGothic"]


def _set_japanese_font() -> None:
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in JP_FONTS:
        if name in available:
            plt.rcParams["font.family"] = name
            return


def make_dilution_chart(path: str) -> None:
    """焼酎の割合と割った後のアルコール分の関係を描く。"""
    ratios = [r / 10 for r in range(1, 11)]
    fig, ax = plt.subplots(figsize=(7, 4.5), dpi=120)
    for degree, color in ((25, "#b5651d"), (20, "#4a7ab5")):
        ax.plot([r * 100 for r in ratios], [degree * r for r in ratios],
                marker="o", color=color, label=f"{degree} 度の焼酎")
    for shochu, water in ((5, 5), (6, 4), (7, 3)):
        value = 25 * shochu / 10
        ax.annotate(f"{shochu}:{water}（約 {value:g} 度）", xy=(shochu * 10, value),
                    xytext=(shochu * 10 - 28, value + 3.5),
                    arrowprops={"arrowstyle": "->", "color": "#555555"}, fontsize=9)
    ax.set_xlabel("全体に占める焼酎の割合（%）")
    ax.set_ylabel("割った後のアルコール分（度）")
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 28)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    ax.set_title("焼酎の割合と割った後のアルコール分（概算）")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main(out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    _set_japanese_font()
    make_dilution_chart(os.path.join(out_dir, "dilution.png"))


if __name__ == "__main__":
    main(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_images"))
