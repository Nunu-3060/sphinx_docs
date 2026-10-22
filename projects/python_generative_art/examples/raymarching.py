"""3 次元の距離関数とレイマーチング（スフィアトレーシング）。

2 次元の距離関数と同じく、3 次元でも「点から図形の表面までの距離」を
返す関数で形を表せる。画面の各画素からカメラの視線（レイ）を飛ばし、
距離関数の値だけ前に進む、という手順を繰り返すと、レイが表面に
ぶつかる位置を求められる。

距離関数の値は「その半径の球の中には表面がない」ことを保証するので、
その分だけ進んでも表面を突き抜けない。この方法をスフィアトレーシング
と呼ぶ。全ての画素のレイを NumPy の配列としてまとめて進める。
"""

import numpy as np
from PIL import Image


def sd_sphere(p: np.ndarray, center: np.ndarray, radius: float) -> np.ndarray:
    """球の距離関数。``p`` は形状 (..., 3) の点の配列。"""
    result: np.ndarray = np.linalg.norm(p - center, axis=-1) - radius
    return result


def sd_torus(p: np.ndarray, center: np.ndarray, major: float, minor: float) -> np.ndarray:
    """y 軸のまわりに水平に置いたトーラス（ドーナツ形）の距離関数。

    ``major`` は中心から管の中心までの半径、``minor`` は管の半径。
    """
    q: np.ndarray = p - center
    ring: np.ndarray = np.hypot(q[..., 0], q[..., 2]) - major
    result: np.ndarray = np.hypot(ring, q[..., 1]) - minor
    return result


def smooth_union(d1: np.ndarray, d2: np.ndarray, k: float) -> np.ndarray:
    """2 つの距離をなめらかにつなぐ和集合（2 次元の場合と同じ式）。"""
    h: np.ndarray = np.clip(0.5 + 0.5 * (d2 - d1) / k, 0.0, 1.0)
    result: np.ndarray = d2 * (1.0 - h) + d1 * h - k * h * (1.0 - h)
    return result


def scene(p: np.ndarray) -> np.ndarray:
    """場面全体の距離関数: 球とトーラスをなめらかにつなぎ、床の上に置く。"""
    sphere: np.ndarray = sd_sphere(p, np.array([0.0, 1.0, 0.0]), 0.8)
    torus: np.ndarray = sd_torus(p, np.array([0.0, 0.55, 0.0]), 1.15, 0.28)
    floor: np.ndarray = p[..., 1]  # 高さ 0 の水平な床
    result: np.ndarray = np.minimum(smooth_union(sphere, torus, 0.35), floor)
    return result


def march(
    origins: np.ndarray,
    directions: np.ndarray,
    max_steps: int = 128,
    max_distance: float = 30.0,
    epsilon: float = 1e-3,
) -> tuple[np.ndarray, np.ndarray]:
    """全てのレイを同時に進め、表面までの距離と、当たったかどうかを返す。

    各ステップで、まだ表面に当たっておらず遠くへ抜けてもいないレイ
    だけを、その位置の距離関数の値だけ進める。
    """
    travelled: np.ndarray = np.zeros(origins.shape[:-1])
    hit: np.ndarray = np.zeros(origins.shape[:-1], dtype=bool)
    active: np.ndarray = np.ones(origins.shape[:-1], dtype=bool)
    for _ in range(max_steps):
        if not active.any():
            break
        p: np.ndarray = origins[active] + directions[active] * travelled[active, np.newaxis]
        d: np.ndarray = scene(p)
        travelled[active] += d
        newly_hit: np.ndarray = d < epsilon
        escaped: np.ndarray = travelled[active] > max_distance
        hit[active] |= newly_hit
        active[active] = ~(newly_hit | escaped)
    return travelled, hit


def surface_normal(p: np.ndarray, h: float = 1e-3) -> np.ndarray:
    """表面の法線（距離関数の勾配の向き）を中心差分で求める。"""
    offsets: np.ndarray = np.eye(3) * h
    gradient: np.ndarray = np.stack(
        [scene(p + offsets[i]) - scene(p - offsets[i]) for i in range(3)], axis=-1
    )
    result: np.ndarray = gradient / np.linalg.norm(gradient, axis=-1, keepdims=True)
    return result


def render(width: int = 480, height: int = 360) -> Image.Image:
    """カメラから場面を見た画像を、拡散反射と影で陰影を付けて描く。"""
    # カメラの位置と、見る向きを表す 3 本の軸。
    eye: np.ndarray = np.array([0.0, 2.0, -3.4])
    target: np.ndarray = np.array([0.0, 0.6, 0.0])
    forward: np.ndarray = (target - eye) / np.linalg.norm(target - eye)
    right: np.ndarray = np.cross(np.array([0.0, 1.0, 0.0]), forward)
    right /= np.linalg.norm(right)
    up: np.ndarray = np.cross(forward, right)

    # 各画素を通るレイの向き。画面の縦の範囲を -1〜1 とする。
    ys: np.ndarray
    xs: np.ndarray
    ys, xs = np.mgrid[0:height, 0:width]
    u: np.ndarray = (2 * (xs + 0.5) - width) / height
    v: np.ndarray = -(2 * (ys + 0.5) - height) / height
    directions: np.ndarray = (
        forward * 1.6 + u[..., np.newaxis] * right + v[..., np.newaxis] * up
    )
    directions /= np.linalg.norm(directions, axis=-1, keepdims=True)
    origins: np.ndarray = np.broadcast_to(eye, directions.shape).copy()

    distance: np.ndarray
    hit: np.ndarray
    distance, hit = march(origins, directions)
    points: np.ndarray = origins + directions * distance[..., np.newaxis]

    # 拡散反射: 法線と光の向きの内積で明るさを決める。
    light: np.ndarray = np.array([-0.6, 0.8, -0.4])
    light /= np.linalg.norm(light)
    brightness: np.ndarray = np.zeros(hit.shape)
    normals: np.ndarray = surface_normal(points[hit])
    diffuse: np.ndarray = np.clip(normals @ light, 0.0, 1.0)

    # 影: 表面から光の向きへもう一度レイを進め、何かに当たれば影にする。
    shadow_origins: np.ndarray = points[hit] + normals * 0.01
    shadow_directions: np.ndarray = np.broadcast_to(light, shadow_origins.shape).copy()
    shadow_hit: np.ndarray
    _, shadow_hit = march(shadow_origins, shadow_directions, max_distance=10.0)
    diffuse[shadow_hit] = 0.0

    brightness[hit] = 0.15 + 0.85 * diffuse  # 0.15 は影の中の明るさ（環境光）
    # 遠くの床ほど背景の明るさに近づける（霧）。
    fog: np.ndarray = np.exp(-0.08 * distance)
    brightness = np.where(hit, brightness * fog + 0.85 * (1 - fog), 0.85)

    warm: np.ndarray = np.array([1.0, 0.94, 0.84])  # 白熱灯のような暖かい白
    rgb: np.ndarray = brightness[..., np.newaxis] * warm * 255
    return Image.fromarray(rgb.clip(0, 255).astype(np.uint8))


def main() -> None:
    render().save("raymarching.png")


if __name__ == "__main__":
    main()
