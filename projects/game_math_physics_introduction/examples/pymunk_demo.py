"""第 14 章: 2D 物理エンジン pymunk の基本。

空間（Space）に、ボディー（質量と慣性モーメントを持つ剛体）と形状（衝突判定に使う形）を登録し、
space.step で時間を進めると、衝突・回転・摩擦・ジョイントの計算をエンジンが行う。
描画は pygame で行い、ボディーの位置と角度から形状の頂点をワールド座標に変換して描く。

操作方法:
    左クリック: 左下からクリックした位置に向けてボールを撃つ
    R キー: 最初からやり直す
    Esc キー: 終了する
"""

import pygame
import pymunk

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRAVITY = (0.0, 900.0)  # 画面座標に合わせて下向きを正にする
STEP = 1 / 120  # 物理の 1 ステップの時間（秒）。1 フレームに 2 回進める
SUBSTEPS = 2
BOX_SIZE = 32.0
SHOT_SPEED = 900.0  # 撃ち出すボールの速さ（ピクセル毎秒）
LAUNCH_POINT = (40.0, SCREEN_HEIGHT - 60.0)


def add_box(space: pymunk.Space, x: float, y: float, mass: float = 1.0) -> None:
    """正方形の箱を追加する。慣性モーメントは形と質量から求める。"""
    body = pymunk.Body(mass, pymunk.moment_for_box(mass, (BOX_SIZE, BOX_SIZE)))
    body.position = (x, y)
    shape = pymunk.Poly.create_box(body, (BOX_SIZE, BOX_SIZE))
    shape.friction = 0.7
    shape.elasticity = 0.1  # 反発係数
    space.add(body, shape)


def add_ball(space: pymunk.Space, position: tuple[float, float], radius: float, mass: float) -> pymunk.Body:
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = position
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.5
    shape.elasticity = 0.4
    space.add(body, shape)
    return body


def build_world() -> pymunk.Space:
    space = pymunk.Space()
    space.gravity = GRAVITY
    # 地面と右の壁: 動かない物は space.static_body に付ける
    for a, b in (((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, SCREEN_HEIGHT - 20)),
                 ((SCREEN_WIDTH - 10, 0), (SCREEN_WIDTH - 10, SCREEN_HEIGHT))):
        segment = pymunk.Segment(space.static_body, a, b, 4)
        segment.friction = 0.8
        space.add(segment)
    # 箱のピラミッド
    ground = SCREEN_HEIGHT - 24
    for row in range(6):
        for col in range(6 - row):
            x = 380 + col * BOX_SIZE + row * BOX_SIZE / 2
            y = ground - BOX_SIZE / 2 - row * BOX_SIZE
            add_box(space, x, y)
    # 振り子: 空中の点とボールの中心を、距離を一定に保つピンジョイントでつなぐ
    pivot = (200.0, 40.0)
    bob = add_ball(space, (320.0, 40.0), 20, 5.0)
    space.add(pymunk.PinJoint(space.static_body, bob, pivot, (0, 0)))
    return space


def draw_space(screen: pygame.Surface, space: pymunk.Space) -> None:
    for shape in space.shapes:
        body = shape.body
        if body is None:
            continue  # ボディーに付いていない形状（本書では作らない）
        if isinstance(shape, pymunk.Poly):
            # 形状の頂点はボディーのローカル座標で定義されている
            points = [body.local_to_world(v) for v in shape.get_vertices()]
            pygame.draw.polygon(screen, (230, 190, 110), points)
            pygame.draw.polygon(screen, (120, 90, 40), points, 1)
        elif isinstance(shape, pymunk.Circle):
            center = body.position
            pygame.draw.circle(screen, (120, 180, 255), center, shape.radius)
            # 回転が見えるよう、ボディーの角度の向きに線を引く
            edge = center + pymunk.Vec2d(shape.radius, 0).rotated(body.angle)
            pygame.draw.line(screen, (20, 24, 36), center, edge, 2)
        elif isinstance(shape, pymunk.Segment):
            pygame.draw.line(screen, (150, 160, 180), shape.a, shape.b, round(shape.radius * 2))
    for constraint in space.constraints:
        if isinstance(constraint, pymunk.PinJoint):
            a = constraint.a.local_to_world(constraint.anchor_a)
            b = constraint.b.local_to_world(constraint.anchor_b)
            pygame.draw.line(screen, (200, 200, 210), a, b, 1)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('pymunk: boxes, balls and a pendulum')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    space = build_world()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                space = build_world()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ball = add_ball(space, LAUNCH_POINT, 12, 3.0)
                direction = pymunk.Vec2d(*event.pos) - ball.position
                if direction.length > 0:
                    ball.velocity = direction.normalized() * SHOT_SPEED
        clock.tick(60)
        for _ in range(SUBSTEPS):
            space.step(STEP)

        screen.fill((20, 24, 36))
        draw_space(screen, space)
        pygame.draw.circle(screen, (240, 240, 240), LAUNCH_POINT, 6, 1)
        moving = sum(1 for b in space.bodies if b.velocity.length > 5)
        text = f'bodies: {len(space.bodies)}  moving: {moving}  (click: shoot, R: reset)'
        screen.blit(font.render(text, True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
