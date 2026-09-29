"""トルシェ・タイル (Truchet tiles) によるタイリングパターン。

正方形の格子に、決まった数種類の「タイル」を1枚ずつ並べていくだけの
単純な仕組みでありながら、タイルごとの向き（回転）を変えるだけで、
迷路のように入り組んだ連続的な模様が生まれる。:doc:`../basics` で
触れた「パラメータ（ここではタイルの向き）を格子状に変えながら同じ
描画関数を繰り返し呼び出す」というグリッド配置の、具体的な一例に
なっている。
"""

from collections.abc import Callable

import numpy as np
from PIL import Image, ImageDraw

TileFn = Callable[
    [ImageDraw.ImageDraw, float, float, float, int, tuple[int, int, int]],
    None,
]


def draw_arc_tile(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    size: float,
    orientation: int,
    color: tuple[int, int, int] = (30, 30, 30),
    width: int = 2,
) -> None:
    """四分円弧2本から成る、古典的なトルシェ・タイルを1枚描く。

    タイルは対角線上にある2つの角を中心とした半径 ``size/2`` の
    四分円弧2本から成る。``orientation`` (0か1) で、どちらの対角線に
    弧を配置するかが決まる。弧の両端は必ず辺の中点に来るため、
    隣り合うタイルの向きの組み合わせ次第で弧どうしがつながり、
    連続した曲線になる。
    """
    r: float = size / 2.0
    if orientation == 0:
        draw.arc(
            [x0 - r, y0 - r, x0 + r, y0 + r],
            start=0,
            end=90,
            fill=color,
            width=width,
        )
        draw.arc(
            [x0 + size - r, y0 + size - r, x0 + size + r, y0 + size + r],
            start=180,
            end=270,
            fill=color,
            width=width,
        )
    else:
        draw.arc(
            [x0 + size - r, y0 - r, x0 + size + r, y0 + r],
            start=90,
            end=180,
            fill=color,
            width=width,
        )
        draw.arc(
            [x0 - r, y0 + size - r, x0 + r, y0 + size + r],
            start=270,
            end=360,
            fill=color,
            width=width,
        )


def draw_diagonal_tile(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    size: float,
    orientation: int,
    color: tuple[int, int, int] = (30, 30, 30),
    width: int = 2,
) -> None:
    """対角線1本から成る、もう1つの定番のトルシェ・タイルを描く。

    ``orientation`` (0か1) で、正方形をどちらの対角線で分割するかが
    決まる。弧タイルと違って滑らかにはつながらず、山型・谷型の
    ジグザグ模様（ヘリンボーンに近い見た目）になる。
    """
    if orientation == 0:
        draw.line([(x0, y0), (x0 + size, y0 + size)], fill=color, width=width)
    else:
        draw.line([(x0 + size, y0), (x0, y0 + size)], fill=color, width=width)


def render_random_tiling(
    cols: int,
    rows: int,
    tile_size: int,
    rng: np.random.Generator,
    tile_fn: TileFn = draw_arc_tile,
    color: tuple[int, int, int] = (30, 30, 30),
) -> Image.Image:
    """各タイルの向きをランダムに選んで格子状に敷き詰める。"""
    orientations: np.ndarray = rng.integers(0, 2, size=(rows, cols))
    img: Image.Image = Image.new(
        "RGB", (cols * tile_size, rows * tile_size), "white"
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for row in range(rows):
        for col in range(cols):
            tile_fn(
                draw,
                col * tile_size,
                row * tile_size,
                tile_size,
                int(orientations[row, col]),
                color,
            )

    return img


def render_noise_tiling(
    cols: int,
    rows: int,
    tile_size: int,
    perm: np.ndarray,
    scale: float,
    color: tuple[int, int, int] = (30, 30, 30),
) -> Image.Image:
    """向きをランダムではなく、パーリンノイズの符号で決める。

    ノイズは近くの格子点どうしでなめらかに変化するため、タイルの
    向きも近傍でそろいやすくなり、ランダム配置とは対照的に、渦を
    巻いたような流れのある模様になる。
    """
    from perlin_noise import fbm2d

    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(cols, dtype=float), np.arange(rows, dtype=float)
    )
    values: np.ndarray = fbm2d(xs * scale, ys * scale, perm, octaves=3)
    orientations: np.ndarray = (values > 0).astype(int)

    img: Image.Image = Image.new(
        "RGB", (cols * tile_size, rows * tile_size), "white"
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for row in range(rows):
        for col in range(cols):
            draw_arc_tile(
                draw,
                col * tile_size,
                row * tile_size,
                tile_size,
                int(orientations[row, col]),
                color=color,
            )

    return img


def draw_weave_tile(
    draw: ImageDraw.ImageDraw,
    x0: float,
    y0: float,
    size: float,
    over_horizontal: bool,
    color: tuple[int, int, int] = (30, 30, 30),
    strand_width: int = 6,
    gap: float = 4.0,
) -> None:
    """タイル中央で交差する縦・横2本の帯を、編み込み風に描く。

    ``over_horizontal`` が真なら横方向の帯を上に、偽なら縦方向の帯を
    上に描く。下になった帯には交差点の前後にわずかな隙間を空け、
    もう一方の帯の下をくぐっているように見せる。
    """
    cx: float = x0 + size / 2.0
    cy: float = y0 + size / 2.0

    if over_horizontal:
        draw.line([(x0, cy), (x0 + size, cy)], fill=color, width=strand_width)
        draw.line([(cx, y0), (cx, cy - gap)], fill=color, width=strand_width)
        draw.line(
            [(cx, cy + gap), (cx, y0 + size)], fill=color, width=strand_width
        )
    else:
        draw.line([(cx, y0), (cx, y0 + size)], fill=color, width=strand_width)
        draw.line([(x0, cy), (cx - gap, cy)], fill=color, width=strand_width)
        draw.line(
            [(cx + gap, cy), (x0 + size, cy)], fill=color, width=strand_width
        )


def render_weave(
    cols: int,
    rows: int,
    tile_size: int,
    color: tuple[int, int, int] = (30, 30, 30),
) -> Image.Image:
    """タイルごとに縦横どちらの帯を上にするか市松模様で切り替え、
    格子全体を編み込みパターンとして描く。

    ランダムに向きを選んだ ``render_random_tiling`` とは違い、ここでは
    向きを ``(row + col) % 2`` という決め打ちの規則で選ぶ。隣り合う
    帯どうしが必ず上下を入れ替えながらつながるようにするには、
    この市松模様の規則性が欠かせない。ランダムに上下を選んでしまうと、
    同じ帯が2マス連続で「上」になり、編み目としてのつじつまが
    合わなくなる。
    """
    img: Image.Image = Image.new(
        "RGB", (cols * tile_size, rows * tile_size), "white"
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for row in range(rows):
        for col in range(cols):
            draw_weave_tile(
                draw,
                col * tile_size,
                row * tile_size,
                tile_size,
                over_horizontal=(row + col) % 2 == 0,
                color=color,
            )

    return img


def main() -> None:
    from perlin_noise import make_permutation

    rng: np.random.Generator = np.random.default_rng(seed=0)

    render_random_tiling(24, 24, 20, rng, tile_fn=draw_arc_tile).save(
        "truchet_random.png"
    )

    rng = np.random.default_rng(seed=1)
    render_random_tiling(24, 24, 20, rng, tile_fn=draw_diagonal_tile).save(
        "truchet_diagonal.png"
    )

    perm: np.ndarray = make_permutation(seed=2)
    render_noise_tiling(24, 24, 20, perm, scale=0.08).save(
        "truchet_noise.png"
    )

    render_weave(16, 16, 30).save("truchet_weave.png")


if __name__ == "__main__":
    main()
