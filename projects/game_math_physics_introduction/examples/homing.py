"""第 5 章: 旋回速度に上限があるホーミング弾。

3 発の弾が、それぞれ異なる旋回速度でマウスを追いかける。
旋回速度が小さい弾ほど大回りになり、目標の周りを回り続けることもある。

操作方法:
    マウス: 目標を動かす
    Esc キー: 終了する
"""

import math

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MISSILE_SPEED = 220.0  # ピクセル毎秒
TURN_RATES_DEG = (90.0, 180.0, 360.0)  # 旋回速度（度毎秒）
COLORS = ((255, 120, 120), (255, 210, 90), (120, 220, 255))
TRAIL_LENGTH = 40


def wrap_angle(angle: float) -> float:
    """角度を -π 以上 π 未満の範囲に収める。"""
    return (angle + math.pi) % math.tau - math.pi


def angle_difference(current: float, target: float) -> float:
    """current から target へ回るときの、最短の回転量（-π 以上 π 未満）。正なら角度が増える向きに回る。"""
    return wrap_angle(target - current)


def move_toward_angle(current: float, target: float, max_delta: float) -> float:
    """current を target へ、最短の向きに最大 max_delta だけ回した角度を返す。"""
    diff = angle_difference(current, target)
    if abs(diff) <= max_delta:
        return target
    return current + math.copysign(max_delta, diff)


def lerp_angle(a: float, b: float, t: float) -> float:
    """角度 a から b へ、最短の向きに割合 t だけ進んだ角度を返す。"""
    return a + angle_difference(a, b) * t


class Missile:
    """一定の速さで進み、向きだけを少しずつ目標へ向けていく弾。"""

    def __init__(self, turn_rate: float, color: tuple[int, int, int]) -> None:
        self.turn_rate = turn_rate  # ラジアン毎秒
        self.color = color
        self.position = pygame.Vector2(40, SCREEN_HEIGHT - 40)
        self.heading = -math.pi / 2  # 進む向き（画面の上向き）
        self.trail: list[pygame.Vector2] = []

    def update(self, dt: float, target: pygame.Vector2) -> None:
        desired = math.atan2(target.y - self.position.y, target.x - self.position.x)
        self.heading = move_toward_angle(self.heading, desired, self.turn_rate * dt)
        self.position += pygame.Vector2(math.cos(self.heading), math.sin(self.heading)) * MISSILE_SPEED * dt
        self.trail.append(pygame.Vector2(self.position))
        del self.trail[:-TRAIL_LENGTH]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Homing missiles with limited turn rate')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    missiles = [Missile(math.radians(rate), color) for rate, color in zip(TURN_RATES_DEG, COLORS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        dt = min(clock.tick(60) / 1000, 0.1)
        target = pygame.Vector2(pygame.mouse.get_pos())
        for missile in missiles:
            missile.update(dt, target)

        screen.fill((20, 24, 36))
        pygame.draw.circle(screen, (240, 240, 240), target, 8, 2)
        for i, missile in enumerate(missiles):
            if len(missile.trail) >= 2:
                pygame.draw.lines(screen, missile.color, False, missile.trail, 1)
            pygame.draw.circle(screen, missile.color, missile.position, 5)
            label = f'turn rate {TURN_RATES_DEG[i]:.0f} deg/s'
            screen.blit(font.render(label, True, missile.color), (10, 10 + 22 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
