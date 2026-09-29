"""ベジェ曲線と Catmull-Rom スプライン。

式で形が決まる曲線(リサージュ曲線やバラ曲線など)とは違い、ベジェ曲線は
「制御点」を並べることで形を直接指定する曲線である。制御点の間の線形補間を
繰り返す de Casteljau のアルゴリズムで、曲線上の点を求められる。

ベジェ曲線は端点以外の制御点を通らないため、「与えた点を全て通る
なめらかな曲線」が欲しい場合は、Catmull-Rom スプラインを使う。
Catmull-Rom スプラインの各区間は3次ベジェ曲線に変換できるため、
同じ de Casteljau のアルゴリズムで描ける。
"""

import math

import numpy as np
from PIL import Image, ImageDraw


def de_casteljau(control_points: np.ndarray, t: np.ndarray) -> np.ndarray:
    """制御点 ``control_points`` (形状 ``(n + 1, 2)``) で決まる n 次の
    ベジェ曲線上の点を、パラメータ ``t`` (形状 ``(m,)``) ごとに求める。

    隣り合う制御点を ``t`` の割合で線形補間すると、点が1つ少ない列が
    できる。これを点が1つになるまで繰り返す。全ての ``t`` をまとめて
    計算するため、途中の点列は形状 ``(点の数, m, 2)`` の配列で持つ。
    戻り値の形状は ``(m, 2)``。
    """
    weights: np.ndarray = t[np.newaxis, :, np.newaxis]
    points: np.ndarray = np.repeat(
        control_points[:, np.newaxis, :], len(t), axis=1
    )
    while len(points) > 1:
        points = (1.0 - weights) * points[:-1] + weights * points[1:]
    return points[0]


def de_casteljau_levels(
    control_points: np.ndarray, t: float
) -> list[np.ndarray]:
    """1つの ``t`` について、de Casteljau のアルゴリズムの途中経過を返す。

    戻り値の先頭は制御点そのもので、以降は線形補間のたびに点が1つずつ
    減っていき、最後の要素が曲線上の1点になる。作図の説明用。
    """
    levels: list[np.ndarray] = [control_points]
    while len(levels[-1]) > 1:
        points: np.ndarray = levels[-1]
        levels.append((1.0 - t) * points[:-1] + t * points[1:])
    return levels


def catmull_rom_to_bezier(points: np.ndarray, closed: bool) -> np.ndarray:
    """点列 ``points`` (形状 ``(n, 2)``) を全て通る Catmull-Rom スプラインを、
    3次ベジェ曲線の区間の列 (形状 ``(区間数, 4, 2)``) に変換する。

    点 ``p1`` から ``p2`` への区間では、``p1`` での接線を前後の点の差
    ``(p2 - p0) / 2`` とする。3次ベジェ曲線の端点での接線は
    ``3 * (制御点 - 端点)`` なので、内側の制御点は
    ``p1 + (p2 - p0) / 6`` と ``p2 - (p3 - p1) / 6`` になる。
    ``closed`` が真なら最後の点と最初の点も結んだ閉曲線にする。
    開曲線の場合は、両端の点を複製して前後の点の代わりにする。
    """
    if closed:
        p0: np.ndarray = np.roll(points, 1, axis=0)
        p1: np.ndarray = points
        p2: np.ndarray = np.roll(points, -1, axis=0)
        p3: np.ndarray = np.roll(points, -2, axis=0)
    else:
        padded: np.ndarray = np.concatenate(
            [points[:1], points, points[-1:]], axis=0
        )
        p0 = padded[:-3]
        p1 = padded[1:-2]
        p2 = padded[2:-1]
        p3 = padded[3:]

    c1: np.ndarray = p1 + (p2 - p0) / 6.0
    c2: np.ndarray = p2 - (p3 - p1) / 6.0
    return np.stack([p1, c1, c2, p2], axis=1)


def sample_bezier_segments(
    segments: np.ndarray, samples_per_segment: int
) -> np.ndarray:
    """3次ベジェ曲線の区間の列を、1本の折れ線の点列に変換する。

    隣り合う区間は端点を共有するため、2番目以降の区間では先頭の点を
    除いて重複をなくす。
    """
    t: np.ndarray = np.linspace(0.0, 1.0, samples_per_segment)
    curves: list[np.ndarray] = [de_casteljau(segments[0], t)]
    for segment in segments[1:]:
        curves.append(de_casteljau(segment, t)[1:])
    return np.concatenate(curves, axis=0)


def _to_tuples(points: np.ndarray) -> list[tuple[float, float]]:
    """NumPy の点列を、ImageDraw に渡せるタプルのリストに変換する。"""
    return [(float(x), float(y)) for x, y in points]


def _draw_dot(
    draw: ImageDraw.ImageDraw,
    point: np.ndarray,
    radius: float,
    fill: tuple[int, int, int],
) -> None:
    """``point`` を中心とする半径 ``radius`` の円を塗りつぶして描く。"""
    x: float = float(point[0])
    y: float = float(point[1])
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)


def render_construction(
    control_points: np.ndarray, t: float, size: int = 480
) -> Image.Image:
    """3次ベジェ曲線と、ある ``t`` における de Casteljau の作図を描く。

    灰色の折れ線が制御点を結んだ多角形(制御多角形)、色付きの線分が
    線形補間を繰り返す途中経過、赤い点が曲線上の点である。
    """
    image: Image.Image = Image.new("RGB", (size, size), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)

    curve: np.ndarray = de_casteljau(
        control_points, np.linspace(0.0, 1.0, 200)
    )
    draw.line(_to_tuples(curve), fill=(40, 70, 160), width=3, joint="curve")

    level_colors: list[tuple[int, int, int]] = [
        (170, 170, 170),
        (90, 170, 120),
        (230, 150, 50),
    ]
    levels: list[np.ndarray] = de_casteljau_levels(control_points, t)
    for points, color in zip(levels[:-1], level_colors):
        draw.line(_to_tuples(points), fill=color, width=2)
        for point in points:
            _draw_dot(draw, point, 5.0, color)

    _draw_dot(draw, levels[-1][0], 7.0, (210, 50, 50))
    return image


def random_blob_points(
    rng: np.random.Generator,
    num_points: int,
    center: tuple[float, float],
    radius: float,
    jitter: float,
) -> np.ndarray:
    """円周上に等間隔で置いた点の半径を、ランダムに伸び縮みさせた点列。

    ``jitter`` は半径を変化させる割合で、0なら正多角形の頂点になる。
    """
    angles: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi, num_points, endpoint=False
    )
    radii: np.ndarray = radius * (
        1.0 + rng.uniform(-jitter, jitter, num_points)
    )
    xs: np.ndarray = center[0] + radii * np.cos(angles)
    ys: np.ndarray = center[1] + radii * np.sin(angles)
    return np.stack([xs, ys], axis=-1)


def render_blob(
    points: np.ndarray, smooth: bool, size: int = 400
) -> Image.Image:
    """閉じた点列を塗りつぶして描く。

    ``smooth`` が偽なら点を直線で結んだ多角形、真なら全ての点を通る
    Catmull-Rom スプラインで結んだ曲線にする。元の点も重ねて描く。
    """
    image: Image.Image = Image.new("RGB", (size, size), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)

    outline: np.ndarray = points
    if smooth:
        segments: np.ndarray = catmull_rom_to_bezier(points, closed=True)
        outline = sample_bezier_segments(segments, samples_per_segment=24)

    draw.polygon(
        _to_tuples(outline), fill=(250, 200, 150), outline=(200, 90, 60)
    )
    for point in points:
        _draw_dot(draw, point, 5.0, (60, 60, 60))
    return image


def render_strands(
    rng: np.random.Generator,
    num_strands: int = 120,
    width: int = 600,
    height: int = 480,
) -> Image.Image:
    """下端から上端へ伸びる多数の3次ベジェ曲線を重ね、髪や草のような
    流れる線の束を描く。

    内側の2つの制御点の横方向のずれを、曲線の番号に対する正弦波で
    決めるため、隣り合う曲線は似た形になり、全体として波打つ流れになる。
    そこに小さな乱数を加えて、1本ずつの揺らぎを出している。
    """
    image: Image.Image = Image.new("RGBA", (width, height), (20, 24, 40, 255))
    layer: Image.Image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(layer)
    t: np.ndarray = np.linspace(0.0, 1.0, 100)

    for index in range(num_strands):
        u: float = index / (num_strands - 1)
        x: float = width * (0.1 + 0.8 * u)
        sway1: float = 90.0 * math.sin(2.0 * math.pi * u * 1.5)
        sway2: float = 120.0 * math.sin(2.0 * math.pi * u * 1.5 + 2.0)
        control_points: np.ndarray = np.array(
            [
                [x, height],
                [x + sway1 + rng.normal(0.0, 10.0), height * 0.65],
                [x + sway2 + rng.normal(0.0, 10.0), height * 0.35],
                [x + 0.5 * sway2 + rng.normal(0.0, 20.0), height * 0.05],
            ]
        )
        curve: np.ndarray = de_casteljau(control_points, t)
        red: int = round(90 + 160 * u)
        blue: int = round(230 - 140 * u)
        draw.line(_to_tuples(curve), fill=(red, 200, blue, 110), width=2)

    return Image.alpha_composite(image, layer).convert("RGB")


def main() -> None:
    control_points: np.ndarray = np.array(
        [[60.0, 400.0], [120.0, 80.0], [360.0, 60.0], [420.0, 380.0]]
    )
    render_construction(control_points, t=0.4).save("bezier_construction.png")

    rng: np.random.Generator = np.random.default_rng(seed=7)
    blob: np.ndarray = random_blob_points(
        rng, num_points=9, center=(200.0, 200.0), radius=130.0, jitter=0.35
    )
    render_blob(blob, smooth=False).save("spline_polygon.png")
    render_blob(blob, smooth=True).save("spline_blob.png")

    render_strands(rng).save("bezier_strands.png")


if __name__ == "__main__":
    main()
