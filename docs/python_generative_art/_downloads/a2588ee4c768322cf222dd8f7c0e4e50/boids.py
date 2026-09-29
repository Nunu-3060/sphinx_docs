"""Craig Reynolds の Boids モデルによる群れシミュレーション。

分離 (separation)・整列 (alignment)・結合 (cohesion) という3つの単純な
ルールをすべての個体に同時適用するだけで、群れ全体としては魚群や
鳥群のように見える複雑な動きが創発する。

N体すべての組み合わせを Python の入れ子ループで処理すると N が
増えたときに極端に遅くなるため、この実装では各個体間の距離や
速度差を ``(N, N, 2)`` 配列にまとめてブロードキャストで一括計算する。
"""

import numpy as np


def _pairwise_delta(positions: np.ndarray) -> np.ndarray:
    """全個体間の位置の差 ``positions[i] - positions[j]`` を返す。

    shape ``(N, 2)`` から shape ``(N, N, 2)`` を作る。
    ``delta[i, j]`` は「個体jから見た個体iの相対位置」。
    """
    return positions[:, None, :] - positions[None, :, :]


def compute_accelerations(
    positions: np.ndarray,
    velocities: np.ndarray,
    perception_radius: float = 50.0,
    separation_radius: float = 15.0,
    separation_weight: float = 1.5,
    alignment_weight: float = 1.0,
    cohesion_weight: float = 1.0,
    max_force: float = 0.5,
) -> np.ndarray:
    """分離・整列・結合の3ルールを合成した加速度を、全個体分まとめて返す。

    ``positions`` ・``velocities`` はともに shape ``(N, 2)``。
    戻り値も同じ shape の加速度配列。
    """
    delta: np.ndarray = _pairwise_delta(positions)
    dist_sq: np.ndarray = np.sum(delta * delta, axis=-1)
    np.fill_diagonal(dist_sq, np.inf)
    dist: np.ndarray = np.sqrt(dist_sq)

    perceived: np.ndarray = dist < perception_radius
    perceived_count: np.ndarray = np.maximum(
        perceived.sum(axis=1, keepdims=True), 1
    )

    # 結合: 知覚範囲内にいる仲間の重心へ向かうベクトル
    neighbor_positions: np.ndarray = np.where(
        perceived[..., None], positions[None, :, :], 0.0
    )
    center_of_mass: np.ndarray = (
        neighbor_positions.sum(axis=1) / perceived_count
    )
    cohesion: np.ndarray = center_of_mass - positions

    # 整列: 知覚範囲内にいる仲間の平均速度に合わせようとするベクトル
    neighbor_velocities: np.ndarray = np.where(
        perceived[..., None], velocities[None, :, :], 0.0
    )
    average_velocity: np.ndarray = (
        neighbor_velocities.sum(axis=1) / perceived_count
    )
    alignment: np.ndarray = average_velocity - velocities

    # 分離: 近づきすぎた個体から離れる向きに、距離が近いほど強く働く
    close: np.ndarray = dist < separation_radius
    safe_dist: np.ndarray = np.where(close, dist, np.inf)
    push: np.ndarray = np.where(
        close[..., None], delta / safe_dist[..., None] ** 2, 0.0
    )
    separation: np.ndarray = push.sum(axis=1)

    acceleration: np.ndarray = (
        separation_weight * separation
        + alignment_weight * alignment
        + cohesion_weight * cohesion
    )
    magnitude: np.ndarray = np.linalg.norm(acceleration, axis=-1)
    scale: np.ndarray = np.minimum(1.0, max_force / np.maximum(
        magnitude, 1e-9
    ))
    return acceleration * scale[:, None]


def step(
    positions: np.ndarray,
    velocities: np.ndarray,
    bounds: tuple[float, float],
    dt: float = 1.0,
    max_speed: float = 4.0,
    **rule_kwargs: float,
) -> tuple[np.ndarray, np.ndarray]:
    """1ステップ分シミュレーションを進め、更新後の位置・速度を返す。

    空間はトーラス状（画面端でループする）とし、境界回避ルールを
    別途用意しなくても群れが画面内に留まり続けるようにしている。
    """
    width: float
    height: float
    width, height = bounds

    acceleration: np.ndarray = compute_accelerations(
        positions, velocities, **rule_kwargs
    )
    new_velocities: np.ndarray = velocities + acceleration * dt
    speed: np.ndarray = np.linalg.norm(new_velocities, axis=-1)
    speed_scale: np.ndarray = np.minimum(
        1.0, max_speed / np.maximum(speed, 1e-9)
    )
    new_velocities = new_velocities * speed_scale[:, None]

    new_positions: np.ndarray = positions + new_velocities * dt
    new_positions[:, 0] %= width
    new_positions[:, 1] %= height
    return new_positions, new_velocities


def simulate(
    n_boids: int = 60,
    n_steps: int = 150,
    bounds: tuple[float, float] = (150.0, 150.0),
    seed: int | None = 0,
) -> tuple[np.ndarray, np.ndarray]:
    """群れシミュレーションを実行し、全ステップの軌跡と最終速度を返す。

    戻り値は軌跡 ``(n_steps, n_boids, 2)`` と、最終ステップの速度
    ``(n_boids, 2)`` のタプル。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    width: float
    height: float
    width, height = bounds
    positions: np.ndarray = rng.uniform(
        [0.0, 0.0], [width, height], size=(n_boids, 2)
    )
    velocities: np.ndarray = rng.uniform(-1.0, 1.0, size=(n_boids, 2))

    trail: np.ndarray = np.empty((n_steps, n_boids, 2), dtype=float)
    for i in range(n_steps):
        positions, velocities = step(positions, velocities, bounds)
        trail[i] = positions

    return trail, velocities


def main() -> None:
    import matplotlib.pyplot as plt

    n_trail_steps: int = 40
    bounds: tuple[float, float] = (150.0, 150.0)
    trail: np.ndarray
    velocities: np.ndarray
    trail, velocities = simulate(bounds=bounds)
    positions: np.ndarray = trail[-1]

    fig, ax = plt.subplots(figsize=(6, 6))

    # 直近数ステップの軌跡を薄く描画する。画面端をまたぐ移動は
    # 線が横断してしまうため、差分が大きい区間は描かずに間引く。
    width: float
    height: float
    width, height = bounds
    recent: np.ndarray = trail[-n_trail_steps:]
    for i in range(recent.shape[1]):
        xs: np.ndarray = recent[:, i, 0]
        ys: np.ndarray = recent[:, i, 1]
        jumps: np.ndarray = np.abs(np.diff(xs)) > width / 2
        jumps |= np.abs(np.diff(ys)) > height / 2
        xs = np.where(jumps, np.nan, xs[:-1])
        ys = np.where(jumps, np.nan, ys[:-1])
        ax.plot(xs, ys, color="steelblue", alpha=0.3, linewidth=0.8)

    heading: np.ndarray = velocities / np.maximum(
        np.linalg.norm(velocities, axis=-1, keepdims=True), 1e-9
    )
    ax.quiver(
        positions[:, 0], positions[:, 1], heading[:, 0], heading[:, 1],
        color="darkslateblue", scale=25, width=0.006,
    )

    # 表示範囲は最終フレームの群れの位置を基準にする。トーラス境界を
    # ラップした軌跡の断片が視界に紛れ込んでも自動スケールが
    # 壊れないようにするため。
    margin: float = 25.0
    x_min: float = float(np.min(positions[:, 0])) - margin
    x_max: float = float(np.max(positions[:, 0])) + margin
    y_min: float = float(np.min(positions[:, 1])) - margin
    y_max: float = float(np.max(positions[:, 1])) + margin
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")
    ax.set_title("Boids: separation, alignment, and cohesion")
    fig.savefig("boids.png", dpi=150)


if __name__ == "__main__":
    main()
