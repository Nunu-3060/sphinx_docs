"""型ヒントと静的型検査の例（第 6 章）.

型ヒントを付けると、関数の入出力が読み手に伝わるだけでなく、
mypy などの型検査器が実行前に誤りを検出できる。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Employee:
    """社員を表す."""

    name: str
    salary: int


def average_salary(employees: list[Employee]) -> float:
    """社員の平均給与を返す。社員がいなければ 0.0 を返す."""
    if not employees:
        return 0.0
    return sum(e.salary for e in employees) / len(employees)


def find_by_name(employees: list[Employee], name: str) -> Employee | None:
    """名前が一致する社員を返す。見つからなければ None を返す."""
    for employee in employees:
        if employee.name == name:
            return employee
    return None


if __name__ == "__main__":
    staff = [Employee("佐藤", 300_000), Employee("鈴木", 360_000)]
    print(f"平均給与: {average_salary(staff):,.0f} 円")

    found = find_by_name(staff, "鈴木")
    # found は Employee | None 型なので、None でないことを確認してから使う。
    # この確認を省略すると mypy が誤りとして報告する。
    if found is not None:
        print(f"{found.name} の給与: {found.salary:,} 円")
