"""step07_polish.py のうち、画面や入力に依存しない計算部分を検証する単体テスト。

実行方法（このファイルがあるディレクトリーで実行する）:
    py -m unittest test_breakout
"""

import math
import unittest

import pygame

from step07_polish import (BALL_SPEED, MAX_BOUNCE_ANGLE, Ball, Block, Paddle, move_ball,
                           paddle_bounce_velocity)


class PaddleBounceVelocityTest(unittest.TestCase):
    def test_center_goes_straight_up(self) -> None:
        velocity = paddle_bounce_velocity(0.0, BALL_SPEED)
        self.assertAlmostEqual(velocity.x, 0.0)
        self.assertAlmostEqual(velocity.y, -BALL_SPEED)

    def test_right_edge_uses_max_angle(self) -> None:
        velocity = paddle_bounce_velocity(1.0, BALL_SPEED)
        angle = math.atan2(velocity.x, -velocity.y)  # 真上からの傾き
        self.assertAlmostEqual(angle, MAX_BOUNCE_ANGLE)

    def test_offset_is_clamped(self) -> None:
        self.assertEqual(paddle_bounce_velocity(-5.0, BALL_SPEED), paddle_bounce_velocity(-1.0, BALL_SPEED))

    def test_speed_is_preserved(self) -> None:
        for offset in (-1.0, -0.3, 0.0, 0.7, 1.0):
            self.assertAlmostEqual(paddle_bounce_velocity(offset, BALL_SPEED).length(), BALL_SPEED)


class MoveBallTest(unittest.TestCase):
    def test_ball_breaks_block_and_bounces_down(self) -> None:
        paddle = Paddle()
        ball = Ball()
        ball.rect.midbottom = (100, 135)  # ブロックの 5 ピクセル下
        ball.velocity = pygame.Vector2(0, -BALL_SPEED)
        block = Block(pygame.Rect(80, 100, 40, 20), (255, 0, 0), 10)
        blocks = [block]

        result = move_ball(ball, 0.05, paddle, blocks)

        self.assertEqual(result.blocks, [block])
        self.assertEqual(blocks, [])
        self.assertGreater(ball.velocity.y, 0)  # 下向きに跳ね返る
        self.assertEqual(ball.rect.top, block.rect.bottom)  # めり込まない位置に押し戻される

    def test_ball_bounces_off_left_wall(self) -> None:
        ball = Ball()
        ball.rect.topleft = (2, 200)
        ball.velocity = pygame.Vector2(-BALL_SPEED, 0)

        result = move_ball(ball, 0.05, Paddle(), [])

        self.assertTrue(result.wall)
        self.assertEqual(ball.rect.left, 0)
        self.assertGreater(ball.velocity.x, 0)


if __name__ == "__main__":
    unittest.main()
