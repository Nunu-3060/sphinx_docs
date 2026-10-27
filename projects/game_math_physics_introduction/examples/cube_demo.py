"""第 7 章: クォータニオンで立方体を回し、透視投影で画面に描く。

立方体の向きを 1 つのクォータニオンで持ち、キー入力に応じて小さな回転を掛け合わせる。
R キーを押すと、球面線形補間で最初の向きに 1 秒かけて戻る。

quaternion.py と同じフォルダーに置いて実行する。

操作方法:
    上下キー: x 軸の周りに回す
    左右キー: y 軸の周りに回す
    Q / E キー: z 軸の周りに回す
    R キー: 最初の向きに戻す
    Esc キー: 終了する
"""

import math

import pygame

from quaternion import X_AXIS, Y_AXIS, Z_AXIS, Quat, Vec3, slerp

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
TURN_SPEED = math.radians(90)  # ラジアン毎秒
CAMERA_DISTANCE = 5.0  # カメラから立方体の中心までの距離
FOCAL_LENGTH = 400.0  # 投影面までの距離（ピクセル）。大きいほど望遠になる
RESET_TIME = 1.0  # 最初の向きに戻るのにかかる時間（秒）

VERTICES: list[Vec3] = [(x, y, z) for x in (-1.0, 1.0) for y in (-1.0, 1.0) for z in (-1.0, 1.0)]
# 1 つの座標だけが異なる頂点どうしを辺で結ぶ
EDGES = [(i, j) for i in range(8) for j in range(i + 1, 8) if bin(i ^ j).count('1') == 1]
AXES = ((X_AXIS, (255, 90, 90)), (Y_AXIS, (90, 230, 120)), (Z_AXIS, (100, 150, 255)))


def project(p: Vec3) -> tuple[float, float]:
    """3D の点を透視投影で画面座標に変換する。カメラは z 軸の負の側から +z の向きを見ている。"""
    x, y, z = p
    depth = z + CAMERA_DISTANCE
    # 遠いほど（depth が大きいほど）中央に寄る。3D の y 軸は上向き、画面の y 軸は下向きなので符号を反転する
    return SCREEN_WIDTH / 2 + FOCAL_LENGTH * x / depth, SCREEN_HEIGHT / 2 - FOCAL_LENGTH * y / depth


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Quaternion rotation and perspective projection')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    orientation = Quat.from_axis_angle((1.0, 1.0, 0.0), math.radians(30))
    reset_from: Quat | None = None  # 戻し始めたときの向き
    reset_t = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_from, reset_t = orientation, 0.0
        dt = min(clock.tick(60) / 1000, 0.1)

        if reset_from is not None:
            reset_t = min(1.0, reset_t + dt / RESET_TIME)
            orientation = slerp(reset_from, Quat(), reset_t)
            if reset_t >= 1.0:
                reset_from = None
        else:
            keys = pygame.key.get_pressed()
            inputs = ((X_AXIS, keys[pygame.K_DOWN] - keys[pygame.K_UP]),
                      (Y_AXIS, keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]),
                      (Z_AXIS, keys[pygame.K_q] - keys[pygame.K_e]))
            for axis, amount in inputs:
                if amount:
                    # ワールドの軸の周りの小さな回転を、今の向きの左から掛ける
                    orientation = Quat.from_axis_angle(axis, amount * TURN_SPEED * dt) * orientation
            orientation = orientation.normalized()

        screen.fill((20, 24, 36))
        points = [project(orientation.rotate(v)) for v in VERTICES]
        for i, j in EDGES:
            pygame.draw.line(screen, (220, 220, 230), points[i], points[j], 2)
        center = project((0.0, 0.0, 0.0))
        for axis, color in AXES:
            tip = project(orientation.rotate((axis[0] * 1.6, axis[1] * 1.6, axis[2] * 1.6)))
            pygame.draw.line(screen, color, center, tip, 3)
        q = orientation
        text = f'q = ({q.w:.3f}, {q.x:.3f}, {q.y:.3f}, {q.z:.3f})   R: reset with slerp'
        screen.blit(font.render(text, True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
