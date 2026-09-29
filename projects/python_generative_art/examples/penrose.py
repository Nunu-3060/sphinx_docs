"""ペンローズ・タイル (Penrose tiling) による非周期タイリング。

ワン・タイルは辺の制約さえ満たせば配置は自由（乱数任せ）だったが、
ペンローズ・タイルは逆に、2種類のひし形だけを使い、しかも決して
周期的に（平行移動しても）ぴったり繰り返さない非周期的なタイリング
になるという、幾何学的に強い制約を持つ。ここでは、黄金比に基づく
2種類の二等辺三角形（Robinson三角形）を、細分割規則に従って
繰り返し分割していくことで構成する。
"""

import math

from PIL import Image, ImageDraw

GOLDEN_RATIO: float = (1 + 5 ** 0.5) / 2

Triangle = tuple[int, complex, complex, complex]


def initial_sun(num_wedges: int = 10) -> list[Triangle]:
    """原点を中心に、細い(color=0)三角形を扇状に並べた初期状態を作る。

    半径1の円周上に頂点を取った ``num_wedges`` 枚の三角形が、原点を
    囲むように並ぶ「太陽」型の初期配置になる。
    """
    triangles: list[Triangle] = []
    for i in range(num_wedges):
        angle_a: float = (2 * i - 1) * math.pi / num_wedges
        angle_b: float = (2 * i + 1) * math.pi / num_wedges
        b: complex = complex(math.cos(angle_a), math.sin(angle_a))
        c: complex = complex(math.cos(angle_b), math.sin(angle_b))
        if i % 2 == 0:
            b, c = c, b
        triangles.append((0, 0j, b, c))
    return triangles


def subdivide_penrose(triangles: list[Triangle]) -> list[Triangle]:
    """各三角形を、黄金比に基づく細分割規則でより小さな三角形に分ける。

    ``color=0`` （細い三角形）は2枚に、``color=1`` （太い三角形）は
    3枚に分割される。この分割を繰り返すことで、全体としては非周期的
    なペンローズ・タイリングに収束していく。
    """
    result: list[Triangle] = []
    for color, a, b, c in triangles:
        if color == 0:
            p: complex = a + (b - a) / GOLDEN_RATIO
            result.append((0, c, p, b))
            result.append((1, p, c, a))
        else:
            q: complex = b + (a - b) / GOLDEN_RATIO
            r: complex = b + (c - b) / GOLDEN_RATIO
            result.append((1, q, r, b))
            result.append((0, r, q, a))
            result.append((0, c, a, r))
    return result


def render_penrose(
    triangles: list[Triangle],
    width: int,
    height: int,
    colors: tuple[tuple[int, int, int], tuple[int, int, int]] = (
        (230, 100, 90),
        (90, 140, 200),
    ),
    scale: float = 220.0,
) -> Image.Image:
    """三角形のリストを、種類ごとに塗り分けた画像として描画する。

    隣接する同じ種類の三角形2枚が、ペンローズ・タイルの太いひし形・
    細いひし形1枚に対応する。三角形単位で塗りつぶすだけで、輪郭線を
    引かなくても自然にひし形の模様が浮かび上がる。
    """
    img: Image.Image = Image.new("RGB", (width, height), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    center_x: float = width / 2.0
    center_y: float = height / 2.0

    def to_pixel(z: complex) -> tuple[float, float]:
        return (center_x + z.real * scale, center_y - z.imag * scale)

    for color, a, b, c in triangles:
        draw.polygon(
            [to_pixel(a), to_pixel(b), to_pixel(c)],
            fill=colors[color],
            outline=(255, 255, 255),
        )

    return img


def main() -> None:
    triangles: list[Triangle] = initial_sun()
    for _ in range(6):
        triangles = subdivide_penrose(triangles)

    render_penrose(triangles, width=480, height=480).save("penrose.png")


if __name__ == "__main__":
    main()
