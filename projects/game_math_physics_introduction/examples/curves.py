"""第 8 章: ベジェ曲線、Catmull-Rom スプライン、弧長による等速移動。

6 つの通過点を通る閉じた Catmull-Rom スプラインに沿って、2 つの点を動かす。
橙の点はパラメーター u を一定の速さで増やすので、通過点の間隔によって速さが変わる。
水色の点は弧長の表を使って、曲線に沿った距離を一定の速さで増やす。

操作方法:
    Esc キー: 終了する
"""

import bisect
from collections.abc import Callable

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WAYPOINTS = [(100, 100), (250, 80), (560, 120), (520, 400), (300, 300), (120, 380)]
SPEED = 200.0  # 水色の点の速さ（ピクセル毎秒）
TABLE_SAMPLES = 600  # 弧長の表を作るときの分割数


def lerp_point(a: pygame.Vector2, b: pygame.Vector2, t: float) -> pygame.Vector2:
    return a + (b - a) * t


def quadratic_bezier(p0: pygame.Vector2, p1: pygame.Vector2, p2: pygame.Vector2, t: float) -> pygame.Vector2:
    """2 次ベジェ曲線。線形補間を 2 段重ねる（ド・カステリョのアルゴリズム）。"""
    return lerp_point(lerp_point(p0, p1, t), lerp_point(p1, p2, t), t)


def cubic_bezier(p0: pygame.Vector2, p1: pygame.Vector2, p2: pygame.Vector2, p3: pygame.Vector2,
                 t: float) -> pygame.Vector2:
    """3 次ベジェ曲線。線形補間を 3 段重ねる。"""
    a, b, c = lerp_point(p0, p1, t), lerp_point(p1, p2, t), lerp_point(p2, p3, t)
    return lerp_point(lerp_point(a, b, t), lerp_point(b, c, t), t)


def catmull_rom(p0: pygame.Vector2, p1: pygame.Vector2, p2: pygame.Vector2, p3: pygame.Vector2,
                t: float) -> pygame.Vector2:
    """p1 から p2 までの区間の Catmull-Rom スプライン。p0 と p3 は区間の両端での向きを決めるのに使う。"""
    t2, t3 = t * t, t * t * t
    return 0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (3 * p1 - p0 - 3 * p2 + p3) * t3)


def closed_spline(points: list[pygame.Vector2]) -> Callable[[float], pygame.Vector2]:
    """すべての点を通る閉じた曲線の関数を返す。引数 u は 0～len(points) で、整数のときに通過点と一致する。"""
    n = len(points)

    def curve(u: float) -> pygame.Vector2:
        i = int(u) % n
        t = u - int(u)
        return catmull_rom(points[(i - 1) % n], points[i], points[(i + 1) % n], points[(i + 2) % n], t)

    return curve


class ArcLengthTable:
    """曲線を細かく区切って測った長さの表。曲線に沿った距離から、パラメーター u を逆引きする。"""

    def __init__(self, curve: Callable[[float], pygame.Vector2], u_max: float, samples: int) -> None:
        self.us = [u_max * i / samples for i in range(samples + 1)]
        self.lengths = [0.0]
        previous = curve(0.0)
        for u in self.us[1:]:
            point = curve(u)
            self.lengths.append(self.lengths[-1] + previous.distance_to(point))
            previous = point

    @property
    def total(self) -> float:
        """曲線全体の長さ。"""
        return self.lengths[-1]

    def u_at(self, distance: float) -> float:
        """始点から曲線に沿って distance だけ進んだ位置のパラメーター u。"""
        distance = max(0.0, min(self.total, distance))
        i = bisect.bisect_left(self.lengths, distance)
        if i == 0:
            return self.us[0]
        # 表の間は直線とみなして補間する
        d0, d1 = self.lengths[i - 1], self.lengths[i]
        ratio = (distance - d0) / (d1 - d0) if d1 > d0 else 0.0
        return self.us[i - 1] + (self.us[i] - self.us[i - 1]) * ratio


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Catmull-Rom spline and arc length')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    points = [pygame.Vector2(p) for p in WAYPOINTS]
    curve = closed_spline(points)
    n = len(points)
    table = ArcLengthTable(curve, n, TABLE_SAMPLES)
    u_speed = n * SPEED / table.total  # 1 周にかかる時間が水色の点と同じになる速さ
    u = 0.0
    distance = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        dt = min(clock.tick(60) / 1000, 0.1)
        u = (u + u_speed * dt) % n
        distance = (distance + SPEED * dt) % table.total

        screen.fill((20, 24, 36))
        outline = [curve(n * i / 300) for i in range(301)]
        pygame.draw.lines(screen, (90, 100, 130), False, outline, 2)
        for p in points:
            pygame.draw.circle(screen, (200, 200, 210), p, 5)
        pygame.draw.circle(screen, (255, 160, 80), curve(u), 10)
        pygame.draw.circle(screen, (90, 200, 255), curve(table.u_at(distance)), 10)
        screen.blit(font.render('orange: uniform u   blue: uniform arc length', True, (230, 230, 230)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
