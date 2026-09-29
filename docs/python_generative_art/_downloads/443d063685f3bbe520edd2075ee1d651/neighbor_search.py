"""格子による空間分割を使った、固定半径の近傍探索。

多数の点の中から「距離が半径 r 以内にある点の組」を全て求める処理は、
Boids の知覚範囲、粒子どうしの衝突、近い点どうしを線で結ぶ表現など、
ジェネラティブアートの多くの場面で必要になる。全ての組を調べる
総当たりでは、点の数 N に対して計算量が O(N^2) になる。平面を1辺 r の
マスに区切り、各点を自分のマスに登録しておけば、距離 r 以内の点は
自分のマスと隣接する8マスの中にしか存在しないため、調べる範囲を
点の周りに限定できる。
"""

import time

import numpy as np
from PIL import Image, ImageDraw

from perlin_noise import fbm2d, make_permutation


def brute_force_pairs(points: np.ndarray, radius: float) -> np.ndarray:
    """全ての点の組の距離を調べ、半径 ``radius`` 未満の組を返す。

    戻り値は形状 (M, 2) の整数配列で、各行は ``i < j`` を満たす点の
    番号の組。点の数を N とすると、N x N の距離の表を作るため、
    計算量もメモリも O(N^2) になる。
    """
    delta: np.ndarray = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    dist_sq: np.ndarray = (delta * delta).sum(axis=-1)
    i: np.ndarray
    j: np.ndarray
    i, j = np.nonzero(np.triu(dist_sq < radius * radius, k=1))
    return np.stack([i, j], axis=1)


def build_grid(
    points: np.ndarray, cell_size: float
) -> dict[tuple[int, int], np.ndarray]:
    """各点を1辺 ``cell_size`` のマスに登録し、マスごとの点の番号を返す。

    点をマスの番号で並べ替えてから、マスの番号が変わる位置で区切る
    ことで、Python のループを使わずに振り分けている。
    """
    cells: np.ndarray = np.floor(points / cell_size).astype(np.int64)
    order: np.ndarray = np.lexsort((cells[:, 1], cells[:, 0]))
    sorted_cells: np.ndarray = cells[order]
    changes: np.ndarray = (
        np.flatnonzero((np.diff(sorted_cells, axis=0) != 0).any(axis=1)) + 1
    )
    grid: dict[tuple[int, int], np.ndarray] = {}
    for members in np.split(order, changes):
        cx, cy = cells[members[0]]
        grid[(int(cx), int(cy))] = members
    return grid


# 自分のマスと、右・左下・下・右下のマス。残りの4方向(左・上など)の
# 組は、相手のマスから見たときにこの4方向のどれかとして数えられる
# ため、ここに含めると同じ組を2回数えてしまう。
_FORWARD_OFFSETS: list[tuple[int, int]] = [
    (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]


def grid_pairs(points: np.ndarray, radius: float) -> np.ndarray:
    """格子を使って、半径 ``radius`` 未満の点の組を返す。

    マスの1辺を ``radius`` にすると、距離が ``radius`` 未満の2点は、
    同じマスか、隣接する8マスのどれかに入っている。そこで、マスごとに
    自分のマスと隣接するマスの点だけを総当たりで調べる。戻り値の形式は
    ``brute_force_pairs`` と同じ(各行 ``i < j``、行の並び順は異なる)。
    """
    grid: dict[tuple[int, int], np.ndarray] = build_grid(points, radius)
    found: list[np.ndarray] = []
    for (cx, cy), members in grid.items():
        for dx, dy in _FORWARD_OFFSETS:
            others: np.ndarray | None = grid.get((cx + dx, cy + dy))
            if others is None:
                continue
            delta: np.ndarray = (
                points[members, np.newaxis, :] - points[np.newaxis, others, :]
            )
            close: np.ndarray = (delta * delta).sum(axis=-1) < radius**2
            if dx == 0 and dy == 0:
                close = np.triu(close, k=1)  # 同じマスの中は i < j の組だけ
            a: np.ndarray
            b: np.ndarray
            a, b = np.nonzero(close)
            found.append(np.stack([members[a], others[b]], axis=1))

    if not found:
        return np.empty((0, 2), dtype=np.int64)
    pairs: np.ndarray = np.concatenate(found)
    return np.sort(pairs, axis=1)  # 各行を (小さい番号, 大きい番号) にそろえる


def noise_weighted_points(
    count: int, size: int, rng: np.random.Generator
) -> np.ndarray:
    """パーリンノイズの値が大きい場所ほど密になるように点を散らす。

    一様乱数で候補点を作り、その場所のノイズの値に応じた確率で採用する
    (棄却法)。
    """
    perm: np.ndarray = make_permutation(seed=6)
    accepted: list[np.ndarray] = []
    total: int = 0
    while total < count:
        candidates: np.ndarray = rng.uniform(0.0, size, size=(count, 2))
        value: np.ndarray = fbm2d(
            candidates[:, 0] * 0.006, candidates[:, 1] * 0.006, perm, octaves=3
        )
        probability: np.ndarray = np.clip(0.5 + value, 0.0, 1.0) ** 3
        keep: np.ndarray = candidates[rng.random(count) < probability]
        accepted.append(keep)
        total += len(keep)
    return np.concatenate(accepted)[:count]


def render_links(
    points: np.ndarray,
    pairs: np.ndarray,
    radius: float,
    size: int,
    background: tuple[int, int, int] = (14, 18, 32),
    color: tuple[int, int, int] = (240, 200, 120),
) -> Image.Image:
    """近い点どうしを線で結ぶ。距離が近い組ほど線を濃く描く。"""
    image: Image.Image = Image.new("RGB", (size, size), background)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    lengths: np.ndarray = np.linalg.norm(
        points[pairs[:, 0]] - points[pairs[:, 1]], axis=1
    )
    back: np.ndarray = np.array(background, dtype=float)
    front: np.ndarray = np.array(color, dtype=float)
    # 薄い線から先に描き、濃い線が上に重なるようにする。
    for k in np.argsort(-lengths):
        strength: float = (1.0 - lengths[k] / radius) ** 1.5
        rgb: np.ndarray = back + (front - back) * strength
        line_color: tuple[int, int, int] = (
            int(rgb[0]), int(rgb[1]), int(rgb[2])
        )
        i, j = pairs[k]
        draw.line(
            [tuple(points[i]), tuple(points[j])], fill=line_color, width=1
        )
    return image


def measure(points: np.ndarray, radius: float) -> None:
    """総当たりと格子の処理時間を比べ、結果が一致することを確かめる。"""
    start: float = time.perf_counter()
    by_grid: np.ndarray = grid_pairs(points, radius)
    grid_time: float = time.perf_counter() - start
    message: str = f"N={len(points)}: grid {grid_time:.3f}s"
    if len(points) <= 4000:
        start = time.perf_counter()
        by_brute: np.ndarray = brute_force_pairs(points, radius)
        brute_time: float = time.perf_counter() - start
        same: bool = {tuple(p) for p in by_grid.tolist()} == {
            tuple(p) for p in by_brute.tolist()
        }
        message += f", brute force {brute_time:.3f}s, same result: {same}"
    print(message)


def main() -> None:
    size: int = 800
    radius: float = 16.0
    rng: np.random.Generator = np.random.default_rng(seed=0)

    for count in (1000, 2000, 4000, 16000):
        measure(rng.uniform(0.0, size, size=(count, 2)), radius)

    points: np.ndarray = noise_weighted_points(12000, size, rng)
    pairs: np.ndarray = grid_pairs(points, radius)
    render_links(points, pairs, radius, size).save("neighbor_links.png")


if __name__ == "__main__":
    main()
