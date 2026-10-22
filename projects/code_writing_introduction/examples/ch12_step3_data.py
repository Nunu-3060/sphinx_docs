"""第 12 章「実践：悪いコードを直してみる」の手順 3（データとエラー処理）の結果。"""

from dataclasses import dataclass

EXCELLENT_THRESHOLD = 80
PASSING_THRESHOLD = 60


@dataclass
class Student:
    """生徒 1 人分の成績。"""

    name: str
    scores: list[int]

    def __post_init__(self) -> None:
        if not self.scores:
            raise ValueError(f"{self.name} の点数が 1 つも無い")

    @property
    def total(self) -> int:
        return sum(self.scores)

    @property
    def average(self) -> float:
        return self.total / len(self.scores)


def grade_of(average: float) -> str:
    """平均点から評価（A, B, C）を決める。"""
    if average >= EXCELLENT_THRESHOLD:
        return "A"
    if average >= PASSING_THRESHOLD:
        return "B"
    return "C"


def format_student_line(student: Student) -> str:
    """生徒 1 人分の成績を 1 行の文字列にする。"""
    return f"{student.name}: 合計 {student.total} 点, 平均 {student.average:.1f} 点, 評価 {grade_of(student.average)}"


def overall_average(students: list[Student]) -> float:
    """全生徒・全科目の点数の平均を返す。

    Raises:
        ValueError: 生徒が 1 人もいない場合。
    """
    if not students:
        raise ValueError("生徒が 1 人もいない")
    score_sum = sum(student.total for student in students)
    score_count = sum(len(student.scores) for student in students)
    return score_sum / score_count


def print_report(students: list[Student]) -> None:
    """生徒ごとの成績と全体の平均を表示する。"""
    for student in students:
        print(format_student_line(student))
    print(f"全体の平均: {overall_average(students):.1f} 点")


if __name__ == "__main__":
    print_report([
        Student("佐藤", [85, 90, 78]),
        Student("鈴木", [60, 55, 70]),
        Student("高橋", [40, 52, 38]),
    ])
