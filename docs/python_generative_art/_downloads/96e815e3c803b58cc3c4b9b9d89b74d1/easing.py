"""補間とイージング関数。

2つの値の間を ``t`` (0〜1) で補間するとき、``t`` をそのまま使えば
一定の速さで変化する線形補間になる。``t`` をいったん「イージング関数」
に通してから補間すると、始まりや終わりをゆっくりにしたり、途中を
急にしたりと、変化の緩急を自由に設計できる。アニメーションでよく
知られる考え方だが、静止画でもグラデーションの色の変化や、図形を
並べる間隔の疎密を決めるのにそのまま使える。
"""

from collections.abc import Callable

import numpy as np
from PIL import Image, ImageDraw

EasingFunction = Callable[[np.ndarray], np.ndarray]


def lerp(a: np.ndarray, b: np.ndarray, t: np.ndarray) -> np.ndarray:
    """``a`` から ``b`` へ、``t`` (0〜1) の割合で線形補間する。"""
    return a + (b - a) * t


def linear(t: np.ndarray) -> np.ndarray:
    """変化の緩急をつけない、恒等関数のイージング。"""
    return t


def ease_in_cubic(t: np.ndarray) -> np.ndarray:
    """始まりがゆっくりで、終わりに向かって加速する。"""
    return t**3


def ease_out_cubic(t: np.ndarray) -> np.ndarray:
    """始まりが速く、終わりに向かって減速する(ease_in_cubic の裏返し)。"""
    return 1.0 - (1.0 - t) ** 3


def smoothstep(t: np.ndarray) -> np.ndarray:
    """3次のエルミート補間。両端で1階微分が0になる。"""
    return t * t * (3.0 - 2.0 * t)


def smootherstep(t: np.ndarray) -> np.ndarray:
    """5次の補間。両端で1階・2階微分がともに0になる。

    パーリンノイズの fade 関数と同じ式である。
    """
    return t * t * t * (t * (6.0 * t - 15.0) + 10.0)


EASINGS: dict[str, EasingFunction] = {
    "linear": linear,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "smoothstep": smoothstep,
    "smootherstep": smootherstep,
}


def render_easing_curves(
    easings: dict[str, EasingFunction],
    cell_size: int = 160,
    margin: int = 20,
) -> Image.Image:
    """各イージング関数のグラフ(横軸 t、縦軸 出力)を横一列に並べる。"""
    width: int = cell_size * len(easings)
    image: Image.Image = Image.new("RGB", (width, cell_size), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    t: np.ndarray = np.linspace(0.0, 1.0, 200)
    plot_size: int = cell_size - 2 * margin

    for index, easing in enumerate(easings.values()):
        left: int = index * cell_size + margin
        bottom: int = cell_size - margin
        draw.rectangle(
            [left, margin, left + plot_size, bottom], outline=(200, 200, 200)
        )
        # 比較用に、線形補間の対角線を薄く描いておく。
        draw.line(
            [(left, bottom), (left + plot_size, margin)], fill=(220, 220, 220)
        )
        xs: np.ndarray = left + t * plot_size
        ys: np.ndarray = bottom - easing(t) * plot_size
        points: list[tuple[float, float]] = list(
            zip(xs.tolist(), ys.tolist())
        )
        draw.line(points, fill=(200, 70, 60), width=3)

    return image


def render_eased_gradient(
    easings: dict[str, EasingFunction],
    start_color: tuple[int, int, int] = (30, 40, 90),
    end_color: tuple[int, int, int] = (250, 190, 90),
    width: int = 800,
    band_height: int = 40,
) -> Image.Image:
    """同じ2色の間を、イージング関数ごとに補間したグラデーションを縦に並べる。"""
    t: np.ndarray = np.linspace(0.0, 1.0, width)
    start: np.ndarray = np.array(start_color, dtype=float)
    end: np.ndarray = np.array(end_color, dtype=float)
    bands: list[np.ndarray] = []

    for easing in easings.values():
        eased: np.ndarray = easing(t)[:, np.newaxis]
        row: np.ndarray = lerp(start, end, eased)
        bands.append(np.repeat(row[np.newaxis, :, :], band_height, axis=0))

    pixels: np.ndarray = np.concatenate(bands, axis=0)
    return Image.fromarray(pixels.round().astype(np.uint8))


def render_eased_rings(
    easing: EasingFunction,
    num_rings: int = 40,
    size: int = 480,
) -> Image.Image:
    """同心円の半径をイージング関数で決め、間隔の疎密で奥行きを表現する。

    ``i / num_rings`` を等間隔に振り、それをイージング関数に通した値を
    半径の割合として使う。線形なら等間隔の同心円になり、
    ``ease_in_cubic`` なら中心付近が密で外側ほど疎になる。
    """
    image: Image.Image = Image.new("RGB", (size, size), (20, 24, 40))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    center: float = size / 2.0
    max_radius: float = size * 0.46
    t: np.ndarray = np.linspace(0.0, 1.0, num_rings + 1)[1:]
    radii: np.ndarray = easing(t) * max_radius
    colors: np.ndarray = lerp(
        np.array([90.0, 200.0, 220.0]),
        np.array([250.0, 120.0, 90.0]),
        t[:, np.newaxis],
    )

    for radius, color in zip(radii.tolist(), colors.round().astype(int)):
        draw.ellipse(
            [
                center - radius,
                center - radius,
                center + radius,
                center + radius,
            ],
            outline=(int(color[0]), int(color[1]), int(color[2])),
            width=2,
        )

    return image


def main() -> None:
    render_easing_curves(EASINGS).save("easing_curves.png")
    render_eased_gradient(EASINGS).save("easing_gradient.png")
    render_eased_rings(linear).save("easing_rings_linear.png")
    render_eased_rings(ease_in_cubic).save("easing_rings_ease_in.png")


if __name__ == "__main__":
    main()
