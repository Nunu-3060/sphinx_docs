"""カールノイズによるフローフィールドと、角度によるフローフィールドの比較。

ノイズ値を角度に変換する ``flow_field.py`` のフローフィールドでは、
パーティクルが流れの「吸い込み口」に集まり、何本かの太い筋に
まとまってしまう。カールノイズは、ノイズをスカラーポテンシャル
(流れ関数) とみなし、その回転 (curl) を速度とすることで、
湧き出しも吸い込みもない (発散が 0 の) ベクトル場を作る。
パーティクルは集まりも散りもせず、流体のように均一に流れる。
"""

import numpy as np
from PIL import Image, ImageDraw

from flow_field import draw_trails, flow_angles
from perlin_noise import fbm2d, make_permutation

# 流れ関数の偏微分を中心差分で求めるときの刻み幅（ノイズの座標の単位）。
_DIFF_STEP: float = 0.01


def curl_velocity(
    x: np.ndarray,
    y: np.ndarray,
    perm: np.ndarray,
    scale: float,
) -> np.ndarray:
    """座標 x, y におけるカールノイズの速度ベクトルを返す。

    fBm を流れ関数 psi とみなし、その回転
    ``(d psi / dy, -d psi / dx)`` を速度とする。偏微分は中心差分で
    近似する。戻り値は形状 ``x.shape + (2,)`` の配列。

    ``scale`` を変えても速さが大きく変わらないよう、偏微分はノイズの
    座標 (ピクセル座標に ``scale`` を掛けたもの) について求める。
    速さの平均はおおよそ 1 になる。
    """
    h: float = _DIFF_STEP
    u: np.ndarray = x * scale
    v: np.ndarray = y * scale

    def psi(pu: np.ndarray, pv: np.ndarray) -> np.ndarray:
        # 流れ関数。
        return fbm2d(pu, pv, perm, octaves=3)

    dpsi_du: np.ndarray = (psi(u + h, v) - psi(u - h, v)) / (2 * h)
    dpsi_dv: np.ndarray = (psi(u, v + h) - psi(u, v - h)) / (2 * h)
    return np.stack([dpsi_dv, -dpsi_du], axis=-1)


def simulate_curl_particles(
    positions: np.ndarray,
    perm: np.ndarray,
    num_steps: int,
    speed: float,
    noise_scale: float,
) -> np.ndarray:
    """パーティクルをカールノイズの速度場に沿って移動させ、軌跡を返す。

    ``positions`` は形状 ``(num_particles, 2)`` の初期位置。戻り値は
    形状 ``(num_steps + 1, num_particles, 2)`` の座標配列。速度の
    大きさは場所によって異なるため、向きだけを取り出して歩幅を
    揃えることはしない（揃えると発散が 0 の性質が失われる）。

    位置の更新には中点法を使う。オイラー法では、渦の周りを回る
    パーティクルが 1 ステップごとに少しずつ外側へずれていき、
    渦の中心に点のない穴ができてしまうためである。
    """
    trail: np.ndarray = np.empty((num_steps + 1,) + positions.shape)
    trail[0] = positions

    for step in range(num_steps):
        # 半歩だけ進んだ位置（中点）での速度を使って 1 歩進める。
        velocity: np.ndarray = curl_velocity(
            positions[:, 0], positions[:, 1], perm, noise_scale
        )
        midpoint: np.ndarray = positions + velocity * (speed / 2)
        velocity = curl_velocity(
            midpoint[:, 0], midpoint[:, 1], perm, noise_scale
        )
        positions = positions + velocity * speed
        trail[step + 1] = positions

    return trail


def simulate_angle_particles(
    positions: np.ndarray,
    perm: np.ndarray,
    num_steps: int,
    step_length: float,
    noise_scale: float,
) -> np.ndarray:
    """比較用に、角度によるフローフィールドで最終位置だけを求める。

    ``flow_field.py`` の ``flow_angles`` を使い、各ステップで一定の
    歩幅 ``step_length`` だけ進める。戻り値は最終位置の配列。
    """
    for _ in range(num_steps):
        angles: np.ndarray = flow_angles(
            positions[:, 0], positions[:, 1], perm, noise_scale
        )
        direction: np.ndarray = np.stack(
            [np.cos(angles), np.sin(angles)], axis=-1
        )
        positions = positions + direction * step_length
    return positions


def draw_points(points: np.ndarray, width: int, height: int) -> Image.Image:
    """点の集まりを小さな黒い点として描いた画像を返す。"""
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    for px, py in points:
        draw.point((float(px), float(py)), fill=(40, 40, 40))
    return img


def main() -> None:
    width: int = 512
    height: int = 512
    noise_scale: float = 0.01
    perm: np.ndarray = make_permutation(seed=1)
    rng: np.random.Generator = np.random.default_rng(0)

    # 1. カールノイズに沿ったパーティクルの軌跡。
    #    flow_field.png と同じ数のパーティクルを、同じ条件で配置する。
    start: np.ndarray = rng.uniform(
        low=[0.0, 0.0],
        high=[float(width), float(height)],
        size=(400, 2),
    )
    # 1 ステップで進む距離は、平均で 2 ピクセル程度になる。
    trail: np.ndarray = simulate_curl_particles(
        start, perm, num_steps=200, speed=2.0, noise_scale=noise_scale
    )
    draw_trails(trail, width, height).save("curl_noise.png")

    # 2. 一様に散らした多数の点を長時間流したあとの分布の比較。
    #    キャンバスの外からも点が流れ込むよう、周囲に余白を取って配置する。
    margin: float = 200.0
    num_points: int = 20000
    area_scale: float = (width + 2 * margin) * (height + 2 * margin) / (
        width * height
    )
    points: np.ndarray = rng.uniform(
        low=[-margin, -margin],
        high=[width + margin, height + margin],
        size=(int(num_points * area_scale), 2),
    )
    num_steps: int = 60
    angle_points: np.ndarray = simulate_angle_particles(
        points, perm, num_steps, step_length=2.0, noise_scale=noise_scale
    )
    curl_points: np.ndarray = simulate_curl_particles(
        points, perm, num_steps, speed=2.0, noise_scale=noise_scale
    )[-1]
    draw_points(angle_points, width, height).save("curl_compare_angle.png")
    draw_points(curl_points, width, height).save("curl_compare_curl.png")


if __name__ == "__main__":
    main()
