"""磁気振り子: 3 つの磁石のどれに引き寄せられて止まるかで、初期位置を色分けする.

振り子のおもりの水平面内の位置 (x, y) が、次の 3 つの力を受けて動くとする。

* 中心に戻そうとするばねの力 -k (x, y)
* 速度に比例する摩擦力 -γ (x', y')
* 3 つの磁石からの引力（磁石は高さ h だけ下にあり、距離の 2 乗に反比例する）

摩擦があるので、おもりはいずれかの磁石の近くで止まる。初期位置（初速度は 0）ごとに、
止まった磁石で色を付けた図が吸引領域（ベイスン）の図である。

使い方: python ch10_magnetic_pendulum.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import ode
import plot_util
from ode import Vector

K = 0.5
GAMMA = 0.2
H = 0.3
MAGNETS = np.array([[np.cos(a), np.sin(a)] for a in np.pi / 2.0 + 2.0 * np.pi * np.arange(3) / 3.0])


def pendulum(state: Vector) -> Vector:
    """状態 (x, y, vx, vy) の時間微分を返す."""
    x, y, vx, vy = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    ax = -K * x - GAMMA * vx
    ay = -K * y - GAMMA * vy
    for mx, my in MAGNETS:
        dx, dy = mx - x, my - y
        r2 = dx * dx + dy * dy + H * H
        inv_r3 = 1.0 / (r2 * np.sqrt(r2))  # 1 / r^3（** 1.5 より速い）
        ax = ax + dx * inv_r3
        ay = ay + dy * inv_r3
    return np.stack([vx, vy, ax, ay], axis=-1)


def basins(x: NDArray[np.float64], y: NDArray[np.float64], dt: float = 0.05,
           max_steps: int = 1500) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """初期位置の格子 (x, y) ごとに、止まった磁石の番号と止まるまでのステップ数を返す.

    25 ステップごとに、磁石の近くで遅くなった点を「止まった」と判定し、計算の対象から
    外して速くする（そこまで遅くなると、摩擦のため、もう別の磁石には移れない）。最後まで止まらなかった点の番号は -1 にする。
    """
    state = np.stack([x.ravel(), y.ravel(), np.zeros(x.size), np.zeros(x.size)], axis=-1)
    which = np.full(x.size, -1, dtype=np.int64)
    steps = np.full(x.size, max_steps, dtype=np.int64)
    active = np.arange(x.size)
    for n in range(0, max_steps, 25):
        for _ in range(25):
            state = ode.rk4_step(pendulum, state, dt)
        dist = np.linalg.norm(state[:, None, :2] - MAGNETS[None, :, :], axis=-1)
        nearest = np.argmin(dist, axis=1)
        speed = np.linalg.norm(state[:, 2:], axis=1)
        settled = (dist[np.arange(len(state)), nearest] < 0.3) & (speed < 0.2)
        which[active[settled]] = nearest[settled]
        steps[active[settled]] = n + 25
        state = state[~settled]
        active = active[~settled]
        if active.size == 0:
            break
    return which.reshape(x.shape), steps.reshape(x.shape)


def basin_image(which: NDArray[np.int64], steps: NDArray[np.int64]) -> NDArray[np.float64]:
    """磁石ごとに色相を変え、止まるまでに時間がかかった点ほど暗くした RGB 画像を作る."""
    hue = np.where(which >= 0, which / 3.0, 0.0)
    value = np.where(which >= 0, 1.0 - 0.75 * (steps - steps.min()) / (steps.max() - steps.min() + 1), 0.0)
    image: NDArray[np.float64] = hsv_to_rgb(np.stack([hue, np.full(hue.shape, 0.6), value], axis=-1))
    return image


def create_figures() -> dict[str, Figure]:
    """吸引領域の全体と、境界付近の拡大を描く（basins）."""
    views = [(0.0, 0.0, 4.0, "全体"), (-1.05, 0.95, 0.5, "白枠の拡大")]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4))
    for ax, (cx, cy, width, title) in zip(axes, views):
        t = np.linspace(-width / 2, width / 2, 200)
        x, y = np.meshgrid(cx + t, cy - t)
        which, steps = basins(x, y)
        extent = (cx - width / 2, cx + width / 2, cy - width / 2, cy + width / 2)
        ax.imshow(basin_image(which, steps), extent=extent)
        ax.plot(MAGNETS[:, 0], MAGNETS[:, 1], "o", color="w", markeredgecolor="k", markersize=7)
        ax.set_xlim(extent[0], extent[1])
        ax.set_ylim(extent[2], extent[3])
        ax.set_title(title)
        ax.set_xlabel("初期位置 $x$")
        ax.set_ylabel("初期位置 $y$")
    cx, cy, width, _ = views[1]
    axes[0].add_patch(Rectangle((cx - width / 2, cy - width / 2), width, width, fill=False,
                                edgecolor="w", linewidth=1.5))
    fig.tight_layout()
    return {"basins": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
