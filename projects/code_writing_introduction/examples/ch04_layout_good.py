"""第 4 章「見た目を整える」の良い例。"""

import math
import statistics


def circle_area(radius: float) -> float:
    return math.pi * radius ** 2


def summarize(values: list[float]) -> str:
    average = statistics.mean(values)
    maximum = max(values)
    return f"平均: {average:.1f}, 最大: {maximum:.1f}"


if __name__ == "__main__":
    print(f"{circle_area(2.0):.2f}")
    print(summarize([3.0, 5.5, 4.0]))
