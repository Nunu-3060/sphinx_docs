"""platformer.py のうち、画面や入力に依存しない計算部分の単体テスト。

実行方法（このファイルがあるフォルダーで実行する）:
    py -m unittest test_platformer
"""

import unittest

from pygame import Vector2

from platformer import (COYOTE_TIME, JUMP_HEIGHT, LEVEL, MAX_FALL_SPEED, PLAYER_HEIGHT, STEP, TILE, Game, Level,
                        Player, update_player)

# 試験用の小さなマップ。床は 5 行目にあり、3～4 列目は深い穴、5 列目は壁
TEST_LEVEL = [
    '##########',
    '#........#',
    '#........#',
    '#....#...#',
    '#....#...#',
    '###..#####',
    '###..#####',
    '###..#####',
    '##########',
]


def run(player: Player, level: Level, seconds: float, move: float = 0.0, jump_held: bool = False,
        jump_at_start: bool = False) -> None:
    """一定の入力のまま seconds 秒だけ進める。"""
    for i in range(round(seconds / STEP)):
        update_player(player, level, STEP, move, jump_at_start and i == 0, jump_held)


def standing_player(level: Level, col: int) -> Player:
    """col 列目の床（5 行目）の上に立っているプレイヤーを作る。"""
    player = Player(Vector2((col + 0.5) * TILE, 5 * TILE - PLAYER_HEIGHT / 2))
    run(player, level, 0.1)
    return player


class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.level = Level(TEST_LEVEL)

    def test_lands_on_floor(self) -> None:
        player = Player(Vector2(1.5 * TILE, 1.5 * TILE))
        run(player, self.level, 1.0)
        self.assertTrue(player.on_ground)
        self.assertAlmostEqual(player.position.y + PLAYER_HEIGHT / 2, 5 * TILE)

    def test_falls_no_faster_than_limit(self) -> None:
        player = Player(Vector2(3.5 * TILE, 1.5 * TILE))
        for _ in range(60):
            update_player(player, self.level, STEP, 0.0, False, False)
            self.assertLessEqual(player.velocity.y, MAX_FALL_SPEED)

    def test_wall_stops_player(self) -> None:
        player = standing_player(self.level, 6)
        run(player, self.level, 1.0, move=-1.0)
        self.assertGreaterEqual(player.box.left, 6 * TILE)  # 5 列目の壁を通り抜けない
        self.assertEqual(player.velocity.x, 0)

    def test_jump_reaches_designed_height(self) -> None:
        level = Level(['#' * 5] + ['#...#'] * 8 + ['#####'])
        player = Player(Vector2(2.5 * TILE, 9 * TILE - PLAYER_HEIGHT / 2))
        run(player, level, 0.1)
        ground_y = player.position.y
        highest = ground_y
        for i in range(120):
            update_player(player, level, STEP, 0.0, i == 0, True)
            highest = min(highest, player.position.y)
        # 半陰的オイラー法なので、設計した高さより最大 1 ステップぶん程度低くなる
        self.assertAlmostEqual(ground_y - highest, JUMP_HEIGHT, delta=JUMP_HEIGHT * 0.03)

    def test_short_hop_when_released(self) -> None:
        level = Level(['#' * 5] + ['#...#'] * 8 + ['#####'])
        player = Player(Vector2(2.5 * TILE, 9 * TILE - PLAYER_HEIGHT / 2))
        run(player, level, 0.1)
        ground_y = player.position.y
        highest = ground_y
        for i in range(120):
            update_player(player, level, STEP, 0.0, i == 0, i < 6)
            highest = min(highest, player.position.y)
        self.assertLess(ground_y - highest, JUMP_HEIGHT * 0.5)

    def test_coyote_time(self) -> None:
        player = standing_player(self.level, 2)
        # 右へ歩いて 3 列目の穴に落ち始めた直後なら、まだジャンプできる
        while player.on_ground:
            update_player(player, self.level, STEP, 1.0, False, False)
        run(player, self.level, COYOTE_TIME / 2, move=1.0)
        jumped, _ = update_player(player, self.level, STEP, 1.0, True, True)
        self.assertTrue(jumped)

    def test_no_jump_after_coyote_time(self) -> None:
        player = standing_player(self.level, 2)
        while player.on_ground:
            update_player(player, self.level, STEP, 1.0, False, False)
        run(player, self.level, COYOTE_TIME * 1.5, move=1.0)
        jumped, _ = update_player(player, self.level, STEP, 1.0, True, True)
        self.assertFalse(jumped)

    def test_jump_buffer(self) -> None:
        player = Player(Vector2(1.5 * TILE, 5 * TILE - PLAYER_HEIGHT / 2 - 6))  # 床の 6 ピクセル上
        # 着地の少し前に押したジャンプが、着地した時点で実行される
        jumped, _ = update_player(player, self.level, STEP, 0.0, True, True)
        self.assertFalse(jumped)
        jumped_any = False
        for _ in range(round(0.1 / STEP)):
            jumped, _ = update_player(player, self.level, STEP, 0.0, False, True)
            jumped_any = jumped_any or jumped
        self.assertTrue(jumped_any)


class GameTest(unittest.TestCase):
    def test_level_is_rectangular(self) -> None:
        self.assertEqual({len(row) for row in LEVEL}, {len(LEVEL[0])})

    def test_coin_is_collected(self) -> None:
        game = Game()
        coin = game.coins[0]
        game.player.position = Vector2(coin)
        game.step(STEP, 0.0, False, False)
        self.assertNotIn(coin, game.coins)

    def test_spike_resets_player(self) -> None:
        game = Game()
        spike = game.level.find('^')[0]
        game.player.position = Vector2(spike.x, spike.y)
        game.step(STEP, 0.0, False, False)
        self.assertEqual(game.deaths, 1)
        self.assertEqual(game.player.position, game.start)

    def test_goal_clears(self) -> None:
        game = Game()
        game.player.position = Vector2(game.goal)
        game.step(STEP, 0.0, False, False)
        self.assertTrue(game.cleared)


if __name__ == '__main__':
    unittest.main()
