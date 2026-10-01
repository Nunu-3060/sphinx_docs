"""単一責任の原則（SRP）の例.

悪い例の BadEmployee クラスは、給与の計算（経理部門の関心）、勤務時間の
報告（人事部門の関心）、保存（システム管理者の関心）という、変更を求める
相手が異なる 3 つの責任を持っています。良い例では、責任ごとにクラスを
分けます。

実行方法::

    python ch07_srp.py
"""

import json
from dataclasses import asdict, dataclass

# ---------------------------------------------------------------------------
# 悪い例: 1 つのクラスが複数の責任を持つ
# ---------------------------------------------------------------------------


class BadEmployee:
    """従業員（悪い例）."""

    def __init__(self, name: str, hourly_wage: int, hours: float) -> None:
        self.name = name
        self.hourly_wage = hourly_wage
        self.hours = hours

    def calculate_pay(self) -> int:
        """給与を計算します（経理部門が変更を求める）."""
        return int(self.hourly_wage * self.hours)

    def report_hours(self) -> str:
        """勤務時間の報告を作ります（人事部門が変更を求める）."""
        return f"{self.name}: {self.hours} 時間"

    def to_json(self) -> str:
        """保存用の JSON を作ります（システム管理者が変更を求める）."""
        return json.dumps(self.__dict__, ensure_ascii=False)


# ---------------------------------------------------------------------------
# 良い例: 責任ごとにクラスを分ける
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Employee:
    """従業員のデータだけを持ちます."""

    name: str
    hourly_wage: int
    hours: float


class PayCalculator:
    """給与を計算します."""

    def calculate(self, employee: Employee) -> int:
        """給与を返します."""
        return int(employee.hourly_wage * employee.hours)


class HourReporter:
    """勤務時間の報告を作ります."""

    def report(self, employee: Employee) -> str:
        """勤務時間の報告の文字列を返します."""
        return f"{employee.name}: {employee.hours} 時間"


class EmployeeJsonSerializer:
    """従業員のデータを JSON に変換します."""

    def dumps(self, employee: Employee) -> str:
        """JSON の文字列を返します."""
        return json.dumps(asdict(employee), ensure_ascii=False)


def main() -> None:
    """悪い例と良い例で、同じ結果が得られることを確認します."""
    bad = BadEmployee("佐藤", 1500, 120.5)
    print(bad.calculate_pay(), bad.report_hours(), bad.to_json())

    employee = Employee("佐藤", 1500, 120.5)
    print(PayCalculator().calculate(employee),
          HourReporter().report(employee),
          EmployeeJsonSerializer().dumps(employee))


if __name__ == "__main__":
    main()
