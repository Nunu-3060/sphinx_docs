"""第 3 章・第 10 章～第 13 章のサンプルコードの計算部分の単体テスト。

実行方法（このファイルがあるフォルダーで実行する）:
    py -m unittest test_physics
"""

import math
import random
import unittest

from pygame import Vector2

from collision import (AABB, aabb_contact, aabbs_overlap, circle_aabb_contact, circle_circle_contact,
                       closest_point_on_segment, polygon_contact, ray_aabb, ray_circle, sweep_circle_circle,
                       tiles_overlapping)
from fixed_timestep import consume_time
from integrators import (STEPPERS, explicit_euler, gravity_acceleration, semi_implicit_euler, simulate,
                         spring_acceleration, spring_energy, velocity_verlet)
from jump import approach, jump_parameters
from response import Body, resolve_contact
from rope import Point, Stick, satisfy
from spatial_grid import brute_force, with_grid
from spring import spring_coefficients, spring_step
from vectors_demo import is_in_view, move_toward, side_of


class FixedTimestepTest(unittest.TestCase):
    def test_steps_and_remainder(self) -> None:
        steps, rest = consume_time(0.0, 0.05, 1 / 60)
        self.assertEqual(steps, 3)
        self.assertAlmostEqual(rest, 0.05 - 3 / 60)

    def test_remainder_is_carried_over(self) -> None:
        total_steps, acc = 0, 0.0
        for _ in range(100):
            steps, acc = consume_time(acc, 1 / 144, 1 / 60)
            total_steps += steps
        self.assertEqual(total_steps, math.floor(100 / 144 * 60 + 1e-9))

    def test_spiral_of_death_guard(self) -> None:
        steps, rest = consume_time(0.0, 10.0, 1 / 60, max_steps=8)
        self.assertEqual(steps, 8)
        self.assertLessEqual(rest, 1 / 60)


class VectorGameplayTest(unittest.TestCase):
    def test_view_cone(self) -> None:
        eye, facing = Vector2(0, 0), Vector2(1, 0)
        self.assertTrue(is_in_view(eye, facing, Vector2(100, 10)))
        self.assertFalse(is_in_view(eye, facing, Vector2(100, 100)))  # 45 度は視界（35 度）の外
        self.assertFalse(is_in_view(eye, facing, Vector2(-50, 0)))  # 後ろ
        self.assertFalse(is_in_view(eye, facing, Vector2(500, 0)))  # 遠すぎる

    def test_side_in_screen_coordinates(self) -> None:
        # 右（+x）を向いているとき、画面の下（+y）は右手側
        self.assertEqual(side_of(Vector2(1, 0), Vector2(0, 1)), 'right')
        self.assertEqual(side_of(Vector2(1, 0), Vector2(0, -1)), 'left')

    def test_move_toward_does_not_overshoot(self) -> None:
        self.assertEqual(move_toward(Vector2(0, 0), Vector2(3, 4), 10), Vector2(3, 4))
        self.assertEqual(move_toward(Vector2(0, 0), Vector2(3, 4), 2.5), Vector2(1.5, 2))


class IntegratorTest(unittest.TestCase):
    def test_energy_behaviour(self) -> None:
        e0 = spring_energy(1.0, 0.0)
        _, x, v = simulate(explicit_euler, spring_acceleration, 1.0, 0.0, 1 / 60, 10.0)[-1]
        self.assertGreater(spring_energy(x, v), 100 * e0)  # オイラー法はエネルギーが増え続ける
        for stepper in (semi_implicit_euler, velocity_verlet):
            _, x, v = simulate(stepper, spring_acceleration, 1.0, 0.0, 1 / 60, 10.0)[-1]
            self.assertAlmostEqual(spring_energy(x, v) / e0, 1, delta=0.01)

    def test_verlet_is_exact_for_constant_acceleration(self) -> None:
        history = simulate(velocity_verlet, gravity_acceleration, 0.0, 4.9, 0.1, 1.0)
        self.assertAlmostEqual(max(x for _, x, _ in history), 1.225)

    def test_all_converge_for_small_dt(self) -> None:
        for name, stepper in STEPPERS.items():
            with self.subTest(name=name):
                _, x, _ = simulate(stepper, spring_acceleration, 1.0, 0.0, 1 / 10000, 0.25)[-1]
                self.assertAlmostEqual(x, math.cos(math.tau * 0.25), delta=1e-3)


class JumpTest(unittest.TestCase):
    def test_jump_parameters_reach_height(self) -> None:
        g, v0 = jump_parameters(96, 0.36)
        self.assertAlmostEqual(v0 / g, 0.36)  # 最高点に達する時間
        self.assertAlmostEqual(v0 * v0 / (2 * g), 96)  # 最高点の高さ

    def test_approach(self) -> None:
        self.assertEqual(approach(0, 10, 3), 3)
        self.assertEqual(approach(9, 10, 3), 10)
        self.assertEqual(approach(0, -10, 3), -3)


class CollisionTest(unittest.TestCase):
    def test_circles(self) -> None:
        self.assertIsNone(circle_circle_contact(Vector2(0, 0), 1, Vector2(3, 0), 1))
        contact = circle_circle_contact(Vector2(0, 0), 2, Vector2(3, 0), 2)
        assert contact is not None
        self.assertEqual(contact, (Vector2(1, 0), 1))

    def test_aabbs(self) -> None:
        a = AABB(0, 0, 10, 10)
        self.assertTrue(aabbs_overlap(a, AABB(5, 5, 15, 15)))
        self.assertFalse(aabbs_overlap(a, AABB(10, 0, 20, 10)))  # 辺が接しているだけ
        self.assertEqual(aabb_contact(a, AABB(8, 2, 18, 12)), (Vector2(1, 0), 2))
        self.assertEqual(aabb_contact(a, AABB(2, -9, 12, 1)), (Vector2(0, -1), 1))

    def test_circle_aabb(self) -> None:
        box = AABB(0, 0, 10, 10)
        self.assertEqual(circle_aabb_contact(Vector2(13, 5), 4, box), (Vector2(1, 0), 1))
        self.assertIsNone(circle_aabb_contact(Vector2(13, 13), 4, box))  # 角までの距離は √18 > 4
        normal, depth = circle_aabb_contact(Vector2(9, 5), 2, box) or (Vector2(), 0.0)  # 中心が内部にある
        self.assertEqual((normal, depth), (Vector2(1, 0), 3))

    def test_closest_point_on_segment(self) -> None:
        a, b = Vector2(0, 0), Vector2(10, 0)
        self.assertEqual(closest_point_on_segment(Vector2(3, 5), a, b), Vector2(3, 0))
        self.assertEqual(closest_point_on_segment(Vector2(-4, 5), a, b), Vector2(0, 0))

    def test_rays(self) -> None:
        self.assertAlmostEqual(ray_circle(Vector2(0, 0), Vector2(1, 0), Vector2(10, 0), 2) or 0, 8)
        self.assertIsNone(ray_circle(Vector2(0, 0), Vector2(-1, 0), Vector2(10, 0), 2))
        self.assertIsNone(ray_circle(Vector2(0, 0), Vector2(1, 0), Vector2(10, 5), 2))
        self.assertAlmostEqual(ray_aabb(Vector2(0, 5), Vector2(1, 0), AABB(4, 0, 8, 10)) or 0, 4)
        self.assertIsNone(ray_aabb(Vector2(0, 15), Vector2(1, 0), AABB(4, 0, 8, 10)))
        self.assertAlmostEqual(ray_aabb(Vector2(0, 0), Vector2(1, 1), AABB(4, 2, 8, 10)) or 0, 4)

    def test_sweep_prevents_tunneling(self) -> None:
        # 1 ステップで 100 進む半径 1 の弾は、途中の半径 1 の的と離散的な判定では重ならない
        start, motion = Vector2(0, 0), Vector2(100, 0)
        self.assertIsNone(circle_circle_contact(start + motion, 1, Vector2(50, 0), 1))
        self.assertAlmostEqual(sweep_circle_circle(start, motion, 1, Vector2(50, 0), 1) or 0, 0.48)

    def test_sat(self) -> None:
        square = [Vector2(0, 0), Vector2(10, 0), Vector2(10, 10), Vector2(0, 10)]
        diamond = [Vector2(15, 5), Vector2(20, 0), Vector2(25, 5), Vector2(20, 10)]
        self.assertIsNone(polygon_contact(square, diamond))
        moved = [p - Vector2(7, 0) for p in diamond]  # 左端の頂点が四角に 2 だけ入る
        contact = polygon_contact(square, moved)
        assert contact is not None
        normal, depth = contact
        self.assertGreater(normal.x, 0)  # 四角から菱形へ向かう向き
        self.assertGreater(depth, 0)

    def test_tiles_overlapping(self) -> None:
        cols, rows = tiles_overlapping(AABB(30, 0, 64, 31.5), 32)
        self.assertEqual((list(cols), list(rows)), ([0, 1], [0]))  # 右端 64 ちょうどのタイル 2 は含まない


class ResponseTest(unittest.TestCase):
    def test_equal_masses_exchange_velocity(self) -> None:
        a = Body(Vector2(0, 0), Vector2(10, 0), 1, 1.0)
        b = Body(Vector2(1.9, 0), Vector2(0, 0), 1, 1.0)
        resolve_contact(a, b, Vector2(1, 0), 0.1, restitution=1.0, friction=0.0)
        self.assertAlmostEqual(a.velocity.x, 0)
        self.assertAlmostEqual(b.velocity.x, 10)

    def test_momentum_is_conserved(self) -> None:
        a = Body(Vector2(0, 0), Vector2(5, 2), 1, 1 / 2)
        b = Body(Vector2(1.5, 0), Vector2(-3, 1), 1, 1 / 6)
        before = a.velocity * a.mass + b.velocity * b.mass
        resolve_contact(a, b, Vector2(1, 0), 0.5, restitution=0.5, friction=0.3)
        after = a.velocity * a.mass + b.velocity * b.mass
        self.assertAlmostEqual(before.x, after.x)
        self.assertAlmostEqual(before.y, after.y)

    def test_restitution_scales_separating_speed(self) -> None:
        a = Body(Vector2(0, 0), Vector2(4, 0), 1, 1.0)
        wall = Body(Vector2(2, 0), Vector2(0, 0), 1, 0.0)  # 動かない
        resolve_contact(a, wall, Vector2(1, 0), 0.0, restitution=0.5, friction=0.0)
        self.assertAlmostEqual(a.velocity.x, -2)
        self.assertEqual(wall.velocity, Vector2(0, 0))

    def test_positional_correction_by_mass(self) -> None:
        light = Body(Vector2(0, 0), Vector2(), 1, 1.0)
        heavy = Body(Vector2(1, 0), Vector2(), 1, 1 / 3)
        resolve_contact(light, heavy, Vector2(1, 0), 1.0, restitution=0.0, friction=0.0)
        self.assertAlmostEqual(light.position.x, -0.75)
        self.assertAlmostEqual(heavy.position.x, 1.25)


class SpringAndRopeTest(unittest.TestCase):
    def test_critical_damping_does_not_overshoot(self) -> None:
        k, c = spring_coefficients(2.0, 1.0)
        x, v = Vector2(0, 0), Vector2(0, 0)
        target = Vector2(100, 0)
        largest = 0.0
        for _ in range(240):
            x, v = spring_step(x, v, target, k, c, 1 / 120)
            largest = max(largest, x.x)
        self.assertLess(largest, 100.5)
        self.assertAlmostEqual(x.x, 100, delta=0.5)

    def test_underdamped_overshoots(self) -> None:
        k, c = spring_coefficients(2.0, 0.2)
        x, v = Vector2(0, 0), Vector2(0, 0)
        largest = 0.0
        for _ in range(240):
            x, v = spring_step(x, v, Vector2(100, 0), k, c, 1 / 120)
            largest = max(largest, x.x)
        self.assertGreater(largest, 140)

    def test_stick_restores_length(self) -> None:
        a = Point(Vector2(0, 0), Vector2(0, 0), pinned=True)
        b = Point(Vector2(20, 0), Vector2(20, 0))
        satisfy(Stick(a, b, 10))
        self.assertEqual(a.position, Vector2(0, 0))
        self.assertEqual(b.position, Vector2(10, 0))


class SpatialGridTest(unittest.TestCase):
    def test_grid_finds_the_same_pairs(self) -> None:
        rng = random.Random(5)
        circles = [(rng.uniform(0, 500), rng.uniform(0, 500), rng.uniform(5, 20)) for _ in range(200)]
        hits_brute, checks_brute = brute_force(circles)
        hits_grid, checks_grid = with_grid(circles)
        self.assertEqual(hits_brute, hits_grid)
        self.assertLess(checks_grid, checks_brute)


if __name__ == '__main__':
    unittest.main()
