"""ブロック崩し Step 6: タイトル・プレイ・結果の 3 つのシーンに分けて画面を切り替える。

操作方法:
    左右キー（または A / D キー）: パドルを動かす
    スペースキー: ボールを発射する、次の画面に進む
    Esc キー: 終了する
"""

import functools
import math
import random
from dataclasses import dataclass

import pygame

# --- 画面とゲーム全体の設定 ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
MAX_DT = 1 / 30  # 1 フレームで進める時間の上限（秒）
START_LIVES = 3

BG_COLOR = (20, 24, 36)
TEXT_COLOR = (230, 230, 240)
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
BLOCK_POINTS = [50, 40, 30, 20, 10]  # 上の段ほど高得点


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
    points: int

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
            blocks.append(Block(pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT), BLOCK_COLORS[row], BLOCK_POINTS[row]))
    return blocks


@functools.cache
def get_font(size: int) -> pygame.font.Font:
    """指定した大きさのフォントを返す。同じ大きさなら 2 回目以降は作成済みのものを使う。"""
    return pygame.font.Font(None, size)


def draw_text(screen: pygame.Surface, text: str, size: int, center: tuple[float, float]) -> None:
    """文字列を、center が中心になるように描画する。"""
    image = get_font(size).render(text, True, TEXT_COLOR)
    screen.blit(image, image.get_rect(center=center))


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


class Scene:
    """シーンの基底クラス。各シーンは必要なメソッドだけを上書きする。"""

    def __init__(self) -> None:
        # 次に切り替えるシーン。None の間は現在のシーンを続ける
        self.next_scene: Scene | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        """キー入力などのイベントを 1 つ処理する。"""

    def update(self, dt: float) -> None:
        """状態を dt 秒ぶん進める。"""

    def draw(self, screen: pygame.Surface) -> None:
        """現在の状態を画面に描画する。"""


class TitleScene(Scene):
    """タイトル画面。スペースキーでプレイを始める。"""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.next_scene = PlayScene()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        draw_text(screen, "BREAKOUT", 80, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        draw_text(screen, "PRESS SPACE TO START", 32, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))


class PlayScene(Scene):
    """プレイ画面。クリアするか残機が無くなったら結果画面に進む。"""

    def __init__(self) -> None:
        super().__init__()
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = create_blocks()
        self.score = 0
        self.lives = START_LIVES

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.ball.launched:
            self.ball.launch()

    def update(self, dt: float) -> None:
        self.paddle.update(dt, read_direction())
        if not self.ball.launched:
            self.ball.follow(self.paddle)
            return

        for block in move_ball(self.ball, dt, self.paddle, self.blocks):
            self.score += block.points
        if not self.blocks:
            self.next_scene = ResultScene(self.score, cleared=True)
        elif self.ball.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives == 0:
                self.next_scene = ResultScene(self.score, cleared=False)
            else:
                self.ball = Ball()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        for block in self.blocks:
            block.draw(screen)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        draw_text(screen, f"SCORE {self.score}", 28, (90, 24))
        draw_text(screen, f"LIVES {self.lives}", 28, (SCREEN_WIDTH - 80, 24))
        if not self.ball.launched:
            draw_text(screen, "PRESS SPACE", 28, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6))


class ResultScene(Scene):
    """結果画面。スペースキーでタイトル画面に戻る。"""

    def __init__(self, score: int, cleared: bool) -> None:
        super().__init__()
        self.score = score
        self.cleared = cleared

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.next_scene = TitleScene()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        message = "GAME CLEAR!" if self.cleared else "GAME OVER"
        draw_text(screen, message, 72, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        draw_text(screen, f"SCORE {self.score}", 40, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        draw_text(screen, "PRESS SPACE TO TITLE", 28, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Step 6: Scenes")
    clock = pygame.time.Clock()
    scene: Scene = TitleScene()

    running = True
    while running:
        dt = min(clock.tick(FPS) / 1000, MAX_DT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            else:
                scene.handle_event(event)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

        # シーンの切り替えは、フレームの最後にまとめて行う
        if scene.next_scene is not None:
            scene = scene.next_scene

    pygame.quit()


if __name__ == "__main__":
    main()
