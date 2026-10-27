"""給与収入（年収）から社会保険料・税金・手取り額を概算するスクリプト。

2026 年（令和 8 年）中の給与収入を想定し、次の前提で計算する。

* 会社員（協会けんぽ・厚生年金に加入）で、給与以外の収入はない。
* 賞与はなく、毎月同じ額の給与を受け取る。
* 扶養親族はなく、所得控除は基礎控除と社会保険料控除のみとする。
* 健康保険料率は協会けんぽの全国平均（9.9 %）を使う。
* 住民税は、2026 年の所得に対して翌年度（令和 9 年度）に課される額を計算する。
* 標準報酬月額の等級表は使わず、月給をそのまま標準報酬月額とみなす（上限と下限は考慮する）。

実際の金額は、都道府県ごとの保険料率、賞与の有無、各種控除などにより異なる。
結果はあくまで目安として利用すること。

使い方::

    python take_home_pay.py 5000000
    python take_home_pay.py 5000000 --age 45
    python take_home_pay.py 1200000 --no-social-insurance
"""

from __future__ import annotations

import argparse
import unicodedata
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# 料率・控除額などの前提（2026 年 10 月時点）
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Assumptions:
    """社会保険料の計算に使う料率と上限。料率は労使合計の値で持つ。"""

    health_rate: float = 0.099  # 健康保険料率（協会けんぽ全国平均）
    care_rate: float = 0.0162  # 介護保険料率（40 歳以上 65 歳未満）
    child_support_rate: float = 0.0023  # 子ども・子育て支援金率
    pension_rate: float = 0.183  # 厚生年金保険料率
    employment_rate_employee: float = 0.005  # 雇用保険料率（労働者負担分、一般の事業）
    health_monthly_floor: int = 58_000  # 健康保険の標準報酬月額の下限
    health_monthly_cap: int = 1_390_000  # 健康保険の標準報酬月額の上限
    pension_monthly_floor: int = 88_000  # 厚生年金の標準報酬月額の下限
    pension_monthly_cap: int = 650_000  # 厚生年金の標準報酬月額の上限


# 所得税の速算表: (課税所得金額の上限, 税率, 控除額)
INCOME_TAX_TABLE: tuple[tuple[float, float, int], ...] = (
    (1_949_000, 0.05, 0),
    (3_299_000, 0.10, 97_500),
    (6_949_000, 0.20, 427_500),
    (8_999_000, 0.23, 636_000),
    (17_999_000, 0.33, 1_536_000),
    (39_999_000, 0.40, 2_796_000),
    (float("inf"), 0.45, 4_796_000),
)

RECONSTRUCTION_TAX_RATE = 0.021  # 復興特別所得税（2026 年分）
RESIDENT_INCOME_LEVY_RATE = 0.10  # 住民税の所得割（標準税率）
RESIDENT_PER_CAPITA_LEVY = 5_000  # 住民税の均等割（森林環境税 1,000 円を含む）
RESIDENT_TAX_EXEMPTION_LIMIT = 450_000  # 住民税が非課税となる合計所得金額（単身・1 級地）


@dataclass(frozen=True)
class Result:
    """計算結果。金額はすべて年額（円）。"""

    annual_salary: int
    health_insurance: int
    care_insurance: int
    child_support: int
    pension: int
    employment_insurance: int
    income_tax: int
    resident_tax: int

    @property
    def social_insurance_total(self) -> int:
        """社会保険料の合計。"""
        return (self.health_insurance + self.care_insurance + self.child_support
                + self.pension + self.employment_insurance)

    @property
    def tax_total(self) -> int:
        """税金の合計。"""
        return self.income_tax + self.resident_tax

    @property
    def take_home(self) -> int:
        """手取り額。"""
        return self.annual_salary - self.social_insurance_total - self.tax_total


# ---------------------------------------------------------------------------
# 社会保険料
# ---------------------------------------------------------------------------


def employee_share(monthly_wage: float, floor: int, cap: int, rate: float) -> int:
    """標準報酬月額に料率を掛け、本人負担分（半額）の年額を返す。"""
    standard = min(max(monthly_wage, floor), cap)
    return round(standard * rate / 2) * 12


def social_insurance(annual_salary: int, age: int, assumptions: Assumptions) -> dict[str, int]:
    """本人が負担する社会保険料（年額）を項目ごとに返す。"""
    monthly = annual_salary / 12
    a = assumptions
    health_floor, health_cap = a.health_monthly_floor, a.health_monthly_cap
    care = employee_share(monthly, health_floor, health_cap, a.care_rate) if 40 <= age < 65 else 0
    pension = 0
    if age < 70:
        pension = employee_share(monthly, a.pension_monthly_floor, a.pension_monthly_cap, a.pension_rate)
    return {
        "health": employee_share(monthly, health_floor, health_cap, a.health_rate),
        "care": care,
        "child_support": employee_share(monthly, health_floor, health_cap, a.child_support_rate),
        "pension": pension,
        "employment": round(annual_salary * a.employment_rate_employee),
    }


# ---------------------------------------------------------------------------
# 所得税
# ---------------------------------------------------------------------------


def salary_income_deduction(salary: int, minimum: int) -> int:
    """給与所得控除額を返す。minimum は最低保障額。"""
    if salary <= 1_900_000:
        amount = 0.0
    elif salary <= 3_600_000:
        amount = salary * 0.3 + 80_000
    elif salary <= 6_600_000:
        amount = salary * 0.2 + 440_000
    elif salary <= 8_500_000:
        amount = salary * 0.1 + 1_100_000
    else:
        amount = 1_950_000
    return min(salary, max(minimum, int(amount)))


def basic_deduction_income_tax(total_income: int) -> int:
    """所得税の基礎控除額（令和 8 年分）を返す。"""
    if total_income <= 4_890_000:
        return 1_040_000  # 本則 62 万円 + 特例 42 万円
    if total_income <= 6_550_000:
        return 670_000  # 本則 62 万円 + 特例 5 万円
    if total_income <= 23_500_000:
        return 620_000
    if total_income <= 24_000_000:
        return 480_000
    if total_income <= 24_500_000:
        return 320_000
    if total_income <= 25_000_000:
        return 160_000
    return 0


def progressive_income_tax(taxable: int) -> int:
    """速算表を使って課税所得金額から所得税額（復興特別所得税を除く）を返す。"""
    for upper, rate, subtract in INCOME_TAX_TABLE:
        if taxable <= upper:
            return max(0, int(taxable * rate) - subtract)
    raise ValueError("課税所得金額が速算表の範囲外である。")


def income_tax(annual_salary: int, social_insurance_total: int) -> int:
    """所得税と復興特別所得税の合計額を返す。"""
    # 令和 8 年分の給与所得控除の最低保障額は 74 万円（本則 69 万円 + 特例 5 万円）
    total_income = annual_salary - salary_income_deduction(annual_salary, 740_000)
    deductions = basic_deduction_income_tax(total_income) + social_insurance_total
    taxable = max(0, total_income - deductions) // 1_000 * 1_000
    total = int(progressive_income_tax(taxable) * (1 + RECONSTRUCTION_TAX_RATE))
    return total // 100 * 100


# ---------------------------------------------------------------------------
# 住民税
# ---------------------------------------------------------------------------


def basic_deduction_resident_tax(total_income: int) -> int:
    """住民税の基礎控除額を返す。"""
    if total_income <= 24_000_000:
        return 430_000
    if total_income <= 24_500_000:
        return 290_000
    if total_income <= 25_000_000:
        return 150_000
    return 0


def adjustment_deduction(taxable: int, total_income: int) -> int:
    """調整控除額（扶養親族がない場合）を返す。"""
    if total_income > 25_000_000:
        return 0
    gap = 50_000  # 基礎控除の所得税と住民税の差
    if taxable <= 2_000_000:
        return int(min(gap, taxable) * 0.05)
    return max(2_500, int((gap - (taxable - 2_000_000)) * 0.05))


def resident_tax(annual_salary: int, social_insurance_total: int) -> int:
    """住民税（所得割と均等割）の合計額を返す。"""
    # 令和 9 年度分の住民税の給与所得控除の最低保障額は 74 万円
    total_income = annual_salary - salary_income_deduction(annual_salary, 740_000)
    if total_income <= RESIDENT_TAX_EXEMPTION_LIMIT:
        return 0
    deductions = basic_deduction_resident_tax(total_income) + social_insurance_total
    taxable = max(0, total_income - deductions) // 1_000 * 1_000
    levy = int(taxable * RESIDENT_INCOME_LEVY_RATE) - adjustment_deduction(taxable, total_income)
    levy = max(0, levy) // 100 * 100
    return levy + RESIDENT_PER_CAPITA_LEVY


# ---------------------------------------------------------------------------
# まとめ
# ---------------------------------------------------------------------------


def calculate(annual_salary: int, age: int = 30, enrolled: bool = True,
              assumptions: Assumptions | None = None) -> Result:
    """年収から社会保険料・税金・手取り額を計算する。

    enrolled が False の場合は、家族の扶養に入っていて社会保険料を負担しないものとして計算する。
    """
    if annual_salary < 0:
        raise ValueError("年収には 0 以上の値を指定すること。")
    if enrolled:
        insurance = social_insurance(annual_salary, age, assumptions or Assumptions())
    else:
        insurance = {"health": 0, "care": 0, "child_support": 0, "pension": 0, "employment": 0}
    insurance_total = sum(insurance.values())
    return Result(
        annual_salary=annual_salary,
        health_insurance=insurance["health"],
        care_insurance=insurance["care"],
        child_support=insurance["child_support"],
        pension=insurance["pension"],
        employment_insurance=insurance["employment"],
        income_tax=income_tax(annual_salary, insurance_total),
        resident_tax=resident_tax(annual_salary, insurance_total),
    )


def display_width(text: str) -> int:
    """全角文字を幅 2 として文字列の表示幅を返す。"""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def format_row(label: str, amount: int) -> str:
    """ラベルと金額を桁をそろえて 1 行にする。"""
    padding = " " * (24 - display_width(label))
    return f"{label}{padding}{amount:>12,} 円"


def report(result: Result) -> str:
    """計算結果を表示用の文字列にする。"""
    rate = result.take_home / result.annual_salary * 100 if result.annual_salary else 0.0
    lines = [
        format_row("年収（給与収入）", result.annual_salary),
        "",
        format_row("  健康保険料", result.health_insurance),
        format_row("  介護保険料", result.care_insurance),
        format_row("  子ども・子育て支援金", result.child_support),
        format_row("  厚生年金保険料", result.pension),
        format_row("  雇用保険料", result.employment_insurance),
        format_row("社会保険料の合計", result.social_insurance_total),
        "",
        format_row("  所得税（復興税を含む）", result.income_tax),
        format_row("  住民税", result.resident_tax),
        format_row("税金の合計", result.tax_total),
        "",
        format_row("手取り（概算）", result.take_home) + f"（年収の {rate:.1f} %）",
    ]
    return "\n".join(lines)


def main() -> None:
    """コマンドライン引数を読み取り、計算結果を表示する。"""
    parser = argparse.ArgumentParser(description="年収から手取り額を概算する（2026 年の収入を想定）。")
    parser.add_argument("salary", type=int, help="年収（給与収入、円）")
    parser.add_argument("--age", type=int, default=30, help="年齢（介護保険料の判定に使う。既定値は 30）")
    parser.add_argument("--no-social-insurance", action="store_true",
                        help="社会保険料を負担しない（家族の扶養に入っている）ものとして計算する")
    args = parser.parse_args()
    result = calculate(args.salary, age=args.age, enrolled=not args.no_social_insurance)
    print(report(result))


if __name__ == "__main__":
    main()
