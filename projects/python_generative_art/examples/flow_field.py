"""パーリンノイズによるフローフィールド上のパーティクル軌跡描画。

ノイズ値を角度に変換してベクトル場（フローフィールド）を作り、
多数のパーティクルをその場に沿って移動させることで、水の流れや
風のような曲線群を描く。
"""

import numpy as np
from PIL import Image, ImageDraw

from perlin_noise import fbm2d, make_permutation


def flow_angles(
    x: np.ndarray,
    y: np.ndarray,
    perm: np.ndarray,
    scale: float,
    rotations: float = 2.0,
) -> np.ndarray:
    """座標 x, y におけるフローフィールドの角度（ラジアン）を返す。

    fBm の値（おおよそ -1〜1）を、``rotations`` 回転分の角度に
    マッピングする。値を大きくするほど渦が細かく複雑になる。
    """
    noise_values: np.ndarray = fbm2d(x * scale, y * scale, perm, octaves=3)
    return noise_values * rotations * np.pi


def simulate_particles(
    width: int,
    height: int,
    perm: np.ndarray,
    num_particles: int = 400,
    num_steps: int = 200,
    step_length: float = 2.0,
    noise_scale: float = 0.01,
    seed: int = 0,
) -> np.ndarray:
    """パーティクルをフローフィールドに沿って移動させ、軌跡を返す。

    戻り値は形状 ``(num_steps + 1, num_particles, 2)`` の座標配列。
    各パーティクルの移動は、その時点の位置におけるフィールドの角度
    方向に、一定の歩幅 ``step_length`` だけ進む単純なオイラー法。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    positions: np.ndarray = rng.uniform(
        low=[0.0, 0.0],
        high=[float(width), float(height)],
        size=(num_particles, 2),
    )

    trail: np.ndarray = np.empty((num_steps + 1, num_particles, 2))
    trail[0] = positions

    for step in range(num_steps):
        angles: np.ndarray = flow_angles(
            positions[:, 0], positions[:, 1], perm, noise_scale
        )
        direction: np.ndarray = np.stack(
            [np.cos(angles), np.sin(angles)], axis=-1
        )
        positions = positions + direction * step_length
        trail[step + 1] = positions

    return trail


def draw_trails(trail: np.ndarray, width: int, height: int) -> Image.Image:
    """パーティクルの軌跡を線分として描画した画像を返す。

    キャンバス外に出た座標も含めて渡してよい。Pillow は描画範囲外の
    座標を自動的に切り詰めるため、追跡を打ち切る処理は不要。
    """
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    num_steps, num_particles, _ = trail.shape
    for particle_index in range(num_particles):
        points: list[tuple[float, float]] = [
            (
                float(trail[step, particle_index, 0]),
                float(trail[step, particle_index, 1]),
            )
            for step in range(num_steps)
        ]
        draw.line(points, fill=(40, 40, 40), width=1)

    return img


def main() -> None:
    width: int = 512
    height: int = 512
    perm: np.ndarray = make_permutation(seed=1)

    trail: np.ndarray = simulate_particles(width, height, perm)
    img: Image.Image = draw_trails(trail, width, height)
    img.save("flow_field.png")


if __name__ == "__main__":
    main()
