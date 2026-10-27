"""第 6 章: 2D カメラ（スクロール・ズーム・回転・揺れ）とクリック位置の逆変換。

ワールド座標から画面座標への変換（ビュー変換）を行列で表し、すべての物をこの行列で描く。
クリックした位置は、ビュー変換の逆行列でワールド座標に戻し、そこに印を置く。

transform2d.py と同じフォルダーに置いて実行する。

操作方法:
    矢印キー: プレイヤー（カメラが追いかける）を動かす
    Z / X キー: ズームアウト / ズームイン
    C / V キー: カメラを回す
    スペースキー: 画面を揺らす
    左クリック: クリックした位置（ワールド座標）に印を置く
    Esc キー: 終了する
"""

import math
import random

import pygame

from transform2d import Mat3

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WORLD_SIZE = 2000
GRID_STEP = 100
PLAYER_SPEED = 300.0  # ワールド座標の単位毎秒
ZOOM_SPEED = 1.5  # 1 秒あたりに何倍にするか
TURN_SPEED = math.radians(60)
SHAKE_DECAY = 1.5  # 揺れの強さが 1 秒に減る量
MAX_SHAKE_OFFSET = 16.0  # 揺れの最大のずれ（ピクセル）


def view_matrix(camera: pygame.Vector2, zoom: float, angle: float, shake: pygame.Vector2) -> Mat3:
    """ワールド座標を画面座標に変換する行列。右から順に適用される。"""
    return (
        Mat3.translation(SCREEN_WIDTH / 2 + shake.x, SCREEN_HEIGHT / 2 + shake.y)  # 4. 画面の中央へ（揺れのずれも加える）
        @ Mat3.scaling(zoom, zoom)  # 3. 拡大縮小
        @ Mat3.rotation(-angle)  # 2. カメラの回転と逆向きに回す
        @ Mat3.translation(-camera.x, -camera.y)  # 1. カメラの位置が原点に来るように動かす
    )


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('2D camera with a view matrix')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    rng = random.Random(1)
    boxes = [(rng.uniform(0, WORLD_SIZE), rng.uniform(0, WORLD_SIZE), rng.uniform(30, 90)) for _ in range(60)]
    player = pygame.Vector2(WORLD_SIZE / 2, WORLD_SIZE / 2)
    markers: list[tuple[float, float]] = []
    zoom = 1.0
    angle = 0.0
    trauma = 0.0  # 揺れの強さ（0～1）

    running = True
    while running:
        view = view_matrix(player, zoom, angle, pygame.Vector2())
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                trauma = 1.0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                markers.append(view.inverse().apply(*event.pos))  # 画面座標 → ワールド座標
        dt = min(clock.tick(60) / 1000, 0.1)

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])
        if move.length_squared() > 0:
            # 画面上の上下左右に動くように、入力の向きをカメラの角度だけ回す
            player += move.normalize().rotate_rad(angle) * PLAYER_SPEED * dt
        zoom *= ZOOM_SPEED ** ((keys[pygame.K_x] - keys[pygame.K_z]) * dt)
        zoom = max(0.25, min(4.0, zoom))
        angle += (keys[pygame.K_v] - keys[pygame.K_c]) * TURN_SPEED * dt
        trauma = max(0.0, trauma - SHAKE_DECAY * dt)
        shake = pygame.Vector2(rng.uniform(-1, 1), rng.uniform(-1, 1)) * MAX_SHAKE_OFFSET * trauma ** 2

        view = view_matrix(player, zoom, angle, shake)
        screen.fill((20, 24, 36))
        for i in range(0, WORLD_SIZE + 1, GRID_STEP):
            pygame.draw.line(screen, (45, 52, 70), view.apply(i, 0), view.apply(i, WORLD_SIZE))
            pygame.draw.line(screen, (45, 52, 70), view.apply(0, i), view.apply(WORLD_SIZE, i))
        for x, y, size in boxes:
            corners = [view.apply(x + dx, y + dy) for dx, dy in ((0, 0), (size, 0), (size, size), (0, size))]
            pygame.draw.polygon(screen, (90, 120, 170), corners)
        for mx, my in markers:
            pygame.draw.circle(screen, (255, 120, 120), view.apply(mx, my), 6 * zoom)
        pygame.draw.circle(screen, (240, 240, 240), view.apply(player.x, player.y), 12 * zoom)

        mouse_world = view.inverse().apply(*pygame.mouse.get_pos())
        lines = [
            f'camera: ({player.x:.0f}, {player.y:.0f})  zoom: {zoom:.2f}  angle: {math.degrees(angle):.0f} deg',
            f'mouse in world: ({mouse_world[0]:.0f}, {mouse_world[1]:.0f})',
        ]
        for i, text in enumerate(lines):
            screen.blit(font.render(text, True, (230, 230, 230)), (10, 10 + 22 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
