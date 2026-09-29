"""反復関数系 (IFS: Iterated Function System) とカオスゲーム。

複数のアフィン変換の集合を用意し、1つの点に対して毎回ランダムに
選んだ変換を繰り返し適用していくと、点は「アトラクター」と呼ばれる
一定のフラクタル図形の上に収束していく。この手続きは **カオスゲーム**
と呼ばれる。1本の軌跡は直前の点に依存する逐次処理だが、多数の軌跡を
独立に同時進行させることで、ステップごとの更新をNumPyでベクトル化
できる。
"""

import numpy as np
from PIL import Image


def chaos_game(
    coeffs: np.ndarray,
    weights: np.ndarray,
    num_points: int,
    num_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """カオスゲームにより num_points 本の軌跡を num_steps ステップ進める。

    ``coeffs`` は形状 ``(変換数, 6)`` の配列で、各行が
    ``(a, b, c, d, e, f)`` というアフィン変換
    ``(x, y) -> (a*x + b*y + e, c*x + d*y + f)`` を表す。``weights``
    は各変換を選ぶ確率。戻り値は形状 ``(num_steps, num_points, 2)``。
    """
    points: np.ndarray = np.zeros((num_points, 2), dtype=float)
    trail: np.ndarray = np.empty((num_steps, num_points, 2), dtype=float)
    num_transforms: int = len(weights)

    for step in range(num_steps):
        choice: np.ndarray = rng.choice(
            num_transforms, size=num_points, p=weights
        )
        selected: np.ndarray = coeffs[choice]
        x: np.ndarray = points[:, 0]
        y: np.ndarray = points[:, 1]
        new_x: np.ndarray = selected[:, 0] * x + selected[:, 1] * y
        new_x += selected[:, 4]
        new_y: np.ndarray = selected[:, 2] * x + selected[:, 3] * y
        new_y += selected[:, 5]
        points = np.stack([new_x, new_y], axis=-1)
        trail[step] = points

    return trail


def render_density(
    trail: np.ndarray,
    height: int,
    color: tuple[int, int, int] = (40, 120, 40),
    warmup: int = 5,
    margin: float = 0.05,
) -> Image.Image:
    """IFSの軌跡を2次元ヒストグラムとして描画し、対数スケールで濃淡をつける。

    描画範囲は点群の実際の分布から自動的に決め、画像の縦横比もその
    範囲に合わせて決定する(``height`` だけを指定すればよい)。最初の
    ``warmup`` ステップは、原点付近から離れて実際のアトラクターに
    乗るまでの過渡的な部分なので描画から除く。
    """
    points: np.ndarray = trail[warmup:].reshape(-1, 2)
    x_min: float = float(points[:, 0].min())
    x_max: float = float(points[:, 0].max())
    y_min: float = float(points[:, 1].min())
    y_max: float = float(points[:, 1].max())
    x_span: float = x_max - x_min
    y_span: float = y_max - y_min
    x_pad: float = x_span * margin
    y_pad: float = y_span * margin
    x_range: tuple[float, float] = (x_min - x_pad, x_max + x_pad)
    y_range: tuple[float, float] = (y_min - y_pad, y_max + y_pad)

    width: int = max(
        1, round(height * (x_span + 2 * x_pad) / (y_span + 2 * y_pad))
    )

    hist: np.ndarray
    hist, _, _ = np.histogram2d(
        points[:, 1],
        points[:, 0],
        bins=[height, width],
        range=[list(y_range), list(x_range)],
    )
    hist = np.flipud(hist)
    density: np.ndarray = np.log1p(hist)
    max_density: float = float(density.max())
    normalized: np.ndarray = (
        density / max_density if max_density > 0 else density
    )

    background: np.ndarray = np.full((height, width, 3), 255.0)
    fg: np.ndarray = np.array(color, dtype=float)
    pixels: np.ndarray = (
        background + (fg - background) * normalized[..., np.newaxis]
    )
    return Image.fromarray(pixels.round().astype(np.uint8))


def barnsley_fern_ifs() -> tuple[np.ndarray, np.ndarray]:
    """バーンズリーのシダを描く4つのアフィン変換と、その選択確率。"""
    coeffs: np.ndarray = np.array(
        [
            [0.00, 0.00, 0.00, 0.16, 0.00, 0.00],
            [0.85, 0.04, -0.04, 0.85, 0.00, 1.60],
            [0.20, -0.26, 0.23, 0.22, 0.00, 1.60],
            [-0.15, 0.28, 0.26, 0.24, 0.00, 0.44],
        ]
    )
    weights: np.ndarray = np.array([0.01, 0.85, 0.07, 0.07])
    return coeffs, weights


def sierpinski_triangle_ifs() -> tuple[np.ndarray, np.ndarray]:
    """正三角形の3頂点それぞれへ向けて縮小する3つのアフィン変換。

    どの変換も「現在の点と頂点の中点に移動する」という
    ``p -> (p + v_i) / 2`` の形をしており、これを繰り返すだけで
    シェルピンスキーの三角形が現れる。
    """
    vertices: np.ndarray = np.array(
        [[0.0, 0.0], [1.0, 0.0], [0.5, 0.8660254]]
    )
    coeffs: np.ndarray = np.array(
        [
            [0.5, 0.0, 0.0, 0.5, 0.5 * vx, 0.5 * vy]
            for vx, vy in vertices
        ]
    )
    weights: np.ndarray = np.full(3, 1.0 / 3.0)
    return coeffs, weights


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=0)

    fern_coeffs: np.ndarray
    fern_weights: np.ndarray
    fern_coeffs, fern_weights = barnsley_fern_ifs()
    fern_trail: np.ndarray = chaos_game(
        fern_coeffs, fern_weights, num_points=4000, num_steps=60, rng=rng
    )
    render_density(fern_trail, height=500, color=(40, 130, 60)).save(
        "ifs_fern.png"
    )

    tri_coeffs: np.ndarray
    tri_weights: np.ndarray
    tri_coeffs, tri_weights = sierpinski_triangle_ifs()
    tri_trail: np.ndarray = chaos_game(
        tri_coeffs, tri_weights, num_points=4000, num_steps=40, rng=rng
    )
    render_density(tri_trail, height=440, color=(60, 80, 160)).save(
        "ifs_sierpinski.png"
    )


if __name__ == "__main__":
    main()
