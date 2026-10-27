"""第 11 章: 衝突判定を目で確かめる。

マウスで図形を動かす。重なると赤くなり、押し戻す向き（法線）とめり込みの深さを線で示す。
押し戻した後の位置を輪郭で描く。

collision.py と同じフォルダーに置いて実行する。

操作方法:
    1 キー: 円と円
    2 キー: 円と長方形（長方形の上で円に最も近い点を示す）
    3 キー: レイと円・長方形（左上からマウスの方向へレイを飛ばす）
    4 キー: 回転した多角形どうし（分離軸定理）
    Esc キー: 終了する
"""

import math

import pygame
from pygame import Vector2

from collision import (AABB, Contact, circle_aabb_contact, circle_circle_contact, closest_point_on_aabb,
                       polygon_contact, ray_aabb, ray_circle)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
HIT_COLOR = (240, 90, 90)
FREE_COLOR = (90, 160, 240)
OTHER_COLOR = (200, 200, 210)
MODE_NAMES = {1: 'circle vs circle', 2: 'circle vs AABB', 3: 'ray vs circle / AABB', 4: 'polygon vs polygon (SAT)'}


def regular_polygon(center: Vector2, radius: float, sides: int, angle: float) -> list[Vector2]:
    """正多角形の頂点のリスト。"""
    return [center + Vector2(radius, 0).rotate_rad(angle + math.tau * i / sides) for i in range(sides)]


def draw_contact(screen: pygame.Surface, point: Vector2, contact: Contact) -> None:
    """接触点から法線の向きに、めり込みの深さの長さ（見やすいよう最低 20 ピクセル）の矢印を描く。"""
    normal, depth = contact
    end = point + normal * max(depth, 20)
    pygame.draw.line(screen, (255, 230, 120), point, end, 3)
    pygame.draw.circle(screen, (255, 230, 120), end, 4)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Collision detection')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    mode = 1
    time = 0.0
    fixed_center = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    box = AABB.from_center(fixed_center.x, fixed_center.y, 200, 120)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_4:
                mode = event.key - pygame.K_0
        time += min(clock.tick(60) / 1000, 0.1)
        mouse = Vector2(pygame.mouse.get_pos())
        screen.fill((20, 24, 36))

        if mode == 1:
            contact = circle_circle_contact(fixed_center, 80, mouse, 40)
            pygame.draw.circle(screen, OTHER_COLOR, fixed_center, 80, 2)
            pygame.draw.circle(screen, HIT_COLOR if contact else FREE_COLOR, mouse, 40, 2)
            if contact:
                normal, depth = contact
                pygame.draw.circle(screen, (120, 120, 140), mouse + normal * depth, 40, 1)
                draw_contact(screen, fixed_center + normal * 80, contact)
        elif mode == 2:
            contact = circle_aabb_contact(mouse, 40, box)
            pygame.draw.rect(screen, OTHER_COLOR, (box.left, box.top, box.right - box.left, box.bottom - box.top), 2)
            pygame.draw.circle(screen, HIT_COLOR if contact else FREE_COLOR, mouse, 40, 2)
            closest = closest_point_on_aabb(mouse, box)
            pygame.draw.line(screen, (120, 120, 140), mouse, closest)
            pygame.draw.circle(screen, (255, 255, 255), closest, 4)
            if contact:
                normal, depth = contact
                pygame.draw.circle(screen, (120, 120, 140), mouse + normal * depth, 40, 1)
                draw_contact(screen, closest, contact)
        elif mode == 3:
            origin = Vector2(30, 30)
            direction = mouse - origin
            if direction.length_squared() > 0:
                direction = direction.normalize()
            circle_center = Vector2(200, 320)
            small_box = AABB(380, 160, 520, 260)
            results = (ray_circle(origin, direction, circle_center, 60), ray_aabb(origin, direction, small_box))
            hits = [t for t in results if t is not None]
            pygame.draw.circle(screen, OTHER_COLOR, circle_center, 60, 2)
            pygame.draw.rect(screen, OTHER_COLOR, (380, 160, 140, 100), 2)
            length = min(hits) if hits else 1000.0
            pygame.draw.line(screen, HIT_COLOR if hits else FREE_COLOR, origin, origin + direction * length, 2)
            if hits:
                pygame.draw.circle(screen, (255, 230, 120), origin + direction * length, 6)
        else:
            rotating = regular_polygon(fixed_center, 90, 4, time * 0.7)
            moving = regular_polygon(mouse, 50, 5, -time)
            contact = polygon_contact(rotating, moving)
            pygame.draw.polygon(screen, OTHER_COLOR, rotating, 2)
            pygame.draw.polygon(screen, HIT_COLOR if contact else FREE_COLOR, moving, 2)
            if contact:
                normal, depth = contact
                pygame.draw.polygon(screen, (120, 120, 140), [p + normal * depth for p in moving], 1)
                draw_contact(screen, mouse, contact)

        screen.blit(font.render(f'{mode}: {MODE_NAMES[mode]}  (keys 1-4)', True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
