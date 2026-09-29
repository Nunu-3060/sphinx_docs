"""図形の面積と周囲の長さを計算するモジュール。

本書の autodoc の章で題材として使うサンプルです。

docstring は Google 形式で記述しています。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Protocol


class Shape(Protocol):
    """面積と周囲の長さを持つ図形のプロトコル。"""

    def area(self) -> float:
        """面積を返します。"""
        ...

    def perimeter(self) -> float:
        """周囲の長さを返します。"""
        ...


@dataclass(frozen=True)
class Rectangle:
    """長方形。

    Attributes:
        width: 幅。0 以上の値を指定します。
        height: 高さ。0 以上の値を指定します。

    Raises:
        ValueError: 幅または高さが負の場合。

    Examples:
        >>> rect = Rectangle(width=3.0, height=4.0)
        >>> rect.area()
        12.0
        >>> rect.perimeter()
        14.0
    """

    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width < 0 or self.height < 0:
            raise ValueError("幅と高さは 0 以上である必要があります。")

    def area(self) -> float:
        """面積を返します。

        Returns:
            幅と高さの積。
        """
        return self.width * self.height

    def perimeter(self) -> float:
        """周囲の長さを返します。

        Returns:
            幅と高さの和の 2 倍。
        """
        return 2 * (self.width + self.height)


@dataclass(frozen=True)
class Circle:
    """円。

    Attributes:
        radius: 半径。0 以上の値を指定します。

    Raises:
        ValueError: 半径が負の場合。

    Examples:
        >>> circle = Circle(radius=1.0)
        >>> round(circle.area(), 5)
        3.14159
    """

    radius: float

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError("半径は 0 以上である必要があります。")

    def area(self) -> float:
        r"""面積を返します。

        面積は :math:`\pi r^2` で計算します。

        Returns:
            円の面積。
        """
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        r"""周囲の長さ（円周）を返します。

        円周は :math:`2 \pi r` で計算します。

        Returns:
            円周の長さ。
        """
        return 2 * math.pi * self.radius


def total_area(shapes: list[Shape]) -> float:
    """複数の図形の面積の合計を返します。

    Args:
        shapes: 面積を合計する図形のリスト。

    Returns:
        面積の合計。``shapes`` が空の場合は 0.0 を返します。

    Examples:
        >>> total_area([Rectangle(2.0, 3.0), Rectangle(1.0, 1.0)])
        7.0
        >>> total_area([])
        0.0
    """
    return sum((shape.area() for shape in shapes), start=0.0)
