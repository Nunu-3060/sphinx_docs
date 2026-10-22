"""第 3 章「名前の付け方」の良い例。"""

PASSING_SCORE = 60
PERFECT_SCORE = 100


def count_passed(scores: list[int]) -> int:
    passed_count = 0
    for score in scores:
        if score >= PASSING_SCORE:
            passed_count += 1
    return passed_count


def is_perfect(score: int) -> bool:
    return score == PERFECT_SCORE


if __name__ == "__main__":
    test_scores = [72, 45, 100, 60, 38]
    print(count_passed(test_scores))
    print(is_perfect(test_scores[2]))
