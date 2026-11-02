"""第 14 章「映像の生成」: 完全にループするアニメーション（4 次元ノイズを円周上でサンプリングする）。

2 次元の画像を時間とともに滑らかに変えるには、画像の座標 (x, y) に時間の座標を加えた
3 次元ノイズを使えばよい。しかし時間の座標を直線的に進めると、最後のフレームと最初のフレームが
つながらない。そこで時間の座標を 2 つ（z, w）にし、時刻 t に応じて (z, w) を円周の上で 1 周させる。
円周は閉じているので、1 周した時点で最初の値に戻り、ループが継ぎ目なくつながる。

* loop_methods.png: 3 つの方法で作ったループの比較（1 画素の値の変化、画像のコントラストの変化）
* loop.mp4: 4 次元ノイズで作った、5 秒で 1 周するループ
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from PIL import Image

from color import cosine_palette
from common import FloatArray, IntArray, grid, output_dir, save_figure, setup_matplotlib
from noise import fade, lerp, perlin3
from prng import hash_u32, to_uint32
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, LOOP = 640, 360, 30, 5.0

# 4 次元パーリンノイズの勾配: 成分の 1 つが 0 で、残りが ±1 の 32 本のベクトル。
_GRADIENTS4 = np.array(
    [g for zero in range(4) for g in itertools.product(*[(0,) if k == zero else (-1, 1) for k in range(4)])],
    dtype=np.float64,
)


def corner_hashes(cells: list[IntArray], seed: int) -> dict[tuple[int, ...], IntArray]:
    """超立方体の 16 個の頂点のハッシュ値。キーは頂点のずれ (dx, dy, dz, dw)。

    prng.hash3 と同じく、シード → w → z → y → x の順にハッシュを入れ子にする。
    途中までの結果を頂点の間で共有すると、ハッシュの計算は 16 × 5 回から 2 + 4 + 8 + 16 回に減る。
    """
    level: dict[tuple[int, ...], IntArray] = {(): hash_u32(to_uint32(seed)).astype(np.int64)}
    with np.errstate(over="ignore"):
        for axis in (3, 2, 1, 0):
            level = {
                (offset,) + key: hash_u32(to_uint32(cells[axis] + offset) + to_uint32(h)).astype(np.int64)
                for key, h in level.items()
                for offset in (0, 1)
            }
    return level


def perlin4(x: FloatArray, y: FloatArray, z: FloatArray, w: FloatArray, seed: int = 0) -> FloatArray:
    """4 次元パーリンノイズ。超立方体の 16 個の頂点の勾配と変位の内積を、4 方向に補間する。"""
    coordinates = [x, y, z, w]
    cells = [np.floor(c).astype(np.int64) for c in coordinates]
    fractions = [c - np.floor(c) for c in coordinates]
    weights = [fade(f) for f in fractions]
    hashes = corner_hashes(cells, seed)

    def corner(offset: tuple[int, ...]) -> FloatArray:
        g = _GRADIENTS4[hashes[offset] % 32]
        return sum((g[..., k] * (fractions[k] - offset[k]) for k in range(4)), np.zeros_like(x))

    # 頂点の値を、w → z → y → x の順に 1 次元ずつ補間して減らしていく。
    values = {offset: corner(offset) for offset in itertools.product((0, 1), repeat=4)}
    for axis in (3, 2, 1, 0):
        values = {
            key: lerp(values[key + (0,) + rest], values[key + (1,) + rest], weights[axis])
            for key, rest in {(k[:axis], k[axis + 1:]) for k in values}
        }
    return values[()]


def loop_noise(x: FloatArray, y: FloatArray, t: float, period: float, radius: float, seed: int = 0) -> FloatArray:
    """周期 period で完全にループするノイズ。時刻 t を半径 radius の円周上の点 (z, w) に写す。"""
    angle = 2.0 * math.pi * t / period
    z = np.full_like(x, radius * math.cos(angle))
    w = np.full_like(x, radius * math.sin(angle))
    return perlin4(x, y, z, w, seed)


def crossfade_noise(x: FloatArray, y: FloatArray, t: float, period: float, speed: float) -> FloatArray:
    """比較用: 時刻 t と t - period の 3 次元ノイズを、t に比例する重みで混ぜてループさせる。"""
    weight = (t % period) / period
    a = perlin3(x, y, np.full_like(x, speed * (t % period)))
    b = perlin3(x, y, np.full_like(x, speed * (t % period - period)))
    result: FloatArray = (1.0 - weight) * a + weight * b
    return result


def draw_methods(file_name: str) -> None:
    import matplotlib.pyplot as plt

    period = 4.0
    speed = 0.5                                # 3 次元ノイズの時間の座標が 1 秒に進む量
    radius = speed * period / (2.0 * math.pi)  # 円周の長さが同じ量になる半径
    times = np.linspace(0.0, 2.0 * period, 400, endpoint=False)
    px = np.array([0.37])
    py = np.array([0.81])
    naive = [float(perlin3(px, py, np.array([speed * (t % period)]))[0]) for t in times]
    fade_values = [float(crossfade_noise(px, py, t, period, speed)[0]) for t in times]
    circle = [float(loop_noise(px, py, t, period, radius)[0]) for t in times]

    x, y = grid(128, 128, scale=24.0)  # 広い範囲で測り、場所によるばらつきを平均する
    sample_times = np.linspace(0.0, period, 41)
    fade_std = [float(np.std(crossfade_noise(x, y, t, period, speed))) for t in sample_times]
    circle_std = [float(np.std(loop_noise(x, y, t, period, radius))) for t in sample_times]

    figure, axes = plt.subplots(1, 2, figsize=(12, 3.6), gridspec_kw={"width_ratios": [1.6, 1.0]})
    axes[0].plot(times, naive, label="時刻をそのまま使う（周期で折り返す）")
    axes[0].plot(times, fade_values, label="2 つの時刻を混ぜる")
    axes[0].plot(times, circle, label="4 次元ノイズの円周")
    for k in range(3):
        axes[0].axvline(k * period, color="gray", lw=0.8, ls="--")
    axes[0].set_xlabel("時刻 t [s]（周期 4 秒）")
    axes[0].set_ylabel("ある 1 画素の値")
    axes[0].set_title("1 画素の値の変化")
    axes[0].legend(fontsize=8, loc="upper right", framealpha=0.9)
    axes[0].grid(alpha=0.3)
    axes[1].plot(sample_times, fade_std, "-o", ms=3, color="#dd8452", label="2 つの時刻を混ぜる")
    axes[1].plot(sample_times, circle_std, "-o", ms=3, color="#55a868", label="4 次元ノイズの円周")
    axes[1].set_ylim(0.0, max(circle_std + fade_std) * 1.2)
    axes[1].set_xlabel("時刻 t [s]")
    axes[1].set_ylabel("画像の値の標準偏差")
    axes[1].set_title("画像のコントラストの変化")
    axes[1].legend(fontsize=8, loc="lower left")
    axes[1].grid(alpha=0.3)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def noise_value(t: float, x: FloatArray, y: FloatArray) -> FloatArray:
    """時刻 t の値。2 オクターブのループするノイズを重ねる（どちらも同じ周期 LOOP で 1 周する）。"""
    radius = 0.6
    return loop_noise(x, y, t, LOOP, radius, seed=1) + 0.5 * loop_noise(x * 2.0, y * 2.0, t, LOOP, radius * 2.0, seed=2)


def colorize(value: FloatArray) -> FloatArray:
    """ノイズの値を、等高線の縞の入った色に変える。"""
    color = cosine_palette(value * 0.6 + 0.55, d=(0.0, 0.1, 0.2))
    lines = np.abs(np.sin(value * 6.0 * math.pi))
    shade = 0.55 + 0.45 * np.clip(lines * 4.0, 0.0, 1.0)  # 等高線の所を暗くする
    result: FloatArray = color * shade[..., None]
    return result


def render_video(file_name: str) -> None:
    # 計算を軽くするため、ノイズの値は縦横 1/4 の解像度で計算し、値を滑らかに拡大してから色を付ける
    # （模様が滑らかなので、拡大による誤差は目立たない。等高線は拡大後に描くのでぼけない）。
    shrink = 4
    x, y = grid(WIDTH // shrink, HEIGHT // shrink, scale=3.0)
    with VideoWriter(output_dir(__file__) / file_name, WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in range(int(LOOP * FPS)):  # 最後のフレームは t = LOOP の 1 フレーム前（t = LOOP は t = 0 と同じ）
            small = noise_value(frame / FPS, x, y).astype(np.float32)
            large = Image.fromarray(small).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
            value = np.asarray(large, dtype=np.float64)
            writer.write(colorize(value))


def main() -> None:
    setup_matplotlib()
    draw_methods("loop_methods.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    render_video("loop.mp4")


if __name__ == "__main__":
    main()
