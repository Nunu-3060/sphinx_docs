"""第 3 章: フレーム数を基準にした移動と、デルタタイムを基準にした移動を比べる。

上の四角は「1 フレームに 4 ピクセル」、下の四角は「1 秒に 240 ピクセル」で動く。
フレームレートの上限を変えると、上の四角だけ速さが変わる。

操作方法:
    1 / 2 / 3 キー: フレームレートの上限を 30 / 60 / 144 FPS にする
    Esc キー: 終了する
"""

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 240
SPEED_PER_FRAME = 4.0  # ピクセル毎フレーム
SPEED_PER_SECOND = 240.0  # ピクセル毎秒（60 FPS なら上の四角と同じ速さ）
MAX_DT = 0.1  # 1 フレームで進める時間の上限（秒）
FPS_KEYS = {pygame.K_1: 30, pygame.K_2: 60, pygame.K_3: 144}


def wrap(x: float, width: float) -> float:
    """画面の右端から出たら左端に戻す。"""
    return x % width


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Frame-based vs time-based movement')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    fps_limit = 60
    x_frame = 0.0
    x_time = 0.0

    running = True
    while running:
        # 1. 入力
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in FPS_KEYS:
                    fps_limit = FPS_KEYS[event.key]

        # 2. 更新（tick は前のフレームからの経過時間をミリ秒で返す）
        dt = min(clock.tick(fps_limit) / 1000, MAX_DT)
        x_frame = wrap(x_frame + SPEED_PER_FRAME, SCREEN_WIDTH)
        x_time = wrap(x_time + SPEED_PER_SECOND * dt, SCREEN_WIDTH)

        # 3. 描画
        screen.fill((20, 24, 36))
        pygame.draw.rect(screen, (255, 160, 80), (x_frame, 60, 32, 32))
        pygame.draw.rect(screen, (90, 200, 255), (x_time, 150, 32, 32))
        info = f'FPS limit: {fps_limit}  actual: {clock.get_fps():.0f}  (keys 1/2/3)'
        screen.blit(font.render(info, True, (230, 230, 230)), (10, 10))
        screen.blit(font.render('per frame', True, (255, 160, 80)), (10, 100))
        screen.blit(font.render('per second (dt)', True, (90, 200, 255)), (10, 190))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
