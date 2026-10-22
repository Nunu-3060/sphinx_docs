"""ブロック崩し Step 4: ブロックを並べ、ボールが当たったら壊す。

操作方法:
    左右キー（または A / D キー）: パドルを動かす
    スペースキー: ボールを発射する
    Esc キー: 終了する
"""

import math
import random
from dataclasses import dataclass

import pygame

# --- 画面とゲーム全体の設定 ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
MAX_DT = 1 / 30  # 1 フレームで進める時間の上限（秒）

BG_COLOR = (20, 24, 36)
PADDLE_COLOR = (200, 210, 255)
BALL_COLOR = (255, 255, 255)

# --- パドル ---
PADDLE_WIDTH = 96
PADDLE_HEIGHT = 12
PADDLE_Y = SCREEN_HEIGHT - 40
PADDLE_SPEED = 480.0  # ピクセル毎秒

# --- ボール ---
BALL_SIZE = 10
BALL_SPEED = 360.0  # ピクセル毎秒
MAX_BOUNCE_ANGLE = math.radians(60)  # パドルの端で反射したときの、真上からの傾き

# --- ブロック ---
BLOCK_COLS = 10
BLOCK_ROWS = 5
BLOCK_WIDTH = 56
BLOCK_HEIGHT = 20
BLOCK_GAP = 4
BLOCK_TOP = 60
BLOCK_COLORS = [(239, 83, 80), (255, 167, 38), (255, 238, 88), (102, 187, 106), (66, 165, 245)]


class Paddle:
    """プレイヤーが操作するパドル。"""

    def __init__(self) -> None:
        self.rect = pygame.FRect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rect.midtop = (SCREEN_WIDTH / 2, PADDLE_Y)

    def update(self, dt: float, direction: float) -> None:
        """direction（-1: 左、0: 停止、1: 右）の向きに dt 秒ぶん動かす。画面外には出さない。"""
        self.rect.x += direction * PADDLE_SPEED * dt
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect, border_radius=4)


class Ball:
    """パドルで打ち返すボール。"""

    def __init__(self) -> None:
        self.rect = pygame.FRect(0, 0, BALL_SIZE, BALL_SIZE)
        self.velocity = pygame.Vector2(0, 0)  # 速度（ピクセル毎秒）
        self.launched = False

    def follow(self, paddle: Paddle) -> None:
        """発射前はパドルの上に乗せておく。"""
        self.rect.midbottom = paddle.rect.midtop

    def launch(self) -> None:
        """真上から左右 30 度の範囲で、ランダムな向きに発射する。"""
        self.velocity = pygame.Vector2(0, -BALL_SPEED).rotate(random.uniform(-30, 30))
        self.launched = True

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)


@dataclass
class Block:
    """壊す対象のブロック。"""

    rect: pygame.Rect
    color: tuple[int, int, int]

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, self.rect, border_radius=3)


def create_blocks() -> list[Block]:
    """ブロックを格子状に並べ、画面の左右中央に配置する。"""
    total_width = BLOCK_COLS * BLOCK_WIDTH + (BLOCK_COLS - 1) * BLOCK_GAP
    left = (SCREEN_WIDTH - total_width) // 2
    blocks: list[Block] = []
    for row in range(BLOCK_ROWS):
        for col in range(BLOCK_COLS):
            x = left + col * (BLOCK_WIDTH + BLOCK_GAP)
            y = BLOCK_TOP + row * (BLOCK_HEIGHT + BLOCK_GAP)
            blocks.append(Block(pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT), BLOCK_COLORS[row]))
    return blocks


def read_direction() -> float:
    """押されているキーから、パドルを動かす向き（-1、0、1）を求める。"""
    keys = pygame.key.get_pressed()
    direction = 0.0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 1
    return direction


def paddle_bounce_velocity(offset: float, speed: float) -> pygame.Vector2:
    """パドルで反射した後の速度を返す。

    offset はパドルの中心から当たった位置までのずれで、左端が -1.0、中心が 0.0、右端が 1.0 である。
    端に当たるほど大きく斜めに跳ね返り、速さ（speed）は変えない。
    """
    offset = max(-1.0, min(1.0, offset))
    angle = offset * MAX_BOUNCE_ANGLE
    return pygame.Vector2(speed * math.sin(angle), -speed * math.cos(angle))


def pop_hit_block(ball: Ball, blocks: list[Block]) -> Block | None:
    """ボールに重なっているブロックを 1 つ blocks から取り除いて返す。無ければ None を返す。"""
    index = ball.rect.collidelist([block.rect for block in blocks])
    if index < 0:
        return None
    return blocks.pop(index)


def move_ball(ball: Ball, dt: float, paddle: Paddle, blocks: list[Block]) -> list[Block]:
    """ボールを dt 秒ぶん動かし、壁・ブロック・パドルで反射させる。

    x 方向と y 方向を別々に動かし、それぞれの移動の直後に当たり判定を行う。
    こうすると、ぶつかった面（側面か上下の面か）が移動の向きから分かる。
    当たったブロックは blocks から取り除き、戻り値のリストに入れて返す。
    """
    hit_blocks: list[Block] = []

    # x 方向に動かし、左右の壁とブロックの側面で反射させる
    ball.rect.x += ball.velocity.x * dt
    if ball.rect.left < 0:
        ball.rect.left = 0
        ball.velocity.x = abs(ball.velocity.x)
    elif ball.rect.right > SCREEN_WIDTH:
        ball.rect.right = SCREEN_WIDTH
        ball.velocity.x = -abs(ball.velocity.x)
    block = pop_hit_block(ball, blocks)
    if block is not None:
        # めり込んだ分を押し戻してから向きを反転する
        if ball.velocity.x > 0:
            ball.rect.right = block.rect.left
        else:
            ball.rect.left = block.rect.right
        ball.velocity.x *= -1
        hit_blocks.append(block)

    # y 方向に動かし、上の壁とブロックの上下の面で反射させる
    ball.rect.y += ball.velocity.y * dt
    if ball.rect.top < 0:
        ball.rect.top = 0
        ball.velocity.y = abs(ball.velocity.y)
    block = pop_hit_block(ball, blocks)
    if block is not None:
        if ball.velocity.y > 0:
            ball.rect.bottom = block.rect.top
        else:
            ball.rect.top = block.rect.bottom
        ball.velocity.y *= -1
        hit_blocks.append(block)

    # 下向きに動いているときだけ判定し、パドルに何度も当たり続けるのを防ぐ
    if ball.velocity.y > 0 and ball.rect.colliderect(paddle.rect):
        ball.rect.bottom = paddle.rect.top
        offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
        ball.velocity = paddle_bounce_velocity(offset, ball.velocity.length())

    return hit_blocks


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Step 4: Blocks")
    clock = pygame.time.Clock()
    paddle = Paddle()
    ball = Ball()
    blocks = create_blocks()

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, MAX_DT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not ball.launched:
                ball.launch()

        paddle.update(dt, read_direction())
        if ball.launched:
            move_ball(ball, dt, paddle, blocks)
            if ball.rect.top > SCREEN_HEIGHT:
                ball = Ball()  # 画面の下に落ちたら、発射前の状態に戻す
        else:
            ball.follow(paddle)
        if not blocks:
            blocks = create_blocks()  # すべて壊したら並べ直す（勝敗の処理は Step 5 で加える）

        screen.fill(BG_COLOR)
        for block in blocks:
            block.draw(screen)
        paddle.draw(screen)
        ball.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
