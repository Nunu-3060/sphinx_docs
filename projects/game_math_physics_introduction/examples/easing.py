"""第 8 章: 線形補間・イージング関数・フレームレートに依存しない追従。

* 上の 5 行: 同じ 1.2 秒の移動を、異なるイージング関数で行う。
* 下の 2 つ: マウスの x 座標を追いかける。橙は「毎フレーム残りの 10 % だけ近づく」方法、
  水色は指数関数的減衰（damp）を使う方法。フレームレートを変えると、橙だけ追いつく速さが変わる。

操作方法:
    1 / 2 / 3 キー: フレームレートの上限を 20 / 60 / 144 FPS にする
    Esc キー: 終了する
"""

import math
from collections.abc import Callable

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
MOVE_TIME = 1.2  # 1 回の移動にかける時間（秒）
PAUSE_TIME = 0.5  # 端で止まる時間（秒）
FOLLOW_RATE = 6.0  # damp の追従の速さ（1 秒あたり）
FPS_KEYS = {pygame.K_1: 20, pygame.K_2: 60, pygame.K_3: 144}


def clamp(x: float, lo: float, hi: float) -> float:
    """x を lo 以上 hi 以下に収める。"""
    return max(lo, min(hi, x))


def lerp(a: float, b: float, t: float) -> float:
    """線形補間。t = 0 で a、t = 1 で b になる。"""
    return a + (b - a) * t


def inverse_lerp(a: float, b: float, value: float) -> float:
    """lerp の逆。value が a から b までのどの割合の位置にあるかを返す。"""
    return (value - a) / (b - a)


def remap(value: float, in_a: float, in_b: float, out_a: float, out_b: float) -> float:
    """範囲 [in_a, in_b] の値を、範囲 [out_a, out_b] の対応する値に変換する。"""
    return lerp(out_a, out_b, inverse_lerp(in_a, in_b, value))


def ease_in_quad(t: float) -> float:
    """ゆっくり動き出して加速する。"""
    return t * t


def ease_out_quad(t: float) -> float:
    """速く動き出して減速しながら止まる。"""
    return 1 - (1 - t) * (1 - t)


def ease_in_out_cubic(t: float) -> float:
    """ゆっくり動き出し、途中で速くなり、ゆっくり止まる。"""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def ease_out_back(t: float) -> float:
    """目標を少し行き過ぎてから戻る。"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


EASINGS: dict[str, Callable[[float], float]] = {
    'linear': lambda t: t,
    'ease_in_quad': ease_in_quad,
    'ease_out_quad': ease_out_quad,
    'ease_in_out_cubic': ease_in_out_cubic,
    'ease_out_back': ease_out_back,
}


def damp(current: float, target: float, rate: float, dt: float) -> float:
    """current を target へ指数関数的に近づける。dt の分け方によらず、同じ時間で同じ位置に着く。"""
    return lerp(current, target, 1 - math.exp(-rate * dt))


def ping_pong_progress(time: float) -> float:
    """移動 → 停止 → 戻る → 停止 を繰り返すときの、進み具合 t（0～1）を返す。"""
    cycle = 2 * (MOVE_TIME + PAUSE_TIME)
    s = time % cycle
    if s < MOVE_TIME:
        return s / MOVE_TIME
    if s < MOVE_TIME + PAUSE_TIME:
        return 1.0
    if s < 2 * MOVE_TIME + PAUSE_TIME:
        return 1 - (s - MOVE_TIME - PAUSE_TIME) / MOVE_TIME
    return 0.0


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Easing functions and damp')
    font = pygame.font.Font(None, 22)
    clock = pygame.time.Clock()
    fps_limit = 60
    time = 0.0
    naive_x = damp_x = SCREEN_WIDTH / 2
    left, right = 180.0, SCREEN_WIDTH - 40.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key in FPS_KEYS:
                fps_limit = FPS_KEYS[event.key]
        dt = min(clock.tick(fps_limit) / 1000, 0.1)
        time += dt
        target_x = float(pygame.mouse.get_pos()[0])
        naive_x = lerp(naive_x, target_x, 0.1)  # フレームレートに依存する
        damp_x = damp(damp_x, target_x, FOLLOW_RATE, dt)

        screen.fill((20, 24, 36))
        t = ping_pong_progress(time)
        for i, (name, ease) in enumerate(EASINGS.items()):
            y = 40 + 48 * i
            screen.blit(font.render(name, True, (200, 200, 210)), (10, y - 6))
            pygame.draw.line(screen, (60, 70, 90), (left, y), (right, y))
            pygame.draw.circle(screen, (240, 200, 90), (lerp(left, right, ease(t)), y), 10)

        pygame.draw.line(screen, (240, 240, 240), (target_x, 300), (target_x, 440))
        pygame.draw.rect(screen, (255, 160, 80), (naive_x - 12, 320, 24, 24))
        pygame.draw.rect(screen, (90, 200, 255), (damp_x - 12, 390, 24, 24))
        screen.blit(font.render('lerp 10% per frame', True, (255, 160, 80)), (10, 325))
        screen.blit(font.render('damp (exp)', True, (90, 200, 255)), (10, 395))
        screen.blit(font.render(f'FPS limit: {fps_limit} (keys 1/2/3)', True, (230, 230, 230)), (10, 455))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
