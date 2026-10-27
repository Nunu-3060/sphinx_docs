"""睡眠の章で使う図を生成する。"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from figure_style import BLUE, GRAY, GREEN, LIGHT_BLUE, NAVY, ORANGE, save_figure, setup_style

# 睡眠段階 (グラフの縦軸の位置)
STAGES: dict[str, int] = {"覚醒": 4, "レム睡眠": 3, "N1": 2, "N2": 1, "N3": 0}

# 一晩の睡眠段階の推移の模式図 (段階, 続く時間 [分])。約 90 分の周期を 5 回繰り返す。
HYPNOGRAM: list[tuple[str, int]] = [
    ("覚醒", 10), ("N1", 5), ("N2", 15), ("N3", 45), ("N2", 10), ("レム睡眠", 10),
    ("N1", 3), ("N2", 20), ("N3", 35), ("N2", 15), ("レム睡眠", 17),
    ("N1", 3), ("N2", 35), ("N3", 15), ("N2", 15), ("レム睡眠", 22),
    ("覚醒", 2), ("N1", 3), ("N2", 50), ("レム睡眠", 30),
    ("N1", 3), ("N2", 40), ("レム睡眠", 35), ("覚醒", 10),
]


def hypnogram() -> Path:
    """一晩の睡眠段階の推移 (模式図)。"""
    setup_style()
    times = [0]
    levels = []
    for stage, minutes in HYPNOGRAM:
        levels.append(STAGES[stage])
        times.append(times[-1] + minutes)
    hours = np.array(times) / 60

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.step(hours, levels + [levels[-1]], where="post", color=BLUE, linewidth=1.8)
    # レム睡眠の区間を強調する
    for start, end, level in zip(hours[:-1], hours[1:], levels):
        if level == STAGES["レム睡眠"]:
            ax.plot([start, end], [level, level], color=ORANGE, linewidth=5, solid_capstyle="butt")
    ax.set_yticks(list(STAGES.values()))
    ax.set_yticklabels([f"{name}" if name in ("覚醒", "レム睡眠") else f"ノンレム {name}" for name in STAGES])
    ax.set_xticks(range(0, 9))
    ax.set_xticklabels([f"{(23 + h) % 24}:00" for h in range(0, 9)])
    ax.set_xlim(0, hours[-1])
    ax.set_ylim(-1.3, 4.5)
    ax.annotate("前半は深いノンレム睡眠 (N3) が多い", xy=(0.8, 0), xytext=(1.2, -0.9), fontsize=9,
                arrowprops={"arrowstyle": "->", "color": GRAY})
    ax.annotate("後半はレム睡眠が長くなる", xy=(6.8, 3), xytext=(3.75, 3.65), fontsize=9,
                arrowprops={"arrowstyle": "->", "color": GRAY})
    ax.grid(axis="x", alpha=0.3)
    return save_figure(fig, "hypnogram.png")


def two_process() -> Path:
    """睡眠圧と体内時計による眠気の調節 (2 プロセスモデルの模式図)。"""
    setup_style()
    hours = np.linspace(7, 7 + 48, 2000)  # 1 日目 7:00 から 48 時間
    clock = hours % 24

    # 睡眠圧: 起きている間は増え、眠っている間は減る (23:00〜7:00 に睡眠)
    asleep = (clock >= 23) | (clock < 7)
    pressure = np.zeros_like(hours)
    value = 0.15
    step = hours[1] - hours[0]
    for i, sleeping in enumerate(asleep):
        if sleeping:
            value -= value * step / 3.0
        else:
            value += (1 - value) * step / 18.0
        pressure[i] = value

    # 体内時計による覚醒の働き: 夕方に最も強く、明け方に最も弱い
    alerting = 0.45 + 0.25 * np.cos(2 * np.pi * (hours - 19) / 24)

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(hours, pressure, color=BLUE, linewidth=2, label="睡眠圧 (起きている時間が長いほど高まる)")
    ax.plot(hours, alerting, color=ORANGE, linewidth=2, linestyle="--", label="体内時計による覚醒の働き")
    for day in (0, 24):
        ax.axvspan(23 + day, 31 + day, color=LIGHT_BLUE, alpha=0.6, linewidth=0)
        ax.text(27 + day, 1.0, "睡眠", ha="center", va="top", fontsize=10)
    ax.set_xticks(np.arange(7, 56, 4))
    ax.set_xticklabels([f"{int(h) % 24}:00" for h in np.arange(7, 56, 4)])
    ax.set_xlim(7, 55)
    ax.set_ylim(0, 1.3)
    ax.set_yticks([])
    ax.set_ylabel("強さ (相対値)")
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    return save_figure(fig, "two_process.png")


# 1 日の過ごし方の例 (時刻 [時], 内容, 色, 帯の長さ [時])
DAILY_EVENTS: list[tuple[float, str, str, float]] = [
    (7.0, "起床・朝の光を浴びる", ORANGE, 0.5),
    (7.5, "朝食", GRAY, 0.5),
    (12.0, "昼食", GRAY, 0.75),
    (13.0, "昼寝をするなら\nこの間に 20〜30 分以内", BLUE, 2.0),
    (14.0, "カフェインは\nこのころまで", ORANGE, 0.0),
    (17.5, "運動に向く時間帯", ORANGE, 2.0),
    (20.0, "夕食 (就寝の 3 時間前まで)", GRAY, 0.75),
    (21.5, "入浴 (就寝の 1〜2 時間前)", GREEN, 0.5),
    (22.0, "照明を落とし、画面を控える", BLUE, 1.0),
    (23.0, "就寝", NAVY, 1.0),
]


def daily_timeline() -> Path:
    """体内時計を整える 1 日の過ごし方の例 (7 時起床、23 時就寝)。"""
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.axhline(0, color="black", linewidth=1)
    for i, (start, label, color, length) in enumerate(DAILY_EVENTS):
        if length > 0:
            ax.barh(0, length, left=start, height=0.35, color=color, alpha=0.8)
        else:
            ax.plot([start, start], [-0.3, 0.3], color=color, linewidth=3)
        y = 0.55 + 0.55 * (i % 3) if i % 2 == 0 else -0.55 - 0.55 * (i % 3)
        ax.annotate(label, xy=(start + length / 2, 0.18 if y > 0 else -0.18), xytext=(start + length / 2, y),
                    ha="center", va="center", fontsize=9,
                    arrowprops={"arrowstyle": "-", "color": GRAY, "linewidth": 0.8})
    ax.set_xlim(6, 24.5)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xticks(range(6, 25, 2))
    ax.set_xticklabels([f"{h}:00" for h in range(6, 25, 2)])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    return save_figure(fig, "daily_timeline.png")


def main() -> list[Path]:
    return [hypnogram(), two_process(), daily_timeline()]


if __name__ == "__main__":
    for path in main():
        print(path)
