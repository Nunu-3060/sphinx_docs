"""第 12 章「プロシージャルアニメーション」: 足の接地点を予測して踏み替える、手続き的な歩行。

胴体を前へ動かすだけで、足は次の規則に従って自分で踏み出す。

1. 各脚には、胴体に対して決まった「休止位置」（腰の真下の地面）がある。
2. 接地している足が休止位置から threshold 以上離れたら、一歩を踏み出す。
3. 着地点は、一歩が終わる時刻の休止位置を予測し、さらに少し先に置く。
4. 対角の 2 本ずつを組にし、もう一方の組が踏み出している間は踏み出さない（交互に歩く）。

脚の関節の位置は、fabrik.py の two_bone_ik（余弦定理による 2 ボーンの逆運動学）で求める。

* walk.mp4: 起伏のある地面を歩く 4 本脚の生き物
* walk_gait.png: 各脚が踏み出していた時間（歩容の図）と胴体の速さ
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from draw2d import Canvas, rgb
from fabrik import two_bone_ik
from noise import fbm, perlin2
from spring import spring_step
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 10.0
HIP_HEIGHT = 0.95      # 胴体の中心の、地面からの高さ
STEP_THRESHOLD = 0.32  # 休止位置からこれ以上離れたら踏み出す
STEP_TIME = 0.28       # 一歩にかける時間 [s]
LEAD_TIME = 0.22       # 着地点を、一歩が終わる時刻よりさらにこの時間ぶん先に置く [s]
LIFT = 0.18            # 足を持ち上げる高さ
THIGH, SHIN = 0.55, 0.55  # 腿と脛の長さ


def ground_height(x: FloatArray) -> FloatArray:
    """位置 x の地面の高さ（ノイズで作った起伏）。"""
    return 0.5 * fbm(perlin2, x * 0.3, np.full_like(x, 0.5), octaves=3, seed=4)


def body_speed(t: float) -> float:
    """時刻 t の胴体の速さ。ノイズで揺らし、6〜7 秒の間は止まる。"""
    wobble = float(fbm(perlin2, np.array([t * 0.4]), np.array([0.5]), octaves=2, seed=9)[0])
    stop = 1.0 - math.exp(-((t - 6.6) / 0.55) ** 4)
    start = min(1.0, t / 0.8)
    return 1.15 * (1.0 + 0.45 * wobble) * stop * start


@dataclass
class Leg:
    """1 本の脚の状態。"""

    hip_offset: float      # 胴体の中心から腰までの前後の距離
    group: int             # 交互に動く組（0 か 1）
    near: bool             # 手前の脚か（描く色と順番を変える）
    knee_forward: bool     # 膝を前に出すか後ろに出すか
    foot: FloatArray = field(default_factory=lambda: np.zeros(2))
    stepping: bool = False
    step_start: FloatArray = field(default_factory=lambda: np.zeros(2))
    step_end: FloatArray = field(default_factory=lambda: np.zeros(2))
    step_time: float = 0.0


def make_legs(body_x: float) -> list[Leg]:
    legs = [
        Leg(0.55, 0, True, True), Leg(-0.55, 1, True, False),
        Leg(0.62, 1, False, True), Leg(-0.48, 0, False, False),
    ]
    for leg in legs:
        # 組ごとに足の位置をずらしておくと、最初から交互に踏み出す。
        x = body_x + leg.hip_offset + (0.15 if leg.group == 0 else -0.15)
        leg.foot = np.array([x, float(ground_height(np.array([x]))[0])])
    return legs


def update_legs(legs: list[Leg], body_x: float, speed: float, dt: float) -> None:
    """足を接地させたまま、または一歩の途中を進め、必要なら新しい一歩を始める。"""
    for leg in legs:
        if leg.stepping:
            leg.step_time += dt
            u = min(leg.step_time / STEP_TIME, 1.0)
            s = u * u * (3.0 - 2.0 * u)  # 水平の動きは smoothstep で加減速する
            leg.foot = leg.step_start + (leg.step_end - leg.step_start) * s
            leg.foot[1] += LIFT * math.sin(math.pi * u)  # 弧を描いて持ち上げる
            if u >= 1.0:
                leg.stepping = False
    for leg in legs:
        rest_x = body_x + leg.hip_offset
        if leg.stepping or abs(leg.foot[0] - rest_x) < STEP_THRESHOLD:
            continue
        if any(other.stepping for other in legs if other.group != leg.group):
            continue  # もう一方の組が踏み出している間は待つ
        # 一歩が終わる時刻の休止位置を予測し、さらに少し先に着地させる。
        land_x = rest_x + speed * (STEP_TIME + LEAD_TIME)
        leg.stepping = True
        leg.step_time = 0.0
        leg.step_start = leg.foot.copy()
        leg.step_end = np.array([land_x, float(ground_height(np.array([land_x]))[0])])


def hip_position(leg: Leg, body: FloatArray, angle: float) -> FloatArray:
    """傾いた胴体に付いた腰の位置。"""
    c, s = math.cos(angle), math.sin(angle)
    offset = np.array([leg.hip_offset * c, leg.hip_offset * s]) + np.array([0.0, -0.12])
    result: FloatArray = body + offset
    return result


def solve_leg(leg: Leg, hip: FloatArray) -> FloatArray:
    """腰・膝・足の 3 点を求める。ボーンが 2 本なので、膝の向きを指定できる解析解を使う。"""
    return two_bone_ik(hip, leg.foot, THIGH, SHIN, bend=1.0 if leg.knee_forward else -1.0)


@dataclass
class Frame:
    """1 フレームの描画に必要な状態。"""

    body: FloatArray
    angle: float
    legs: list[tuple[FloatArray, bool, bool]]  # (腰・膝・足の 3 点, 手前か, 踏み出し中か)
    rest: list[float]
    camera_x: float


def simulate() -> tuple[list[Frame], FloatArray, list[list[bool]]]:
    """全フレームの状態と、胴体の速さ、各脚が踏み出し中かどうかの記録を返す。"""
    dt = 1.0 / FPS
    body_x = 0.0
    legs = make_legs(body_x)
    body_y, body_vy = np.array(HIP_HEIGHT), np.array(0.0)
    angle, angle_v = np.array(0.0), np.array(0.0)
    camera_x = 0.0
    frames: list[Frame] = []
    speeds = []
    stepping: list[list[bool]] = []
    for index in range(int(DURATION * FPS)):
        t = index * dt
        speed = body_speed(t)
        body_x += speed * dt
        update_legs(legs, body_x, speed, dt)
        # 胴体の高さと傾きは、足の位置から決めた目標値をばねで追う（揺れに柔らかさが出る）。
        feet = np.array([leg.foot for leg in legs])
        target_y = np.array(float(ground_height(np.array([body_x]))[0]) * 0.5 + feet[:, 1].mean() * 0.5 + HIP_HEIGHT)
        body_y, body_vy = spring_step(body_y, body_vy, target_y, 2.5, 0.6, dt)
        front = np.mean([leg.foot[1] for leg in legs if leg.hip_offset > 0])
        back = np.mean([leg.foot[1] for leg in legs if leg.hip_offset < 0])
        angle, angle_v = spring_step(angle, angle_v, np.array(math.atan2(front - back, 1.1)), 2.0, 0.7, dt)
        camera_x += (body_x + 0.4 - camera_x) * (1.0 - math.exp(-3.0 * dt))
        body = np.array([body_x, float(body_y)])
        drawn = []
        for leg in legs:
            chain = solve_leg(leg, hip_position(leg, body, float(angle)))
            drawn.append((chain, leg.near, leg.stepping))
        frames.append(Frame(body, float(angle), drawn, [body_x + leg.hip_offset for leg in legs], camera_x))
        speeds.append(speed)
        stepping.append([leg.stepping for leg in legs])
    return frames, np.array(speeds), stepping


def draw_frame(frame: Frame) -> FloatArray:
    canvas = Canvas(WIDTH, HEIGHT, background=(0.93, 0.95, 0.98), center=(frame.camera_x, 0.7), scale=110.0)
    left = frame.camera_x - 3.0
    xs = np.linspace(left, left + 6.0, 160)
    ground = np.stack([xs, ground_height(xs)], axis=1)
    canvas.polygon(np.vstack([ground, [[xs[-1], -3.0], [xs[0], -3.0]]]), fill=rgb((0.78, 0.74, 0.66)))
    canvas.polyline(ground, 2.0, rgb((0.45, 0.40, 0.33)))
    for x in frame.rest:  # 休止位置（腰の真下の地面）の目印
        y = float(ground_height(np.array([x]))[0])
        canvas.polyline([[x, y - 0.06], [x, y + 0.06]], 2.0, rgb((0.85, 0.35, 0.25), 0.7))

    def draw_legs(near: bool) -> None:
        color = (0.20, 0.25, 0.35) if near else (0.55, 0.60, 0.68)
        for chain, is_near, _ in frame.legs:
            if is_near == near:
                canvas.polyline(chain, 6.0 if near else 5.0, rgb(color))
                canvas.dot(chain[1], 4.0, rgb(color))
                canvas.dot(chain[2], 3.5, rgb(color))

    draw_legs(near=False)
    theta = np.linspace(0.0, 2.0 * math.pi, 48)
    c, s = math.cos(frame.angle), math.sin(frame.angle)
    ellipse = np.stack([0.8 * np.cos(theta), 0.28 * np.sin(theta)], axis=1)
    rotation = np.array([[c, s], [-s, c]])
    canvas.polygon(frame.body + ellipse @ rotation, fill=rgb((0.30, 0.45, 0.70)))
    eye = frame.body + np.array([0.6, 0.08]) @ rotation
    canvas.circle(eye, 0.07, fill=rgb((1.0, 1.0, 1.0)))
    canvas.circle(eye + np.array([0.02, 0.0]), 0.035, fill=rgb((0.1, 0.1, 0.1)))
    draw_legs(near=True)
    canvas.text((12, 10), "赤い印: 休止位置。足が離れすぎたら踏み出す", 14, rgb((0.2, 0.2, 0.2)))
    return canvas.to_array().astype(np.float64) / 255.0


def draw_gait(speeds: FloatArray, stepping: list[list[bool]], file_name: str) -> None:
    import matplotlib.pyplot as plt

    times = np.arange(len(speeds)) / FPS
    states = np.array(stepping)
    names = ["前・手前（組 A）", "後・手前（組 B）", "前・奥（組 B）", "後・奥（組 A）"]
    colors = ["#4c72b0", "#dd8452", "#dd8452", "#4c72b0"]
    figure, axes = plt.subplots(2, 1, figsize=(10, 4.2), sharex=True, gridspec_kw={"height_ratios": [1, 1.6]})
    axes[0].plot(times, speeds, color="#333333")
    axes[0].set_ylabel("胴体の速さ")
    axes[0].grid(alpha=0.3)
    for row, (name, color) in enumerate(zip(names, colors)):
        active = states[:, row]
        starts = np.flatnonzero(active & ~np.r_[False, active[:-1]])
        ends = np.flatnonzero(active & ~np.r_[active[1:], False])
        spans = [(times[a], times[b] - times[a] + 1.0 / FPS) for a, b in zip(starts, ends)]
        axes[1].broken_barh(spans, (row - 0.35, 0.7), color=color)
    axes[1].set_yticks(range(4), names)
    axes[1].invert_yaxis()
    axes[1].set_xlabel("時刻 t [s]")
    axes[1].set_title("足を上げて踏み出している時間", fontsize=10)
    axes[1].grid(alpha=0.3, axis="x")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    frames, speeds, stepping = simulate()
    draw_gait(speeds, stepping, "walk_gait.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    with VideoWriter(output_dir(__file__) / "walk.mp4", WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in frames:
            writer.write(draw_frame(frame))


if __name__ == "__main__":
    main()
