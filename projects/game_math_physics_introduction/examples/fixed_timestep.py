"""第 3 章: 固定タイムステップと描画の補間。

物理の更新を 1 秒に 15 回（わざと少なくしている）に固定し、描画は 60 FPS で行う。
上の四角は最後に更新した位置をそのまま描き、下の四角は直前の 2 回の更新結果を補間して描く。

操作方法:
    1 / 2 / 3 キー: 物理の更新頻度を 15 / 30 / 60 Hz にする
    Esc キー: 終了する
"""

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 240
SPEED = 300.0  # ピクセル毎秒
BOX_SIZE = 32
MAX_FRAME_TIME = 0.25  # 1 フレームで処理する時間の上限（秒）
MAX_STEPS = 8  # 1 フレームで行う更新の回数の上限
RATE_KEYS = {pygame.K_1: 15, pygame.K_2: 30, pygame.K_3: 60}


def consume_time(accumulator: float, frame_time: float, step: float, max_steps: int = MAX_STEPS) -> tuple[int, float]:
    """経過時間をアキュムレーターに貯め、固定ステップで何回更新するかと、残った時間を返す。"""
    accumulator += frame_time
    steps = 0
    while accumulator >= step and steps < max_steps:
        accumulator -= step
        steps += 1
    if steps == max_steps:
        # 処理が追いつかないときは、残りの時間を捨てて遅れが膨らみ続けるのを防ぐ
        accumulator = min(accumulator, step)
    return steps, accumulator


def lerp(a: float, b: float, t: float) -> float:
    """a から b へ割合 t（0～1）だけ進んだ値を返す。"""
    return a + (b - a) * t


class Box:
    """左右の壁で跳ね返りながら等速で動く四角。"""

    def __init__(self) -> None:
        self.x = 0.0
        self.previous_x = 0.0  # 直前の更新の前の位置（補間に使う）
        self.vx = SPEED

    def update(self, step: float) -> None:
        self.previous_x = self.x
        self.x += self.vx * step
        if self.x < 0:
            self.x, self.vx = -self.x, -self.vx
        elif self.x > SCREEN_WIDTH - BOX_SIZE:
            self.x, self.vx = 2 * (SCREEN_WIDTH - BOX_SIZE) - self.x, -self.vx


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Fixed timestep and interpolation')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    box = Box()
    rate = 15
    accumulator = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in RATE_KEYS:
                    rate = RATE_KEYS[event.key]

        frame_time = min(clock.tick(60) / 1000, MAX_FRAME_TIME)
        step = 1 / rate
        steps, accumulator = consume_time(accumulator, frame_time, step)
        for _ in range(steps):
            box.update(step)
        alpha = accumulator / step  # 次の更新までに進んだ割合

        screen.fill((20, 24, 36))
        pygame.draw.rect(screen, (255, 160, 80), (box.x, 60, BOX_SIZE, BOX_SIZE))
        drawn_x = lerp(box.previous_x, box.x, alpha)
        pygame.draw.rect(screen, (90, 200, 255), (drawn_x, 150, BOX_SIZE, BOX_SIZE))
        screen.blit(font.render(f'physics: {rate} Hz  (keys 1/2/3)', True, (230, 230, 230)), (10, 10))
        screen.blit(font.render('latest state', True, (255, 160, 80)), (10, 100))
        screen.blit(font.render('interpolated', True, (90, 200, 255)), (10, 190))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
