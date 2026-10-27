"""第 5 章: 三角関数と atan2 を使って、マウスの方向を向く砲台を作る。

* 砲身は atan2 で求めた角度だけ回転させて描く。
* 砲台の周りを、cos と sin で求めた位置で衛星が回る。
* クリックすると、砲身の向きに弾を撃つ。

操作方法:
    マウス: 狙う
    左クリック: 弾を撃つ
    Esc キー: 終了する
"""

import math

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
ORBIT_RADIUS = 70.0  # 衛星の軌道の半径（ピクセル）
ORBIT_SPEED = math.radians(90)  # 衛星の角速度（ラジアン毎秒）
BULLET_SPEED = 400.0  # ピクセル毎秒
# 砲身の形（砲台の中心を原点とし、右向きを 0 度とした座標）
BARREL_SHAPE = [(0.0, -6.0), (40.0, -6.0), (40.0, 6.0), (0.0, 6.0)]


def angle_to(origin: pygame.Vector2, target: pygame.Vector2) -> float:
    """origin から target を見た向きの角度（ラジアン）。x 軸の正の向きが 0 で、画面上では時計回りに増える。"""
    return math.atan2(target.y - origin.y, target.x - origin.x)


def from_polar(radius: float, angle: float) -> pygame.Vector2:
    """極座標（半径と角度）を直交座標のベクトルに変換する。"""
    return pygame.Vector2(radius * math.cos(angle), radius * math.sin(angle))


def rotate_point(x: float, y: float, angle: float) -> tuple[float, float]:
    """点 (x, y) を原点の周りに angle ラジアン回転させる。"""
    c, s = math.cos(angle), math.sin(angle)
    return x * c - y * s, x * s + y * c


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Turret: atan2, sin and cos')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    center = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    orbit_angle = 0.0
    bullets: list[tuple[pygame.Vector2, pygame.Vector2]] = []  # (位置, 速度)

    running = True
    while running:
        aim = angle_to(center, pygame.Vector2(pygame.mouse.get_pos()))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                muzzle = center + from_polar(40, aim)
                bullets.append((muzzle, from_polar(BULLET_SPEED, aim)))
        dt = min(clock.tick(60) / 1000, 0.1)

        orbit_angle += ORBIT_SPEED * dt
        satellite = center + from_polar(ORBIT_RADIUS, orbit_angle)
        bullets = [(p + v * dt, v) for p, v in bullets if screen.get_rect().collidepoint(p)]

        screen.fill((20, 24, 36))
        barrel = []
        for x, y in BARREL_SHAPE:
            rx, ry = rotate_point(x, y, aim)
            barrel.append((center.x + rx, center.y + ry))
        pygame.draw.polygon(screen, (160, 200, 160), barrel)
        pygame.draw.circle(screen, (90, 140, 90), center, 20)
        pygame.draw.circle(screen, (60, 70, 90), center, ORBIT_RADIUS, 1)
        pygame.draw.circle(screen, (240, 200, 80), satellite, 8)
        for p, _ in bullets:
            pygame.draw.circle(screen, (255, 255, 255), p, 4)
        text = f'aim: {math.degrees(aim):6.1f} deg  (atan2)'
        screen.blit(font.render(text, True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
