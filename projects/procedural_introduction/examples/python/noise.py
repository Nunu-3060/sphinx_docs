"""ノイズ関数（NumPy でベクトル化した実装）。

どの関数も、座標の配列を受け取って同じ形の配列を返す。値はおおむね -1〜1 の範囲に
なる（worley2 は距離を返す）。格子点の乱数には prng のハッシュ関数を使うので、
順列表を持たず、シードを変えるだけで別のノイズになる。

period を与えると、格子が period ごとに繰り返し、ノイズが周期 period で
継ぎ目なくつながる（シームレスなテクスチャに使う）。
"""

from __future__ import annotations

import math
from typing import Protocol

import numpy as np

from common import FloatArray, IntArray
from prng import random2, random3, hash3


class Noise2(Protocol):
    """2 次元ノイズ関数の型。"""

    def __call__(self, x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray: ...


def fade(t: FloatArray) -> FloatArray:
    """5 次の補間曲線 6t^5 - 15t^4 + 10t^3（両端で 1 階・2 階微分が 0 になる）。"""
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def lerp(a: FloatArray, b: FloatArray, t: FloatArray) -> FloatArray:
    """線形補間。"""
    return a + (b - a) * t


def _split(x: FloatArray) -> tuple[IntArray, FloatArray]:
    """座標を、格子の番号（整数部）とセル内の位置（小数部）に分ける。"""
    floor = np.floor(x)
    return floor.astype(np.int64), x - floor


def _wrap(i: IntArray, period: int | None) -> IntArray:
    """period が与えられていれば、格子の番号を period で割った余りにする。"""
    return i if period is None else np.mod(i, period)


def value2(x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray:
    """バリューノイズ。格子点に乱数の値を置き、その間を滑らかに補間する。"""
    ix, fx = _split(x)
    iy, fy = _split(y)

    def corner(dx: int, dy: int) -> FloatArray:
        return random2(_wrap(ix + dx, period), _wrap(iy + dy, period), seed)

    u = fade(fx)
    v = fade(fy)
    bottom = lerp(corner(0, 0), corner(1, 0), u)
    top = lerp(corner(0, 1), corner(1, 1), u)
    return lerp(bottom, top, v) * 2.0 - 1.0


def _gradient_dot(ix: IntArray, iy: IntArray, dx: FloatArray, dy: FloatArray, seed: int) -> FloatArray:
    """格子点 (ix, iy) の単位勾配ベクトルと、格子点からの変位 (dx, dy) の内積。"""
    angle = random2(ix, iy, seed) * (2.0 * math.pi)
    return np.cos(angle) * dx + np.sin(angle) * dy


def perlin2(x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray:
    """パーリンノイズ（勾配ノイズ）。格子点に勾配を置き、勾配と変位の内積を補間する。"""
    ix, fx = _split(x)
    iy, fy = _split(y)

    def corner(dx: int, dy: int) -> FloatArray:
        return _gradient_dot(_wrap(ix + dx, period), _wrap(iy + dy, period), fx - dx, fy - dy, seed)

    u = fade(fx)
    v = fade(fy)
    bottom = lerp(corner(0, 0), corner(1, 0), u)
    top = lerp(corner(0, 1), corner(1, 1), u)
    # 単位勾配の 2 次元パーリンノイズの値は ±1/√2 に収まるので、√2 倍して ±1 にそろえる。
    return lerp(bottom, top, v) * math.sqrt(2.0)


_SKEW = 0.5 * (math.sqrt(3.0) - 1.0)
_UNSKEW = (3.0 - math.sqrt(3.0)) / 6.0
# 単位勾配を使ったときに、値がおよそ ±1 に収まるようにする係数（実測による）。
_SIMPLEX_SCALE = 99.0


def simplex2(x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray:
    """シンプレックスノイズ。平面を正三角形に近い三角形に分け、3 頂点の寄与を足す。

    三角形の格子は正方形の周期と合わないので、period には対応しない。
    """
    if period is not None:
        raise ValueError("simplex2 は period に対応していない")
    # 斜めに引き伸ばした座標で、点が含まれる単位正方形と、その中の三角形を決める。
    s = (x + y) * _SKEW
    i = np.floor(x + s).astype(np.int64)
    j = np.floor(y + s).astype(np.int64)
    t = (i + j) * _UNSKEW
    x0 = x - (i - t)
    y0 = y - (j - t)
    i1 = (x0 > y0).astype(np.int64)
    j1 = 1 - i1
    x1 = x0 - i1 + _UNSKEW
    y1 = y0 - j1 + _UNSKEW
    x2 = x0 - 1.0 + 2.0 * _UNSKEW
    y2 = y0 - 1.0 + 2.0 * _UNSKEW

    def contribution(dx: FloatArray, dy: FloatArray, ci: IntArray, cj: IntArray) -> FloatArray:
        # 頂点からの距離が一定以上なら寄与は 0 になる（影響範囲が円で区切られる）。
        falloff = np.maximum(0.5 - dx * dx - dy * dy, 0.0)
        return falloff ** 4 * _gradient_dot(ci, cj, dx, dy, seed)

    total = contribution(x0, y0, i, j) + contribution(x1, y1, i + i1, j + j1) + contribution(x2, y2, i + 1, j + 1)
    return total * _SIMPLEX_SCALE


# 3 次元パーリンノイズの勾配に使う、立方体の辺の中点を向く 12 本のベクトル。
_GRADIENTS3 = np.array(
    [[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0],
     [1, 0, 1], [-1, 0, 1], [1, 0, -1], [-1, 0, -1],
     [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1]],
    dtype=np.float64,
)


def perlin3(x: FloatArray, y: FloatArray, z: FloatArray, seed: int = 0) -> FloatArray:
    """3 次元パーリンノイズ。z を時刻とみなすと、2 次元の模様を滑らかに変化させられる。"""
    ix, fx = _split(x)
    iy, fy = _split(y)
    iz, fz = _split(z)

    def corner(dx: int, dy: int, dz: int) -> FloatArray:
        g = _GRADIENTS3[hash3(ix + dx, iy + dy, iz + dz, seed) % 12]
        return g[..., 0] * (fx - dx) + g[..., 1] * (fy - dy) + g[..., 2] * (fz - dz)

    u = fade(fx)
    v = fade(fy)
    w = fade(fz)
    near = lerp(lerp(corner(0, 0, 0), corner(1, 0, 0), u), lerp(corner(0, 1, 0), corner(1, 1, 0), u), v)
    far = lerp(lerp(corner(0, 0, 1), corner(1, 0, 1), u), lerp(corner(0, 1, 1), corner(1, 1, 1), u), v)
    return lerp(near, far, w)


def value3(x: FloatArray, y: FloatArray, z: FloatArray, seed: int = 0) -> FloatArray:
    """3 次元バリューノイズ（雲などの密度場に使う）。"""
    ix, fx = _split(x)
    iy, fy = _split(y)
    iz, fz = _split(z)

    def corner(dx: int, dy: int, dz: int) -> FloatArray:
        return random3(ix + dx, iy + dy, iz + dz, seed)

    u = fade(fx)
    v = fade(fy)
    w = fade(fz)
    near = lerp(lerp(corner(0, 0, 0), corner(1, 0, 0), u), lerp(corner(0, 1, 0), corner(1, 1, 0), u), v)
    far = lerp(lerp(corner(0, 0, 1), corner(1, 0, 1), u), lerp(corner(0, 1, 1), corner(1, 1, 1), u), v)
    return lerp(near, far, w) * 2.0 - 1.0


def worley2(
    x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None, jitter: float = 1.0
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """セルラーノイズ（ウォーリーノイズ）。

    格子の各セルに特徴点を 1 個ずつ置き、最も近い特徴点までの距離 F1、
    2 番目に近い特徴点までの距離 F2、最も近い特徴点のセルに固有の乱数 (0〜1) を返す。
    jitter は特徴点をセル内でずらす量で、0 なら規則的な格子になる。
    """
    ix, fx = _split(x)
    iy, fy = _split(y)
    f1 = np.full(x.shape, np.inf)
    f2 = np.full(x.shape, np.inf)
    cell_id = np.zeros(x.shape)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            cx = _wrap(ix + dx, period)
            cy = _wrap(iy + dy, period)
            px = dx + 0.5 + jitter * (random2(cx, cy, seed) - 0.5)
            py = dy + 0.5 + jitter * (random2(cx, cy, seed + 1) - 0.5)
            distance = np.hypot(px - fx, py - fy)
            closer = distance < f1
            f2 = np.where(closer, f1, np.minimum(f2, distance))
            f1 = np.where(closer, distance, f1)
            cell_id = np.where(closer, random2(cx, cy, seed + 2), cell_id)
    return f1, f2, cell_id


def fbm(
    noise: Noise2,
    x: FloatArray,
    y: FloatArray,
    octaves: int = 5,
    lacunarity: float = 2.0,
    gain: float = 0.5,
    seed: int = 0,
    period: int | None = None,
) -> FloatArray:
    """フラクタル・ブラウン運動（fBm）。周波数を上げ、振幅を下げながらノイズを重ねる。

    結果は振幅の合計で割り、おおむね -1〜1 にそろえる。period を与える場合は
    lacunarity を整数にすると、すべてのオクターブが同じ周期でつながる。
    """
    total = np.zeros_like(x)
    amplitude = 1.0
    frequency = 1.0
    norm = 0.0
    for octave in range(octaves):
        octave_period = None if period is None else int(round(period * frequency))
        total += amplitude * noise(x * frequency, y * frequency, seed + octave, octave_period)
        norm += amplitude
        amplitude *= gain
        frequency *= lacunarity
    return total / norm


def turbulence(noise: Noise2, x: FloatArray, y: FloatArray, octaves: int = 5, seed: int = 0) -> FloatArray:
    """乱流。ノイズの絶対値を重ねる。値が 0 になる所に鋭い谷ができる（0〜1）。"""

    def absolute(x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray:
        return np.abs(noise(x, y, seed, period))

    return fbm(absolute, x, y, octaves, seed=seed)


def ridged(noise: Noise2, x: FloatArray, y: FloatArray, octaves: int = 5, seed: int = 0) -> FloatArray:
    """リッジノイズ。乱流を反転して 2 乗し、谷を鋭い尾根に変える（0〜1）。"""

    def ridge(x: FloatArray, y: FloatArray, seed: int = 0, period: int | None = None) -> FloatArray:
        return (1.0 - np.abs(noise(x, y, seed, period))) ** 2

    return fbm(ridge, x, y, octaves, seed=seed)


def fbm3(x: FloatArray, y: FloatArray, z: FloatArray, octaves: int = 5, seed: int = 0) -> FloatArray:
    """3 次元パーリンノイズによる fBm（-1〜1）。"""
    total = np.zeros_like(x)
    amplitude = 1.0
    frequency = 1.0
    norm = 0.0
    for octave in range(octaves):
        total += amplitude * perlin3(x * frequency, y * frequency, z * frequency, seed + octave)
        norm += amplitude
        amplitude *= 0.5
        frequency *= 2.0
    return total / norm
