"""反復関数系（IFS）: 決定的な反復、カオスゲーム、バーンズリーのシダ.

IFS は、いくつかの縮小写像（ここではアフィン変換 x -> A x + t）の組である。
すべての写像を同時に適用する操作を繰り返すと、どんな図形から始めても、同じ 1 つの図形
（IFS のアトラクタ）に近づく。

使い方: python ch08_ifs.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Array = NDArray[np.float64]


class Affine:
    """平面のアフィン変換 x -> A x + t."""

    def __init__(self, a: float, b: float, c: float, d: float, e: float, f: float) -> None:
        """行列 A = [[a, b], [c, d]] と平行移動 t = (e, f) を指定する."""
        self.matrix = np.array([[a, b], [c, d]])
        self.shift = np.array([e, f])

    def __call__(self, points: Array) -> Array:
        """点の集まり points（形は (n, 2)）を変換する."""
        result: Array = points @ self.matrix.T + self.shift
        return result

    def contraction(self) -> float:
        """面積の縮小率 |det A| を返す."""
        return float(abs(np.linalg.det(self.matrix)))


# 3 つの頂点に向かって 1/2 に縮める写像（シェルピンスキーのギャスケット）
SIERPINSKI = [
    Affine(0.5, 0.0, 0.0, 0.5, 0.0, 0.0),
    Affine(0.5, 0.0, 0.0, 0.5, 0.5, 0.0),
    Affine(0.5, 0.0, 0.0, 0.5, 0.25, np.sqrt(3.0) / 4.0),
]

# バーンズリーのシダ（茎、本体の縮小複製、左の葉、右の葉）と、各写像を選ぶ確率
FERN = [
    Affine(0.0, 0.0, 0.0, 0.16, 0.0, 0.0),
    Affine(0.85, 0.04, -0.04, 0.85, 0.0, 1.6),
    Affine(0.2, -0.26, 0.23, 0.22, 0.0, 1.6),
    Affine(-0.15, 0.28, 0.26, 0.24, 0.0, 0.44),
]
FERN_WEIGHTS = [0.01, 0.85, 0.07, 0.07]


def deterministic_iteration(maps: list[Affine], points: Array, n: int) -> Array:
    """すべての写像を同時に適用し、結果を合わせる操作を n 回繰り返す（点の数は写像の数の n 乗倍になる）."""
    for _ in range(n):
        points = np.concatenate([f(points) for f in maps])
    return points


def chaos_game(maps: list[Affine], weights: list[float] | None, n: int, n_walkers: int = 1000,
               seed: int = 0) -> Array:
    """カオスゲーム: 毎回 1 つの写像を確率的に選んで適用し、訪れた点を記録する.

    1 個の点で n 回反復する代わりに、n_walkers 個の点を同時に動かして速く計算する。
    最初の 20 回は、アトラクタに近づくまでの過渡状態として捨てる。
    """
    rng = np.random.default_rng(seed)
    p = np.asarray(weights) if weights is not None else np.full(len(maps), 1.0 / len(maps))
    x = rng.random((n_walkers, 2))
    steps = n // n_walkers
    result = np.empty((steps, n_walkers, 2))
    for i in range(steps + 20):
        choice = rng.choice(len(maps), size=n_walkers, p=p)
        new = np.empty_like(x)
        for k, f in enumerate(maps):
            mask = choice == k
            new[mask] = f(x[mask])
        x = new
        if i >= 20:
            result[i - 20] = x
    return result.reshape(-1, 2)


def weights_by_area(maps: list[Affine]) -> list[float]:
    """各写像を選ぶ確率を、面積の縮小率 |det A| に比例させる（0 の場合は小さな値にする）."""
    dets = np.array([max(f.contraction(), 0.01) for f in maps])
    return list(dets / dets.sum())


def create_figures() -> dict[str, Figure]:
    """決定的な反復（deterministic）、カオスゲーム（chaos_game）、確率の違い（weights）の図を作る."""
    t = np.linspace(0.0, 1.0, 60)
    square = np.concatenate([np.column_stack([t, 0 * t]), np.column_stack([1 + 0 * t, t]),
                             np.column_stack([1 - t, 1 + 0 * t]), np.column_stack([0 * t, 1 - t])])
    face = np.column_stack([0.5 + 0.3 * np.cos(2 * np.pi * t), 0.5 + 0.3 * np.sin(2 * np.pi * t)])
    start = np.concatenate([square, face])
    fig1, axes1 = plt.subplots(1, 5, figsize=(14.0, 3.0))
    for ax, n in zip(axes1, (0, 1, 2, 3, 7)):
        pts = deterministic_iteration(SIERPINSKI, start, n)
        ax.plot(pts[:, 0], pts[:, 1], ",", color="k")
        ax.set_title(f"{n} 回")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_aspect("equal")
        ax.axis("off")
    fig1.tight_layout()

    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 5.6))
    pts = chaos_game(SIERPINSKI, None, 200000)
    ax1.plot(pts[:, 0], pts[:, 1], ",", color="k", alpha=0.5)
    ax1.set_title("シェルピンスキーのギャスケット")
    pts = chaos_game(FERN, FERN_WEIGHTS, 400000)
    ax2.plot(pts[:, 0], pts[:, 1], ",", color="#2e7d32", alpha=0.5)
    ax2.set_title("バーンズリーのシダ")
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.axis("off")
    fig2.tight_layout()

    fig3, axes3 = plt.subplots(1, 3, figsize=(11.0, 5.0))
    cases = [("指定の確率", FERN_WEIGHTS), ("面積比の確率", weights_by_area(FERN)), ("等しい確率", None)]
    for ax, (title, weights) in zip(axes3, cases):
        pts = chaos_game(FERN, weights, 100000)
        ax.plot(pts[:, 0], pts[:, 1], ",", color="#2e7d32", alpha=0.6)
        label = "" if weights is None else "\n(" + ", ".join(f"{w:.2f}" for w in weights) + ")"
        ax.set_title(title + label, fontsize=10)
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(0.0, 10.0)
        ax.set_aspect("equal")
        ax.axis("off")
    fig3.tight_layout()
    return {"deterministic": fig1, "chaos_game": fig2, "weights": fig3}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
