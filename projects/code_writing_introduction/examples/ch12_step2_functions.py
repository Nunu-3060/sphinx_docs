"""第 12 章「実践：悪いコードを直してみる」の手順 2（関数の分割と処理の流れ）の結果。"""

EXCELLENT_THRESHOLD = 80
PASSING_THRESHOLD = 60
SUBJECT_COUNT = 3

Record = tuple[str, int, int, int]  # (名前, 科目 1 の点数, 科目 2 の点数, 科目 3 の点数)


def total_score(record: Record) -> int:
    _, score1, score2, score3 = record
    return score1 + score2 + score3


def grade_of(average: float) -> str:
    if average >= EXCELLENT_THRESHOLD:
        return "A"
    if average >= PASSING_THRESHOLD:
        return "B"
    return "C"


def format_record_line(record: Record) -> str:
    name = record[0]
    total = total_score(record)
    average = total / SUBJECT_COUNT
    return f"{name}: 合計 {total} 点, 平均 {average:.1f} 点, 評価 {grade_of(average)}"


def print_report(records: list[Record]) -> None:
    for record in records:
        print(format_record_line(record))
    grand_total = sum(total_score(record) for record in records)
    print(f"全体の平均: {grand_total / (len(records) * SUBJECT_COUNT):.1f} 点")


if __name__ == "__main__":
    print_report([("佐藤", 85, 90, 78), ("鈴木", 60, 55, 70), ("高橋", 40, 52, 38)])
