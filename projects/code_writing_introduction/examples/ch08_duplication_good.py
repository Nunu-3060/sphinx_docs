"""第 8 章「重複をなくす」の良い例。"""

import statistics


def print_average(subject: str, scores: list[int]) -> None:
    print(f"{subject}の平均点: {statistics.mean(scores):.1f}")


def report(scores_by_subject: dict[str, list[int]]) -> None:
    for subject, scores in scores_by_subject.items():
        print_average(subject, scores)


if __name__ == "__main__":
    report({
        "数学": [80, 70, 90],
        "英語": [60, 75],
        "理科": [55, 65, 85],
    })
