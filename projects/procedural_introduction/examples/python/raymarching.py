"""第 9 章「陰関数と体積表現」: レイマーチングで距離関数と雲を直接描く。

* sphere_tracing.png: スフィアトレーシングの進み方（2 次元の図）
* raymarch_scene.png: NumPy で書いたスフィアトレーシングで描いたシーン（480 × 270）
* raymarch_buffers.png: 同じシーンの距離・反復回数・法線
* cloud.png: 3 次元ノイズの密度場を、吸収と散乱を簡略化したボリュームレンダリングで描いた雲
* cloud_params.png: 雲のパラメーター（自己影・被覆・消散係数）を変えた比較
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import map_coordinates

from common import FloatArray, output_dir, save_figure, save_image, setup_matplotlib
from noise import fbm3
from prng import random2
from sdf3d import gradient, length, sd_box, sd_plane, sd_sphere, sd_torus, smooth_min

WIDTH, HEIGHT = 480, 270
SUN = np.array([-0.5, -0.4, 0.75]) / np.linalg.norm([-0.5, -0.4, 0.75])  # 太陽の方向（光が来る向き）


def normalize3(v: FloatArray) -> FloatArray:
    """ベクトル（最後の軸）を長さ 1 にする。"""
    result: FloatArray = v / np.maximum(length(v), 1e-12)[..., None]
    return result


def camera_rays(eye: FloatArray, target: FloatArray, width: int, height: int, fov: float = 1.0) -> FloatArray:
    """カメラ eye から target を見たときの、各画素を通るレイの向き (height, width, 3) を返す。

    fov は画面の横幅の半分を、カメラから距離 1 の所で測った長さ（視野の広さ）。
    """
    forward = normalize3(target - eye)
    right = normalize3(np.cross(forward, np.array([0.0, 0.0, 1.0])))
    up = np.cross(right, forward)
    u = (np.arange(width) + 0.5) / width * 2.0 - 1.0
    v = ((np.arange(height) + 0.5) / height * 2.0 - 1.0) * height / width
    uu, vv = np.meshgrid(u, -v)
    rays = forward + fov * (uu[..., None] * right + vv[..., None] * up)
    return normalize3(rays)


def scene_parts(p: FloatArray, k: float = 0.35) -> tuple[FloatArray, FloatArray]:
    """シーンの物体（球と直方体をスムーズにつないだものと、トーラス）と床の距離を別々に返す。"""
    sphere = sd_sphere(p - np.array([-0.35, 0.0, 0.95]), 0.55)
    box = sd_box(p - np.array([0.35, 0.1, 0.45]), (0.45, 0.45, 0.45)) - 0.03  # 0.03 引いて角を丸める
    torus = sd_torus(p - np.array([1.45, -0.9, 0.22]), 0.42, 0.18)
    objects = smooth_min(smooth_min(sphere, box, k), torus, k)
    return objects, sd_plane(p, 0.0)


def scene_sdf(p: FloatArray) -> FloatArray:
    """シーン全体の距離関数。"""
    objects, floor = scene_parts(p)
    return np.minimum(objects, floor)


@dataclass
class Hits:
    """レイマーチングの結果。t はレイに沿って進んだ距離、steps は反復回数。"""

    t: FloatArray
    steps: FloatArray
    hit: FloatArray


def sphere_trace(origin: FloatArray, rays: FloatArray, max_steps: int = 128, max_distance: float = 30.0,
                 epsilon: float = 1e-3) -> Hits:
    """スフィアトレーシング。各レイを、その点の距離関数の値だけ進めることを繰り返す。

    距離関数の値は「その半径の球の中には何も無い」ことを保証するので、その分だけ
    進んでも物体を突き抜けない。値が epsilon より小さくなったら表面に当たったとする。
    """
    shape = rays.shape[:-1]
    t = np.zeros(shape)
    steps = np.zeros(shape)
    hit = np.zeros(shape, dtype=bool)
    active = np.ones(shape, dtype=bool)
    for _ in range(max_steps):
        index = np.nonzero(active)
        d = scene_sdf(origin + rays[index] * t[index][..., None])
        t[index] += d
        steps[index] += 1
        arrived = d < epsilon * t[index]  # 遠くの物体ほど、許す誤差を大きくする
        hit[index] |= arrived
        active[index] = ~arrived & (t[index] < max_distance)
        if not active.any():
            break
    return Hits(t, steps, hit.astype(np.float64))


def soft_shadow(points: FloatArray, direction: FloatArray, softness: float = 10.0, max_steps: int = 48) -> FloatArray:
    """光源へ向かうレイを進め、途中で物体にどれだけ近づいたかから柔らかい影を求める（0: 影、1: 日なた）。

    レイが物体をかすめた所では、距離 h と進んだ距離 t の比 h / t が小さくなる。
    その最小値を影の濃さに使うと、半影のある影になる（Inigo Quilez による方法）。
    """
    t = np.full(points.shape[:-1], 0.02)
    shade = np.ones(points.shape[:-1])
    for _ in range(max_steps):
        h = scene_sdf(points + direction * t[..., None])
        shade = np.minimum(shade, softness * h / t)
        t += np.clip(h, 0.02, 0.3)
    result: FloatArray = np.clip(shade, 0.0, 1.0)
    return result


def shade_scene(eye: FloatArray, rays: FloatArray, hits: Hits) -> FloatArray:
    """当たった点の法線・材質・光から色を決める。当たらなかった画素は空の色にする。"""
    sky = np.array([0.62, 0.75, 0.92]) - 0.35 * np.clip(rays[..., 2:3], 0.0, 1.0)
    points = eye + rays * hits.t[..., None]
    normals = gradient(scene_sdf, points)
    objects, floor = scene_parts(points)
    # 材質: 床は市松模様、物体は 1 色
    checker = (np.floor(points[..., 0] * 2.0) + np.floor(points[..., 1] * 2.0)) % 2.0
    floor_color = (0.55 + 0.15 * checker)[..., None] * np.array([1.0, 1.0, 1.0])
    albedo = np.where((objects < floor)[..., None], np.array([0.85, 0.45, 0.30]), floor_color)
    diffuse = np.clip(np.sum(normals * SUN, axis=-1), 0.0, 1.0)
    shadow = soft_shadow(points + normals * 2e-3, SUN)
    ambient = 0.5 + 0.5 * normals[..., 2]  # 上を向いた面ほど空の光を受ける
    light = (diffuse * shadow)[..., None] * np.array([1.0, 0.92, 0.8]) + 0.3 * ambient[..., None] * np.array(
        [0.6, 0.7, 0.9])
    color = albedo * light
    fog = 1.0 - np.exp(-0.004 * hits.t ** 2)  # 遠いほど空の色に近づける
    color = color + (sky - color) * fog[..., None]
    color = np.where(hits.hit[..., None] > 0.0, color, sky)
    result: FloatArray = np.clip(color, 0.0, 1.0) ** (1.0 / 2.2)  # 線形の明るさを表示用（sRGB）に近似変換
    return result


def draw_sphere_tracing(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, Rectangle

    def scene2d(x: FloatArray, y: FloatArray) -> FloatArray:
        circle = np.hypot(x - 7.0, y - 3.4) - 1.3
        box = np.maximum(np.abs(x - 3.6) - 1.2, np.abs(y - 0.4) - 0.9)
        return np.minimum(circle, box)

    figure, ax = plt.subplots(figsize=(9, 4.0))
    ax.add_patch(Circle((7.0, 3.4), 1.3, color="#dd8452", alpha=0.8))
    ax.add_patch(Rectangle((2.4, -0.5), 2.4, 1.8, color="#dd8452", alpha=0.8))
    origin = np.array([0.0, 1.5])
    direction = np.array([1.0, 0.14]) / np.hypot(1.0, 0.14)
    t = 0.0
    points = []
    for _ in range(30):
        p = origin + direction * t
        d = float(scene2d(np.array(p[0]), np.array(p[1])))
        points.append(p)
        ax.add_patch(Circle(tuple(p), d, fill=False, edgecolor="#4c72b0", linewidth=0.9))
        if d < 0.02:
            break
        t += d
    points_array = np.array(points)
    ax.plot(*np.vstack([origin, origin + direction * (t + 0.6)]).T, color="#999999", linestyle="--", linewidth=0.8)
    ax.plot(*points_array.T, "o-", color="#4c72b0", markersize=4)
    ax.annotate("カメラ", (float(origin[0]), float(origin[1])), xytext=(-1.2, 0.9), fontsize=10)
    ax.annotate("表面に到達", points_array[-1], xytext=(points_array[-1][0] - 1.0, points_array[-1][1] - 2.2),
                fontsize=10, arrowprops={"arrowstyle": "->"})
    ax.set_xlim(-1.6, 9.0)
    ax.set_ylim(-1.2, 5.0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    save_figure(figure, output_dir(__file__) / file_name)


def render_scene() -> tuple[FloatArray, FloatArray, Hits, FloatArray]:
    """シーンを描き、画像・レイ・当たり・法線を返す。"""
    eye = np.array([3.2, -4.6, 2.2])
    rays = camera_rays(eye, np.array([0.3, 0.0, 0.5]), WIDTH, HEIGHT, fov=0.55)
    hits = sphere_trace(eye, rays)
    normals = gradient(scene_sdf, eye + rays * hits.t[..., None])
    return shade_scene(eye, rays, hits), rays, hits, normals


def draw_buffers(file_name: str, hits: Hits, normals: FloatArray) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(12, 2.6))
    depth = np.where(hits.hit > 0.0, hits.t, np.nan)
    panels = [
        ("当たった点までの距離 t", depth, "viridis"),
        ("反復回数（物体の縁と遠くで増える）", hits.steps, "magma"),
    ]
    for ax, (title, image, cmap) in zip(axes, panels):
        shown = ax.imshow(image, cmap=cmap)
        figure.colorbar(shown, ax=ax, fraction=0.03, pad=0.02)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    axes[2].imshow(np.where(hits.hit[..., None] > 0.0, normals * 0.5 + 0.5, 1.0))
    axes[2].set_title("法線（x, y, z を R, G, B で表示）", fontsize=10)
    axes[2].set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


# ---- 雲（ボリュームレンダリング） ----------------------------------------------------------

CLOUD_LOW = np.array([-1.8, -1.1, -0.7])  # 雲を入れる直方体の範囲
CLOUD_HIGH = np.array([1.8, 1.1, 0.7])
CLOUD_SHAPE = (108, 66, 42)  # 密度を計算しておく格子の点の数


def cloud_density(coverage: float = 0.0) -> FloatArray:
    """雲の密度の格子 (nx, ny, nz)。楕円体の形に fBm を足し、負の部分を 0 にする。

    coverage を大きくすると、雲の量（密度が正になる範囲）が増える。
    """
    axes = [np.linspace(CLOUD_LOW[i], CLOUD_HIGH[i], CLOUD_SHAPE[i]) for i in range(3)]
    x, y, z = np.meshgrid(*axes, indexing="ij")
    shape = 1.0 - np.sqrt((x / 1.5) ** 2 + (y / 0.9) ** 2 + (z / 0.55) ** 2)  # 中心で 1、楕円体の表面で 0
    detail = fbm3(x * 2.2, y * 2.2, z * 2.2, octaves=5, seed=3)
    return np.maximum(shape + 1.2 * detail - 0.15 + coverage, 0.0) * 4.0


def sample(volume: FloatArray, points: FloatArray) -> FloatArray:
    """格子の値を、任意の点 (..., 3) で 3 線形補間して読む。範囲の外は 0 とする。"""
    scale = (np.array(CLOUD_SHAPE) - 1) / (CLOUD_HIGH - CLOUD_LOW)
    index = ((points - CLOUD_LOW) * scale).reshape(-1, 3).T
    values = map_coordinates(volume, index, order=1, mode="constant", cval=0.0)
    result: FloatArray = values.reshape(points.shape[:-1])
    return result


def light_transmittance(density: FloatArray, extinction: float, steps: int = 24) -> FloatArray:
    """格子の各点から太陽へ向かって進んだとき、光がどれだけ残るか（0〜1）を前もって計算する。"""
    axes = [np.linspace(CLOUD_LOW[i], CLOUD_HIGH[i], CLOUD_SHAPE[i]) for i in range(3)]
    points = np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1)
    step = 1.6 / steps
    optical_depth = np.zeros(CLOUD_SHAPE)
    for k in range(steps):
        optical_depth += sample(density, points + SUN * (k + 0.5) * step) * step
    result: FloatArray = np.exp(-extinction * optical_depth)
    return result


def ray_box(origin: FloatArray, rays: FloatArray) -> tuple[FloatArray, FloatArray]:
    """レイが直方体に入る距離と出る距離を求める（スラブ法）。当たらないレイは入る距離 > 出る距離になる。"""
    with np.errstate(divide="ignore"):
        inverse = 1.0 / rays
    t1 = (CLOUD_LOW - origin) * inverse
    t2 = (CLOUD_HIGH - origin) * inverse
    t_near = np.max(np.minimum(t1, t2), axis=-1)
    t_far = np.min(np.maximum(t1, t2), axis=-1)
    return np.maximum(t_near, 0.0), t_far


def render_cloud(width: int, height: int, coverage: float = 0.0, extinction: float = 3.0,
                 self_shadow: bool = True, steps: int = 96) -> FloatArray:
    """雲を描く。レイに沿って一定の間隔で密度を読み、光の吸収と散乱を足し合わせる。

    Beer–Lambert の法則により、密度 ρ の媒質を距離 ds 進むと、光は exp(−σ ρ ds) 倍に減る
    （σ は消散係数 extinction。吸収と散乱で光が減る割合）。各点で散乱して目に届く光は、太陽の光がそこまで届く割合
    （自己影）と、その点から目までの透過率 T を掛けたものとする。
    """
    density = cloud_density(coverage)
    to_sun = light_transmittance(density, extinction) if self_shadow else np.ones(CLOUD_SHAPE)
    eye = np.array([0.0, -4.3, -0.35])
    rays = camera_rays(eye, np.array([0.0, 0.0, 0.05]), width, height, fov=0.55)
    t_near, t_far = ray_box(eye, rays)
    ds = np.maximum(t_far - t_near, 0.0) / steps
    # 標本点の位置を画素ごとに少しずらし、一定間隔の標本による縞模様（バンディング）を防ぐ。
    py, px = np.mgrid[0:height, 0:width]
    jitter = random2(px, py, seed=5)

    transmittance = np.ones((height, width))
    light = np.zeros((height, width, 3))
    sun_color = np.array([1.0, 0.95, 0.85]) * 1.4
    ambient_color = np.array([0.55, 0.65, 0.8]) * 0.45
    for k in range(steps):
        t = t_near + (k + jitter) * ds
        points = eye + rays * t[..., None]
        rho = sample(density, points)
        absorbed = 1.0 - np.exp(-extinction * rho * ds)  # この区間で散乱・吸収される光の割合
        lit = sample(to_sun, points)[..., None] * sun_color + ambient_color
        light += (transmittance * absorbed)[..., None] * lit
        transmittance *= 1.0 - absorbed
    sky = np.array([0.35, 0.55, 0.85]) + 0.3 * (np.linspace(0.0, 1.0, height)[:, None, None])
    color = light + transmittance[..., None] * sky
    result: FloatArray = np.clip(color, 0.0, 1.0)
    return result


def draw_cloud_params(file_name: str) -> None:
    import matplotlib.pyplot as plt

    settings = [
        ("自己影なし", {"self_shadow": False}),
        ("基準（被覆 0、消散係数 3）", {}),
        ("被覆を増やす（被覆 0.25）", {"coverage": 0.25}),
        ("消散係数を下げる（消散係数 0.8）", {"extinction": 0.8}),
    ]
    figure, axes = plt.subplots(2, 2, figsize=(10, 6.0))
    for ax, (title, options) in zip(axes.ravel(), settings):
        ax.imshow(render_cloud(320, 180, steps=72, **options))  # type: ignore[arg-type]
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    out = output_dir(__file__)
    draw_sphere_tracing("sphere_tracing.png")
    image, _, hits, normals = render_scene()
    save_image(image, out / "raymarch_scene.png")
    draw_buffers("raymarch_buffers.png", hits, normals)
    save_image(render_cloud(WIDTH, HEIGHT), out / "cloud.png")
    draw_cloud_params("cloud_params.png")


if __name__ == "__main__":
    main()
