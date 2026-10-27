"""vec2.py の単体テスト。

実行方法（このファイルがあるフォルダーで実行する）:
    py -m unittest test_vec2
"""

import math
import unittest

import pygame

from vec2 import Vec2


class Vec2Test(unittest.TestCase):
    def test_arithmetic(self) -> None:
        a, b = Vec2(3, 4), Vec2(1, -2)
        self.assertEqual(a + b, Vec2(4, 2))
        self.assertEqual(a - b, Vec2(2, 6))
        self.assertEqual(a * 2, Vec2(6, 8))
        self.assertEqual(2 * a, Vec2(6, 8))
        self.assertEqual(-a, Vec2(-3, -4))

    def test_length_and_normalize(self) -> None:
        self.assertEqual(Vec2(3, 4).length(), 5)
        self.assertAlmostEqual(Vec2(3, 4).normalized().length(), 1)
        self.assertEqual(Vec2(0, 0).normalized(), Vec2(0, 0))
        # 斜めの入力 (1, 1) は長さが √2 なので、正規化しないと速くなる
        self.assertAlmostEqual(Vec2(1, 1).length(), math.sqrt(2))

    def test_dot_and_cross(self) -> None:
        self.assertEqual(Vec2(1, 0).dot(Vec2(0, 1)), 0)  # 直交
        self.assertGreater(Vec2(1, 0).dot(Vec2(1, 1)), 0)  # 前方
        self.assertLess(Vec2(1, 0).dot(Vec2(-1, 1)), 0)  # 後方
        self.assertEqual(Vec2(1, 0).cross(Vec2(0, 1)), 1)
        self.assertEqual(Vec2(0, 1).cross(Vec2(1, 0)), -1)

    def test_project_and_reflect(self) -> None:
        self.assertEqual(Vec2(3, 4).project_onto(Vec2(2, 0)), Vec2(3, 0))
        self.assertEqual(Vec2(1, -1).reflect(Vec2(0, 1)), Vec2(1, 1))

    def test_rotated(self) -> None:
        r = Vec2(1, 0).rotated(math.pi / 2)
        self.assertAlmostEqual(r.x, 0)
        self.assertAlmostEqual(r.y, 1)

    def test_matches_pygame_vector2(self) -> None:
        a, b = Vec2(2.5, -1), Vec2(0.5, 3)
        pa, pb = pygame.Vector2(2.5, -1), pygame.Vector2(0.5, 3)
        self.assertAlmostEqual(a.dot(b), pa.dot(pb))
        self.assertAlmostEqual(a.cross(b), pa.cross(pb))
        n = Vec2(1, 2).normalized()
        reflected = a.reflect(n)
        expected = pa.reflect(pygame.Vector2(n.x, n.y))
        self.assertAlmostEqual(reflected.x, expected.x)
        self.assertAlmostEqual(reflected.y, expected.y)


if __name__ == '__main__':
    unittest.main()
