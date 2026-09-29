"""同じ単純な模様を、配色だけを変えて描き比べる。

格子の各マスに、背景色と、円・四分円・半円のどれか1つの図形を描く
だけの模様を使う。図形の種類・向き・色の選び方(乱数)は1度だけ
決めておき、色を取り出すパレットだけを差し替えることで、配色の
違いだけが見た目に与える影響を確かめる。
"""

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from palette import tone_in_tone_palette, tone_on_tone_palette

Color = tuple[int, int, int]


@dataclass
class Layout:
    """模様の配置。全ての配列は形状 (rows, cols)。

    ``shape`` は図形の種類(0=円、1=四分円、2=半円)、``turn`` は
    図形の向き(90度単位)、``u_back`` と ``u_front`` は背景色と図形の
    色を選ぶための 0.0-1.0 の乱数。
    """

    shape: np.ndarray
    turn: np.ndarray
    u_back: np.ndarray
    u_front: np.ndarray


def make_layout(rows: int, cols: int, rng: np.random.Generator) -> Layout:
    """模様の配置を乱数で決める。"""
    return Layout(
        shape=rng.integers(0, 3, size=(rows, cols)),
        turn=rng.integers(0, 4, size=(rows, cols)),
        u_back=rng.random((rows, cols)),
        u_front=rng.random((rows, cols)),
    )


def pick_index(u: float, weights: np.ndarray) -> int:
    """0.0-1.0 の乱数 u から、重み weights に比例した確率で番号を選ぶ。"""
    cumulative: np.ndarray = np.cumsum(weights) / weights.sum()
    return int(np.searchsorted(cumulative, u, side="right"))


def draw_tile(
    draw: ImageDraw.ImageDraw,
    left: int,
    top: int,
    size: int,
    shape: int,
    turn: int,
    back: Color,
    front: Color,
) -> None:
    """1マス分の背景と図形を描く。"""
    right: int = left + size
    bottom: int = top + size
    draw.rectangle((left, top, right - 1, bottom - 1), fill=back)
    if shape == 0:  # マスに内接する円
        margin: int = size // 8
        draw.ellipse(
            (left + margin, top + margin, right - margin, bottom - margin),
            fill=front,
        )
    elif shape == 1:  # マスの角を中心とし、半径がマスの1辺に等しい四分円
        corners: list[tuple[int, int]] = [
            (left, top), (right, top), (right, bottom), (left, bottom)
        ]
        cx, cy = corners[turn]
        start: int = [0, 90, 180, 270][turn]
        draw.pieslice(
            (cx - size, cy - size, cx + size, cy + size),
            start,
            start + 90,
            fill=front,
        )
    else:  # マスの辺の中点を中心とする半円
        centers: list[tuple[float, float]] = [
            (left + size / 2, top),
            (right, top + size / 2),
            (left + size / 2, bottom),
            (left, top + size / 2),
        ]
        cx2, cy2 = centers[turn]
        start2: int = [0, 90, 180, 270][turn]
        half: float = size / 2
        draw.pieslice(
            (cx2 - half, cy2 - half, cx2 + half, cy2 + half),
            start2,
            start2 + 180,
            fill=front,
        )


def render_pattern(
    layout: Layout,
    palette: list[Color],
    weights: np.ndarray | None = None,
    cell: int = 50,
) -> Image.Image:
    """配置 ``layout`` に従い、``palette`` から色を選んで模様を描く。

    ``weights`` を与えると、パレットの色ごとに選ばれやすさを変えられる。
    図形の色が背景色と同じになった場合は、パレットの次の色に替える。
    """
    rows: int
    cols: int
    rows, cols = layout.shape.shape
    w: np.ndarray = np.ones(len(palette)) if weights is None else weights
    image: Image.Image = Image.new("RGB", (cols * cell, rows * cell))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for r in range(rows):
        for c in range(cols):
            back: int = pick_index(float(layout.u_back[r, c]), w)
            front: int = pick_index(float(layout.u_front[r, c]), w)
            if front == back:
                front = (front + 1) % len(palette)
            draw_tile(
                draw, c * cell, r * cell, cell,
                int(layout.shape[r, c]), int(layout.turn[r, c]),
                palette[back], palette[front],
            )
    return image


def random_rgb_palette(count: int, rng: np.random.Generator) -> list[Color]:
    """RGB の各成分を一様乱数で決めた、配色を考えていないパレット。"""
    values: np.ndarray = rng.integers(0, 256, size=(count, 3))
    return [(int(r), int(g), int(b)) for r, g, b in values]


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=11)
    layout: Layout = make_layout(8, 8, rng)

    # 1. RGB の一様乱数で選んだ 12 色。
    render_pattern(layout, random_rgb_palette(12, rng)).save(
        "color_pattern_random.png"
    )

    # 2. soft トーンに固定し、色相環を5等分したトーンイントーン配色。
    hues: list[float] = [0.02 + i / 5 for i in range(5)]
    render_pattern(layout, tone_in_tone_palette("soft", hues)).save(
        "color_pattern_tone.png"
    )

    # 3. 青のトーンオントーンを主役にし、補色の橙を少量だけ差し色にする。
    blues: list[Color] = tone_on_tone_palette(
        0.6, ["pale", "light", "soft", "deep", "dark"]
    )
    accent: Color = tone_in_tone_palette("vivid", [0.08])[0]
    weights: np.ndarray = np.array([3.0, 3.0, 3.0, 3.0, 3.0, 1.0])
    render_pattern(layout, blues + [accent], weights).save(
        "color_pattern_accent.png"
    )


if __name__ == "__main__":
    main()
