"""クラスと抽象基底クラスによる抽象化の例。"""

import math
from abc import ABC, abstractmethod
from collections.abc import Iterable


class Shape(ABC):
    """図形を表す抽象基底クラス。面積を求める方法だけを約束する。"""

    @abstractmethod
    def area(self) -> float:
        """図形の面積を返す。"""


class Rectangle(Shape):
    """長方形。"""

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    """円。"""

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


def total_area(shapes: Iterable[Shape]) -> float:
    """図形の種類を区別せずに、面積の合計を求める。"""
    return sum(shape.area() for shape in shapes)


def main() -> None:
    """種類の異なる図形をまとめて扱う。"""
    shapes: list[Shape] = [Rectangle(3.0, 4.0), Circle(1.0)]
    print(f"{total_area(shapes):.4f}")  # 15.1416


if __name__ == "__main__":
    main()
