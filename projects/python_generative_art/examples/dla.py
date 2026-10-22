"""拡散律速凝集（DLA: Diffusion-Limited Aggregation）。

格子の中央に「種」を 1 つ置き、遠くから放った粒子をランダムウォーク
させる。粒子が凝集体（すでに付着した粒子の集まり）の隣に来たら、
その場で付着して凝集体の一部になる。これを繰り返すと、珊瑚や雷、
霜の結晶のような枝分かれした構造が育つ。

粒子を 1 個ずつ歩かせると時間がかかるため、多数の粒子を同時に歩かせ、
位置の更新と付着の判定を NumPy の配列演算でまとめて行う。
"""

import numpy as np
from PIL import Image
from matplotlib import colormaps

# 上下左右の 4 方向の移動量。
_STEPS: np.ndarray = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])


def touches_cluster(occupied: np.ndarray, positions: np.ndarray) -> np.ndarray:
    """各粒子の上下左右のどれかに、凝集体の粒子があるかを返す。"""
    x: np.ndarray = positions[:, 0]
    y: np.ndarray = positions[:, 1]
    result: np.ndarray = (
        occupied[y, x + 1] | occupied[y, x - 1] | occupied[y + 1, x] | occupied[y - 1, x]
    )
    return result


def spawn(rng: np.random.Generator, count: int, center: int, radius: float) -> np.ndarray:
    """中心から距離 ``radius`` の円周上に、粒子を ``count`` 個置く。"""
    angles: np.ndarray = rng.uniform(0, 2 * np.pi, count)
    xs: np.ndarray = np.round(center + radius * np.cos(angles))
    ys: np.ndarray = np.round(center + radius * np.sin(angles))
    result: np.ndarray = np.stack([xs, ys], axis=1).astype(np.int64)
    return result


def grow_dla(
    size: int = 400,
    num_particles: int = 12000,
    walker_density: float = 0.3,
    seed: int = 0,
) -> np.ndarray:
    """DLA の凝集体を育て、各格子点に粒子が付着した順番を返す。

    戻り値は形状 ``(size, size)`` の整数配列で、付着していない格子点は
    -1、種は 0、以降は付着した順に 1, 2, ... となる。

    粒子は、凝集体の外接円（中心から最も遠い粒子までの距離）より
    少し外側の円周上から放つ。外接円から大きく離れた粒子は、戻って
    くるまでに時間がかかるため、放ち直す。

    同時に歩かせる粒子が多すぎると、粒子が凝集体の奥まで入り込む前に
    入り口付近で次々に付着し、枝の間の隙間が埋まってしまう。そこで、
    歩かせる粒子の数を、放つ円周の長さ 1 ピクセルあたり
    ``walker_density`` 個に抑え、凝集体が育つにつれて増やしていく。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    center: int = size // 2
    occupied: np.ndarray = np.zeros((size, size), dtype=bool)
    order: np.ndarray = np.full((size, size), -1, dtype=np.int64)
    occupied[center, center] = True
    order[center, center] = 0

    cluster_radius: float = 1.0
    attached: int = 0
    walkers: np.ndarray = np.empty((0, 2), dtype=np.int64)

    while attached < num_particles:
        # 放つ円周の長さに応じて、歩かせる粒子を補充する。
        wanted: int = int(walker_density * 2 * np.pi * (cluster_radius + 5))
        if len(walkers) < wanted:
            walkers = np.concatenate(
                [walkers, spawn(rng, wanted - len(walkers), center, cluster_radius + 5)]
            )

        # 全ての粒子を、上下左右のどれかに 1 歩動かす。
        walkers = walkers + _STEPS[rng.integers(0, 4, len(walkers))]

        # 外接円から離れすぎた粒子と、格子の端に近づいた粒子は放ち直す。
        # 同じ回に隣の格子点へ別の粒子が付着したために、凝集体の上へ
        # 踏み込んでしまった粒子も放ち直す。
        distance: np.ndarray = np.hypot(walkers[:, 0] - center, walkers[:, 1] - center)
        lost: np.ndarray = (distance > cluster_radius + 20) | (walkers.min(axis=1) < 1) | (
            walkers.max(axis=1) > size - 2
        )
        lost[~lost] = occupied[walkers[~lost, 1], walkers[~lost, 0]]
        walkers[lost] = spawn(rng, int(lost.sum()), center, cluster_radius + 5)

        # 凝集体に接した粒子を付着させる。同じ格子点に複数の粒子が
        # 同時に付着しようとした場合は、1 つだけを残す。
        stick: np.ndarray = touches_cluster(occupied, walkers)
        if stick.any():
            new_points: np.ndarray = np.unique(walkers[stick], axis=0)
            new_points = new_points[: num_particles - attached]
            occupied[new_points[:, 1], new_points[:, 0]] = True
            order[new_points[:, 1], new_points[:, 0]] = np.arange(
                attached + 1, attached + 1 + len(new_points)
            )
            attached += len(new_points)
            far: float = float(
                np.hypot(new_points[:, 0] - center, new_points[:, 1] - center).max()
            )
            cluster_radius = max(cluster_radius, far)
            if cluster_radius + 25 > center:
                break  # 凝集体が格子の端に近づいたら終える
            # 付着した粒子は、新しい粒子として放ち直す。
            walkers[stick] = spawn(rng, int(stick.sum()), center, cluster_radius + 5)

    return order


def render_dla(order: np.ndarray) -> Image.Image:
    """付着した順番に応じて色を付けた凝集体の画像を返す。

    種に近い（早く付着した）粒子ほど明るく、外側の粒子ほど暗い色にする。
    """
    attached: np.ndarray = order >= 0
    t: np.ndarray = np.zeros(order.shape)
    t[attached] = order[attached] / order.max()
    rgb: np.ndarray = colormaps["magma"](1.0 - 0.85 * t)[..., :3]
    rgb[~attached] = (0.05, 0.04, 0.08)
    image: Image.Image = Image.fromarray((rgb * 255).astype(np.uint8))
    # 1 格子点を 2 × 2 画素に拡大して、枝を見やすくする。
    return image.resize((order.shape[1] * 2, order.shape[0] * 2), Image.Resampling.NEAREST)


def main() -> None:
    order: np.ndarray = grow_dla()
    print(f"attached particles: {int(order.max())}")
    render_dla(order).save("dla.png")


if __name__ == "__main__":
    main()
