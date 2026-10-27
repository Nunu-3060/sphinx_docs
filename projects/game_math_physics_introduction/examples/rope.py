"""第 13 章: ベルレ法と距離拘束で、ロープと布を揺らす。

各点は「今の位置」と「1 ステップ前の位置」だけを持ち、速度はその差から求める（位置ベルレ法）。
点と点の距離を一定に保つ拘束を何度も繰り返し満たすことで、伸びないロープや布になる。

操作方法:
    C キー: ロープと布を切り替える
    ロープ: 先頭の点がマウスに付いてくる
    布: 左ボタンを押している間、マウスに最も近い点をつかんで動かす
    Esc キー: 終了する
"""

from dataclasses import dataclass

import pygame
from pygame import Vector2

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = Vector2(0, 900)  # ピクセル毎秒毎秒
DAMPING = 0.995  # 1 ステップごとに速度に掛ける値（空気抵抗の代わり）
ITERATIONS = 12  # 拘束を満たす処理を繰り返す回数
STEP = 1 / 60
ROPE_POINTS = 24
ROPE_SEGMENT = 12.0
CLOTH_COLUMNS = 20
CLOTH_ROWS = 14
CLOTH_SPACING = 16.0


@dataclass
class Point:
    position: Vector2
    previous: Vector2
    pinned: bool = False  # True なら拘束やベルレ法で動かさない


@dataclass
class Stick:
    """2 つの点の距離を length に保つ拘束。"""

    a: Point
    b: Point
    length: float


def verlet_step(points: list[Point], dt: float) -> None:
    """位置ベルレ法: 新しい位置 = 今の位置 + (今の位置 - 前の位置) + 加速度 × dt^2。"""
    for p in points:
        if p.pinned:
            continue
        velocity = (p.position - p.previous) * DAMPING  # 1 ステップあたりの移動量
        p.previous = Vector2(p.position)
        p.position += velocity + GRAVITY * (dt * dt)


def satisfy(stick: Stick) -> None:
    """2 つの点を結ぶ線の向きに動かして、距離を length に戻す。固定された点は動かさない。"""
    delta = stick.b.position - stick.a.position
    distance = delta.length()
    if distance < 1e-9:
        return
    error = (distance - stick.length) / distance  # 伸びている割合
    movable = (not stick.a.pinned) + (not stick.b.pinned)
    if movable == 0:
        return
    shift = delta * (error / movable)
    if not stick.a.pinned:
        stick.a.position += shift
    if not stick.b.pinned:
        stick.b.position -= shift


def make_rope() -> tuple[list[Point], list[Stick]]:
    starts = [Vector2(320 + i * ROPE_SEGMENT, 80) for i in range(ROPE_POINTS)]
    points = [Point(p, Vector2(p)) for p in starts]
    points[0].pinned = True
    sticks = [Stick(points[i], points[i + 1], ROPE_SEGMENT) for i in range(ROPE_POINTS - 1)]
    return points, sticks


def make_cloth() -> tuple[list[Point], list[Stick]]:
    left = (SCREEN_WIDTH - (CLOTH_COLUMNS - 1) * CLOTH_SPACING) / 2
    points = []
    for row in range(CLOTH_ROWS):
        for col in range(CLOTH_COLUMNS):
            p = Vector2(left + col * CLOTH_SPACING, 60 + row * CLOTH_SPACING)
            points.append(Point(p, Vector2(p), pinned=(row == 0 and col % 4 == 0)))
    sticks = []
    for row in range(CLOTH_ROWS):
        for col in range(CLOTH_COLUMNS):
            i = row * CLOTH_COLUMNS + col
            if col + 1 < CLOTH_COLUMNS:
                sticks.append(Stick(points[i], points[i + 1], CLOTH_SPACING))
            if row + 1 < CLOTH_ROWS:
                sticks.append(Stick(points[i], points[i + CLOTH_COLUMNS], CLOTH_SPACING))
    return points, sticks


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Verlet rope and cloth')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    cloth_mode = False
    points, sticks = make_rope()
    grabbed: Point | None = None

    running = True
    while running:
        mouse = Vector2(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                cloth_mode = not cloth_mode
                points, sticks = make_cloth() if cloth_mode else make_rope()
                grabbed = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and cloth_mode:
                grabbed = min(points, key=lambda p: p.position.distance_squared_to(mouse))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                grabbed = None
        clock.tick(60)

        if not cloth_mode:
            points[0].position = Vector2(mouse)
        verlet_step(points, STEP)
        for _ in range(ITERATIONS):
            if grabbed is not None:
                grabbed.position = Vector2(mouse)
            for stick in sticks:
                satisfy(stick)

        screen.fill((20, 24, 36))
        for stick in sticks:
            pygame.draw.line(screen, (200, 210, 230), stick.a.position, stick.b.position)
        for p in points:
            if p.pinned:
                pygame.draw.circle(screen, (240, 120, 120), p.position, 4)
        mode = 'cloth (drag with the mouse)' if cloth_mode else 'rope (follows the mouse)'
        screen.blit(font.render(f'{mode}   C: switch', True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
