"""第 2 章: 座標の変換と浮動小数点数の性質を確かめる。

画面は使わず、結果をコンソールに表示する。

実行方法:
    py float_precision.py
"""

import math

PIXELS_PER_METER = 32.0  # 1 メートルを何ピクセルで描くか
SCREEN_HEIGHT = 480  # 画面の高さ（ピクセル）


def world_to_screen(x: float, y: float) -> tuple[float, float]:
    """y 軸が上向き・単位がメートルのワールド座標を、y 軸が下向き・単位がピクセルの画面座標に変換する。"""
    return x * PIXELS_PER_METER, SCREEN_HEIGHT - y * PIXELS_PER_METER


def screen_to_world(sx: float, sy: float) -> tuple[float, float]:
    """world_to_screen の逆変換。"""
    return sx / PIXELS_PER_METER, (SCREEN_HEIGHT - sy) / PIXELS_PER_METER


def nearly_equal(a: float, b: float, tolerance: float = 1e-9) -> bool:
    """誤差を許して 2 つの小数が等しいかを判定する。"""
    return abs(a - b) <= tolerance


def main() -> None:
    print('--- 座標の変換 ---')
    print('ワールド (2.0, 1.5) m -> 画面', world_to_screen(2.0, 1.5))
    print('画面 (64, 432) px -> ワールド', screen_to_world(64, 432))

    print('--- 小数の誤差 ---')
    print('0.1 + 0.2 =', 0.1 + 0.2)
    print('0.1 + 0.2 == 0.3 :', 0.1 + 0.2 == 0.3)
    print('nearly_equal(0.1 + 0.2, 0.3) :', nearly_equal(0.1 + 0.2, 0.3))
    print('math.isclose(0.1 + 0.2, 0.3) :', math.isclose(0.1 + 0.2, 0.3))

    print('--- 誤差の蓄積（1/60 秒を 60 万回足す。正しくは 10000 秒） ---')
    total = 0.0
    for _ in range(600_000):
        total += 1 / 60
    print('合計 =', total)

    print('--- 値の大きさと精度（隣の表せる数との差） ---')
    for value in (1.0, 1_000.0, 1_000_000.0, 1e12):
        print(f'{value:>16,.0f} の隣との差: 64 ビット {math.ulp(value):.3e}')
    for value in (1.0, 1_000.0, 100_000.0, 1_000_000.0):
        print(f'{value:>16,.0f} の隣との差: 32 ビット {float32_spacing(value):.3e}')


def float32_spacing(value: float) -> float:
    """32 ビット浮動小数点数（ゲームエンジンでよく使われる）で、value の隣の表せる数との差を返す。"""
    _, exponent = math.frexp(value)
    return math.ldexp(1.0, exponent - 24)


if __name__ == '__main__':
    main()
