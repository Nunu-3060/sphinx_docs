"""ブロック崩し Step 2: キー入力でパドルを動かす。

操作方法:
    左右キー（または A / D キー）: パドルを動かす
    Esc キー: 終了する
"""

import pygame

# --- 画面とゲーム全体の設定 ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
MAX_DT = 1 / 30  # 1 フレームで進める時間の上限（秒）

BG_COLOR = (20, 24, 36)
PADDLE_COLOR = (200, 210, 255)

# --- パドル ---
PADDLE_WIDTH = 96
PADDLE_HEIGHT = 12
PADDLE_Y = SCREEN_HEIGHT - 40
PADDLE_SPEED = 480.0  # ピクセル毎秒


class Paddle:
    """プレイヤーが操作するパドル。"""

    def __init__(self) -> None:
        # 位置を小数で保持するため、pygame-ce の FRect を使う
        self.rect = pygame.FRect(0, 0, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.rect.midtop = (SCREEN_WIDTH / 2, PADDLE_Y)

    def update(self, dt: float, direction: float) -> None:
        """direction（-1: 左、0: 停止、1: 右）の向きに dt 秒ぶん動かす。画面外には出さない。"""
        self.rect.x += direction * PADDLE_SPEED * dt
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect, border_radius=4)


def read_direction() -> float:
    """押されているキーから、パドルを動かす向き（-1、0、1）を求める。"""
    keys = pygame.key.get_pressed()
    direction = 0.0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        direction -= 1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        direction += 1
    return direction


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Step 2: Paddle")
    clock = pygame.time.Clock()
    paddle = Paddle()

    running = True
    while running:
        # 前のフレームからの経過時間（秒）。処理落ちしても MAX_DT を超えないようにする
        dt = min(clock.tick(FPS) / 1000, MAX_DT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        paddle.update(dt, read_direction())

        screen.fill(BG_COLOR)
        paddle.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
