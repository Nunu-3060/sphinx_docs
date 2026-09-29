"""Worley ノイズ(セルラーノイズ)の自前実装。

平面を正方形のマスに区切り、各マスに1つずつ「特徴点」をランダムに
置く。評価する点から、もっとも近い特徴点までの距離 F1 と、2番目に
近い特徴点までの距離 F2 をノイズの値として使う。F1 は細胞や泡の
ような模様に、F2 - F1 は特徴点の間の境界(ボロノイ図の境界)で 0 に
なるため、ひび割れや細胞膜のような網目模様になる。
"""

import numpy as np
from PIL import Image

from perlin_noise import fbm2d, make_permutation


def make_feature_points(
    cells: int, rng: np.random.Generator
) -> np.ndarray:
    """``cells`` x ``cells`` のマスそれぞれに置く特徴点の、マス内での位置。

    戻り値は形状 (cells, cells, 2) の配列で、値は 0.0-1.0。
    """
    return rng.random((cells, cells, 2))


def worley2d(
    x: np.ndarray, y: np.ndarray, features: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """座標 (x, y) (マス単位)における Worley ノイズの F1 と F2 を返す。

    評価点が属するマスと、その周囲 8 マスの計 9 個の特徴点までの
    距離を求め、小さいほうから2つを F1・F2 とする。特徴点の配列は
    端で折り返して参照するため、生成される模様は上下左右に継ぎ目なく
    つながる。
    """
    cells: int = features.shape[0]
    ix: np.ndarray = np.floor(x).astype(np.int64)
    iy: np.ndarray = np.floor(y).astype(np.int64)
    distances: list[np.ndarray] = []
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            cx: np.ndarray = ix + dx
            cy: np.ndarray = iy + dy
            offset: np.ndarray = features[cy % cells, cx % cells]
            fx: np.ndarray = cx + offset[..., 0]
            fy: np.ndarray = cy + offset[..., 1]
            distances.append(np.hypot(x - fx, y - fy))

    nearest: np.ndarray = np.sort(np.stack(distances), axis=0)
    return nearest[0], nearest[1]


def to_image(values: np.ndarray, invert: bool = False) -> Image.Image:
    """値の配列を 0-255 に正規化したグレースケール画像にする。"""
    low: float = float(values.min())
    high: float = float(values.max())
    normalized: np.ndarray = (values - low) / (high - low)
    if invert:
        normalized = 1.0 - normalized
    return Image.fromarray((normalized * 255).round().astype(np.uint8), "L")


def main() -> None:
    size: int = 400
    cells: int = 8
    rng: np.random.Generator = np.random.default_rng(seed=4)
    features: np.ndarray = make_feature_points(cells, rng)

    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(size, dtype=float), np.arange(size, dtype=float)
    )
    u: np.ndarray = xs * cells / size
    v: np.ndarray = ys * cells / size

    f1: np.ndarray
    f2: np.ndarray
    f1, f2 = worley2d(u, v, features)
    to_image(f1).save("worley_f1.png")
    to_image(f2 - f1).save("worley_edges.png")

    # 評価する座標をパーリンノイズの fBm でずらすと(ドメインワーピング)、
    # 直線的だった境界が波打ち、有機的な細胞の模様になる。
    perm: np.ndarray = make_permutation(seed=2)
    warp: float = 0.6
    wu: np.ndarray = u + warp * fbm2d(u * 0.5, v * 0.5, perm, octaves=4)
    wv: np.ndarray = v + warp * fbm2d(
        u * 0.5 + 5.2, v * 0.5 + 1.3, perm, octaves=4
    )
    f1, f2 = worley2d(wu, wv, features)
    to_image(f2 - f1).save("worley_warped.png")


if __name__ == "__main__":
    main()
