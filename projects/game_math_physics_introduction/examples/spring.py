"""第 13 章: ばねとダンパーでマウスを追いかける。

同じ固有振動数で減衰比だけが異なる 3 つの四角が、マウスの位置を目標にして動く。
減衰比が 1 未満だと行き過ぎて揺れ、1 だと揺れずに最も早く落ち着き、1 より大きいとゆっくり近づく。

操作方法:
    マウス: 目標を動かす
    Esc キー: 終了する
"""

import math

import pygame
from pygame import Vector2

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FREQUENCY = 2.0  # 固有振動数（Hz）。減衰が無いときに 1 秒に揺れる回数
DAMPING_RATIOS = (0.2, 1.0, 2.5)  # 減衰比
COLORS = ((255, 120, 120), (120, 230, 140), (120, 170, 255))
OFFSETS = (Vector2(-60, 0), Vector2(0, 0), Vector2(60, 0))  # 重ならないよう、目標を左右にずらす


def spring_coefficients(frequency: float, damping_ratio: float) -> tuple[float, float]:
    """固有振動数と減衰比から、質量 1 あたりのばね定数 k と減衰係数 c を求める。"""
    omega = math.tau * frequency  # 角振動数
    return omega * omega, 2 * damping_ratio * omega


def spring_step(position: Vector2, velocity: Vector2, target: Vector2, k: float, c: float,
                dt: float) -> tuple[Vector2, Vector2]:
    """ばねの力 -k(x - target) と減衰力 -cv を受けて dt 秒進める（半陰的オイラー法）。"""
    acceleration = (target - position) * k - velocity * c
    velocity = velocity + acceleration * dt
    return position + velocity * dt, velocity


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Damped springs')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    coefficients = [spring_coefficients(FREQUENCY, ratio) for ratio in DAMPING_RATIOS]
    positions = [Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) + o for o in OFFSETS]
    velocities = [Vector2() for _ in OFFSETS]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        dt = min(clock.tick(60) / 1000, 1 / 30)
        mouse = Vector2(pygame.mouse.get_pos())

        screen.fill((20, 24, 36))
        for i, ((k, c), offset, color) in enumerate(zip(coefficients, OFFSETS, COLORS)):
            target = mouse + offset
            positions[i], velocities[i] = spring_step(positions[i], velocities[i], target, k, c, dt)
            pygame.draw.circle(screen, color, target, 4)
            pygame.draw.line(screen, (70, 80, 100), target, positions[i])
            pygame.draw.rect(screen, color, (positions[i].x - 14, positions[i].y - 14, 28, 28))
            label = f'damping ratio {DAMPING_RATIOS[i]}'
            screen.blit(font.render(label, True, color), (10, 10 + 22 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
