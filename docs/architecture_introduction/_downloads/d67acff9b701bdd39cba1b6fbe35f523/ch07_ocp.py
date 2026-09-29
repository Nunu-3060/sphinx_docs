"""開放閉鎖の原則（OCP）の例.

悪い例では、図形の種類を追加するたびに total_area 関数の分岐を書き換える
必要があります。良い例では、図形がそれぞれ自分の面積を計算するので、
新しい図形を追加しても total_area 関数は変更しません。

実行方法::

    python ch07_ocp.py
"""

import math
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: 種類ごとの分岐が、利用する側に書かれている
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BadShape:
    """図形（悪い例）. kind によって使う属性が異なります."""

    kind: str
    width: float = 0.0
    height: float = 0.0
    radius: float = 0.0


def bad_total_area(shapes: Iterable[BadShape]) -> float:
    """面積の合計を返します（悪い例）."""
    total = 0.0
    for shape in shapes:
        if shape.kind == "rectangle":
            total += shape.width * shape.height
        elif shape.kind == "circle":
            total += math.pi * shape.radius ** 2
        # 三角形を追加するには、ここに分岐を追加する必要がある
    return total


# ---------------------------------------------------------------------------
# 良い例: 拡張に対して開き、変更に対して閉じている
# ---------------------------------------------------------------------------


class Shape(Protocol):
    """図形のインターフェースです."""

    def area(self) -> float:
        """面積を返します."""
        ...


@dataclass(frozen=True)
class Rectangle:
    """長方形です."""

    width: float
    height: float

    def area(self) -> float:
        return self.width * self.height


@dataclass(frozen=True)
class Circle:
    """円です."""

    radius: float

    def area(self) -> float:
        return math.pi * self.radius ** 2


@dataclass(frozen=True)
class Triangle:
    """三角形です. 追加しても total_area 関数は変更しません."""

    base: float
    height: float

    def area(self) -> float:
        return self.base * self.height / 2


def total_area(shapes: Iterable[Shape]) -> float:
    """面積の合計を返します（良い例）."""
    return sum(shape.area() for shape in shapes)


def main() -> None:
    """悪い例と良い例で面積の合計を求めます."""
    print(bad_total_area([BadShape("rectangle", width=2, height=3),
                          BadShape("circle", radius=1)]))
    print(total_area([Rectangle(2, 3), Circle(1)]))
    print(total_area([Rectangle(2, 3), Circle(1), Triangle(4, 3)]))


if __name__ == "__main__":
    main()
