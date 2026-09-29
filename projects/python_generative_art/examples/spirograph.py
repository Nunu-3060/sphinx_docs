"""サイクロイド族の曲線によるスピログラフ模様。

円が直線や別の円に沿って滑らずに転がるとき、円周上の1点が描く
軌跡を **サイクロイド族** の曲線と呼ぶ。転がる円の外側の点を
追いかけると花びらのような模様（エピトロコイド）に、固定円の
内側を転がる円の点を追いかけると星形のような模様（ハイポ
トロコイド、いわゆる「スピログラフ」のおもちゃの模様）になる。
どちらも、時刻 :math:`t` を振ってできる座標をまとめて計算できる、
単純なパラメトリック曲線である。
"""

import math

import numpy as np
from PIL import Image, ImageDraw


def cycloid_points(
    radius: float, num_points: int, revolutions: float
) -> np.ndarray:
    """半径 radius の円が直線上を転がるときの、円周上の1点の軌跡。

    :math:`x = r(t - \\sin t)`, :math:`y = r(1 - \\cos t)` という
    古典的なサイクロイドの式をそのままベクトル化しただけである。
    """
    t: np.ndarray = np.linspace(0.0, 2.0 * math.pi * revolutions, num_points)
    x: np.ndarray = radius * (t - np.sin(t))
    y: np.ndarray = radius * (1.0 - np.cos(t))
    return np.stack([x, y], axis=-1)


def hypotrochoid_points(
    fixed_radius: int,
    rolling_radius: int,
    pen_offset: float,
    num_points: int = 3000,
) -> np.ndarray:
    """固定円の内側を転がる円の上の点の軌跡(ハイポトロコイド)。

    ``fixed_radius`` / ``rolling_radius`` の最大公約数から、曲線が
    ちょうど閉じるまでに転がる円が何周する必要があるかを求め、
    その分だけパラメータ ``t`` を動かす。
    """
    g: int = math.gcd(fixed_radius, rolling_radius)
    revolutions: int = rolling_radius // g
    t: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    k: float = (fixed_radius - rolling_radius) / rolling_radius
    x: np.ndarray = (fixed_radius - rolling_radius) * np.cos(
        t
    ) + pen_offset * np.cos(k * t)
    y: np.ndarray = (fixed_radius - rolling_radius) * np.sin(
        t
    ) - pen_offset * np.sin(k * t)
    return np.stack([x, y], axis=-1)


def epitrochoid_points(
    fixed_radius: int,
    rolling_radius: int,
    pen_offset: float,
    num_points: int = 3000,
) -> np.ndarray:
    """固定円の外側を転がる円の上の点の軌跡(エピトロコイド)。"""
    g: int = math.gcd(fixed_radius, rolling_radius)
    revolutions: int = rolling_radius // g
    t: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    k: float = (fixed_radius + rolling_radius) / rolling_radius
    x: np.ndarray = (fixed_radius + rolling_radius) * np.cos(
        t
    ) - pen_offset * np.cos(k * t)
    y: np.ndarray = (fixed_radius + rolling_radius) * np.sin(
        t
    ) - pen_offset * np.sin(k * t)
    return np.stack([x, y], axis=-1)


def render_curve(
    points: np.ndarray,
    width: int,
    height: int,
    color: tuple[int, int, int] = (40, 70, 160),
    line_width: int = 2,
    margin: float = 0.9,
) -> Image.Image:
    """点列を、キャンバスに収まるよう自動的に拡大縮小して折れ線で描く。"""
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    x_min: float = float(points[:, 0].min())
    x_max: float = float(points[:, 0].max())
    y_min: float = float(points[:, 1].min())
    y_max: float = float(points[:, 1].max())
    span: float = max(x_max - x_min, y_max - y_min, 1e-9)
    scale: float = min(width, height) * margin / span
    cx: float = width / 2.0 - (x_min + x_max) / 2.0 * scale
    cy: float = height / 2.0 - (y_min + y_max) / 2.0 * scale

    pixels: list[tuple[float, float]] = [
        (cx + x * scale, cy + y * scale) for x, y in points
    ]
    draw.line(pixels, fill=color, width=line_width, joint="curve")

    return img


def main() -> None:
    width: int = 480
    height: int = 480

    render_curve(
        cycloid_points(radius=1.0, num_points=800, revolutions=3.0),
        width,
        height,
    ).save("cycloid.png")

    render_curve(
        hypotrochoid_points(
            fixed_radius=5, rolling_radius=3, pen_offset=5.0
        ),
        width,
        height,
        color=(190, 70, 90),
    ).save("hypotrochoid.png")

    render_curve(
        epitrochoid_points(
            fixed_radius=5, rolling_radius=3, pen_offset=5.0
        ),
        width,
        height,
        color=(50, 140, 100),
    ).save("epitrochoid.png")


if __name__ == "__main__":
    main()
