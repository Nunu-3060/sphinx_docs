"""ブロック崩し Step 1: ウィンドウを表示し、ゲームループを回す。

ウィンドウの閉じるボタンを押すと終了する。
"""

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60  # 1 秒あたりの更新回数の目標値
BG_COLOR = (20, 24, 36)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Step 1: Window")
    clock = pygame.time.Clock()

    running = True
    while running:
        # フレームレートを一定に保つため、必要なら待機する
        clock.tick(FPS)

        # 1. 入力: 溜まっているイベントをすべて処理する
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. 更新: まだ動かすものは無い

        # 3. 描画: 画面を塗りつぶしてから表示に反映する
        screen.fill(BG_COLOR)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
