"""第 13 章: パーティクル（火花・噴水）。

1 つ 1 つの粒子は、位置・速度・残り寿命だけを持つ単純な点である。
重力と空気抵抗を受けて動き、寿命が減るにつれて小さく暗くなり、寿命が尽きたら消える。

操作方法:
    左クリック: クリックした位置で爆発させる
    Esc キー: 終了する
"""

import math
import random
from dataclasses import dataclass

import pygame
from pygame import Vector2

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = Vector2(0, 400)  # ピクセル毎秒毎秒
DRAG = 1.5  # 空気抵抗の強さ（1 秒あたり）
FOUNTAIN_RATE = 120  # 噴水が 1 秒あたりに出す粒子の数
BURST_COUNT = 150  # 爆発 1 回で出す粒子の数


@dataclass
class Particle:
    position: Vector2
    velocity: Vector2
    life: float  # 残り寿命（秒）
    max_life: float
    color: tuple[int, int, int]
    size: float


def update_particles(particles: list[Particle], dt: float) -> list[Particle]:
    """粒子を dt 秒進め、寿命が残っているものだけを返す。"""
    drag_factor = math.exp(-DRAG * dt)  # 速度が 1 秒で exp(-DRAG) 倍になる減衰（フレームレートによらない）
    alive = []
    for p in particles:
        p.life -= dt
        if p.life <= 0:
            continue
        p.velocity = (p.velocity + GRAVITY * dt) * drag_factor
        p.position += p.velocity * dt
        alive.append(p)
    return alive


def burst(rng: random.Random, position: Vector2) -> list[Particle]:
    """全方向に飛び散る火花。"""
    result = []
    for _ in range(BURST_COUNT):
        angle = rng.uniform(0, math.tau)
        speed = rng.uniform(50, 400)
        life = rng.uniform(0.4, 1.2)
        color = (255, rng.randint(120, 220), 60)
        result.append(Particle(Vector2(position), Vector2(speed, 0).rotate_rad(angle), life, life, color, 4))
    return result


def fountain(rng: random.Random, position: Vector2) -> Particle:
    """上向きに少し広がって吹き出す水しぶき。"""
    angle = math.radians(-90 + rng.uniform(-12, 12))
    speed = rng.uniform(380, 460)
    life = rng.uniform(1.5, 2.0)
    color = (90, rng.randint(160, 220), 255)
    return Particle(Vector2(position), Vector2(speed, 0).rotate_rad(angle), life, life, color, 3)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Particles')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    rng = random.Random(0)
    particles: list[Particle] = []
    spawn_debt = 0.0  # まだ出していない粒子の数（端数を次のフレームに持ち越す）

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                particles.extend(burst(rng, Vector2(event.pos)))
        dt = min(clock.tick(60) / 1000, 0.1)

        spawn_debt += FOUNTAIN_RATE * dt
        while spawn_debt >= 1:
            particles.append(fountain(rng, Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20)))
            spawn_debt -= 1
        particles = update_particles(particles, dt)

        screen.fill((20, 24, 36))
        for p in particles:
            ratio = p.life / p.max_life  # 1 から 0 へ減っていく
            color = tuple(int(c * ratio) for c in p.color)
            pygame.draw.circle(screen, color, p.position, max(1.0, p.size * ratio))
        screen.blit(font.render(f'particles: {len(particles)}  (click to explode)', True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
