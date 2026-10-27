"""第 9 章: バリューノイズとパーリンノイズ（1 次元）、フラクタルノイズ。

* 上半分: パーリンノイズのオクターブを重ねた地形が横に流れる。
* 下半分: 左の照準は毎フレーム一様乱数で、右の照準はノイズで揺らす。

操作方法:
    上下キー: オクターブの数を増減する
    Esc キー: 終了する
"""

import math
import random

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCROLL_SPEED = 2.0  # ノイズの入力座標を 1 秒あたりに進める量
SHAKE_AMPLITUDE = 12.0  # 照準の揺れの最大のずれ（ピクセル）
SHAKE_FREQUENCY = 8.0  # ノイズで揺らすときの 1 秒あたりの格子点の数
MASK64 = (1 << 64) - 1


def hash_to_unit(i: int, seed: int) -> float:
    """整数 i とシードから、-1 以上 1 未満の値を決定的に作る（同じ入力には常に同じ値を返す）。"""
    h = (i * 0x9E3779B97F4A7C15 + seed * 0xBF58476D1CE4E5B9) & MASK64
    h ^= h >> 31
    h = (h * 0x94D049BB133111EB) & MASK64
    h ^= h >> 29
    return (h & 0xFFFFFF) / 0x800000 - 1


def smoothstep(t: float) -> float:
    """0 と 1 で傾きが 0 になる補間の重み。"""
    return t * t * (3 - 2 * t)


def fade(t: float) -> float:
    """パーリンノイズで使う 5 次の補間の重み（6t^5 - 15t^4 + 10t^3）。"""
    return t * t * t * (t * (t * 6 - 15) + 10)


def value_noise(x: float, seed: int = 0) -> float:
    """バリューノイズ。整数の格子点に乱数の値を置き、その間を滑らかに補間する。"""
    i = math.floor(x)
    t = x - i
    a, b = hash_to_unit(i, seed), hash_to_unit(i + 1, seed)
    return a + (b - a) * smoothstep(t)


def perlin_noise(x: float, seed: int = 0) -> float:
    """1 次元のパーリンノイズ。格子点に乱数の傾き（勾配）を置き、その直線を補間する。格子点での値は 0。"""
    i = math.floor(x)
    t = x - i
    g0, g1 = hash_to_unit(i, seed), hash_to_unit(i + 1, seed)
    v0 = g0 * t  # 左の格子点の傾きで引いた直線の、x での高さ
    v1 = g1 * (t - 1)  # 右の格子点の傾きで引いた直線の、x での高さ
    return (v0 + (v1 - v0) * fade(t)) * 2  # おおよそ -1～1 に収まるよう 2 倍する


def fractal_noise(x: float, octaves: int, seed: int = 0) -> float:
    """周波数を 2 倍、振幅を半分にしたノイズを octaves 個重ねる。結果はおおよそ -1～1。"""
    total = 0.0
    amplitude = 1.0
    frequency = 1.0
    norm = 0.0
    for octave in range(octaves):
        total += perlin_noise(x * frequency, seed + octave) * amplitude
        norm += amplitude
        amplitude *= 0.5
        frequency *= 2.0
    return total / norm


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Value noise, Perlin noise and shake')
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    rng = random.Random(0)
    octaves = 4
    time = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                octaves = min(8, octaves + 1)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                octaves = max(1, octaves - 1)
        dt = min(clock.tick(60) / 1000, 0.1)
        time += dt

        screen.fill((20, 24, 36))
        # 地形: 画面の 1 ピクセルを、ノイズの入力座標の 1/100 に対応させる
        ground = [(0.0, 260.0)]
        for sx in range(0, SCREEN_WIDTH + 1, 4):
            h = fractal_noise(sx / 100 + time * SCROLL_SPEED, octaves)
            ground.append((sx, 150 - h * 90))
        ground.append((SCREEN_WIDTH, 260.0))
        pygame.draw.polygon(screen, (70, 130, 90), ground)
        screen.blit(font.render(f'octaves: {octaves} (up/down)', True, (230, 230, 230)), (10, 10))

        random_offset = pygame.Vector2(rng.uniform(-1, 1), rng.uniform(-1, 1)) * SHAKE_AMPLITUDE
        noise_offset = pygame.Vector2(perlin_noise(time * SHAKE_FREQUENCY, 100),
                                      perlin_noise(time * SHAKE_FREQUENCY, 200)) * SHAKE_AMPLITUDE
        for center, offset, label in (((180, 370), random_offset, 'random'), ((460, 370), noise_offset, 'noise')):
            p = pygame.Vector2(center) + offset
            pygame.draw.circle(screen, (240, 240, 240), p, 24, 2)
            pygame.draw.line(screen, (240, 240, 240), p - (30, 0), p + (30, 0))
            pygame.draw.line(screen, (240, 240, 240), p - (0, 30), p + (0, 30))
            screen.blit(font.render(label, True, (230, 230, 230)), (center[0] - 25, 430))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
