"""本文で使う matplotlib の図をまとめて作成する。

conf.py からビルド時に呼び出される。単独で実行することもできる。
すべての図は理論値・仮定の数値による模式図であり、実際の市場データは使っていない。
"""

from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

# 図の出力先 (source/figures)
FIGURE_DIR: Path = Path(__file__).resolve().parent.parent / "figures"

# 日本語を表示できるフォントを優先順に指定する
JAPANESE_FONTS: list[str] = ["Yu Gothic", "Meiryo", "MS Gothic"]

# 系列の色 (区別しやすい色を順に使う)
COLORS: list[str] = ["#2b6cb0", "#dd6b20", "#2f855a", "#9b2c2c", "#6b46c1"]
GRAY: str = "#a0aec0"


def setup_style() -> None:
    """日本語フォントと全体の見た目を設定する。"""
    plt.rcParams["font.family"] = JAPANESE_FONTS
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.color"] = "#e2e8f0"
    plt.rcParams["axes.axisbelow"] = True


def save_figure(fig: Figure, name: str) -> Path:
    """図を PNG として保存し、保存先のパスを返す。"""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path


def man_yen(ax: Axes) -> None:
    """縦軸の目盛りを万円単位の表記にする。"""
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.set_ylabel("金額 (万円)")


def accumulate(monthly: float, annual_rate: float, years: int) -> list[float]:
    """毎月積み立てたときの各年末の残高 (万円) を返す。先頭は 0 年目 (0 円) とする。"""
    monthly_rate = (1.0 + annual_rate) ** (1.0 / 12.0) - 1.0
    balance = 0.0
    result = [0.0]
    for _ in range(years):
        for _ in range(12):
            balance = (balance + monthly) * (1.0 + monthly_rate)
        result.append(balance)
    return result


def inflation_real_value() -> Path:
    """インフレ率別に、預金 100 万円の実質価値の推移を描く。"""
    years = list(range(31))
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    for color, rate in zip(COLORS, [0.01, 0.02, 0.03]):
        values = [100.0 / (1.0 + rate) ** t for t in years]
        ax.plot(years, values, color=color, linewidth=2.2, label=f"インフレ率 {rate:.0%}")
        ax.annotate(f"{values[-1]:.0f} 万円", xy=(30, values[-1]), xytext=(4, 0),
                    textcoords="offset points", va="center", color=color, fontsize=10)
    ax.axhline(100.0, color=GRAY, linestyle="--", linewidth=1.2)
    ax.text(0.5, 101.5, "額面 (100 万円のまま)", color="#4a5568", fontsize=10)
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 110)
    ax.set_xlabel("経過年数")
    man_yen(ax)
    ax.set_ylabel("現在の価値に換算した金額 (万円)")
    ax.legend(loc="lower left")
    return save_figure(fig, "inflation_real_value.png")


def simple_vs_compound() -> Path:
    """100 万円を年 5 % で運用したときの単利と複利を比べる。"""
    years = list(range(31))
    simple = [100.0 * (1.0 + 0.05 * t) for t in years]
    compound = [100.0 * 1.05 ** t for t in years]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(years, compound, color=COLORS[0], linewidth=2.2, label="複利")
    ax.plot(years, simple, color=COLORS[1], linewidth=2.2, label="単利")
    for values, color in ((compound, COLORS[0]), (simple, COLORS[1])):
        ax.annotate(f"{values[-1]:.0f} 万円", xy=(30, values[-1]), xytext=(4, 0),
                    textcoords="offset points", va="center", color=color, fontsize=10)
    ax.set_xlim(0, 34)
    ax.set_xlabel("経過年数")
    man_yen(ax)
    ax.legend(loc="upper left")
    return save_figure(fig, "simple_vs_compound.png")


def accumulation_growth() -> Path:
    """毎月 3 万円を 30 年間積み立てたときの残高を利回り別に描く。"""
    years = list(range(31))
    principal = [3.0 * 12 * t for t in years]
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.fill_between(years, principal, color="#cbd5e0", label="元本 (積み立てた金額)")
    for color, rate in zip(COLORS[1:], [0.03, 0.05]):
        values = accumulate(3.0, rate, 30)
        ax.plot(years, values, color=color, linewidth=2.2, label=f"年 {rate:.0%} で運用")
        ax.annotate(f"{values[-1]:,.0f} 万円", xy=(30, values[-1]), xytext=(4, 0),
                    textcoords="offset points", va="center", color=color, fontsize=10)
    ax.annotate(f"{principal[-1]:,.0f} 万円", xy=(30, principal[-1]), xytext=(4, 0),
                textcoords="offset points", va="center", color="#4a5568", fontsize=10)
    ax.set_xlim(0, 35)
    ax.set_xlabel("経過年数")
    man_yen(ax)
    ax.legend(loc="upper left")
    return save_figure(fig, "accumulation_growth.png")


def cost_difference() -> Path:
    """運用コスト (年率) の違いによる最終残高の差を描く。"""
    years = list(range(31))
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    for color, cost in zip(COLORS, [0.001, 0.008, 0.015]):
        values = accumulate(3.0, 0.05 - cost, 30)
        ax.plot(years, values, color=color, linewidth=2.2, label=f"コスト 年 {cost * 100:.1f} %")
        ax.annotate(f"{values[-1]:,.0f} 万円", xy=(30, values[-1]), xytext=(4, 0),
                    textcoords="offset points", va="center", color=color, fontsize=10)
    ax.set_xlim(0, 35)
    ax.set_xlabel("経過年数")
    man_yen(ax)
    ax.legend(loc="upper left", title="コスト控除前の利回り 年 5 %")
    return save_figure(fig, "cost_difference.png")


def risk_return_map() -> Path:
    """主な金融商品のリスクとリターンの位置関係を模式的に描く。"""
    # (名称, リスクの目安, リターンの目安) いずれも相対的な位置を示す値で、実際の数値ではない
    items: list[tuple[str, float, float]] = [
        ("預貯金", 0.3, 0.3),
        ("個人向け国債", 0.6, 0.6),
        ("国内債券", 1.5, 1.0),
        ("外国債券", 4.0, 2.2),
        ("REIT", 6.5, 3.8),
        ("国内株式", 7.2, 4.3),
        ("外国株式", 8.0, 5.0),
    ]
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    ax.plot([0.0, 9.0], [0.0, 5.6], color=GRAY, linestyle="--", linewidth=1.2)
    for name, risk, ret in items:
        ax.scatter(risk, ret, s=90, color=COLORS[0], zorder=3)
        ax.annotate(name, xy=(risk, ret), xytext=(8, -4), textcoords="offset points", fontsize=10)
    ax.text(5.6, 2.2, "リターンを高めようとすると\nリスクも大きくなる", color="#4a5568", fontsize=10)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("リスク (値動きの大きさ) → 大")
    ax.set_ylabel("期待できるリターン → 大")
    ax.set_title("模式図 (位置は相対的な目安)", fontsize=10, color="#4a5568")
    return save_figure(fig, "risk_return_map.png")


def holding_period_range() -> Path:
    """保有期間と年率リターンのばらつきの関係を描く。

    年率の期待リターン 5 %、標準偏差 18 % の資産を仮定し、
    保有期間 T 年の年率リターンの標準偏差を 18 % / √T として近似する。
    """
    mean = 5.0
    sigma = 18.0
    periods = list(range(1, 31))
    upper = [mean + 2.0 * sigma / t ** 0.5 for t in periods]
    lower = [mean - 2.0 * sigma / t ** 0.5 for t in periods]
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.fill_between(periods, lower, upper, color="#bee3f8", label="おおむね 95 % の結果が入る範囲")
    ax.plot(periods, [mean] * len(periods), color=COLORS[0], linewidth=2.2, label="期待リターン (年 5 %)")
    ax.axhline(0.0, color="#4a5568", linewidth=1.0)
    ax.set_xlim(1, 30)
    ax.set_xlabel("保有期間 (年)")
    ax.set_ylabel("保有期間の年率リターン (%)")
    ax.legend(loc="upper right")
    return save_figure(fig, "holding_period_range.png")


def allocation_examples() -> Path:
    """資産配分の例を積み上げ横棒グラフで描く。"""
    # (名称, 無リスク資産, 債券, 株式) 単位は %
    plans: list[tuple[str, int, int, int]] = [
        ("例 A: 安定重視", 60, 10, 30),
        ("例 B: 中間", 40, 10, 50),
        ("例 C: 成長重視", 20, 0, 80),
    ]
    labels = ["無リスク資産 (預貯金・個人向け国債)", "債券 (投資信託)", "株式 (投資信託)"]
    colors = [GRAY, COLORS[2], COLORS[0]]
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    for row, (name, *weights) in enumerate(plans):
        left = 0
        for index, weight in enumerate(weights):
            if weight == 0:
                continue
            ax.barh(row, weight, left=left, color=colors[index], edgecolor="white",
                    label=labels[index] if row == 0 or (row == 2 and index == 1) else None)
            ax.text(left + weight / 2, row, f"{weight} %", ha="center", va="center", color="white",
                    fontsize=10)
            left += weight
    ax.set_yticks(range(len(plans)))
    ax.set_yticklabels([plan[0] for plan in plans])
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("資産全体に占める割合 (%)")
    ax.grid(False)
    handles, names = ax.get_legend_handles_labels()
    order = [names.index(label) for label in labels]
    ax.legend([handles[i] for i in order], labels, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=3,
              fontsize=9, frameon=False)
    return save_figure(fig, "allocation_examples.png")


def withdrawal_comparison() -> Path:
    """2,000 万円を年 3 % で運用しながら取り崩す場合の定額・定率の違いを描く。"""
    years = list(range(31))
    rate = 0.03
    fixed_amount = [2000.0]
    fixed_withdraw: list[float] = []
    fixed_ratio = [2000.0]
    ratio_withdraw: list[float] = []
    for _ in years[1:]:
        fixed_withdraw.append(min(100.0, fixed_amount[-1]))
        fixed_amount.append(max(0.0, (fixed_amount[-1] - 100.0) * (1.0 + rate)))
        amount = fixed_ratio[-1] * 0.05
        ratio_withdraw.append(amount)
        fixed_ratio.append((fixed_ratio[-1] - amount) * (1.0 + rate))

    fig, (left, right) = plt.subplots(1, 2, figsize=(10.0, 4.4))
    left.plot(years, fixed_amount, color=COLORS[0], linewidth=2.2, label="定額 (毎年 100 万円)")
    left.plot(years, fixed_ratio, color=COLORS[1], linewidth=2.2, label="定率 (毎年 残高の 5 %)")
    left.set_title("残高", fontsize=11)
    left.set_xlabel("取り崩し開始からの年数")
    man_yen(left)
    left.legend(loc="upper right", fontsize=9)

    right.plot(years[1:], fixed_withdraw, color=COLORS[0], linewidth=2.2, label="定額")
    right.plot(years[1:], ratio_withdraw, color=COLORS[1], linewidth=2.2, label="定率")
    right.set_title("その年に受け取る金額", fontsize=11)
    right.set_xlabel("取り崩し開始からの年数")
    man_yen(right)
    right.set_ylim(0, 120)
    right.legend(loc="lower left", fontsize=9)
    return save_figure(fig, "withdrawal_comparison.png")


FIGURES: list[Callable[[], Path]] = [
    inflation_real_value,
    simple_vs_compound,
    accumulation_growth,
    cost_difference,
    risk_return_map,
    holding_period_range,
    allocation_examples,
    withdrawal_comparison,
]


def main() -> None:
    """すべての図を作成する。"""
    setup_style()
    for make in FIGURES:
        make()


if __name__ == "__main__":
    main()
