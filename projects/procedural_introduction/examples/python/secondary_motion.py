"""第 12 章「プロシージャルアニメーション」: 尻尾や髪のような揺れものを、鎖状につないだばねで動かす。

各節は「親の節から決めた向きに 1 節ぶん進んだ位置」を目標にしてばねで追い、最後に親との距離を
元の長さに戻す。親（頭）を動かすだけで、遅れ・行き過ぎ・揺り戻しといった二次動作が生まれる。

各節は親の動きを追う 2 次系なので、減衰比を小さくすると、節を経るごとに揺れが増幅されて
先端が暴れる。ここでは減衰比を 0.7 以上にし、柔らかさは固有振動数で調整する。

* chain_stop.png: 急に止まった頭に付いた尻尾の動き（ストロボ写真のように重ねて描く）
* secondary.mp4: ばねの固有振動数と減衰比を変えた 3 体の動き
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from draw2d import Canvas, rgb
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 10.0
GRAVITY = np.array([0.0, -2.0])  # 画面の大きさに合わせて弱めた重力


@dataclass
class Chain:
    """鎖状のばね。points[0] は親（頭）に固定された根元。"""

    points: FloatArray      # 各節の位置 (N, 2)
    velocities: FloatArray  # 各節の速度 (N, 2)
    rest: FloatArray        # 各節が親から見て向こうとする方向（単位ベクトル）
    length: float           # 節の間の長さ
    frequency: float        # ばねの固有振動数 [Hz]
    damping: float          # 減衰比


def make_chain(root: FloatArray, rest: tuple[float, float], count: int, length: float,
               frequency: float, damping: float) -> Chain:
    direction = np.array(rest) / np.linalg.norm(rest)
    points = root + np.arange(count)[:, None] * length * direction
    return Chain(points, np.zeros_like(points), direction, length, frequency, damping)


def chain_step(chain: Chain, root: FloatArray, dt: float, gravity: FloatArray = GRAVITY) -> None:
    """根元を root に動かし、残りの節を時間 dt だけ進める。"""
    p, v = chain.points, chain.velocities
    omega = 2.0 * math.pi * chain.frequency
    v[0] = (root - p[0]) / dt
    p[0] = root
    for i in range(1, len(p)):
        # 目標は、親の節から決めた向き rest に 1 節ぶん進んだ位置。
        target = p[i - 1] + chain.rest * chain.length
        # 減衰は親との速度の差に掛ける（全体が一緒に動くときには効かない。空気抵抗とは区別する）。
        a = omega * omega * (target - p[i]) - 2.0 * chain.damping * omega * (v[i] - v[i - 1]) + gravity
        v[i] += a * dt
        new = p[i] + v[i] * dt
        # 親との距離を元の長さに戻す（伸び縮みしない鎖にする）。
        offset = new - p[i - 1]
        new = p[i - 1] + offset * (chain.length / max(float(np.linalg.norm(offset)), 1e-9))
        v[i] = (new - p[i]) / dt
        p[i] = new


def ease_in_out(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


# 頭が順に移動する位置。各区間は 0.6 秒で移動し、0.65 秒止まる。
KEYS = [(0.0, 0.5), (-0.6, 0.5), (0.6, 0.8), (0.6, -0.1), (-0.5, 0.2), (0.0, 0.9), (0.0, 0.5)]


def head_position(t: float) -> FloatArray:
    """時刻 t の頭の位置（1 体ぶんの局所座標）。最後の 1.5 秒は円を描いて動く。"""
    move, hold = 0.6, 0.65
    span = move + hold
    index = int(t // span)
    if index < len(KEYS) - 1:
        a = np.array(KEYS[index])
        b = np.array(KEYS[index + 1])
        result: FloatArray = a + (b - a) * ease_in_out((t - index * span) / move)
        return result
    local = t - (len(KEYS) - 1) * span
    angle = 2.0 * math.pi * local / 1.6
    return np.array(KEYS[-1]) + 0.35 * np.array([math.sin(angle), 1.0 - math.cos(angle)]) * min(local / 0.3, 1.0)


SETTINGS = [(1.5, 0.7), (3.0, 0.7), (8.0, 1.0)]


def draw_chain_stop(file_name: str) -> None:
    import matplotlib.pyplot as plt

    dt = 1.0 / 240.0
    figure, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    for ax, (frequency, damping) in zip(axes, SETTINGS):
        chain = make_chain(np.array([-0.75, 0.0]), (0.0, -1.0), 12, 0.1, frequency, damping)
        for step in range(int(1.6 / dt)):
            t = step * dt
            # 一定の速さ 1.5 で右へ動き、t = 0.5 で急に止まる。
            root = np.array([-0.75 + 0.75 * min(t / 0.5, 1.0), 0.0])
            chain_step(chain, root, dt)
            if step % 24 == 0 and t >= 0.5:
                alpha = 0.15 + 0.85 * (1.0 - (t - 0.5) / 1.1)
                ax.plot(chain.points[:, 0], chain.points[:, 1], "-", color="#4c72b0", alpha=alpha, lw=2)
        ax.plot([0.0], [0.0], "o", color="#dd8452", ms=12)
        ax.set_title(f"f = {frequency:g} Hz、ζ = {damping:g}", fontsize=11)
        ax.set_aspect("equal")
        ax.set_xlim(-1.0, 1.0)
        ax.set_ylim(-1.3, 0.3)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.suptitle("右へ動いてきた頭（橙）が急に止まった後の尻尾（濃いほど止まった直後）", fontsize=11)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def render_video(file_name: str) -> None:
    substeps = 4
    dt = 1.0 / FPS / substeps
    columns = [-2.25, 0.0, 2.25]
    creatures = []
    for column, (frequency, damping) in zip(columns, SETTINGS):
        head = np.array([column, 0.5])
        tail = make_chain(head, (0.0, -1.0), 14, 0.09, frequency, damping)
        hair = [make_chain(head, (math.sin(a), math.cos(a)), 7, 0.08, frequency, damping) for a in (-0.5, 0.0, 0.5)]
        creatures.append((column, tail, hair))
    with VideoWriter(output_dir(__file__) / file_name, WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in range(int(DURATION * FPS)):
            for sub in range(substeps):
                t = (frame * substeps + sub + 1) * dt
                for column, tail, hair in creatures:
                    head = head_position(t) + np.array([column, -0.2])
                    chain_step(tail, head + np.array([0.0, -0.18]), dt)
                    for strand in hair:
                        chain_step(strand, head + strand.rest * 0.18, dt)
            canvas = Canvas(WIDTH, HEIGHT, background=(0.97, 0.96, 0.93), center=(0.0, 0.1), scale=88.0)
            for index, (column, tail, hair) in enumerate(creatures):
                frequency, damping = SETTINGS[index]
                canvas.text((WIDTH / 2 + column * 88.0, 14), f"f = {frequency:g} Hz、ζ = {damping:g}", 15,
                            rgb((0.2, 0.2, 0.2)), anchor="ma")
                for strand in [tail, *hair]:
                    count = len(strand.points)
                    for i in range(count - 1):
                        width = 7.0 * (1.0 - i / count) + 1.5
                        canvas.polyline(strand.points[i:i + 2], width, rgb((0.85, 0.45, 0.25)))
                head = tail.points[0] - np.array([0.0, -0.18])
                canvas.circle(head, 0.22, fill=rgb((0.30, 0.45, 0.70)))
                canvas.circle(head + np.array([-0.07, 0.04]), 0.04, fill=rgb((1.0, 1.0, 1.0)))
                canvas.circle(head + np.array([0.07, 0.04]), 0.04, fill=rgb((1.0, 1.0, 1.0)))
            writer.write(canvas.to_array())


def main() -> None:
    setup_matplotlib()
    draw_chain_stop("chain_stop.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    render_video("secondary.mp4")


if __name__ == "__main__":
    main()
