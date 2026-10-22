"""第 8 章「重複をなくす」の悪い例。"""


def report(math_scores: list[int], english_scores: list[int], science_scores: list[int]) -> None:
    math_average = sum(math_scores) / len(math_scores)
    print(f"数学の平均点: {math_average:.1f}")
    english_average = sum(english_scores) / len(math_scores)
    print(f"英語の平均点: {english_average:.1f}")
    science_average = sum(science_scores) / len(science_scores)
    print(f"理科の平均点: {science_average:.1f}")


if __name__ == "__main__":
    report([80, 70, 90], [60, 75], [55, 65, 85])
