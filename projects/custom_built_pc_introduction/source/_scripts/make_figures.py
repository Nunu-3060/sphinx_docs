"""本文で使う matplotlib の図を生成する. conf.py から呼び出される."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrow, Rectangle  # noqa: E402

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]

# 3 章の構成例と同じ値 [W]
CONFIGS: list[tuple[str, int, int, int]] = [
    ("開発・事務用", 90, 0, 60),
    ("ゲーム用", 120, 250, 75),
    ("機械学習用", 170, 450, 100),
]
MARGIN = 1.5
COMMON_CAPACITIES = (450, 550, 650, 750, 850, 1000, 1200, 1300, 1600)


def power_budget(out: Path) -> None:
    """構成例ごとの消費電力の内訳と推奨容量の棒グラフ."""
    names = [c[0] for c in CONFIGS]
    cpu = [c[1] for c in CONFIGS]
    gpu = [c[2] for c in CONFIGS]
    other = [c[3] for c in CONFIGS]
    x = range(len(CONFIGS))

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=120)
    ax.bar(x, cpu, width=0.5, label="CPU", color="#4C78A8")
    ax.bar(x, gpu, width=0.5, bottom=cpu, label="GPU", color="#F58518")
    bottom = [a + b for a, b in zip(cpu, gpu)]
    ax.bar(x, other, width=0.5, bottom=bottom, label="その他", color="#9D9D9D")

    for i, (_, c, g, o) in enumerate(CONFIGS):
        total = c + g + o
        required = total * MARGIN
        recommended = next(cap for cap in COMMON_CAPACITIES if cap >= required)
        ax.text(i, total + 15, f"合計 {total} W", ha="center", fontsize=9)
        ax.hlines(recommended, i - 0.35, i + 0.35, colors="#D62728", linestyles="--")
        ax.text(i + 0.37, recommended, f"推奨 {recommended} W", va="center", fontsize=9, color="#D62728")

    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.set_ylabel("消費電力 [W]")
    ax.set_xlim(-0.6, len(CONFIGS) - 0.1)
    ax.set_ylim(0, 1300)
    ax.set_title("構成例ごとの最大消費電力と推奨電源容量（余裕係数 1.5）")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def _box(ax: plt.Axes, x: float, y: float, w: float, h: float, label: str, color: str) -> None:
    ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#333333"))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=10)


def _arrow(ax: plt.Axes, x: float, y: float, dx: float, dy: float, color: str) -> None:
    ax.add_patch(FancyArrow(x, y, dx, dy, width=0.12, head_width=0.35, head_length=0.3,
                            length_includes_head=True, color=color))


def airflow(out: Path) -> None:
    """ケースを側面から見たエアフローの模式図."""
    fig, ax = plt.subplots(figsize=(7.5, 5), dpi=120)
    ax.add_patch(Rectangle((1, 0.5), 8, 6.5, facecolor="#F4F4F4", edgecolor="#333333", linewidth=2))
    _box(ax, 1.1, 0.6, 7.8, 1.3, "電源ユニット（シュラウド内）", "#D9D9D9")
    _box(ax, 3.2, 2.6, 5.6, 0.7, "GPU", "#FFD8A8")
    _box(ax, 5.6, 4.5, 1.6, 1.4, "CPU\nクーラー", "#BFD7EA")

    blue = "#1F77B4"
    red = "#D62728"
    for y in (2.6, 3.9, 5.2):
        _arrow(ax, -0.2, y, 1.6, 0, blue)
    _arrow(ax, 8.6, 5.2, 1.6, 0, red)
    for x in (5.0, 6.8):
        _arrow(ax, x, 6.6, 0, 1.4, red)
    _arrow(ax, 4.5, -0.6, 0, 1.4, blue)

    ax.text(-0.2, 6.0, "前面：吸気", color=blue, fontsize=11)
    ax.text(8.4, 6.0, "背面：排気", color=red, fontsize=11)
    ax.text(3.0, 7.6, "天面：排気", color=red, fontsize=11)
    ax.text(5.0, -0.4, "底面：電源ユニットの吸気", color=blue, fontsize=10)

    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.8, 8.3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("ケース内のエアフローの例（側面図、左が前面）")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def generate_all(out_dir: Path) -> None:
    """全ての図を out_dir に出力する."""
    out_dir.mkdir(parents=True, exist_ok=True)
    power_budget(out_dir / "power_budget.png")
    airflow(out_dir / "airflow.png")


if __name__ == "__main__":
    generate_all(Path(__file__).resolve().parent.parent / "figures")
