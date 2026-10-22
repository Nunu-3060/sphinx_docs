"""第 12 章「実践：悪いコードを直してみる」の手順 1（名前と定数）の結果。"""

EXCELLENT_THRESHOLD = 80
PASSING_THRESHOLD = 60
SUBJECT_COUNT = 3


def main(records: list[tuple[str, int, int, int]]) -> None:
    grand_total = 0
    for record in records:
        total = record[1] + record[2] + record[3]
        average = total / SUBJECT_COUNT
        if average >= EXCELLENT_THRESHOLD:
            grade = "A"
        else:
            if average >= PASSING_THRESHOLD:
                grade = "B"
            else:
                grade = "C"
        print(f"{record[0]}: 合計 {total} 点, 平均 {average:.1f} 点, 評価 {grade}")
    for record in records:
        grand_total += record[1] + record[2] + record[3]
    print(f"全体の平均: {grand_total / (len(records) * SUBJECT_COUNT):.1f} 点")


if __name__ == "__main__":
    main([("佐藤", 85, 90, 78), ("鈴木", 60, 55, 70), ("高橋", 40, 52, 38)])
