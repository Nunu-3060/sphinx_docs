"""本文の図と配布用の zip を source/_generated に作る。conf.py からビルドのたびに呼ばれる。"""

import statistics
import sys
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

SOURCE_DIR = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = SOURCE_DIR.parent / "examples"
OUT_DIR = SOURCE_DIR / "_generated"

sys.path.insert(0, str(EXAMPLES_DIR / "py"))

import dice  # noqa: E402
import difficulty_plot  # noqa: E402
import gacha  # noqa: E402
import shuffle  # noqa: E402
import sugoroku  # noqa: E402

BLUE = "#1f5f99"
ORANGE = "#d9822b"
GREEN = "#3a8f5c"
GRAY = "#888888"


def _use_japanese_font() -> None:
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in ["Meiryo", "Yu Gothic", "MS Gothic", "Noto Sans JP"]:
        if name in installed:
            plt.rcParams["font.family"] = name
            return


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT_DIR / name, dpi=100)
    plt.close(fig)


def timeline() -> None:
    """アナログゲームとデジタルゲームの年表（2 章）。"""
    analog = [
        (1824, "兵棋演習\n（クリーグシュピール）"),
        (1889, "任天堂が\n花札の製造を始める"),
        (1935, "モノポリー"),
        (1974, "D&D"),
        (1993, "マジック：\nザ・ギャザリング"),
        (1995, "カタン"),
    ]
    digital = [
        (1958, "Tennis for Two"),
        (1962, "Spacewar!"),
        (1972, "Pong"),
        (1978, "スペース\nインベーダー"),
        (1983, "ファミコン"),
        (1994, "家庭用ゲーム機の\n3D 化"),
        (2003, "Steam"),
        (2008, "スマートフォンの\nアプリストア"),
        (2014, "Godot が\nオープンソースに"),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.6))
    panels = [(axes[0], analog, ORANGE, "アナログゲーム", 1800, 2010), (axes[1], digital, BLUE, "デジタルゲーム", 1950, 2020)]
    levels = [0.35, -0.35, 0.8, -0.8]
    for ax, events, color, label, start, stop in panels:
        ax.hlines(0, start, stop, color=GRAY, linewidth=1)
        ax.set_title(label, color=color, fontsize=11, fontweight="bold", loc="left")
        for i, (year, text) in enumerate(events):
            offset = levels[i % len(levels)]
            ax.plot(year, 0, "o", color=color)
            ax.vlines(year, 0, offset * 0.8, color=color, linewidth=0.8)
            ax.text(year, offset, f"{year}\n{text}" if offset > 0 else f"{text}\n{year}",
                    ha="center", va="bottom" if offset > 0 else "top", fontsize=8)
        margin = (stop - start) * 0.06
        ax.set_xlim(start - margin, stop + margin)
        ax.set_ylim(-1.6, 1.6)
        ax.axis("off")
    _save(fig, "timeline.png")


def dice_distribution() -> None:
    """1d6、2d6、3d6 の和の分布（5 章）。"""
    fig, axes = plt.subplots(1, 3, figsize=(10, 3), sharey=True)
    for ax, n in zip(axes, (1, 2, 3)):
        dist = dice.sum_distribution(n)
        values = sorted(dist)
        ax.bar(values, [float(dist[v]) for v in values], color=BLUE)
        m = float(dice.mean(dist))
        sd = float(dice.variance(dist)) ** 0.5
        ax.set_title(f"{n}d6（期待値 {m:.1f}、標準偏差 {sd:.2f}）", fontsize=10)
        ax.set_xlabel("出目の和")
        ax.set_xticks(values if n < 3 else values[::3])
    axes[0].set_ylabel("確率")
    _save(fig, "dice.png")


def gacha_histogram() -> None:
    """10 種類をそろえるまでの回数の分布（5 章）。"""
    results = gacha.simulate(10, 20_000)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.hist(results, bins=range(10, 101, 2), color=BLUE)
    mean = gacha.expected_draws(10)
    ax.axvline(mean, color=ORANGE, linestyle="--", label=f"期待値 {mean:.1f} 回")
    p90 = sorted(results)[int(len(results) * 0.9)]
    ax.axvline(p90, color=GREEN, linestyle=":", label=f"運の悪い 10 % は {p90} 回以上")
    ax.set_xlabel("全 10 種類がそろうまでに引いた回数")
    ax.set_ylabel("人数（20,000 人中）")
    ax.legend()
    _save(fig, "gacha.png")


def shuffle_bias() -> None:
    """正しいシャッフルと誤ったシャッフルの比較（5 章）。"""
    exact = shuffle.naive_exact(["A", "B", "C"])
    orders = sorted(exact)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    x = range(len(orders))
    ax.bar([i - 0.2 for i in x], [1 / 6] * len(orders), width=0.4, color=BLUE, label="Fisher-Yates（すべて 1/6）")
    ax.bar([i + 0.2 for i in x], [exact[o] / 27 for o in orders], width=0.4, color=ORANGE, label="誤ったシャッフル")
    ax.set_xticks(list(x), orders)
    ax.set_ylabel("その並びになる確率")
    ax.set_ylim(0, 0.25)
    ax.legend(loc="upper right", fontsize=9)
    _save(fig, "shuffle.png")


def sugoroku_skill() -> None:
    """ゴールまでの長さと、振り直しを上手に使う側の勝率（8 章 演習 3）。"""
    lengths = [10, 20, 30, 50, 100, 200, 300]
    skilled = [sugoroku.win_rate(sugoroku.run("basic", n, ("skilled", "random"), 20_000, swap=True)) for n in lengths]
    first = [sugoroku.win_rate(sugoroku.run("basic", n, ("random", "random"), 20_000)) for n in lengths]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.plot(lengths, skilled, marker="o", color=BLUE, label="skilled 対 random での skilled の勝率")
    ax.plot(lengths, first, marker="s", color=ORANGE, label="random 対 random での先手の勝率")
    ax.axhline(0.5, color=GRAY, linewidth=0.8)
    ax.set_xscale("log")
    ax.set_xticks(lengths, [str(n) for n in lengths])
    ax.set_xlabel("ゴールまでのマス数")
    ax.set_ylabel("勝率")
    ax.set_ylim(0.4, 1.02)
    ax.legend(fontsize=9)
    _save(fig, "sugoroku_skill.png")


def sugoroku_gap() -> None:
    """ルールによる、終了時の差（負けた側の残りマス）の分布（8 章 演習 4）。"""
    labels = {"basic": "基本ルール", "catch_up": "追いつきルール", "run_away": "独走ルール"}
    colors = {"basic": GRAY, "catch_up": GREEN, "run_away": ORANGE}
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    for rule in sugoroku.RULES:
        results = sugoroku.run(rule, 30, ("skilled", "random"), 20_000, swap=True)
        gaps = [r.gap for r in results]
        counts = [gaps.count(g) / len(gaps) for g in range(0, 31)]
        ax.plot(range(0, 31), counts, marker=".", color=colors[rule],
                label=f"{labels[rule]}（平均 {statistics.mean(gaps):.1f}）")
    ax.set_xlabel("ゲーム終了時に負けた側が残していたマス数")
    ax.set_ylabel("割合")
    ax.legend(fontsize=9)
    _save(fig, "sugoroku_gap.png")


def difficulty_curve() -> None:
    """演習 7 の記入例の難易度曲線（8 章）。"""
    data = difficulty_plot.load(difficulty_plot.SAMPLE)
    difficulty_plot.plot(data, OUT_DIR / "difficulty.png")


def godot_zip() -> None:
    """Godot のサンプルを zip にまとめる（Godot が作るキャッシュは含めない）。"""
    project = EXAMPLES_DIR / "godot" / "dodge_lab"
    with zipfile.ZipFile(OUT_DIR / "dodge_lab.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(project.rglob("*")):
            relative = path.relative_to(project.parent)
            if path.is_file() and ".godot" not in relative.parts:
                archive.write(path, relative.as_posix())


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    _use_japanese_font()
    timeline()
    dice_distribution()
    gacha_histogram()
    shuffle_bias()
    sugoroku_skill()
    sugoroku_gap()
    difficulty_curve()
    godot_zip()


if __name__ == "__main__":
    main()
