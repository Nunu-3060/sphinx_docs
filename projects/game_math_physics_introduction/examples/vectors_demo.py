"""第 4 章: ベクトルの長さ・正規化・内積・外積をゲームの場面で使う。

* プレイヤー（白）を WASD キーで動かす。N キーで入力ベクトルの正規化を切り替え、斜め移動の速さを比べる。
* 見張り（中央）はゆっくり向きを変える。内積でプレイヤーが視界に入ったかを、外積で左右どちらにいるかを判定する。
* 追跡者（赤）は、プレイヤーへ向かう単位ベクトルに速さを掛けて追いかける。

操作方法:
    W / A / S / D キー: プレイヤーを動かす
    N キー: 入力ベクトルの正規化の有無を切り替える
    Esc キー: 終了する
"""

import math

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PLAYER_SPEED = 200.0  # ピクセル毎秒
CHASER_SPEED = 90.0  # ピクセル毎秒
GUARD_TURN_SPEED = math.radians(30)  # 見張りが向きを変える速さ（ラジアン毎秒）
VIEW_DISTANCE = 220.0  # 見張りの視界の距離（ピクセル）
VIEW_HALF_ANGLE = math.radians(35)  # 見張りの視界の半分の角度
COS_VIEW_HALF_ANGLE = math.cos(VIEW_HALF_ANGLE)


def read_input(keys: pygame.key.ScancodeWrapper) -> pygame.Vector2:
    """WASD キーの状態から入力ベクトルを作る。各成分は -1、0、1 のいずれか。"""
    x = keys[pygame.K_d] - keys[pygame.K_a]
    y = keys[pygame.K_s] - keys[pygame.K_w]
    return pygame.Vector2(x, y)


def is_in_view(eye: pygame.Vector2, facing: pygame.Vector2, target: pygame.Vector2) -> bool:
    """target が、eye から facing（単位ベクトル）の向きに広がる扇形の視界に入っているか。"""
    to_target = target - eye
    distance = to_target.length()
    if distance > VIEW_DISTANCE:
        return False
    if distance < 1e-9:  # 同じ位置にいる
        return True
    return facing.dot(to_target / distance) >= COS_VIEW_HALF_ANGLE


def side_of(facing: pygame.Vector2, to_target: pygame.Vector2) -> str:
    """facing の向きから見て、to_target が左右どちらにあるか。画面座標（y 軸が下向き）での判定。"""
    c = facing.cross(to_target)
    if c > 0:
        return 'right'
    if c < 0:
        return 'left'
    return 'straight'


def move_toward(position: pygame.Vector2, target: pygame.Vector2, max_distance: float) -> pygame.Vector2:
    """position から target へ、最大 max_distance だけ近づいた位置を返す。行き過ぎない。"""
    offset = target - position
    distance = offset.length()
    if distance <= max_distance:
        return pygame.Vector2(target)
    return position + offset / distance * max_distance


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Vectors: normalize, dot, cross')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()

    player = pygame.Vector2(120, 360)
    chaser = pygame.Vector2(560, 400)
    guard = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40)
    guard_angle = 0.0
    normalize_input = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_n:
                    normalize_input = not normalize_input
        dt = min(clock.tick(60) / 1000, 0.1)

        direction = read_input(pygame.key.get_pressed())
        if normalize_input and direction.length_squared() > 0:
            direction = direction.normalize()
        velocity = direction * PLAYER_SPEED
        player += velocity * dt
        player.x = max(0, min(SCREEN_WIDTH, player.x))
        player.y = max(0, min(SCREEN_HEIGHT, player.y))

        chaser = move_toward(chaser, player, CHASER_SPEED * dt)
        guard_angle += GUARD_TURN_SPEED * dt
        facing = pygame.Vector2(math.cos(guard_angle), math.sin(guard_angle))
        seen = is_in_view(guard, facing, player)

        screen.fill((20, 24, 36))
        # 見張りの視界（扇形を多角形で近似して描く）
        points = [guard]
        for i in range(17):
            a = guard_angle - VIEW_HALF_ANGLE + 2 * VIEW_HALF_ANGLE * i / 16
            points.append(guard + pygame.Vector2(math.cos(a), math.sin(a)) * VIEW_DISTANCE)
        pygame.draw.polygon(screen, (120, 40, 40) if seen else (50, 60, 80), points)
        pygame.draw.circle(screen, (240, 200, 80), guard, 12)
        pygame.draw.line(screen, (240, 200, 80), guard, guard + facing * 30, 3)
        pygame.draw.circle(screen, (230, 80, 80), chaser, 10)
        pygame.draw.circle(screen, (240, 240, 240), player, 10)

        lines = [
            f'normalize input: {normalize_input} (N)   speed: {velocity.length():.0f} px/s',
            f'guard sees player: {seen}   player is on the guard\'s {side_of(facing, player - guard)}',
        ]
        for i, text in enumerate(lines):
            screen.blit(font.render(text, True, (230, 230, 230)), (10, 10 + 22 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
