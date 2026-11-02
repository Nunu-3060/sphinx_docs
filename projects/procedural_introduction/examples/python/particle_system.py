"""第 13 章「群れと粒子」: パーティクルシステム（発生・寿命・力・寿命に応じた色）。

粒子の状態は、位置・速度・経過時間・寿命の配列で持つ（粒子ごとのオブジェクトは作らない）。
毎フレーム、エミッターが新しい粒子を加え、力で速度と位置を更新し、寿命が尽きた粒子を取り除く。

* particle_params.png: 空気抵抗の強さと軌跡の関係、寿命に応じた色と明るさ
* sparks.mp4: 動き回るエミッターから飛び散る火花
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

from color import gradient_map, hex_to_rgb
from common import FloatArray, output_dir, save_figure, setup_matplotlib
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 8.0
SCALE = 100.0  # 1 単位あたりの画素数

# 寿命の割合（0: 生まれた直後、1: 消える直前）に応じた色
LIFE_COLORS = [
    (0.0, hex_to_rgb("#ffffff")), (0.15, hex_to_rgb("#fff2a8")), (0.4, hex_to_rgb("#ffb03b")),
    (0.7, hex_to_rgb("#e8471c")), (1.0, hex_to_rgb("#5a1010")),
]


@dataclass
class Particles:
    """粒子の集まり。各配列の先頭の次元が粒子の番号。"""

    position: FloatArray  # (N, 2)
    velocity: FloatArray  # (N, 2)
    age: FloatArray       # (N,) 生まれてからの時間 [s]
    lifetime: FloatArray  # (N,) 寿命 [s]

    @staticmethod
    def empty() -> Particles:
        return Particles(np.zeros((0, 2)), np.zeros((0, 2)), np.zeros(0), np.zeros(0))


@dataclass
class Emitter:
    """粒子を発生させる仕組み。"""

    rate: float                          # 1 秒あたりに発生させる数
    speed: tuple[float, float]           # 初速の範囲
    lifetime: tuple[float, float]        # 寿命の範囲 [s]
    direction: float = math.pi / 2.0     # 発射の向き（ラジアン。上向きが π/2）
    spread: float = math.pi              # 向きのばらつき（± spread）
    carry: float = 0.0                   # 端数の繰り越し（1 フレームに 0.4 個なら、何フレームかに 1 個）

    def emit(self, particles: Particles, origin: FloatArray, origin_velocity: FloatArray, dt: float,
             rng: np.random.Generator) -> Particles:
        """時間 dt のあいだに発生する粒子を加えた集まりを返す。"""
        self.carry += self.rate * dt
        count = int(self.carry)
        self.carry -= count
        if count == 0:
            return particles
        angle = self.direction + rng.uniform(-self.spread, self.spread, count)
        speed = rng.uniform(*self.speed, count)
        velocity = np.stack([np.cos(angle), np.sin(angle)], axis=1) * speed[:, None] + origin_velocity
        # 1 フレームの間に発生した粒子は、発生した時刻に応じて少しずつ進めておく（塊にならないように）。
        offset = rng.uniform(0.0, dt, count)
        position = origin + velocity * offset[:, None]
        return Particles(
            np.vstack([particles.position, position]),
            np.vstack([particles.velocity, velocity]),
            np.concatenate([particles.age, offset]),
            np.concatenate([particles.lifetime, rng.uniform(*self.lifetime, count)]),
        )


def update(particles: Particles, dt: float, gravity: FloatArray, drag: float) -> Particles:
    """力で速度と位置を進め、寿命の尽きた粒子を取り除く。

    空気抵抗は速度に比例する力 -drag × v とし、厳密な解 v × exp(-drag × dt) で減らす。
    """
    velocity = (particles.velocity + gravity * dt) * math.exp(-drag * dt)
    position = particles.position + velocity * dt
    age = particles.age + dt
    alive = age < particles.lifetime
    return Particles(position[alive], velocity[alive], age[alive], particles.lifetime[alive])


def splat(image: FloatArray, points: FloatArray, colors: FloatArray) -> None:
    """点の色を画像 (H, W, 3) に加算する。点の位置の端数に応じて、隣り合う 4 画素に分けて足す（双線形）。"""
    height, width = image.shape[:2]
    ix = np.floor(points[:, 0]).astype(np.int64)
    iy = np.floor(points[:, 1]).astype(np.int64)
    fx = (points[:, 0] - ix)[:, None]
    fy = (points[:, 1] - iy)[:, None]
    indices = []
    values = []
    for dx, dy, weight in [(0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)]:
        px = ix + dx
        py = iy + dy
        inside = (px >= 0) & (px < width) & (py >= 0) & (py < height)
        # 画素 (py, px) のチャンネル c は、平らに並べた配列の (py * width + px) * 3 + c 番目
        base = (py[inside] * width + px[inside]) * 3
        indices.append((base[:, None] + np.arange(3)).ravel())
        values.append((colors * weight)[inside].ravel())
    total = np.bincount(np.concatenate(indices), np.concatenate(values), minlength=height * width * 3)
    image += total.reshape(height, width, 3)


def blur(image: FloatArray, sigma: float, shrink: int = 1) -> FloatArray:
    """ガウスぼかし。shrink > 1 なら縮小してからぼかして拡大する（広いぼかしを速く計算する）。"""
    if shrink == 1:
        result: FloatArray = gaussian_filter(image, sigma=(sigma, sigma, 0.0))
        return result
    height, width = image.shape[:2]
    small = image.reshape(height // shrink, shrink, width // shrink, shrink, 3).mean(axis=(1, 3))
    small = gaussian_filter(small, sigma=(sigma / shrink, sigma / shrink, 0.0))
    # 拡大は Pillow の双線形補間で行う（32 bit 浮動小数点数の画像としてチャンネルごとに）。
    channels = [Image.fromarray(small[:, :, c].astype(np.float32)).resize((width, height), Image.Resampling.BILINEAR)
                for c in range(3)]
    return np.stack([np.asarray(channel, dtype=np.float64) for channel in channels], axis=2)


def render(particles: Particles, dt: float) -> FloatArray:
    """粒子を光の点として加算し、ぼかして光のにじみを付ける。

    各粒子は、1 フレームの間に動いた線分の上に点を並べて描く（動きのぶれ、モーションブラー）。
    """
    life = particles.age / particles.lifetime
    colors = gradient_map(life, LIFE_COLORS) * ((1.0 - life) ** 1.5)[:, None]
    samples = 6
    steps = np.arange(samples) / samples
    positions = (particles.position[None, :, :] - particles.velocity[None, :, :] * dt * steps[:, None, None])
    positions = positions.reshape(-1, 2)
    pixels = np.stack([positions[:, 0] * SCALE + WIDTH / 2, HEIGHT / 2 - positions[:, 1] * SCALE], axis=1)
    light = np.zeros((HEIGHT, WIDTH, 3))
    splat(light, pixels, np.tile(colors / samples, (samples, 1)))
    exposed = 5.0 * blur(light, 0.6) + 6.0 * blur(light, 5.0, shrink=4)
    background = np.array([0.02, 0.02, 0.05])
    result: FloatArray = 1.0 - (1.0 - background) * np.exp(-exposed)  # 明るい所が飽和しないように丸める
    return result


def emitter_path(t: float) -> FloatArray:
    """時刻 t のエミッターの位置（8 の字を描く）。"""
    return np.array([1.8 * math.sin(0.9 * t), 0.5 + 0.7 * math.sin(1.8 * t)])


def render_video(file_name: str) -> None:
    rng = np.random.default_rng(3)
    dt = 1.0 / FPS
    emitter = Emitter(rate=600.0, speed=(0.5, 3.0), lifetime=(0.4, 1.6))
    gravity = np.array([0.0, -2.5])
    particles = Particles.empty()
    with VideoWriter(output_dir(__file__) / file_name, WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in range(int(DURATION * FPS)):
            t = frame * dt
            origin = emitter_path(t)
            origin_velocity = (emitter_path(t + 1e-3) - origin) / 1e-3
            # エミッターの速度の一部を粒子に引き継がせると、動く向きに尾を引く。
            particles = emitter.emit(particles, origin, origin_velocity * 0.4, dt, rng)
            particles = update(particles, dt, gravity, drag=1.2)
            writer.write(render(particles, dt))


def draw_params(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(12, 3.8), gridspec_kw={"width_ratios": [1.3, 1.0]})
    dt = 1.0 / 120.0
    gravity = np.array([0.0, -9.8])
    for drag in [0.0, 0.5, 1.5, 4.0]:
        p = Particles(np.zeros((1, 2)), np.array([[6.0, 6.0]]), np.zeros(1), np.full(1, 10.0))
        path = [p.position[0].copy()]
        for _ in range(int(2.0 / dt)):
            p = update(p, dt, gravity, drag)
            path.append(p.position[0].copy())
        trace = np.array(path)
        trace = trace[trace[:, 1] > -0.5]
        axes[0].plot(trace[:, 0], trace[:, 1], label=f"drag = {drag:g}")
    axes[0].set_title("同じ初速（右上 45°）で投げた粒子の軌跡")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].set_aspect("equal")
    axes[0].set_ylim(-0.5, 2.5)
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=9)

    life = np.linspace(0.0, 1.0, 256)
    colors = gradient_map(life, LIFE_COLORS)
    brightness = (1.0 - life) ** 1.5
    axes[1].imshow(colors[None, :, :], extent=(0.0, 1.0, -0.25, -0.05), aspect="auto")
    axes[1].imshow((colors * brightness[:, None])[None, :, :], extent=(0.0, 1.0, -0.5, -0.3), aspect="auto")
    axes[1].plot(life, brightness, color="#333333", label="明るさ (1 - 割合)^1.5")
    axes[1].text(0.02, -0.15, "色", va="center", fontsize=9)
    axes[1].text(0.02, -0.4, "色 × 明るさ", va="center", fontsize=9, color="white")
    axes[1].set_xlim(0.0, 1.0)
    axes[1].set_ylim(-0.55, 1.05)
    axes[1].set_yticks([0.0, 0.5, 1.0])
    axes[1].set_xlabel("寿命に対する経過時間の割合")
    axes[1].set_title("寿命に応じた色と明るさ")
    axes[1].legend(fontsize=9, loc="upper right")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_params("particle_params.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    render_video("sparks.mp4")


if __name__ == "__main__":
    main()
