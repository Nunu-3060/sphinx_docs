"""第 13 章「群れと粒子」: ベルレ積分と距離の拘束による紐と布（Jakobsen、2001 年の方法）。

点の速度を持たず、現在の位置と 1 つ前の位置の差を速度とみなして進める（位置ベルレ積分）。
そのあと、つながった点どうしの距離を元の長さに戻す処理（拘束の解消）を何回か繰り返す。

* rope_iterations.png: 拘束を解消する反復の回数と、紐の伸びの関係
* cloth.mp4: 風に揺れ、動く球に押される布
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib
from draw2d import Canvas, rgb
from noise import perlin3
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 10.0


def verlet_step(position: FloatArray, previous: FloatArray, acceleration: FloatArray, dt: float,
                damping: float = 0.01) -> tuple[FloatArray, FloatArray]:
    """位置ベルレ積分で 1 歩進め、(新しい位置, 今の位置) を返す。damping は 1 歩あたりの速度の減衰の割合。"""
    new = position + (position - previous) * (1.0 - damping) + acceleration * dt * dt
    return new, position


def color_edges(edges: IntArray, count: int) -> list[IntArray]:
    """辺を、頂点を共有しないグループに分ける（貪欲な辺の彩色）。

    同じグループの辺は互いに独立なので、まとめて（ベクトル化して）拘束を解消しても、
    1 本ずつ順に解消したのと同じ結果になる。
    """
    used: list[set[int]] = [set() for _ in range(count)]
    colors = np.zeros(len(edges), dtype=np.int64)
    for index, (i, j) in enumerate(edges.tolist()):
        color = 0
        while color in used[i] or color in used[j]:
            color += 1
        colors[index] = color
        used[i].add(color)
        used[j].add(color)
    return [np.flatnonzero(colors == c) for c in range(int(colors.max()) + 1)]


def satisfy_constraints(position: FloatArray, edges: IntArray, rest: FloatArray, inverse_mass: FloatArray,
                        groups: list[IntArray], iterations: int) -> None:
    """各辺の長さを元の長さ rest に戻す処理を iterations 回繰り返す（position をその場で書き換える）。

    inverse_mass は質量の逆数で、0 の点（固定した点）は動かない。
    """
    for _ in range(iterations):
        for group in groups:
            i, j = edges[group, 0], edges[group, 1]
            delta = position[j] - position[i]
            length = np.maximum(np.linalg.norm(delta, axis=1), 1e-9)
            weight = inverse_mass[i] + inverse_mass[j]
            # 伸びた分（縮んだ分）を、質量の逆数の比で 2 点に振り分けて戻す。
            correction = delta * ((length - rest[group]) / (length * np.maximum(weight, 1e-9)))[:, None]
            position[i] += correction * inverse_mass[i][:, None]
            position[j] -= correction * inverse_mass[j][:, None]


def simulate_rope(iterations: int, duration: float, count: int = 30,
                  dt: float = 1.0 / 60.0) -> tuple[list[FloatArray], FloatArray]:
    """左端を固定し、水平にした紐を放す。各時刻の形と、全長と元の長さの比を返す。"""
    segment = 1.5 / (count - 1)
    position = np.stack([np.arange(count) * segment, np.zeros(count)], axis=1)
    previous = position.copy()
    edges = np.stack([np.arange(count - 1), np.arange(1, count)], axis=1)
    rest = np.full(count - 1, segment)
    inverse_mass = np.ones(count)
    inverse_mass[0] = 0.0
    groups = color_edges(edges, count)
    gravity = np.array([0.0, -9.8])
    shapes = []
    ratios = []
    for _ in range(int(duration / dt)):
        position, previous = verlet_step(position, previous, gravity, dt)
        position[0] = 0.0  # 固定した点は毎回元に戻す
        satisfy_constraints(position, edges, rest, inverse_mass, groups, iterations)
        shapes.append(position.copy())
        ratios.append(np.linalg.norm(np.diff(position, axis=0), axis=1).sum() / 1.5)
    return shapes, np.array(ratios)


def draw_rope(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(12, 3.8), gridspec_kw={"width_ratios": [1.0, 1.2]})
    dt = 1.0 / 60.0
    colors = {1: "#dd8452", 4: "#55a868", 16: "#4c72b0"}
    for iterations, color in colors.items():
        shapes, _ = simulate_rope(iterations, 0.6)
        for k, time_index in enumerate([12, 24, 35]):
            label = f"反復 {iterations} 回" if k == 0 else None
            axes[0].plot(shapes[time_index][:, 0], shapes[time_index][:, 1], "-", color=color, lw=1.8,
                         alpha=0.5 + 0.25 * k, label=label)
    axes[0].plot([0.0], [0.0], "s", color="black")
    axes[0].set_aspect("equal")
    axes[0].set_title("放してから 0.2・0.4・0.6 秒後の紐の形", fontsize=11)
    axes[0].legend(fontsize=9, loc="lower left")
    axes[0].grid(alpha=0.3)
    for iterations in [1, 2, 4, 16, 64]:
        _, ratios = simulate_rope(iterations, 2.0)
        axes[1].plot(np.arange(1, len(ratios) + 1) * dt, ratios, label=f"反復 {iterations} 回")
    axes[1].set_xlabel("時刻 t [s]")
    axes[1].set_ylabel("紐の全長 / 元の長さ")
    axes[1].set_title("紐の伸び（1 なら伸びていない）", fontsize=11)
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=9, ncol=2)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def make_cloth(columns: int, rows: int, spacing: float) -> tuple[FloatArray, IntArray, FloatArray]:
    """縦に吊るした布の点の位置 (rows × columns, 3)、辺 (E, 2)、辺の元の長さ (E,) を作る。"""
    c, r = np.meshgrid(np.arange(columns), np.arange(rows))
    position = np.stack([(c - (columns - 1) / 2) * spacing, -r * spacing + 0.9, np.zeros_like(c) * 0.0],
                        axis=-1).reshape(-1, 3).astype(np.float64)
    index = np.arange(rows * columns).reshape(rows, columns)
    edges = [
        np.stack([index[:, :-1].ravel(), index[:, 1:].ravel()], axis=1),      # 横
        np.stack([index[:-1, :].ravel(), index[1:, :].ravel()], axis=1),      # 縦
        np.stack([index[:-1, :-1].ravel(), index[1:, 1:].ravel()], axis=1),   # 斜め（せん断に抵抗する）
        np.stack([index[:-1, 1:].ravel(), index[1:, :-1].ravel()], axis=1),   # 斜め（逆向き）
        np.stack([index[:, :-2].ravel(), index[:, 2:].ravel()], axis=1),      # 1 つ飛ばし（曲げに抵抗する）
        np.stack([index[:-2, :].ravel(), index[2:, :].ravel()], axis=1),
    ]
    all_edges = np.concatenate(edges).astype(np.int64)
    rest = np.linalg.norm(position[all_edges[:, 1]] - position[all_edges[:, 0]], axis=1)
    return position, all_edges, rest


def sphere_center(t: float) -> FloatArray:
    """布を後ろから押す球の中心。4 秒から 9 秒の間に、布の裏から手前へ押し出して戻る。"""
    phase = min(max((t - 4.0) / 5.0, 0.0), 1.0)
    return np.array([0.3 * math.sin(2.0 * math.pi * phase), 0.3, 0.9 - 1.0 * math.sin(math.pi * phase)])


def render_cloth(file_name: str) -> None:
    columns, rows, spacing = 28, 20, 0.06
    position, edges, rest = make_cloth(columns, rows, spacing)
    previous = position.copy()
    count = len(position)
    inverse_mass = np.ones(count)
    pinned = np.arange(0, columns, 3)  # 上の辺の 3 点おきに留める（カーテンのフック）
    inverse_mass[pinned] = 0.0
    anchors = position[pinned].copy()
    anchors[:, 0] *= 0.75  # 留める間隔を布の幅より狭くし、たるみ（ひだ）を作る
    groups = color_edges(edges, count)
    radius = 0.28
    substeps = 2
    dt = 1.0 / FPS / substeps
    # 描画: 布の 4 角形と、カメラの向き
    quad = np.arange(rows * columns).reshape(rows, columns)
    quads = np.stack([quad[:-1, :-1], quad[:-1, 1:], quad[1:, 1:], quad[1:, :-1]], axis=-1).reshape(-1, 4)
    yaw, pitch = math.radians(-35.0), math.radians(12.0)
    rotate_y = np.array([[math.cos(yaw), 0, math.sin(yaw)], [0, 1, 0], [-math.sin(yaw), 0, math.cos(yaw)]])
    rotate_x = np.array([[1, 0, 0], [0, math.cos(pitch), -math.sin(pitch)], [0, math.sin(pitch), math.cos(pitch)]])
    view = rotate_x @ rotate_y
    light = np.array([0.3, 0.6, 0.75])
    light /= np.linalg.norm(light)
    with VideoWriter(output_dir(__file__) / file_name, WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in range(int(DURATION * FPS)):
            for sub in range(substeps):
                t = (frame * substeps + sub) * dt
                # 風: +z 向きの力を、場所と時刻で変わるノイズで揺らす。
                gust = perlin3(position[:, 0] * 2.5, position[:, 1] * 2.5, np.full(count, t * 1.2), seed=3)
                wind = np.zeros((count, 3))
                wind[:, 2] = 3.0 + 10.0 * gust + 2.0 * math.sin(t * 1.3)
                acceleration = wind + np.array([0.0, -9.8, 0.0])
                position, previous = verlet_step(position, previous, acceleration, dt, damping=0.02)
                position[pinned] = anchors
                satisfy_constraints(position, edges, rest, inverse_mass, groups, iterations=8)
                # 球との衝突: 球の中に入った点を、球の表面へ押し出す。
                center = sphere_center(t)
                offset = position - center
                distance = np.linalg.norm(offset, axis=1)
                inside = distance < radius + 0.02
                position[inside] = center + offset[inside] / distance[inside, None] * (radius + 0.02)
            canvas = Canvas(WIDTH, HEIGHT, background=(0.93, 0.93, 0.95), center=(0.0, 0.25), scale=200.0)
            projected = position @ view.T
            corners = projected[quads]
            normal = np.cross(corners[:, 1] - corners[:, 0], corners[:, 3] - corners[:, 0])
            normal /= np.maximum(np.linalg.norm(normal, axis=1, keepdims=True), 1e-9)
            facing = normal[:, 2] < 0.0  # カメラは -z 側から +z の向きを見ている
            shade = 0.35 + 0.65 * np.abs(normal @ light)
            depth = corners[:, :, 2].mean(axis=1)
            sphere = sphere_center(frame / FPS) @ view.T
            items = [(float(d), k) for k, d in enumerate(depth)] + [(float(sphere[2]), -1)]
            for _, k in sorted(items, reverse=True):  # 奥から順に描く（画家のアルゴリズム）
                if k < 0:
                    canvas.circle(sphere[:2], radius, fill=rgb((0.85, 0.55, 0.30)))
                    canvas.circle(sphere[:2] + np.array([-0.08, 0.08]), radius * 0.35, fill=rgb((0.95, 0.75, 0.55)))
                    continue
                base = np.array([0.25, 0.45, 0.75]) if facing[k] else np.array([0.80, 0.80, 0.85])
                color = rgb(base * shade[k])
                canvas.polygon(corners[k, :, :2], fill=color, outline=color)
            for anchor in anchors @ view.T:
                canvas.dot(anchor[:2], 3.0, rgb((0.2, 0.2, 0.2)))
            writer.write(canvas.to_array())


def main() -> None:
    setup_matplotlib()
    draw_rope("rope_iterations.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    render_cloth("cloth.mp4")


if __name__ == "__main__":
    main()
