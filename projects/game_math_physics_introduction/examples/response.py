"""第 12 章: 衝突応答（めり込みの解消、反発係数、力積、摩擦）。

箱の中で、大きさ（質量）の異なるボールがぶつかり合う。
重力と摩擦を切って反発係数を 1 にすると、運動エネルギーの合計がほぼ保たれることを確かめられる。

collision.py と同じフォルダーに置いて実行する。

操作方法:
    左クリック: ボールを追加する
    上下キー: 反発係数を増減する
    F キー: 摩擦の有無を切り替える
    G キー: 重力の有無を切り替える
    Esc キー: 終了する
"""

import itertools
import math
import random
from dataclasses import dataclass, field

import pygame
from pygame import Vector2

from collision import circle_circle_contact

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = 600.0  # ピクセル毎秒毎秒
STEP = 1 / 240  # 物理の 1 ステップの時間（秒）。1 フレームに 4 回進める
SUBSTEPS = 4
FRICTION = 0.3  # 摩擦係数
DENSITY = 0.01  # 面積あたりの質量


@dataclass
class Body:
    """円形の物体。inv_mass は質量の逆数で、0 なら動かない物体（質量が無限大）として扱う。"""

    position: Vector2
    velocity: Vector2
    radius: float
    inv_mass: float
    color: tuple[int, int, int] = field(default=(200, 200, 210))

    @property
    def mass(self) -> float:
        return 1 / self.inv_mass if self.inv_mass > 0 else float('inf')


def resolve_contact(a: Body, b: Body, normal: Vector2, depth: float, restitution: float, friction: float) -> None:
    """a と b の接触を解消する。normal は a から b へ向かう単位ベクトル、depth はめり込みの深さ。"""
    total_inv_mass = a.inv_mass + b.inv_mass
    if total_inv_mass == 0:
        return  # どちらも動かない

    # 1. めり込みの解消: 質量の逆数の比で押し分ける（軽い方が大きく動く）
    correction = normal * (depth / total_inv_mass)
    a.position -= correction * a.inv_mass
    b.position += correction * b.inv_mass

    # 2. 法線方向の速度を、反発係数に応じて反転させる力積
    relative = b.velocity - a.velocity
    normal_speed = relative.dot(normal)
    if normal_speed > 0:
        return  # すでに離れつつある
    j = -(1 + restitution) * normal_speed / total_inv_mass
    a.velocity -= normal * (j * a.inv_mass)
    b.velocity += normal * (j * b.inv_mass)

    # 3. 接線方向の摩擦: ずれる速度を打ち消す力積。大きさは法線方向の力積の friction 倍まで（クーロン摩擦）
    relative = b.velocity - a.velocity
    tangent = relative - normal * relative.dot(normal)
    if tangent.length_squared() < 1e-12:
        return
    tangent = tangent.normalize()
    jt = -relative.dot(tangent) / total_inv_mass
    jt = max(-friction * j, min(friction * j, jt))
    a.velocity -= tangent * (jt * a.inv_mass)
    b.velocity += tangent * (jt * b.inv_mass)


def bounce_inside(body: Body, width: float, height: float, restitution: float) -> None:
    """画面の四辺を、動かない壁として扱う。"""
    r = body.radius
    if body.position.x < r:
        body.position.x = r
        body.velocity.x = abs(body.velocity.x) * restitution
    elif body.position.x > width - r:
        body.position.x = width - r
        body.velocity.x = -abs(body.velocity.x) * restitution
    if body.position.y < r:
        body.position.y = r
        body.velocity.y = abs(body.velocity.y) * restitution
    elif body.position.y > height - r:
        body.position.y = height - r
        body.velocity.y = -abs(body.velocity.y) * restitution


def step_world(bodies: list[Body], dt: float, gravity: float, restitution: float, friction: float) -> None:
    """全体を dt 秒進める: 速度と位置の更新（半陰的オイラー法）→ 衝突の検出と応答。"""
    for body in bodies:
        if body.inv_mass > 0:
            body.velocity.y += gravity * dt
            body.position += body.velocity * dt
    for a, b in itertools.combinations(bodies, 2):
        contact = circle_circle_contact(a.position, a.radius, b.position, b.radius)
        if contact:
            resolve_contact(a, b, *contact, restitution, friction)
    for body in bodies:
        bounce_inside(body, SCREEN_WIDTH, SCREEN_HEIGHT, restitution)


def make_ball(rng: random.Random, position: Vector2) -> Body:
    radius = rng.uniform(10, 40)
    mass = DENSITY * math.pi * radius * radius  # 質量は面積に比例させる
    color = (rng.randint(100, 255), rng.randint(100, 255), rng.randint(100, 255))
    velocity = Vector2(rng.uniform(-200, 200), rng.uniform(-200, 0))
    return Body(Vector2(position), velocity, radius, 1 / mass, color)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Collision response with impulses')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    rng = random.Random(2)
    bodies = [make_ball(rng, Vector2(rng.uniform(50, 590), rng.uniform(50, 300))) for _ in range(12)]
    restitution = 0.8
    use_friction = True
    use_gravity = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bodies.append(make_ball(rng, Vector2(event.pos)))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    restitution = min(1.0, restitution + 0.1)
                elif event.key == pygame.K_DOWN:
                    restitution = max(0.0, restitution - 0.1)
                elif event.key == pygame.K_f:
                    use_friction = not use_friction
                elif event.key == pygame.K_g:
                    use_gravity = not use_gravity
        clock.tick(60)
        for _ in range(SUBSTEPS):
            step_world(bodies, STEP, GRAVITY if use_gravity else 0.0, restitution, FRICTION if use_friction else 0.0)

        energy = sum(0.5 * b.mass * b.velocity.length_squared() for b in bodies)
        screen.fill((20, 24, 36))
        for b in bodies:
            pygame.draw.circle(screen, b.color, b.position, b.radius)
        lines = [
            f'restitution: {restitution:.1f} (up/down)  friction: {use_friction} (F)  gravity: {use_gravity} (G)',
            f'kinetic energy: {energy:11.0f}',
        ]
        for i, text in enumerate(lines):
            screen.blit(font.render(text, True, (230, 230, 230)), (10, 10 + 22 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
