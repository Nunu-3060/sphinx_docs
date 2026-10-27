"""第 2 章・第 5 章～第 9 章のサンプルコードの計算部分の単体テスト。

実行方法（このファイルがあるフォルダーで実行する）:
    py -m unittest test_math_tools
"""

import math
import random
import unittest

from pygame import Vector2

from curves import ArcLengthTable, catmull_rom, closed_spline, cubic_bezier, quadratic_bezier
from easing import EASINGS, damp, inverse_lerp, lerp, remap
from float_precision import float32_spacing, screen_to_world, world_to_screen
from homing import angle_difference, lerp_angle, move_toward_angle, wrap_angle
from noise import fractal_noise, perlin_noise, value_noise
from quaternion import X_AXIS, Y_AXIS, Z_AXIS, Quat, from_euler, slerp
from random_tools import Bag, probability_at_least_once, random_point_in_circle, tries_needed, weighted_choice
from transform2d import Mat3
from turret import angle_to, from_polar


class CoordinateTest(unittest.TestCase):
    def test_world_screen_round_trip(self) -> None:
        sx, sy = world_to_screen(2.0, 1.5)
        self.assertEqual((sx, sy), (64.0, 432.0))
        self.assertEqual(screen_to_world(sx, sy), (2.0, 1.5))

    def test_float32_spacing(self) -> None:
        self.assertEqual(float32_spacing(1.0), 2.0 ** -23)
        self.assertEqual(float32_spacing(1_000_000.0), 0.0625)


class AngleTest(unittest.TestCase):
    def test_angle_to(self) -> None:
        self.assertAlmostEqual(angle_to(Vector2(0, 0), Vector2(0, 10)), math.pi / 2)
        self.assertAlmostEqual(angle_to(Vector2(0, 0), Vector2(-1, 0)), math.pi)
        p = from_polar(2, math.pi / 2)
        self.assertAlmostEqual(p.x, 0)
        self.assertAlmostEqual(p.y, 2)

    def test_wrap_angle(self) -> None:
        self.assertAlmostEqual(wrap_angle(math.radians(270)), math.radians(-90))
        self.assertAlmostEqual(wrap_angle(math.radians(-190)), math.radians(170))

    def test_shortest_turn(self) -> None:
        # 170 度から -170 度へは、340 度戻るより 20 度進む方が近い
        self.assertAlmostEqual(angle_difference(math.radians(170), math.radians(-170)), math.radians(20))
        self.assertAlmostEqual(lerp_angle(math.radians(170), math.radians(-170), 0.5), math.radians(180))

    def test_move_toward_angle_is_limited(self) -> None:
        self.assertAlmostEqual(move_toward_angle(0.0, 1.0, 0.25), 0.25)
        self.assertAlmostEqual(move_toward_angle(0.0, -1.0, 0.25), -0.25)
        self.assertEqual(move_toward_angle(0.0, 0.1, 0.25), 0.1)


class Mat3Test(unittest.TestCase):
    def assert_point(self, actual: tuple[float, float], expected: tuple[float, float]) -> None:
        self.assertAlmostEqual(actual[0], expected[0])
        self.assertAlmostEqual(actual[1], expected[1])

    def test_order_matters(self) -> None:
        rotate = Mat3.rotation(math.pi / 2)
        move = Mat3.translation(100, 0)
        self.assert_point((move @ rotate).apply(10, 0), (100, 10))
        self.assert_point((rotate @ move).apply(10, 0), (0, 110))

    def test_inverse(self) -> None:
        m = Mat3.translation(5, -3) @ Mat3.rotation(0.7) @ Mat3.scaling(2, 3)
        self.assert_point((m.inverse() @ m).apply(4, 9), (4, 9))
        with self.assertRaises(ValueError):
            Mat3.scaling(0, 1).inverse()

    def test_vector_ignores_translation(self) -> None:
        self.assert_point(Mat3.translation(50, 50).apply_vector(1, 2), (1, 2))


class QuaternionTest(unittest.TestCase):
    def assert_vec(self, actual: tuple[float, float, float], expected: tuple[float, float, float]) -> None:
        for a, e in zip(actual, expected):
            self.assertAlmostEqual(a, e)

    def test_axis_angle(self) -> None:
        q = Quat.from_axis_angle(Z_AXIS, math.pi / 2)
        self.assert_vec(q.rotate(X_AXIS), (0, 1, 0))
        q = Quat.from_axis_angle(Y_AXIS, math.pi / 2)
        self.assert_vec(q.rotate(Z_AXIS), (1, 0, 0))

    def test_composition_order(self) -> None:
        a = Quat.from_axis_angle(Z_AXIS, math.pi / 2)
        b = Quat.from_axis_angle(X_AXIS, math.pi / 2)
        v = (0.0, 1.0, 0.0)
        self.assert_vec((a * b).rotate(v), a.rotate(b.rotate(v)))

    def test_gimbal_lock(self) -> None:
        r1, r2 = from_euler(30, 90, 0), from_euler(0, 90, -30)
        for axis in (X_AXIS, Y_AXIS, Z_AXIS):
            self.assert_vec(r1.rotate(axis), r2.rotate(axis))

    def test_slerp_constant_speed(self) -> None:
        a, b = Quat(), Quat.from_axis_angle(Y_AXIS, math.radians(120))
        for t in (0.0, 0.25, 0.5, 1.0):
            expected = Quat.from_axis_angle(Y_AXIS, math.radians(120 * t))
            self.assertAlmostEqual(abs(slerp(a, b, t).dot(expected)), 1)

    def test_slerp_takes_short_path(self) -> None:
        a, b = Quat(), -Quat.from_axis_angle(Y_AXIS, math.radians(90))  # -q は q と同じ回転
        mid = slerp(a, b, 0.5)
        self.assertAlmostEqual(abs(mid.dot(Quat.from_axis_angle(Y_AXIS, math.radians(45)))), 1)


class EasingTest(unittest.TestCase):
    def test_lerp_family(self) -> None:
        self.assertEqual(lerp(10, 20, 0.25), 12.5)
        self.assertEqual(inverse_lerp(10, 20, 12.5), 0.25)
        self.assertEqual(remap(5, 0, 10, 100, 200), 150)

    def test_easing_end_points(self) -> None:
        for name, ease in EASINGS.items():
            with self.subTest(name=name):
                self.assertAlmostEqual(ease(0.0), 0.0)
                self.assertAlmostEqual(ease(1.0), 1.0)

    def test_damp_is_frame_rate_independent(self) -> None:
        results = []
        for fps in (20, 60, 144):
            x = 0.0
            for _ in range(fps):  # 1 秒ぶん
                x = damp(x, 100.0, 5.0, 1 / fps)
            results.append(x)
        for x in results:
            self.assertAlmostEqual(x, 100 * (1 - math.exp(-5)))


class CurveTest(unittest.TestCase):
    def test_bezier_end_points(self) -> None:
        p0, p1, p2, p3 = Vector2(0, 0), Vector2(1, 2), Vector2(3, 2), Vector2(4, 0)
        self.assertEqual(quadratic_bezier(p0, p1, p2, 0), p0)
        self.assertEqual(quadratic_bezier(p0, p1, p2, 1), p2)
        self.assertEqual(cubic_bezier(p0, p1, p2, p3, 1), p3)
        self.assertEqual(cubic_bezier(p0, p1, p2, p3, 0.5), Vector2(2, 1.5))

    def test_catmull_rom_passes_through_points(self) -> None:
        p = [Vector2(0, 0), Vector2(1, 1), Vector2(3, 1), Vector2(4, 0)]
        self.assertEqual(catmull_rom(p[0], p[1], p[2], p[3], 0), p[1])
        self.assertEqual(catmull_rom(p[0], p[1], p[2], p[3], 1), p[2])

    def test_arc_length_of_circle(self) -> None:
        # 半径 100 の円周の長さ 2π×100 を、細かく区切って測る
        def circle(u: float) -> Vector2:
            return Vector2(100, 0).rotate_rad(u)

        table = ArcLengthTable(circle, math.tau, 2000)
        self.assertAlmostEqual(table.total, math.tau * 100, delta=0.1)
        self.assertAlmostEqual(table.u_at(table.total / 4), math.tau / 4, delta=1e-3)

    def test_closed_spline_loops(self) -> None:
        points = [Vector2(0, 0), Vector2(10, 0), Vector2(10, 10), Vector2(0, 10)]
        curve = closed_spline(points)
        self.assertEqual(curve(0), points[0])
        self.assertEqual(curve(2), points[2])
        self.assertEqual(curve(4), points[0])


class RandomTest(unittest.TestCase):
    def test_weighted_choice_frequency(self) -> None:
        rng = random.Random(0)
        n = 20_000
        hits = sum(weighted_choice(rng, ['a', 'b'], [3, 1]) == 'b' for _ in range(n))
        self.assertAlmostEqual(hits / n, 0.25, delta=0.01)

    def test_bag_contains_each_item_once_per_round(self) -> None:
        bag = Bag(random.Random(1), [1, 2, 3, 4])
        for _ in range(3):
            self.assertEqual(sorted(bag.draw() for _ in range(4)), [1, 2, 3, 4])

    def test_point_in_circle_is_uniform(self) -> None:
        rng = random.Random(2)
        points = [random_point_in_circle(rng, 1.0) for _ in range(20_000)]
        inner = sum(x * x + y * y < 0.25 for x, y in points)  # 半径 0.5 の円は面積の 1/4
        self.assertAlmostEqual(inner / len(points), 0.25, delta=0.01)

    def test_probability(self) -> None:
        self.assertAlmostEqual(probability_at_least_once(0.01, 100), 0.634, places=3)
        self.assertEqual(tries_needed(0.01, 0.5), 69)
        self.assertEqual(tries_needed(0.01, 0.99), 459)


class NoiseTest(unittest.TestCase):
    def test_deterministic_and_bounded(self) -> None:
        for i in range(200):
            x = i * 0.137
            self.assertEqual(value_noise(x, 3), value_noise(x, 3))
            self.assertLessEqual(abs(value_noise(x)), 1)
            self.assertLessEqual(abs(perlin_noise(x)), 1)
            self.assertLessEqual(abs(fractal_noise(x, 5)), 1)

    def test_perlin_is_zero_on_lattice(self) -> None:
        for i in range(-5, 5):
            self.assertEqual(perlin_noise(float(i)), 0)

    def test_continuity(self) -> None:
        self.assertAlmostEqual(value_noise(2.0 - 1e-9), value_noise(2.0), places=6)
        self.assertAlmostEqual(perlin_noise(2.0 - 1e-9), perlin_noise(2.0), places=6)


if __name__ == '__main__':
    unittest.main()
