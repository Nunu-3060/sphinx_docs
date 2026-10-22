"""ブロック崩し Step 7: 効果音と演出を加えて完成させる。

操作方法:
    左右キー（または A / D キー）: パドルを動かす
    スペースキー: ボールを発射する、次の画面に進む
    Esc キー: 終了する

ブラウザー版（pygbag）でも動くように、メインループは asyncio を使って書いている。
"""

import asyncio
import functools
import math
import random
from array import array
from dataclasses import dataclass, field

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

# --- 演出 ---
PARTICLE_COUNT = 12  # ブロック 1 つを壊したときに飛び散る破片の数
PARTICLE_LIFE = 0.5  # 破片が消えるまでの時間（秒）
GRAVITY = 600.0  # 破片にかかる重力加速度（ピクセル毎秒毎秒）


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


@dataclass
class HitResult:
    """1 フレームの移動の間に、ボールが何に当たったか。"""

    wall: bool = False
    paddle: bool = False
    blocks: list[Block] = field(default_factory=list)


def move_ball(ball: Ball, dt: float, paddle: Paddle, blocks: list[Block]) -> HitResult:
    """ボールを dt 秒ぶん動かし、壁・ブロック・パドルで反射させる。

    x 方向と y 方向を別々に動かし、それぞれの移動の直後に当たり判定を行う。
    こうすると、ぶつかった面（側面か上下の面か）が移動の向きから分かる。
    当たったブロックは blocks から取り除き、戻り値の HitResult に入れて返す。
    """
    result = HitResult()

    # x 方向に動かし、左右の壁とブロックの側面で反射させる
    ball.rect.x += ball.velocity.x * dt
    if ball.rect.left < 0:
        ball.rect.left = 0
        ball.velocity.x = abs(ball.velocity.x)
        result.wall = True
    elif ball.rect.right > SCREEN_WIDTH:
        ball.rect.right = SCREEN_WIDTH
        ball.velocity.x = -abs(ball.velocity.x)
        result.wall = True
    block = pop_hit_block(ball, blocks)
    if block is not None:
        # めり込んだ分を押し戻してから向きを反転する
        if ball.velocity.x > 0:
            ball.rect.right = block.rect.left
        else:
            ball.rect.left = block.rect.right
        ball.velocity.x *= -1
        result.blocks.append(block)

    # y 方向に動かし、上の壁とブロックの上下の面で反射させる
    ball.rect.y += ball.velocity.y * dt
    if ball.rect.top < 0:
        ball.rect.top = 0
        ball.velocity.y = abs(ball.velocity.y)
        result.wall = True
    block = pop_hit_block(ball, blocks)
    if block is not None:
        if ball.velocity.y > 0:
            ball.rect.bottom = block.rect.top
        else:
            ball.rect.top = block.rect.bottom
        ball.velocity.y *= -1
        result.blocks.append(block)

    # 下向きに動いているときだけ判定し、パドルに何度も当たり続けるのを防ぐ
    if ball.velocity.y > 0 and ball.rect.colliderect(paddle.rect):
        ball.rect.bottom = paddle.rect.top
        offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
        ball.velocity = paddle_bounce_velocity(offset, ball.velocity.length())
        result.paddle = True

    return result


def make_tone(frequency: float, duration: float, volume: float = 0.3) -> pygame.mixer.Sound:
    """矩形波の効果音をプログラムで生成する。音声ファイルを用意しなくてよい。"""
    mixer_settings = pygame.mixer.get_init()
    if mixer_settings is None:
        raise pygame.error("mixer is not initialized")
    # 量子化ビット数は、pygame の既定である 16 ビット符号付き整数を前提とする
    sample_rate, _, channels = mixer_settings
    period = sample_rate / frequency  # 波 1 周期あたりのサンプル数
    total = int(sample_rate * duration)
    samples = array("h")
    for i in range(total):
        value = volume * 32767 if i % period < period / 2 else -volume * 32767
        fade = 1 - i / total  # 徐々に音量を下げ、音の終わりに出る雑音を防ぐ
        samples.extend([int(value * fade)] * channels)
    return pygame.mixer.Sound(buffer=samples.tobytes())


class SoundBank:
    """効果音をまとめて管理する。音声を出力できない環境では何も鳴らさない。"""

    def __init__(self) -> None:
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            return
        self.sounds = {
            "wall": make_tone(330, 0.03),
            "paddle": make_tone(440, 0.05),
            "block": make_tone(880, 0.06),
            "miss": make_tone(110, 0.4),
            "clear": make_tone(1320, 0.5),
        }

    def play(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()


@dataclass
class Particle:
    """ブロックを壊したときに飛び散る破片。"""

    position: pygame.Vector2
    velocity: pygame.Vector2
    color: tuple[int, int, int]
    life: float = PARTICLE_LIFE  # 残り時間（秒）


def spawn_particles(particles: list[Particle], center: tuple[float, float], color: tuple[int, int, int]) -> None:
    """center からランダムな向きに飛び散る破片を追加する。"""
    for _ in range(PARTICLE_COUNT):
        velocity = pygame.Vector2(random.uniform(60, 240), 0).rotate(random.uniform(0, 360))
        particles.append(Particle(pygame.Vector2(center), velocity, color))


def update_particles(particles: list[Particle], dt: float) -> None:
    """破片を重力に従って動かし、時間切れのものを取り除く。"""
    for particle in particles:
        particle.velocity.y += GRAVITY * dt
        particle.position += particle.velocity * dt
        particle.life -= dt
    particles[:] = [particle for particle in particles if particle.life > 0]


def draw_particles(screen: pygame.Surface, particles: list[Particle]) -> None:
    """破片を描画する。残り時間が短いものほど小さく描く。"""
    for particle in particles:
        size = 2 + 4 * particle.life / PARTICLE_LIFE
        rect = pygame.FRect(0, 0, size, size)
        rect.center = (particle.position.x, particle.position.y)
        pygame.draw.rect(screen, particle.color, rect)


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

    def __init__(self, sounds: SoundBank) -> None:
        super().__init__()
        self.sounds = sounds

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.next_scene = PlayScene(self.sounds)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        draw_text(screen, "BREAKOUT", 80, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        draw_text(screen, "PRESS SPACE TO START", 32, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))


class PlayScene(Scene):
    """プレイ画面。クリアするか残機が無くなったら結果画面に進む。"""

    def __init__(self, sounds: SoundBank) -> None:
        super().__init__()
        self.sounds = sounds
        self.paddle = Paddle()
        self.ball = Ball()
        self.blocks = create_blocks()
        self.particles: list[Particle] = []
        self.score = 0
        self.lives = START_LIVES

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.ball.launched:
            self.ball.launch()

    def update(self, dt: float) -> None:
        self.paddle.update(dt, read_direction())
        update_particles(self.particles, dt)
        if not self.ball.launched:
            self.ball.follow(self.paddle)
            return

        result = move_ball(self.ball, dt, self.paddle, self.blocks)
        if result.wall:
            self.sounds.play("wall")
        if result.paddle:
            self.sounds.play("paddle")
        for block in result.blocks:
            self.score += block.points
            spawn_particles(self.particles, block.rect.center, block.color)
            self.sounds.play("block")

        if not self.blocks:
            self.sounds.play("clear")
            self.next_scene = ResultScene(self.sounds, self.score, cleared=True)
        elif self.ball.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            self.sounds.play("miss")
            if self.lives == 0:
                self.next_scene = ResultScene(self.sounds, self.score, cleared=False)
            else:
                self.ball = Ball()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        for block in self.blocks:
            block.draw(screen)
        draw_particles(screen, self.particles)
        self.paddle.draw(screen)
        self.ball.draw(screen)
        draw_text(screen, f"SCORE {self.score}", 28, (90, 24))
        draw_text(screen, f"LIVES {self.lives}", 28, (SCREEN_WIDTH - 80, 24))
        if not self.ball.launched:
            draw_text(screen, "PRESS SPACE", 28, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6))


class ResultScene(Scene):
    """結果画面。スペースキーでタイトル画面に戻る。"""

    def __init__(self, sounds: SoundBank, score: int, cleared: bool) -> None:
        super().__init__()
        self.sounds = sounds
        self.score = score
        self.cleared = cleared

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.next_scene = TitleScene(self.sounds)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BG_COLOR)
        message = "GAME CLEAR!" if self.cleared else "GAME OVER"
        draw_text(screen, message, 72, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
        draw_text(screen, f"SCORE {self.score}", 40, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        draw_text(screen, "PRESS SPACE TO TITLE", 28, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 3))


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout")
    clock = pygame.time.Clock()
    scene: Scene = TitleScene(SoundBank())

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

        # ブラウザー上では、ここで処理をブラウザーに返して画面を更新させる
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
