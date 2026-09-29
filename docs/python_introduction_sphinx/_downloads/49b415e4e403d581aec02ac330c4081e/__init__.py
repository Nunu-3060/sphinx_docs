"""Sphinx 入門のサンプルパッケージ。

図形の面積を計算する :mod:`sample_package.shapes` モジュールを含みます。
"""

from sample_package.shapes import Circle, Rectangle, Shape, total_area

__all__ = ["Circle", "Rectangle", "Shape", "total_area"]
