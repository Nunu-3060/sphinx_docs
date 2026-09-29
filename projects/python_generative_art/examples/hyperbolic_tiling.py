"""ポアンカレディスク模型による双曲タイリング {p, q}。

正方形・正三角形・正六角形が平面を隙間なく埋め尽くせたのは、1つの
頂点の周りに内角がちょうど360度分だけ集まったからだった
(:doc:`../tiling` 参照)。正五角形や正七角形では、頂点の周りに正多角形
を何枚並べても内角の合計が360度にきっちり収まらない。この「収まらな
い分」は、平面を双曲的に湾曲させることで初めて破綻なく解消できる。
**ポアンカレディスク模型** は、この双曲平面全体を単位円板の内部に
写し取った表現で、双曲的な直線(測地線)は円板の中心を通る直線か、
円板の境界に直交する円弧のどちらかとして現れる。
"""

import math
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw

Polygon = tuple[int, np.ndarray]


def polygon_circumradius(p: int, q: int) -> float:
    """1つの頂点に ``q`` 枚が集まる正 ``p`` 角形タイリングの、正多角形1枚
    の外接円半径(ポアンカレディスク上でのユークリッド距離)を返す。

    頂点・辺の中点・中心の3点がなす双曲三角形(角度は順に ``pi/q``・
    ``pi/2``・``pi/p``)に双曲的な余弦定理を適用して導ける。``1/p + 1/q``
    が ``1/2`` 未満のとき双曲的なタイリングになり、値はちょうど単位円の
    内側(半径1未満)に収まる。
    """
    a = math.pi / p
    b = math.pi / q
    return math.sqrt(math.cos(a + b) / math.cos(a - b))


def fundamental_polygon(p: int, q: int) -> np.ndarray:
    """原点を中心とした、最初の正 ``p`` 角形の頂点(複素数)を返す。"""
    radius = polygon_circumradius(p, q)
    angles = 2 * np.pi * np.arange(p) / p
    return radius * np.exp(1j * angles)


def geodesic_reflection(
    z1: complex, z2: complex
) -> Callable[[np.ndarray], np.ndarray]:
    """``z1``・``z2`` を通る測地線に関して点を鏡映する変換を返す。

    測地線(円板境界に直交する円弧、またはそれが退化した原点を通る直線)
    は単位円板に関する反転で不変なので、``z1`` の反転像 ``1/conj(z1)``
    も同じ測地線上に乗る。この3点から円(退化する場合は直線)を決定し、
    その円に関する反転として鏡映を実装する。
    """
    z3 = 1 / np.conj(z1)
    x1, y1 = z1.real, z1.imag
    x2, y2 = z2.real, z2.imag
    x3, y3 = z3.real, z3.imag

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9:
        theta = np.angle(z1)
        return lambda z: np.exp(2j * theta) * np.conj(z)

    cx = (
        (x1**2 + y1**2) * (y2 - y3)
        + (x2**2 + y2**2) * (y3 - y1)
        + (x3**2 + y3**2) * (y1 - y2)
    ) / d
    cy = (
        (x1**2 + y1**2) * (x3 - x2)
        + (x2**2 + y2**2) * (x1 - x3)
        + (x3**2 + y3**2) * (x2 - x1)
    ) / d
    center = complex(cx, cy)
    radius = abs(z1 - center)

    def reflect(z: np.ndarray) -> np.ndarray:
        return center + radius**2 / np.conj(z - center)

    return reflect


def generate_tiling(p: int, q: int, depth: int) -> list[Polygon]:
    """最初の正 ``p`` 角形を各辺に関して繰り返し鏡映し、タイリングを広げる。

    幅優先探索(:doc:`../tiling` の迷路の解探索と同じ考え方)で、まだ
    現れていない多角形だけを重心の座標で見分けながら ``depth`` 段階
    先まで広げる。多角形は最初に現れた段階の番号(0が中心の1枚)を
    付けて返し、中心からの層の深さを色分けに使えるようにしている。
    """
    base = fundamental_polygon(p, q)
    seen: set[tuple[float, float]] = set()

    def key(vertices: np.ndarray) -> tuple[float, float]:
        centroid = vertices.mean()
        return (round(centroid.real, 4), round(centroid.imag, 4))

    seen.add(key(base))
    polygons: list[Polygon] = [(0, base)]
    frontier: list[np.ndarray] = [base]

    for layer in range(1, depth + 1):
        next_frontier: list[np.ndarray] = []
        for vertices in frontier:
            n = len(vertices)
            for i in range(n):
                reflect = geodesic_reflection(
                    vertices[i], vertices[(i + 1) % n]
                )
                neighbor = reflect(vertices)
                neighbor_key = key(neighbor)
                if neighbor_key not in seen:
                    seen.add(neighbor_key)
                    polygons.append((layer, neighbor))
                    next_frontier.append(neighbor)
        frontier = next_frontier
        if not frontier:
            break

    return polygons


def render_tiling(
    polygons: list[Polygon],
    size: int = 800,
    inner_color: tuple[int, int, int] = (235, 110, 90),
    outer_color: tuple[int, int, int] = (60, 90, 160),
) -> Image.Image:
    """層の深さに応じて中心付近を暖色・外周を寒色にグラデーションで塗る。

    円板の境界に近づくほど多角形が指数的に小さくなるのが、双曲タイリング
    をユークリッド平面に写し取ったときの特徴である。
    """
    img = Image.new("RGB", (size, size), (15, 15, 25))
    draw = ImageDraw.Draw(img)
    center = size / 2.0
    scale = size * 0.48
    max_layer = max(layer for layer, _ in polygons) or 1

    def to_pixel(z: complex) -> tuple[float, float]:
        return (center + z.real * scale, center - z.imag * scale)

    for layer, vertices in polygons:
        t = layer / max_layer
        color = tuple(
            round(inner_color[c] * (1 - t) + outer_color[c] * t)
            for c in range(3)
        )
        draw.polygon(
            [to_pixel(z) for z in vertices],
            fill=color,
            outline=(255, 255, 255),
        )

    draw.ellipse(
        [center - scale, center - scale, center + scale, center + scale],
        outline=(255, 255, 255),
        width=2,
    )
    return img


def main() -> None:
    polygons = generate_tiling(p=7, q=3, depth=5)
    render_tiling(polygons).save("hyperbolic_7_3.png")

    polygons = generate_tiling(p=6, q=4, depth=4)
    render_tiling(polygons).save("hyperbolic_6_4.png")


if __name__ == "__main__":
    main()
