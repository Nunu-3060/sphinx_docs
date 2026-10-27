"""第 15 章: 総合演習 — 2D プラットフォーマー。

本書で扱った道具を 1 つのゲームにまとめる。

* 固定タイムステップと描画の補間（第 3 章）
* ジャンプの重力と初速、加速・減速、コヨーテタイムと先行入力（第 10 章）
* タイルマップとの衝突判定と、軸ごとの押し戻し（第 11 章・第 12 章）
* 円と長方形の判定でコインを取る（第 11 章）
* 指数関数的減衰で追いかけるカメラと、ノイズによる画面の揺れ（第 8 章・第 9 章）
* ばねによる着地時の伸び縮み（第 13 章）
* パーティクル（第 13 章）

collision.py と同じフォルダーに置いて実行する。

操作方法:
    左右キー（または A / D キー）: 走る
    スペースキー（または上キー、W キー）: ジャンプ（押す長さで高さが変わる）
    R キー: 最初からやり直す
    Esc キー: 終了する
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import pygame
from pygame import Vector2

from collision import AABB, circle_aabb_contact, tiles_overlapping

# --- 画面と時間 ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TILE = 32  # タイルの大きさ（ピクセル）
STEP = 1 / 120  # 物理の 1 ステップの時間（秒）
MAX_FRAME_TIME = 0.25
MAX_STEPS = 30

# --- プレイヤーの動き ---
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 28
JUMP_HEIGHT = 3.5 * TILE  # 最高点の高さ（ピクセル）
TIME_TO_APEX = 0.38  # 最高点に達するまでの時間（秒）
GRAVITY = 2 * JUMP_HEIGHT / TIME_TO_APEX ** 2
JUMP_SPEED = 2 * JUMP_HEIGHT / TIME_TO_APEX
FALL_GRAVITY_SCALE = 1.8
JUMP_CUT_SCALE = 0.4
MAX_FALL_SPEED = 720.0  # 1 ステップに 6 ピクセルしか動かないので、タイルをすり抜けない
RUN_SPEED = 240.0
GROUND_ACCEL = 2000.0
GROUND_DECEL = 2600.0
AIR_ACCEL = 1100.0
COYOTE_TIME = 0.1
JUMP_BUFFER_TIME = 0.12

# --- カメラと演出 ---
CAMERA_FOLLOW_RATE = 8.0  # カメラが追いかける速さ（1 秒あたり）
LOOK_AHEAD = 48.0  # 進む向きの先をどれだけ見せるか（ピクセル）
LOOK_AHEAD_RATE = 3.0
SHAKE_DECAY = 1.8
MAX_SHAKE = 10.0  # 画面の揺れの最大のずれ（ピクセル）
SHAKE_FREQUENCY = 25.0
SQUASH_STIFFNESS = (math.tau * 4.0) ** 2  # 伸び縮みのばね（固有振動数 4 Hz）
SQUASH_DAMPING = 2 * 0.35 * math.tau * 4.0  # 減衰比 0.35（少し揺れてから戻る）
COIN_RADIUS = 7.0

LEVEL = [
    '############################################################',
    '#..........................................................#',
    '#..........................................................#',
    '#..........................................................#',
    '#..........................................................#',
    '#..........................................................#',
    '#...................................CC.....................#',
    '#..................................####....................#',
    '#..........................................................#',
    '#..................CC...........CC................CC.......#',
    '#.................####.........####...............##.......#',
    '#.................................................##.......#',
    '#.............CC...............................C..##.......#',
    '#............####......C...####......C........###.##.......#',
    '#.................................................##.......#',
    '#.P...C..................................^^.......##..C.G..#',
    '#########...##########...###########...#####################',
    '#########^^^##########^^^###########^^^#####################',
]
SOLID = '#'
SPIKE = '^'


def approach(current: float, target: float, max_delta: float) -> float:
    """current を target へ最大 max_delta だけ近づける。"""
    if current < target:
        return min(current + max_delta, target)
    return max(current - max_delta, target)


def damp(current: float, target: float, rate: float, dt: float) -> float:
    """フレームレートに依存しない指数関数的な追従。"""
    return current + (target - current) * (1 - math.exp(-rate * dt))


def hash_to_unit(i: int, seed: int) -> float:
    """整数から -1 以上 1 未満の値を決定的に作る（noise.py と同じもの）。"""
    h = (i * 0x9E3779B97F4A7C15 + seed * 0xBF58476D1CE4E5B9) & ((1 << 64) - 1)
    h ^= h >> 31
    h = (h * 0x94D049BB133111EB) & ((1 << 64) - 1)
    h ^= h >> 29
    return (h & 0xFFFFFF) / 0x800000 - 1


def perlin_noise(x: float, seed: int) -> float:
    """1 次元のパーリンノイズ（noise.py と同じもの）。"""
    i = math.floor(x)
    t = x - i
    v0 = hash_to_unit(i, seed) * t
    v1 = hash_to_unit(i + 1, seed) * (t - 1)
    return (v0 + (v1 - v0) * t * t * t * (t * (t * 6 - 15) + 10)) * 2


class Level:
    """文字列のリストで書いたタイルマップ。"""

    def __init__(self, rows: list[str]) -> None:
        self.rows = rows
        self.width = len(rows[0]) * TILE
        self.height = len(rows) * TILE

    def tile(self, col: int, row: int) -> str:
        """マップの外は壁として扱う。"""
        if 0 <= row < len(self.rows) and 0 <= col < len(self.rows[row]):
            return self.rows[row][col]
        return SOLID

    def find(self, char: str) -> list[Vector2]:
        """指定した文字のタイルの中心座標をすべて返す。"""
        return [Vector2((c + 0.5) * TILE, (r + 0.5) * TILE)
                for r, row in enumerate(self.rows) for c, ch in enumerate(row) if ch == char]

    def solid_tiles(self, box: AABB) -> list[AABB]:
        """box と重なっている壁のタイル。"""
        cols, rows = tiles_overlapping(box, TILE)
        return [AABB(c * TILE, r * TILE, (c + 1) * TILE, (r + 1) * TILE)
                for r in rows for c in cols if self.tile(c, r) == SOLID]

    def touches_spike(self, box: AABB) -> bool:
        """トゲはタイルの下半分だけを衝突判定に使う（見た目より少し小さくすると理不尽さが減る）。"""
        cols, rows = tiles_overlapping(box, TILE)
        for r in rows:
            for c in cols:
                if self.tile(c, r) == SPIKE:
                    spike = AABB(c * TILE + 6, r * TILE + TILE / 2, (c + 1) * TILE - 6, (r + 1) * TILE)
                    if box.left < spike.right and spike.left < box.right and box.top < spike.bottom:
                        return True
        return False


@dataclass
class Player:
    """位置はプレイヤーの長方形の中心。"""

    position: Vector2
    velocity: Vector2 = field(default_factory=Vector2)
    on_ground: bool = False
    facing: float = 1.0  # 1: 右向き、-1: 左向き
    coyote_timer: float = 0.0
    buffer_timer: float = 0.0
    squash: float = 0.0  # 伸び縮みの量（正で横に広がる）
    squash_velocity: float = 0.0

    @property
    def box(self) -> AABB:
        return AABB.from_center(self.position.x, self.position.y, PLAYER_WIDTH, PLAYER_HEIGHT)


def move_and_collide(player: Player, level: Level, dt: float) -> bool:
    """x 方向と y 方向を別々に動かし、壁にめり込んだら押し戻す。着地したら True を返す。"""
    player.position.x += player.velocity.x * dt
    for tile in level.solid_tiles(player.box):
        if player.velocity.x > 0:
            player.position.x = tile.left - PLAYER_WIDTH / 2
        elif player.velocity.x < 0:
            player.position.x = tile.right + PLAYER_WIDTH / 2
        player.velocity.x = 0

    was_on_ground = player.on_ground
    player.on_ground = False
    player.position.y += player.velocity.y * dt
    for tile in level.solid_tiles(player.box):
        if player.velocity.y > 0:
            player.position.y = tile.top - PLAYER_HEIGHT / 2
            player.on_ground = True
        elif player.velocity.y < 0:
            player.position.y = tile.bottom + PLAYER_HEIGHT / 2  # 天井に頭をぶつけた
        player.velocity.y = 0
    if was_on_ground and not player.on_ground and player.velocity.y >= 0:
        player.coyote_timer = COYOTE_TIME  # 足場から歩いて離れた
    return player.on_ground and not was_on_ground


def update_player(player: Player, level: Level, dt: float, move: float, jump_pressed: bool,
                  jump_held: bool) -> tuple[bool, bool]:
    """プレイヤーを 1 ステップ進める。(ジャンプしたか, 着地したか) を返す。"""
    if move != 0:
        player.facing = math.copysign(1.0, move)
    accel = (GROUND_ACCEL if move != 0 else GROUND_DECEL) if player.on_ground else AIR_ACCEL
    player.velocity.x = approach(player.velocity.x, move * RUN_SPEED, accel * dt)

    if jump_pressed:
        player.buffer_timer = JUMP_BUFFER_TIME
    jumped = False
    if player.buffer_timer > 0 and (player.on_ground or player.coyote_timer > 0):
        player.velocity.y = -JUMP_SPEED
        player.on_ground = False
        player.buffer_timer = player.coyote_timer = 0.0
        player.squash_velocity -= 6.0  # 縦に伸びる
        jumped = True
    player.buffer_timer = max(0.0, player.buffer_timer - dt)
    player.coyote_timer = max(0.0, player.coyote_timer - dt)
    if not jump_held:
        player.velocity.y = max(player.velocity.y, -JUMP_SPEED * JUMP_CUT_SCALE)

    gravity = GRAVITY * (FALL_GRAVITY_SCALE if player.velocity.y > 0 else 1.0)
    fall_speed = player.velocity.y
    player.velocity.y = min(player.velocity.y + gravity * dt, MAX_FALL_SPEED)
    landed = move_and_collide(player, level, dt)
    if landed:
        player.squash_velocity += min(fall_speed / 100, 8.0)  # 速く落ちるほど大きくつぶれる

    # 伸び縮みは 0 を目標にしたばね
    player.squash_velocity += (-SQUASH_STIFFNESS * player.squash - SQUASH_DAMPING * player.squash_velocity) * dt
    player.squash += player.squash_velocity * dt
    return jumped, landed


@dataclass
class Particle:
    position: Vector2
    velocity: Vector2
    life: float


class Game:
    def __init__(self) -> None:
        self.level = Level(LEVEL)
        self.start = self.level.find('P')[0]
        self.player = Player(Vector2(self.start))
        self.previous_position = Vector2(self.start)  # 描画の補間用
        self.coins = self.level.find('C')
        self.coin_count = len(self.coins)
        self.goal = self.level.find('G')[0]
        self.camera = Vector2(self.start)
        self.look_ahead = 0.0
        self.trauma = 0.0
        self.particles: list[Particle] = []
        self.rng = random.Random(0)
        self.time = 0.0
        self.deaths = 0
        self.cleared = False

    def step(self, dt: float, move: float, jump_pressed: bool, jump_held: bool) -> None:
        """固定タイムステップの 1 回分の更新。"""
        self.previous_position = Vector2(self.player.position)
        if self.cleared:
            return
        self.time += dt
        jumped, landed = update_player(self.player, self.level, dt, move, jump_pressed, jump_held)
        if jumped or landed:
            self.spawn_dust(self.player.box.bottom)

        box = self.player.box
        for coin in self.coins[:]:
            if circle_aabb_contact(coin, COIN_RADIUS, box):
                self.coins.remove(coin)
                self.spawn_sparks(coin)
        if self.level.touches_spike(box) or self.player.position.y > self.level.height:
            self.deaths += 1
            self.trauma = 1.0
            self.spawn_sparks(self.player.position)
            self.player = Player(Vector2(self.start))
            self.previous_position = Vector2(self.start)
        if circle_aabb_contact(self.goal, TILE / 2, box):
            self.cleared = True

        for p in self.particles:
            p.velocity.y += 600 * dt
            p.position += p.velocity * dt
            p.life -= dt
        self.particles = [p for p in self.particles if p.life > 0]

    def spawn_dust(self, y: float) -> None:
        for _ in range(8):
            v = Vector2(self.rng.uniform(-80, 80), self.rng.uniform(-60, -10))
            self.particles.append(Particle(Vector2(self.player.position.x, y), v, 0.3))

    def spawn_sparks(self, position: Vector2) -> None:
        for _ in range(16):
            v = Vector2(self.rng.uniform(60, 180), 0).rotate_rad(self.rng.uniform(0, math.tau))
            self.particles.append(Particle(Vector2(position), v, 0.5))

    def update_camera(self, frame_time: float, player_drawn: Vector2) -> Vector2:
        """カメラを追従させ、揺れを加えた最終的なカメラの位置を返す（描画のフレームごとに呼ぶ）。"""
        self.look_ahead = damp(self.look_ahead, self.player.facing * LOOK_AHEAD, LOOK_AHEAD_RATE, frame_time)
        target = player_drawn + Vector2(self.look_ahead, -TILE)
        self.camera.x = damp(self.camera.x, target.x, CAMERA_FOLLOW_RATE, frame_time)
        self.camera.y = damp(self.camera.y, target.y, CAMERA_FOLLOW_RATE, frame_time)
        # マップの外が映らないように、カメラの中心の範囲を制限する
        self.camera.x = max(SCREEN_WIDTH / 2, min(self.level.width - SCREEN_WIDTH / 2, self.camera.x))
        self.camera.y = max(SCREEN_HEIGHT / 2, min(self.level.height - SCREEN_HEIGHT / 2, self.camera.y))
        self.trauma = max(0.0, self.trauma - SHAKE_DECAY * frame_time)
        shake = MAX_SHAKE * self.trauma ** 2
        offset = Vector2(perlin_noise(self.time * SHAKE_FREQUENCY, 1), perlin_noise(self.time * SHAKE_FREQUENCY, 2))
        return self.camera + offset * shake

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, alpha: float, frame_time: float) -> None:
        player_drawn = self.previous_position.lerp(self.player.position, alpha)
        camera = self.update_camera(frame_time, player_drawn)
        origin = Vector2(round(camera.x - SCREEN_WIDTH / 2), round(camera.y - SCREEN_HEIGHT / 2))

        screen.fill((24, 28, 44))
        first_col, first_row = int(origin.x // TILE), int(origin.y // TILE)
        for r in range(first_row, first_row + SCREEN_HEIGHT // TILE + 2):
            for c in range(first_col, first_col + SCREEN_WIDTH // TILE + 2):
                ch = self.level.tile(c, r)
                x, y = c * TILE - origin.x, r * TILE - origin.y
                if ch == SOLID:
                    pygame.draw.rect(screen, (70, 90, 130), (x, y, TILE, TILE))
                    pygame.draw.rect(screen, (50, 64, 96), (x, y, TILE, TILE), 1)
                elif ch == SPIKE:
                    points = [(x + 4, y + TILE), (x + TILE / 2, y + TILE / 2 - 4), (x + TILE - 4, y + TILE)]
                    pygame.draw.polygon(screen, (220, 220, 230), points)
        for coin in self.coins:
            bob = math.sin(self.time * 4 + coin.x * 0.05) * 3  # 上下にゆっくり揺らす
            pygame.draw.circle(screen, (250, 210, 70), coin - origin + Vector2(0, bob), COIN_RADIUS)
        goal = self.goal - origin
        pygame.draw.line(screen, (230, 230, 230), goal + (0, TILE / 2), goal - (0, TILE / 2), 3)
        pygame.draw.polygon(screen, (90, 230, 120), [goal - (0, TILE / 2), goal + (18, -TILE / 2 + 7), goal - (0, 2)])
        for p in self.particles:
            pygame.draw.circle(screen, (230, 230, 240), p.position - origin, 2)

        # 伸び縮み: 面積をほぼ保つよう、横に広がった分だけ縦を縮める
        scale_x = 1 + 0.25 * self.player.squash
        scale_y = 1 / scale_x
        w, h = PLAYER_WIDTH * scale_x, PLAYER_HEIGHT * scale_y
        feet = player_drawn - origin + Vector2(0, PLAYER_HEIGHT / 2)
        body = pygame.FRect(feet.x - w / 2, feet.y - h, w, h)
        pygame.draw.rect(screen, (240, 240, 240), body, border_radius=4)
        eye = Vector2(body.centerx + self.player.facing * w * 0.2, body.top + h * 0.35)
        pygame.draw.circle(screen, (24, 28, 44), eye, 2.5)

        collected = self.coin_count - len(self.coins)
        hud = f'coins: {collected}/{self.coin_count}  time: {self.time:5.1f}  misses: {self.deaths}'
        screen.blit(font.render(hud, True, (230, 230, 230)), (10, 10))
        if self.cleared:
            message = font.render('CLEAR!  Press R to restart', True, (255, 230, 120))
            screen.blit(message, message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))


def read_move(keys: pygame.key.ScancodeWrapper) -> float:
    right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    left = keys[pygame.K_LEFT] or keys[pygame.K_a]
    return float(right) - float(left)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Platformer')
    font = pygame.font.Font(None, 26)
    clock = pygame.time.Clock()
    game = Game()
    accumulator = 0.0
    jump_keys = (pygame.K_SPACE, pygame.K_UP, pygame.K_w)
    jump_pressed = False  # 押した瞬間の入力。次の更新で 1 回だけ使う

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = Game()
                elif event.key in jump_keys:
                    jump_pressed = True
        keys = pygame.key.get_pressed()
        move = read_move(keys)
        jump_held = any(keys[k] for k in jump_keys)

        # 固定タイムステップ: 経過時間を貯め、STEP ごとに更新する
        frame_time = min(clock.tick(60) / 1000, MAX_FRAME_TIME)
        accumulator += frame_time
        steps = 0
        while accumulator >= STEP and steps < MAX_STEPS:
            game.step(STEP, move, jump_pressed, jump_held)
            jump_pressed = False
            accumulator -= STEP
            steps += 1
        accumulator = min(accumulator, STEP)

        game.draw(screen, font, accumulator / STEP, frame_time)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
