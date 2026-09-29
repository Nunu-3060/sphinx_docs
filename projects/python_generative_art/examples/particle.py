"""位置・速度・加速度を持つ基本的なパーティクルクラスと、
重力・床との反発・粒子間の反発力を組み込んだ簡単な物理シミュレーション。

積分にはもっとも単純なオイラー法を用いる。時間刻み ``dt`` を十分小さく
取れば実用上問題のない精度で運動を再現できる。

.. math::

   v_{t+1} = v_t + a_t \\, dt, \\qquad p_{t+1} = p_t + v_{t+1} \\, dt
"""

from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageDraw


@dataclass
class Particle:
    """位置・速度・加速度を ``np.ndarray`` で保持するパーティクル。

    ``apply_force`` で力を加え、``update`` で1ステップ分の運動を
    オイラー積分によって進める。力は毎ステップ加速度に蓄積され、
    ``update`` の最後にリセットされる（次のフレームに持ち越さない）。
    """

    position: np.ndarray
    velocity: np.ndarray = field(
        default_factory=lambda: np.zeros(2, dtype=float)
    )
    acceleration: np.ndarray = field(
        default_factory=lambda: np.zeros(2, dtype=float)
    )
    mass: float = 1.0

    def apply_force(self, force: np.ndarray) -> None:
        """ニュートンの運動方程式 F = ma に従い、加速度に力を加算する。"""
        self.acceleration = self.acceleration + force / self.mass

    def update(self, dt: float) -> None:
        """オイラー積分で速度・位置を1ステップ更新し、加速度を0に戻す。"""
        self.velocity = self.velocity + self.acceleration * dt
        self.position = self.position + self.velocity * dt
        self.acceleration = np.zeros(2, dtype=float)


def repulsion_forces(
    positions: np.ndarray,
    strength: float = 150.0,
    min_distance: float = 10.0,
) -> np.ndarray:
    """全パーティクル間に働く反発力を、ループを使わず一括計算する。

    ``positions`` は shape ``(N, 2)``。各粒子の受ける反発力の合計を
    同じ shape で返す。力の大きさは距離の2乗に反比例させ、
    ``min_distance`` で発散を防ぐ（ソフトニング）。
    """
    diff: np.ndarray = positions[:, None, :] - positions[None, :, :]
    dist_sq: np.ndarray = np.sum(diff * diff, axis=-1)
    dist_sq = np.maximum(dist_sq, min_distance ** 2)
    np.fill_diagonal(dist_sq, np.inf)

    dist: np.ndarray = np.sqrt(dist_sq)
    direction: np.ndarray = diff / dist[..., None]
    magnitude: np.ndarray = strength / dist_sq
    return np.sum(direction * magnitude[..., None], axis=1)


def simulate_gravity_bounce(
    n_particles: int = 12,
    n_steps: int = 300,
    dt: float = 0.05,
    gravity: float = -9.8,
    floor_y: float = 0.0,
    restitution: float = 0.5,
    width: float = 10.0,
    seed: int | None = 0,
) -> np.ndarray:
    """重力・床との反発・粒子間反発を組み込んだ落下シミュレーション。

    戻り値は各ステップの位置を記録した shape ``(n_steps, n_particles, 2)``
    の軌跡配列。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    particles: list[Particle] = [
        Particle(
            position=np.array(
                [rng.uniform(0.2 * width, 0.8 * width),
                 rng.uniform(6.0, 9.0)],
                dtype=float,
            ),
            velocity=np.array(
                [rng.uniform(-1.0, 1.0), 0.0], dtype=float
            ),
        )
        for _ in range(n_particles)
    ]

    trail: np.ndarray = np.empty((n_steps, n_particles, 2), dtype=float)
    gravity_force: np.ndarray = np.array([0.0, gravity], dtype=float)

    for step in range(n_steps):
        positions: np.ndarray = np.stack(
            [p.position for p in particles]
        )
        repulsions: np.ndarray = repulsion_forces(positions)

        for particle, repulsion in zip(particles, repulsions):
            particle.apply_force(gravity_force * particle.mass)
            particle.apply_force(repulsion)
            particle.update(dt)

            # 床との衝突判定: めり込んだら押し戻し、速度を反転させる
            if particle.position[1] < floor_y:
                particle.position[1] = floor_y
                if particle.velocity[1] < 0:
                    particle.velocity[1] *= -restitution
            # 左右の壁でも同様に跳ね返す
            if particle.position[0] < 0.0:
                particle.position[0] = 0.0
                particle.velocity[0] *= -restitution
            elif particle.position[0] > width:
                particle.position[0] = width
                particle.velocity[0] *= -restitution

        trail[step] = np.stack([p.position for p in particles])

    return trail


def verlet_step(
    positions: np.ndarray,
    previous_positions: np.ndarray,
    acceleration: np.ndarray,
    dt: float,
    damping: float = 0.995,
) -> tuple[np.ndarray, np.ndarray]:
    """位置ベースのVerlet積分で1ステップ進める。

    ``Particle`` クラスは速度を明示的な状態として持ち、力を毎ステップ
    加速度に蓄積してから積分する **力ベース** の方式だった。Verlet積分
    はこれとは異なり、速度を陽には持たず、前ステップの位置との差分
    ``position - previous_position`` を「暗黙の速度」として扱う。

    .. math::

       p_{t+1} = p_t + (p_t - p_{t-1}) \\cdot \\mathrm{damping}
                + a_t \\, dt^2

    速度を明示的に持たないこの方式は、後述する距離拘束(constraint)を
    位置に対して直接押し引きするだけで安定して解けるという利点があり、
    ロープやクロスのような、多数の点が拘束で連結された系でよく使われる
    (Thomas Jakobsenの "Advanced Character Physics", 2001)。
    """
    velocity_like: np.ndarray = (positions - previous_positions) * damping
    new_positions: np.ndarray = (
        positions + velocity_like + acceleration * dt * dt
    )
    return new_positions, positions


def satisfy_distance_constraints(
    positions: np.ndarray,
    constraints: list[tuple[int, int, float]],
    pinned: set[int],
    iterations: int = 10,
) -> np.ndarray:
    """2点間の距離を ``rest_length`` に近づける拘束を繰り返し解く。

    各拘束 ``(i, j, rest_length)`` について、2点の距離と目標距離との
    差の半分ずつを、互いに離れる/近づく向きに押し戻す。1回の反復では
    他の拘束とのつじつまが合わなくなる(1つ直すと別の1つがずれる)ため、
    ``iterations`` 回繰り返すことで全体を緩やかに目標距離へ収束させる
    (Gauss-Seidel法に近い緩和法)。``pinned`` に含まれる点は固定点として
    動かさない。
    """
    positions = positions.copy()
    for _ in range(iterations):
        for i, j, rest_length in constraints:
            delta: np.ndarray = positions[j] - positions[i]
            distance: float = float(np.hypot(*delta)) or 1e-9
            correction: np.ndarray = delta * (
                (distance - rest_length) / distance
            )
            if i in pinned and j in pinned:
                continue
            if i in pinned:
                positions[j] -= correction
            elif j in pinned:
                positions[i] += correction
            else:
                positions[i] += correction * 0.5
                positions[j] -= correction * 0.5
    return positions


def simulate_rope(
    n_points: int = 24,
    length: float = 9.0,
    steps: int = 250,
    dt: float = 0.12,
    gravity: float = -9.8,
    left_anchor: tuple[float, float] = (1.0, 9.0),
    right_anchor: tuple[float, float] = (9.0, 9.0),
) -> np.ndarray:
    """両端を固定したロープが、重力で垂れ下がる様子をVerlet積分で解く。

    両端の間の直線距離より ``length`` (ロープの全長)を長めに取ることで
    「たるみ」を持たせておく。戻り値は最終形状 ``(n_points, 2)``で、
    垂れ下がった形は理論上の懸垂線(カテナリー曲線)に近づく。
    """
    rest_length: float = length / (n_points - 1)
    t: np.ndarray = np.linspace(0.0, 1.0, n_points)[:, None]
    positions: np.ndarray = (1 - t) * np.array(left_anchor) + t * np.array(
        right_anchor
    )
    previous_positions: np.ndarray = positions.copy()
    constraints: list[tuple[int, int, float]] = [
        (i, i + 1, rest_length) for i in range(n_points - 1)
    ]
    pinned: set[int] = {0, n_points - 1}
    anchor_points: dict[int, np.ndarray] = {
        i: positions[i].copy() for i in pinned
    }
    acceleration: np.ndarray = np.array([0.0, gravity])

    for _ in range(steps):
        positions, previous_positions = verlet_step(
            positions, previous_positions, acceleration, dt
        )
        for i, anchor_point in anchor_points.items():
            positions[i] = anchor_point
            previous_positions[i] = anchor_point
        positions = satisfy_distance_constraints(
            positions, constraints, pinned
        )

    return positions


def simulate_cloth(
    cols: int = 16,
    rows: int = 16,
    spacing: float = 0.5,
    steps: int = 150,
    dt: float = 0.1,
    gravity: float = -9.8,
    origin: tuple[float, float] = (1.0, 9.0),
) -> np.ndarray:
    """上端の両端だけを固定した格子状の布が、重力で垂れる様子を解く。

    ロープが1本の鎖(隣接点だけを結ぶ拘束)だったのに対し、クロスは
    格子状に並んだ点を縦横の拘束で結ぶ。斜め方向の拘束(シア拘束)を
    加えていないため、正方形のマスが台形状に歪みながら垂れる、
    やや伸縮性の高い布になる。
    """
    def index(row: int, col: int) -> int:
        return row * cols + col

    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        origin[0] + np.arange(cols) * spacing,
        origin[1] - np.arange(rows) * spacing,
    )
    positions: np.ndarray = np.stack([xs.ravel(), ys.ravel()], axis=-1)
    previous_positions: np.ndarray = positions.copy()

    constraints: list[tuple[int, int, float]] = []
    for row in range(rows):
        for col in range(cols):
            if col + 1 < cols:
                constraints.append(
                    (index(row, col), index(row, col + 1), spacing)
                )
            if row + 1 < rows:
                constraints.append(
                    (index(row, col), index(row + 1, col), spacing)
                )

    pinned: set[int] = {index(0, 0), index(0, cols - 1)}
    anchor_points: dict[int, np.ndarray] = {
        i: positions[i].copy() for i in pinned
    }
    acceleration: np.ndarray = np.array([0.0, gravity])

    for _ in range(steps):
        positions, previous_positions = verlet_step(
            positions, previous_positions, acceleration, dt
        )
        for i, anchor_point in anchor_points.items():
            positions[i] = anchor_point
            previous_positions[i] = anchor_point
        positions = satisfy_distance_constraints(
            positions, constraints, pinned, iterations=6
        )

    return positions.reshape(rows, cols, 2)


def _to_pixels(
    positions: np.ndarray,
    width: int,
    height: int,
    world: float = 10.0,
    margin: float = 20.0,
) -> np.ndarray:
    """シミュレーション座標(原点左下、y上向き)を画像座標へ変換する。"""
    scale: float = (min(width, height) - 2 * margin) / world
    pixels: np.ndarray = positions.copy()
    pixels[..., 0] = margin + pixels[..., 0] * scale
    pixels[..., 1] = height - (margin + pixels[..., 1] * scale)
    return pixels


def render_rope(
    positions: np.ndarray,
    width: int = 400,
    height: int = 400,
    color: tuple[int, int, int] = (60, 90, 160),
) -> Image.Image:
    """ロープを、頂点をつないだ折れ線と、頂点ごとの丸印で描画する。"""
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    pixels: np.ndarray = _to_pixels(positions, width, height)
    joints: list[tuple[float, float]] = [
        (float(x), float(y)) for x, y in pixels
    ]
    draw.line(joints, fill=color, width=4, joint="curve")
    for x, y in joints:
        draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=color)
    return img


def render_cloth(
    grid_positions: np.ndarray,
    width: int = 400,
    height: int = 400,
    color: tuple[int, int, int] = (150, 70, 110),
) -> Image.Image:
    """クロスを、縦横の拘束を結ぶ線分の格子として描画する。"""
    rows: int
    cols: int
    rows, cols, _ = grid_positions.shape
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    pixels: np.ndarray = _to_pixels(grid_positions, width, height)

    for row in range(rows):
        strand: list[tuple[float, float]] = [
            (float(x), float(y)) for x, y in pixels[row, :]
        ]
        draw.line(strand, fill=color, width=2)
    for col in range(cols):
        strand = [(float(x), float(y)) for x, y in pixels[:, col]]
        draw.line(strand, fill=color, width=2)
    return img


def main() -> None:
    import matplotlib.pyplot as plt

    trail: np.ndarray = simulate_gravity_bounce()
    n_steps: int
    n_particles: int
    n_steps, n_particles, _ = trail.shape

    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = plt.get_cmap("plasma")
    for i in range(n_particles):
        xs: np.ndarray = trail[:, i, 0]
        ys: np.ndarray = trail[:, i, 1]
        ax.plot(
            xs, ys, color=cmap(i / max(n_particles - 1, 1)),
            alpha=0.7, linewidth=1.0,
        )
        ax.scatter(xs[-1], ys[-1], color=cmap(i / max(n_particles - 1, 1)))

    ax.axhline(0.0, color="black", linewidth=2.0)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect("equal")
    ax.set_title("Gravity, floor bounce, and inter-particle repulsion")
    fig.savefig("particle_gravity.png", dpi=150)

    rope_positions: np.ndarray = simulate_rope()
    render_rope(rope_positions).save("particle_rope.png")

    cloth_positions: np.ndarray = simulate_cloth()
    render_cloth(cloth_positions).save("particle_cloth.png")


if __name__ == "__main__":
    main()
