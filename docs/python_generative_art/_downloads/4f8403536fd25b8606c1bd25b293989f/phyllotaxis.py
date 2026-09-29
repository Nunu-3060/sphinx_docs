"""フィロタキシスと貴金属比による螺旋状の点配置。

ひまわりの種やパイナップルの実、松かさの鱗片は、中心から一定の
角度ずつ回転しながら外側へ広がる螺旋状に並んでいる。この配置は
**フィロタキシス** (phyllotaxis、葉序) と呼ばれ、1点ずつ「一定角度
だけ回転し、外側へ少し進む」という単純な規則を繰り返すだけで
再現できる。

回転角に何を使うかが模様を大きく左右する。黄金比 :math:`\\varphi`
から作られる **黄金角** を使うと、どの点も他の点と正確には重ならず、
隙間なく詰まった自然な螺旋になる。角度を貴金属比の別の値（例えば
白銀比）に変えると、詰まり方の性質が変わり、放射状の「腕」が
はっきり見えるような、より規則的な印象の螺旋になる。
"""

import math

import numpy as np
from PIL import Image, ImageDraw

GOLDEN_RATIO: float = (1 + 5 ** 0.5) / 2
SILVER_RATIO: float = 1 + 2 ** 0.5


def metallic_angle(ratio: float) -> float:
    """貴金属比 ``ratio`` に対応する回転角(ラジアン)を返す。

    黄金比 :math:`\\varphi` を渡すと、いわゆる黄金角
    :math:`2\\pi/\\varphi^2` （およそ137.5度）になる。同じ式に
    他の貴金属比（白銀比など）を渡せば、それぞれの比に対応する
    回転角が得られる。
    """
    return 2.0 * math.pi / (ratio ** 2)


def phyllotaxis_points(
    n: int, angle: float, scale: float = 1.0
) -> np.ndarray:
    """n個の点を、1点ごとに angle ラジアンずつ回転させながら、
    中心から :math:`\\sqrt{i}` に比例する距離だけ離して配置する。

    距離を点の番号の平方根に比例させるのは、螺旋が外側にいくほど
    間延びしないよう、単位面積あたりの点の密度をほぼ一定に保つ
    ためである。戻り値は形状 ``(n, 2)`` の座標配列。
    """
    i: np.ndarray = np.arange(n, dtype=float)
    theta: np.ndarray = i * angle
    r: np.ndarray = scale * np.sqrt(i)
    x: np.ndarray = r * np.cos(theta)
    y: np.ndarray = r * np.sin(theta)
    return np.stack([x, y], axis=-1)


def render_phyllotaxis(
    points: np.ndarray,
    width: int,
    height: int,
    dot_radius: float = 4.0,
    background: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """点配置を、中心をキャンバスの中央に合わせて描画する。

    点の色は番号(古い点ほど暗く、新しい点ほど明るい青)で変化させ、
    螺旋の広がる向きが視覚的にも追いやすいようにしている。
    """
    img: Image.Image = Image.new("RGB", (width, height), background)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)
    cx: float = width / 2.0
    cy: float = height / 2.0
    n: int = len(points)

    for i, (x, y) in enumerate(points):
        t: float = i / max(n - 1, 1)
        color: tuple[int, int, int] = (
            int(30 + 60 * t),
            int(60 + 100 * t),
            int(120 + 120 * t),
        )
        px: float = cx + x
        py: float = cy + y
        bounds: list[float] = [
            px - dot_radius,
            py - dot_radius,
            px + dot_radius,
            py + dot_radius,
        ]
        draw.ellipse(bounds, fill=color)

    return img


def main() -> None:
    n: int = 500
    width: int = 480
    height: int = 480
    scale: float = 18.0

    golden_points: np.ndarray = phyllotaxis_points(
        n, metallic_angle(GOLDEN_RATIO), scale=scale
    )
    render_phyllotaxis(golden_points, width, height).save(
        "phyllotaxis_golden.png"
    )

    silver_points: np.ndarray = phyllotaxis_points(
        n, metallic_angle(SILVER_RATIO), scale=scale
    )
    render_phyllotaxis(silver_points, width, height).save(
        "phyllotaxis_silver.png"
    )


if __name__ == "__main__":
    main()
