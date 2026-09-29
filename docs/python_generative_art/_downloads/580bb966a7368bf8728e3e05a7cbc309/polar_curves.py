"""極座標で表される曲線: 各種の螺旋とバラ曲線。

距離 r を角度 theta の関数として定義するだけで、様々な曲線が表現
できる。r が theta に比例して増える **アルキメデスの螺旋**、
指数的に増える **対数螺旋**、反比例して減っていく **双曲螺旋**、
theta の余弦で振動する **バラ曲線** (rhodonea curve) は、どれも
この発想の代表例である。
"""

import math
from fractions import Fraction

import numpy as np
from PIL import Image

from phyllotaxis import GOLDEN_RATIO
from spirograph import render_curve


def logarithmic_spiral_points(
    a: float, b: float, num_points: int, revolutions: float
) -> np.ndarray:
    """対数螺旋 :math:`r = a e^{b\\theta}` 上の点列を返す。

    ``b`` が正なら外側に向かって広がる螺旋、負なら内側に向かって
    収束する螺旋になる。:doc:`../spirals` のフィロタキシス節で見た
    黄金角による点群は、実はこの対数螺旋を何本も重ねた形の
    近似になっている。
    """
    theta: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    r: np.ndarray = a * np.exp(b * theta)
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def golden_spiral_b(quarter_turn_growth: float = GOLDEN_RATIO) -> float:
    """4分の1回転ごとに ``quarter_turn_growth`` 倍に広がる螺旋の
    成長率 ``b`` を返す(既定では黄金比を使う、いわゆる黄金螺旋)。
    """
    return math.log(quarter_turn_growth) / (math.pi / 2.0)


def archimedean_spiral_points(
    a: float, b: float, num_points: int, revolutions: float
) -> np.ndarray:
    """アルキメデスの螺旋 :math:`r = a + b\\theta` 上の点列を返す。

    対数螺旋が回転するにつれて指数的に広がっていくのに対し、
    こちらは ``theta`` に比例して線形に広がる。レコード盤の溝や、
    ノートの螺旋綴じで見かける、腕の間隔が常に一定な螺旋になる。
    """
    theta: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    r: np.ndarray = a + b * theta
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def hyperbolic_spiral_points(
    a: float, num_points: int, theta_min: float, revolutions: float
) -> np.ndarray:
    """双曲螺旋 :math:`r = a/\\theta` 上の点列を返す。

    ``theta`` が0に近づくほど ``r`` が発散してしまうため、
    ``theta_min`` より内側は評価しない。外側にいくほど巻きが緩く
    なり、ある直線（漸近線）に近づいていく点が対数螺旋とは対照的
    である。
    """
    theta: np.ndarray = np.linspace(
        theta_min, 2.0 * math.pi * revolutions, num_points
    )
    r: np.ndarray = a / theta
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def rose_curve_points(
    k: float, num_points: int, scale: float = 1.0
) -> np.ndarray:
    """バラ曲線 :math:`r = \\cos(k\\theta)` 上の点列を返す。

    ``k`` が既約分数 ``n/d`` のとき、花びらの数は ``n`` が奇数なら
    ``n`` 枚、偶数なら ``2n`` 枚になる。1周だけでは曲線が閉じない
    場合があるため、分母 ``d`` の分だけ ``theta`` を多く動かす。
    """
    fraction: Fraction = Fraction(k).limit_denominator(64)
    revolutions: int = fraction.denominator
    theta: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    r: np.ndarray = scale * np.cos(k * theta)
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def superformula_points(
    m: float,
    n1: float,
    n2: float,
    n3: float,
    num_points: int = 2000,
    a: float = 1.0,
    b: float = 1.0,
    scale: float = 1.0,
) -> np.ndarray:
    """スーパーフォーミュラ上の点列を返す。

    .. math::

       r(\\theta) = \\left(
           \\left|\\frac{\\cos(m\\theta/4)}{a}\\right|^{n_2}
           + \\left|\\frac{\\sin(m\\theta/4)}{b}\\right|^{n_3}
       \\right)^{-1/n_1}

    バラ曲線が :math:`r=\\cos(k\\theta)` という1つの式で花びらの数だけを
    操作したのに対し、スーパーフォーミュラは指数 :math:`n_1, n_2, n_3`
    と対称性の次数 :math:`m` という4つのパラメータを持つことで、
    円・多角形・星形・歯車状・花びら状など、質的に全く異なる輪郭を
    同じ式から作り分けられる。指数が全て2で :math:`m=4` なら円に、
    指数を大きくすると角の尖った超楕円（squircle）に近づく。
    """
    theta: np.ndarray = np.linspace(0.0, 2.0 * math.pi, num_points)
    term1: np.ndarray = np.abs(np.cos(m * theta / 4.0) / a) ** n2
    term2: np.ndarray = np.abs(np.sin(m * theta / 4.0) / b) ** n3
    r: np.ndarray = (term1 + term2) ** (-1.0 / n1) * scale
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def main() -> None:
    width: int = 480
    height: int = 480

    spiral: np.ndarray = logarithmic_spiral_points(
        a=2.0, b=golden_spiral_b(), num_points=1000, revolutions=3.0
    )
    render_curve(spiral, width, height, color=(200, 140, 40)).save(
        "logarithmic_spiral.png"
    )

    archimedean: np.ndarray = archimedean_spiral_points(
        a=0.0, b=1.0, num_points=1000, revolutions=6.0
    )
    render_curve(archimedean, width, height, color=(70, 150, 90)).save(
        "archimedean_spiral.png"
    )

    hyperbolic: np.ndarray = hyperbolic_spiral_points(
        a=6.0, num_points=2000, theta_min=0.4, revolutions=4.0
    )
    render_curve(hyperbolic, width, height, color=(150, 80, 160)).save(
        "hyperbolic_spiral.png"
    )

    rose_5: np.ndarray = rose_curve_points(k=5.0, num_points=2000, scale=200.0)
    render_curve(rose_5, width, height, color=(190, 70, 110)).save(
        "rose_5.png"
    )

    rose_4: np.ndarray = rose_curve_points(k=4.0, num_points=4000, scale=200.0)
    render_curve(rose_4, width, height, color=(90, 130, 190)).save(
        "rose_4.png"
    )

    superformula_presets: list[
        tuple[float, float, float, float, tuple[int, int, int]]
    ] = [
        (3.0, 1.0, 1.0, 1.0, (210, 90, 60)),
        (6.0, 1.0, 7.0, 7.0, (90, 150, 90)),
        (16.0, 0.5, 0.5, 16.0, (80, 110, 190)),
        (5.0, 0.3, 0.3, 0.3, (170, 90, 170)),
    ]
    tile_size: int = 240
    grid: Image.Image = Image.new(
        "RGB", (tile_size * 2, tile_size * 2), "white"
    )
    for i, (m, n1, n2, n3, color) in enumerate(superformula_presets):
        points: np.ndarray = superformula_points(
            m, n1, n2, n3, num_points=2000, scale=100.0
        )
        tile: Image.Image = render_curve(
            points, tile_size, tile_size, color=color
        )
        grid.paste(tile, ((i % 2) * tile_size, (i // 2) * tile_size))
    grid.save("superformula.png")


if __name__ == "__main__":
    main()
