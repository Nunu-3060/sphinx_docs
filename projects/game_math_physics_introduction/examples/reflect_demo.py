"""第 4 章: 反射ベクトルを求める。

マウスの位置から鏡の中心に向けて光線を飛ばし、反射した向きを描く。

操作方法:
    マウス: 光線の出発点を動かす
    Q / E キー: 鏡を回す
    Esc キー: 終了する
"""

import math

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MIRROR_HALF_LENGTH = 120.0
TURN_SPEED = math.radians(60)  # 鏡を回す速さ（ラジアン毎秒）


def reflect(v: pygame.Vector2, normal: pygame.Vector2) -> pygame.Vector2:
    """単位ベクトル normal を法線とする面で v を反射させる（pygame.Vector2.reflect と同じ結果になる）。"""
    return v - normal * (2 * v.dot(normal))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Reflection vector')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7)
    mirror_angle = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        dt = min(clock.tick(60) / 1000, 0.1)
        keys = pygame.key.get_pressed()
        mirror_angle += (keys[pygame.K_e] - keys[pygame.K_q]) * TURN_SPEED * dt

        along = pygame.Vector2(math.cos(mirror_angle), math.sin(mirror_angle))  # 鏡に沿った単位ベクトル
        normal = pygame.Vector2(along.y, -along.x)  # 鏡に垂直な単位ベクトル（法線）
        source = pygame.Vector2(pygame.mouse.get_pos())
        incoming = center - source  # 入射する光線の向き
        outgoing = reflect(incoming, normal)

        screen.fill((20, 24, 36))
        pygame.draw.line(screen, (180, 200, 230), center - along * MIRROR_HALF_LENGTH,
                         center + along * MIRROR_HALF_LENGTH, 4)
        pygame.draw.line(screen, (120, 120, 140), center, center + normal * 60, 2)
        pygame.draw.line(screen, (255, 200, 80), source, center, 2)
        pygame.draw.line(screen, (90, 220, 255), center, center + outgoing, 2)
        pygame.draw.circle(screen, (255, 200, 80), source, 6)
        text = f'incoming: ({incoming.x:.0f}, {incoming.y:.0f})  reflected: ({outgoing.x:.0f}, {outgoing.y:.0f})'
        screen.blit(font.render(text, True, (230, 230, 230)), (10, 10))
        screen.blit(font.render('Q / E: rotate the mirror', True, (230, 230, 230)), (10, 32))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
