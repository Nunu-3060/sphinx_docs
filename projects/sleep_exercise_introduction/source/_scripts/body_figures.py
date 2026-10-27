"""身体の基礎知識と姿勢の章で使う図を生成する。"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

from figure_style import BLUE, GRAY, GREEN, LIGHT_BLUE, ORANGE, save_figure, setup_style


def energy_breakdown() -> Path:
    """1 日のエネルギー消費量の内訳 (おおよその割合)。"""
    setup_style()
    parts = [("基礎代謝\n約 60%", 60, BLUE), ("", 10, GRAY), ("身体活動\n約 30%", 30, ORANGE)]
    fig, ax = plt.subplots(figsize=(8, 2.6))
    left = 0
    for label, value, color in parts:
        ax.barh(0, value, left=left, color=color, height=0.6, edgecolor="white")
        ax.text(left + value / 2, 0, label, ha="center", va="center", color="white", fontsize=10)
        left += value
    # 幅の狭い部分は、名前を棒の上に書く
    ax.annotate("食事誘発性熱産生 約 10%", xy=(65, 0.3), xytext=(65, 0.75), ha="center", fontsize=9,
                arrowprops={"arrowstyle": "-", "color": GRAY})
    # 身体活動の内訳を示す
    ax.annotate("", xy=(70, -0.45), xytext=(100, -0.45),
                arrowprops={"arrowstyle": "<->", "color": GRAY})
    ax.text(85, -0.62, "運動 + 運動以外の身体活動 (NEAT)", ha="center", va="top", fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.0, 0.95)
    ax.axis("off")
    return save_figure(fig, "energy_breakdown.png")


# 首の前傾角度 [度] と、首にかかる負荷の推定値 [kg] (Hansraj, 2014 による)
NECK_LOADS: list[tuple[int, float]] = [(0, 5), (15, 12), (30, 18), (45, 22), (60, 27)]


def neck_load() -> Path:
    """頭の前傾角度と首にかかる負荷の推定値。"""
    setup_style()
    angles = [a for a, _ in NECK_LOADS]
    loads = [w for _, w in NECK_LOADS]
    fig, ax = plt.subplots(figsize=(7, 3.4))
    bars = ax.bar([f"{a} 度" for a in angles], loads, color=[BLUE] + [ORANGE] * 4, width=0.6)
    for bar, load in zip(bars, loads):
        ax.text(bar.get_x() + bar.get_width() / 2, load + 0.6, f"約 {load:g} kg", ha="center", fontsize=10)
    ax.set_xlabel("頭を前に傾けた角度")
    ax.set_ylabel("首にかかる負荷 (kg)")
    ax.set_ylim(0, 31)
    ax.grid(axis="y", alpha=0.3)
    return save_figure(fig, "neck_load.png")


def _limb(ax: Axes, points: list[tuple[float, float]], width: float = 9, color: str = LIGHT_BLUE) -> None:
    """人の手足や胴を太い線で描く。"""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=width, solid_capstyle="round", solid_joinstyle="round", zorder=3)


def _note(ax: Axes, text: str, xy: tuple[float, float], xytext: tuple[float, float]) -> None:
    """図の中の説明文を矢印付きで書く。"""
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9, va="center",
                arrowprops={"arrowstyle": "->", "color": GRAY, "linewidth": 0.8}, zorder=5)


def desk_layout() -> Path:
    """モニター・椅子・机の位置関係 (側面から見た模式図)。単位はおおよそ cm。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))

    # 床
    ax.plot([-5, 150], [0, 0], color="black", linewidth=1)
    # 椅子 (座面、支柱、脚、背もたれ)
    ax.add_patch(Rectangle((12, 40), 42, 4, color=GRAY, zorder=2))
    ax.add_patch(Rectangle((31, 4), 4, 36, color=GRAY, zorder=2))
    ax.plot([14, 52], [3, 3], color=GRAY, linewidth=4)
    ax.add_patch(Rectangle((8, 44), 4, 50, color=GRAY, zorder=2))
    # 机と天板の上の機器
    ax.add_patch(Rectangle((58, 70), 80, 3, color="#b08d6a", zorder=2))
    ax.add_patch(Rectangle((132, 0), 3, 70, color="#b08d6a", zorder=2))
    ax.add_patch(Rectangle((62, 73), 16, 2, color="black", zorder=2))  # キーボード
    ax.add_patch(Rectangle((110, 73), 14, 1.5, color="black", zorder=2))  # モニターの台座
    ax.add_patch(Rectangle((115.5, 74.5), 3, 16, color="black", zorder=2))  # モニターの支柱
    ax.add_patch(Rectangle((112, 88), 3, 32, color="#333333", zorder=2))  # 画面

    # 人 (右を向いて座る)
    arm_color = "#9dbbd8"
    _limb(ax, [(22, 50), (24, 100)], width=22)  # 胴
    _limb(ax, [(25, 100), (27, 110)], width=9)  # 首
    _limb(ax, [(24, 50), (64, 52)], width=14)  # 太もも
    _limb(ax, [(64, 50), (66, 6)], width=10)  # すね
    _limb(ax, [(64, 3), (80, 3)], width=7)  # 足
    _limb(ax, [(25, 99), (31, 77)], width=7, color=arm_color)  # 上腕
    _limb(ax, [(31, 77), (66, 78)], width=6, color=arm_color)  # 前腕
    ax.add_patch(Circle((28, 120), 11, color=LIGHT_BLUE, zorder=3))  # 頭
    ax.add_patch(Circle((35, 122), 1.3, color="black", zorder=4))  # 目

    # 視線と視距離
    ax.plot([36, 112], [122, 106], color=BLUE, linestyle="--", linewidth=1)
    ax.add_patch(FancyArrowPatch((36, 132), (112, 132), arrowstyle="<->", mutation_scale=12, color=GREEN))
    ax.text(74, 134, "視距離はおおむね 40 cm 以上", ha="center", va="bottom", fontsize=10, color=GREEN)
    ax.plot([36, 120], [122, 122], color=GREEN, linewidth=0.8, linestyle=":")

    _note(ax, "画面の上端は目の高さと\nほぼ同じか、やや下", (114, 120), (124, 108))
    _note(ax, "上腕と前腕の角度は\n90 度以上", (32, 79), (38, 94))
    _note(ax, "背もたれで腰を支え、\n骨盤を立てて座る", (8, 62), (-32, 28))
    _note(ax, "膝の角度はおおむね 90 度", (64, 50), (70, 40))
    _note(ax, "足裏全体を床につける\n(届かなければ足台を使う)", (76, 4), (86, 18))
    _note(ax, "キーボードは\n肘の高さ付近に", (72, 75), (76, 92))

    ax.set_xlim(-34, 150)
    ax.set_ylim(-2, 142)
    ax.set_aspect("equal")
    ax.axis("off")
    return save_figure(fig, "desk_layout.png")


def main() -> list[Path]:
    return [energy_breakdown(), neck_load(), desk_layout()]


if __name__ == "__main__":
    for path in main():
        print(path)
