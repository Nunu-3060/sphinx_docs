"""第 6 章: 親子関係のある変換で、3 つの関節を持つロボットアームを動かす。

各部品は、自分の根元を原点・自分の向きを x 軸とするローカル座標で形を定義する。
親のワールド変換に自分のローカル変換を掛けると、自分のワールド変換になる。
親（根元に近い関節）を回すと、子（先端側）も一緒に動く。

transform2d.py と同じフォルダーに置いて実行する。

操作方法:
    Q / A キー: 第 1 関節を回す
    W / S キー: 第 2 関節を回す
    E / D キー: 第 3 関節を回す
    Esc キー: 終了する
"""

import math

import pygame

from transform2d import Mat3

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TURN_SPEED = math.radians(90)  # 関節を回す速さ（ラジアン毎秒）
SEGMENT_LENGTHS = (130.0, 100.0, 70.0)
SEGMENT_WIDTH = 16.0
JOINT_KEYS = ((pygame.K_q, pygame.K_a), (pygame.K_w, pygame.K_s), (pygame.K_e, pygame.K_d))
COLORS = ((120, 170, 255), (120, 220, 170), (240, 200, 90))


def segment_world_transforms(base: Mat3, angles: list[float]) -> list[Mat3]:
    """各部品のワールド変換を、根元から順に求める。"""
    transforms = []
    parent = base
    parent_length = 0.0
    for angle, length in zip(angles, SEGMENT_LENGTHS):
        # 親の先端へ移動してから、自分の関節の角度だけ回す
        local = Mat3.translation(parent_length, 0) @ Mat3.rotation(angle)
        world = parent @ local
        transforms.append(world)
        parent, parent_length = world, length
    return transforms


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Parent-child transforms: robot arm')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    base = Mat3.translation(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40) @ Mat3.rotation(-math.pi / 2)
    angles = [0.0, math.radians(30), math.radians(30)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        dt = min(clock.tick(60) / 1000, 0.1)
        keys = pygame.key.get_pressed()
        for i, (plus, minus) in enumerate(JOINT_KEYS):
            angles[i] += (keys[plus] - keys[minus]) * TURN_SPEED * dt

        screen.fill((20, 24, 36))
        transforms = segment_world_transforms(base, angles)
        for world, length, color in zip(transforms, SEGMENT_LENGTHS, COLORS):
            # ローカル座標で定義した長方形の 4 つの角を、ワールド座標に変換して描く
            half = SEGMENT_WIDTH / 2
            corners = [world.apply(x, y) for x, y in ((0, -half), (length, -half), (length, half), (0, half))]
            pygame.draw.polygon(screen, color, corners)
            pygame.draw.circle(screen, (240, 240, 240), world.apply(0, 0), 6)
        tip = transforms[-1].apply(SEGMENT_LENGTHS[-1], 0)
        pygame.draw.circle(screen, (255, 100, 100), tip, 6)
        text = 'angles: ' + ', '.join(f'{math.degrees(a):.0f}' for a in angles) + f'  tip: ({tip[0]:.0f}, {tip[1]:.0f})'
        screen.blit(font.render(text, True, (230, 230, 230)), (10, 10))
        screen.blit(font.render('Q/A, W/S, E/D: rotate the joints', True, (230, 230, 230)), (10, 32))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
