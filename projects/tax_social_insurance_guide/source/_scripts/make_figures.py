"""本文で使う matplotlib の図を生成する。conf.py からビルド開始時に呼び出される。"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

import take_home_pay  # noqa: E402

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

MAN = 10_000  # 1 万円


def _man_formatter(value: float, _pos: int) -> str:
    return f"{value:,.0f}"


def fig_income_tax_rate(out: Path) -> None:
    """課税所得金額と所得税の限界税率・実効税率の関係。"""
    xs = [i * 5 * MAN for i in range(1, 1001)]  # 5 万円〜5,000 万円
    marginal = []
    effective = []
    for x in xs:
        for upper, rate, _ in take_home_pay.INCOME_TAX_TABLE:
            if x <= upper:
                marginal.append(rate * 100)
                break
        effective.append(take_home_pay.progressive_income_tax(x) / x * 100)

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    ax.step([x / MAN for x in xs], marginal, where="post", label="限界税率（最後の 1 円にかかる税率）", color="#c0392b")
    ax.plot([x / MAN for x in xs], effective, label="実効税率（所得税額 ÷ 課税所得金額）", color="#2471a3")
    ax.set_xlabel("課税所得金額（万円）")
    ax.set_ylabel("税率（%）")
    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 50)
    ax.xaxis.set_major_formatter(FuncFormatter(_man_formatter))
    ax.grid(alpha=0.3)
    ax.legend(loc="lower right")
    ax.set_title("所得税の累進税率（復興特別所得税を除く）")
    fig.tight_layout()
    fig.savefig(out / "income_tax_rate.png")
    plt.close(fig)


def fig_take_home(out: Path) -> None:
    """年収と手取り額・手取り率の関係（会社員、30 歳、単身）。"""
    salaries = [i * 10 * MAN for i in range(20, 201)]  # 200 万円〜2,000 万円
    results = [take_home_pay.calculate(s) for s in salaries]
    xs = [s / MAN for s in salaries]

    fig, ax1 = plt.subplots(figsize=(8, 4.8), dpi=120)
    ax1.stackplot(
        xs,
        [r.take_home / MAN for r in results],
        [r.social_insurance_total / MAN for r in results],
        [r.tax_total / MAN for r in results],
        labels=["手取り", "社会保険料", "税金（所得税・住民税）"],
        colors=["#7fb3d5", "#f5b041", "#ec7063"],
        alpha=0.9,
    )
    ax1.set_xlabel("年収（万円）")
    ax1.set_ylabel("金額（万円）")
    ax1.set_xlim(200, 2000)
    ax1.xaxis.set_major_formatter(FuncFormatter(_man_formatter))
    ax1.yaxis.set_major_formatter(FuncFormatter(_man_formatter))
    ax1.grid(alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(xs, [r.take_home / r.annual_salary * 100 for r in results], color="#1b2631", linewidth=2,
             label="手取り率（右軸）")
    ax2.set_ylabel("手取り率（%）")
    ax2.set_ylim(50, 100)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left", fontsize=9)
    ax1.set_title("年収と手取りの関係（概算）")
    fig.tight_layout()
    fig.savefig(out / "take_home.png")
    plt.close(fig)


def fig_part_time_wall(out: Path) -> None:
    """パート収入と本人の手取り額。社会保険に加入する場合と扶養内の場合の比較。"""
    salaries = [i * MAN for i in range(80, 251)]  # 80 万円〜250 万円
    xs = [s / MAN for s in salaries]
    enrolled = [take_home_pay.calculate(s).take_home / MAN for s in salaries]
    dependent_xs = [x for x in xs if x < 130]
    dependent = [take_home_pay.calculate(int(x * MAN), enrolled=False).take_home / MAN for x in dependent_xs]

    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=120)
    ax.plot(xs, xs, color="#aab7b8", linestyle=":", label="年収（参考）")
    ax.plot(dependent_xs, dependent, color="#2471a3", linewidth=2, label="家族の扶養に入り、社会保険料を負担しない場合")
    ax.plot(xs, enrolled, color="#c0392b", linewidth=2, label="勤務先の健康保険・厚生年金に加入する場合")
    ax.axvline(130, color="#7d3c98", linestyle="--", linewidth=1)
    ax.text(131, 85, "130 万円", color="#7d3c98")

    # 扶養内の最大手取りを、加入した場合に上回る年収を求める
    best_dependent = max(dependent)
    crossing = next(x for x, y in zip(xs, enrolled) if y >= best_dependent)
    ax.axhline(best_dependent, color="#2471a3", linestyle=":", linewidth=1)
    ax.annotate(f"約 {crossing:.0f} 万円で\n扶養内の手取りに追いつく", xy=(crossing, best_dependent),
                xytext=(crossing + 15, best_dependent - 35), arrowprops={"arrowstyle": "->"})

    ax.set_xlabel("本人の年収（万円）")
    ax.set_ylabel("本人の手取り（万円）")
    ax.set_xlim(80, 250)
    ax.set_ylim(60, 250)
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("パート収入と本人の手取り（概算、30 歳、2026 年の収入）")
    fig.tight_layout()
    fig.savefig(out / "part_time_wall.png")
    plt.close(fig)


def fig_pension_timing(out: Path) -> None:
    """繰上げ・繰下げ受給による年金額の変化と累計受給額。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5), dpi=120)

    ages = list(range(60, 76))
    rates = [100 - (65 - a) * 12 * 0.4 if a < 65 else 100 + (a - 65) * 12 * 0.7 for a in ages]
    colors = ["#ec7063" if a < 65 else "#5dade2" if a > 65 else "#58d68d" for a in ages]
    ax1.bar(ages, rates, color=colors)
    for a, r in zip(ages, rates):
        if a in (60, 65, 70, 75):
            ax1.text(a, r + 3, f"{r:.0f} %", ha="center", fontsize=9)
    ax1.set_xlabel("受給開始年齢（歳）")
    ax1.set_ylabel("65 歳受給開始を 100 とした年金額（%）")
    ax1.set_ylim(0, 200)
    ax1.set_title("受給開始年齢と年金額")
    ax1.grid(axis="y", alpha=0.3)

    lifetime = list(range(60, 101))
    for start, color in ((60, "#ec7063"), (65, "#58d68d"), (70, "#5dade2"), (75, "#7d3c98")):
        rate = 100 - (65 - start) * 12 * 0.4 if start < 65 else 100 + (start - 65) * 12 * 0.7
        totals = [max(0, age - start) * rate / 100 for age in lifetime]
        ax2.plot(lifetime, totals, color=color, label=f"{start} 歳から受給")
    ax2.set_xlabel("年齢（歳）")
    ax2.set_ylabel("累計受給額（65 歳受給開始時の年額 = 1）")
    ax2.set_xlim(60, 100)
    ax2.set_title("累計受給額の比較")
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=9)

    fig.tight_layout()
    fig.savefig(out / "pension_timing.png")
    plt.close(fig)


def main(out: Path) -> None:
    """すべての図を out に出力する。"""
    out.mkdir(parents=True, exist_ok=True)
    fig_income_tax_rate(out)
    fig_take_home(out)
    fig_part_time_wall(out)
    fig_pension_timing(out)


if __name__ == "__main__":
    main(Path(__file__).resolve().parent.parent / "_generated")
