"""錯視とオプ・アートの作例。

単純な図形の並べ方を工夫するだけで、実際には存在しない傾き・点・
動き・奥行きが見える図を作れる。ここでは次の 5 種類を描く。

1. カフェウォール錯視: 平行な横線が傾いて見える（幾何学的錯視）
2. きらめき格子錯視: 白い円の中に黒い点がちらつく（明るさの錯視）
3. 周辺ドリフト錯視: 静止画の円盤が回転して見える（動きの錯視）
4. モアレ: 2 つの縞模様を重ねると、どちらにもない縞が現れる
5. 格子の歪みによる膨らみ: 平面の市松模様が球のように膨らんで見える

錯視は表示の大きさに左右される。画像を縮小・拡大して表示すると、
細かい模様が崩れたり、意図しないモアレが生じたりするため、
生成した画像は等倍で表示するのが望ましい。
"""

import numpy as np
from PIL import Image, ImageDraw

# モアレの縞で、周期のうち黒い線が占める割合。
_LINE_RATIO: float = 0.4

# 細い線や円弧の縁のぎざぎざを抑えるため、拡大した画像で描いてから
# 縮小する（スーパーサンプリング）。その倍率。
_SUPERSAMPLE: int = 4


def downsample(values: np.ndarray, factor: int) -> Image.Image:
    """0〜255 の明るさの配列を ``factor`` 分の 1 に縮小した画像を返す。

    縦横 ``factor`` 画素ずつの平均を取る。``values`` は形状 (H, W) または
    (H, W, 3) で、H と W は ``factor`` で割り切れること。
    """
    h: int = values.shape[0] // factor
    w: int = values.shape[1] // factor
    blocks: np.ndarray = values.reshape(h, factor, w, factor, *values.shape[2:])
    mean: np.ndarray = blocks.mean(axis=(1, 3))
    return Image.fromarray(np.round(mean).astype(np.uint8))


def pixel_grid(size: int, factor: int) -> tuple[np.ndarray, np.ndarray]:
    """``factor`` 倍に拡大した画像の各画素の中心の座標を返す。

    座標は縮小後の画像の画素単位で表す（0〜``size``）。
    """
    coords: np.ndarray = (np.arange(size * factor) + 0.5) / factor
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(coords, coords)
    return xs, ys


def cafe_wall(
    cols: int = 8,
    rows: int = 9,
    tile: int = 48,
    mortar: int = 3,
) -> Image.Image:
    """カフェウォール錯視の図を返す。

    白と黒のタイルを交互に並べた行を、灰色の細い目地で区切って積む。
    行ごとにタイルを 1/4 枚ずつずらし、2 行ごとにずらす向きを
    逆にすると、実際には水平な目地が交互に傾いて見える。
    """
    width: int = cols * tile
    height: int = rows * tile + (rows + 1) * mortar
    img: Image.Image = Image.new("L", (width, height), 128)  # 灰色の目地
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    # 各行のずれ（タイルの 1/4 を単位とする）。0, 1, 2, 1, 0, 1, ... と
    # 往復させる。
    shift_pattern: list[int] = [0, 1, 2, 1]
    for row in range(rows):
        y0: int = mortar + row * (tile + mortar)
        offset: int = shift_pattern[row % 4] * tile // 4
        # 左端にできる隙間を埋めるため、1 枚左から描き始める。
        for col in range(-1, cols + 1):
            x0: int = col * tile + offset
            fill: int = 0 if col % 2 == 0 else 255
            draw.rectangle([x0, y0, x0 + tile - 1, y0 + tile - 1], fill=fill)
    return img


def scintillating_grid(
    size: int = 400,
    cell: int = 50,
    line_width: float = 7.0,
    dot_diameter: float = 11.0,
) -> Image.Image:
    """きらめき格子錯視の図を返す。

    黒い背景に灰色の格子線を引き、交点に白い円を置く。格子全体を
    眺めると、視線を向けていない交点の白い円の中に、黒い点が
    ちらついて見える。
    """
    factor: int = _SUPERSAMPLE
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = pixel_grid(size, factor)

    # 最寄りの格子線（セルの中央を通る線）までの距離。
    dx: np.ndarray = np.abs((xs % cell) - cell / 2)
    dy: np.ndarray = np.abs((ys % cell) - cell / 2)

    values: np.ndarray = np.zeros_like(xs)  # 黒い背景
    on_line: np.ndarray = (dx < line_width / 2) | (dy < line_width / 2)
    values[on_line] = 110.0  # 灰色の格子線
    on_dot: np.ndarray = np.hypot(dx, dy) < dot_diameter / 2
    values[on_dot] = 255.0  # 交点の白い円
    return downsample(values, factor)


def peripheral_drift(
    size: int = 480,
    discs_per_side: int = 2,
    rings: int = 4,
    segments: int = 24,
) -> Image.Image:
    """周辺ドリフト錯視の図を返す。

    円盤を同心円状のリングに分け、各リングを扇形の区画に分ける。
    区画を「黒 → 濃い灰色 → 白 → 薄い灰色」の順で繰り返し塗ると、
    円盤を視野の端で見たとき、この順の向きに回転して見える。
    隣り合うリングで塗る順を逆にすると、リングどうしが逆向きに
    回って見え、効果が強くなる。中心付近は区画が細かくなりすぎる
    ため、リングを置かずに空けておく。
    """
    factor: int = _SUPERSAMPLE
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = pixel_grid(size, factor)

    cell: float = size / discs_per_side
    radius: float = cell * 0.46
    # 各画素が属する円盤の中心からの相対座標。
    px: np.ndarray = xs % cell - cell / 2
    py: np.ndarray = ys % cell - cell / 2
    r: np.ndarray = np.hypot(px, py)
    theta: np.ndarray = np.arctan2(py, px)  # -pi〜pi

    # 中心から半径の 1/5 までを空け、残りを ``rings`` 本のリングに分ける。
    inner: float = radius * 0.2
    ring: np.ndarray = np.floor((r - inner) / (radius - inner) * rings).astype(np.int64)
    # リングごとに区画を半分ずつ回し、区画の境界がそろわないようにする。
    segment: np.ndarray = np.floor(
        (theta + np.pi) / (2 * np.pi) * segments + ring * 0.5
    ).astype(np.int64)
    step: np.ndarray = segment % 4
    # 奇数番目のリングは塗る順を逆にし、逆向きに回って見えるようにする。
    step = np.where(ring % 2 == 1, 3 - step, step)

    # 黒 → 濃い灰色 → 白 → 薄い灰色。
    levels: np.ndarray = np.array([0.0, 90.0, 255.0, 170.0])
    values: np.ndarray = levels[step]
    values[(r >= radius) | (r < inner)] = 128.0  # 円盤の外と中心は中間の灰色
    return downsample(values, factor)


def line_grating(
    xs: np.ndarray, ys: np.ndarray, period: float, angle: float
) -> np.ndarray:
    """角度 ``angle``（ラジアン）の向きに並ぶ、周期 ``period`` の縞を返す。

    戻り値は、黒い線の上にある画素で True になるブール配列。線の
    太さは周期の ``_LINE_RATIO`` 倍。
    """
    # 縞に直交する向きの座標。この値が周期ごとに線と隙間を繰り返す。
    across: np.ndarray = xs * np.cos(angle) + ys * np.sin(angle)
    result: np.ndarray = (across % period) < period * _LINE_RATIO
    return result


def moire_lines(
    size: int = 400, period: float = 8.0, angle_deg: float = 5.0
) -> Image.Image:
    """わずかに回転させた 2 組の縞を重ねたモアレの図を返す。"""
    factor: int = _SUPERSAMPLE
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = pixel_grid(size, factor)
    half: float = np.radians(angle_deg) / 2
    # 黒い線を描いた透明なシートを 2 枚重ねるのと同じく、どちらかの
    # 線がある画素を黒にする。
    black: np.ndarray = line_grating(xs, ys, period, -half) | line_grating(
        xs, ys, period, half
    )
    values: np.ndarray = np.where(black, 0.0, 255.0)
    return downsample(values, factor)


def moire_circles(
    size: int = 400, period: float = 8.0, offset: float = 30.0
) -> Image.Image:
    """中心を少しずらした 2 組の同心円を重ねたモアレの図を返す。"""
    factor: int = _SUPERSAMPLE
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = pixel_grid(size, factor)
    center: float = size / 2
    r1: np.ndarray = np.hypot(xs - (center - offset / 2), ys - center)
    r2: np.ndarray = np.hypot(xs - (center + offset / 2), ys - center)
    black: np.ndarray = ((r1 % period) < period * _LINE_RATIO) | (
        (r2 % period) < period * _LINE_RATIO
    )
    values: np.ndarray = np.where(black, 0.0, 255.0)
    return downsample(values, factor)


def bulge_checkerboard(
    size: int = 400,
    cells: int = 16,
    bulge_radius: float = 150.0,
    power: float = 1.5,
) -> Image.Image:
    """中央が球のように膨らんで見える市松模様を返す。

    中心から半径 ``bulge_radius`` 以内の画素では、市松模様を参照する
    座標を中心へ引き寄せる。中心に近いほど引き寄せる割合が大きい
    ため、中央のマスほど大きく引き伸ばされ、凸レンズで拡大した
    ように見える。さらに、膨らみの縁に向かって少し暗くし、立体感を
    補う。
    """
    factor: int = _SUPERSAMPLE
    xs: np.ndarray
    ys: np.ndarray
    xs, ys = pixel_grid(size, factor)
    center: float = size / 2
    px: np.ndarray = xs - center
    py: np.ndarray = ys - center
    t: np.ndarray = np.hypot(px, py) / bulge_radius  # 膨らみの縁で 1
    inside: np.ndarray = t < 1.0

    # 参照する座標の倍率。中心で 0、縁で 1 になり、縁の外は 1 のまま。
    scale: np.ndarray = np.where(inside, t ** (power - 1.0), 1.0)
    u: np.ndarray = px * scale + center
    v: np.ndarray = py * scale + center

    cell: float = size / cells
    checker: np.ndarray = (
        np.floor(u / cell).astype(np.int64) + np.floor(v / cell).astype(np.int64)
    ) % 2
    dark: np.ndarray = np.array([30.0, 40.0, 90.0])
    light: np.ndarray = np.array([240.0, 225.0, 200.0])
    rgb: np.ndarray = np.where(checker[..., np.newaxis] == 1, light, dark)

    # 膨らみの縁ほど暗くする陰影。
    shade: np.ndarray = np.where(inside, 1.0 - 0.35 * t**2, 1.0)
    rgb = rgb * shade[..., np.newaxis]
    return downsample(rgb, factor)


def main() -> None:
    cafe_wall().save("illusion_cafe_wall.png")
    scintillating_grid().save("illusion_scintillating_grid.png")
    peripheral_drift().save("illusion_peripheral_drift.png")
    moire_lines().save("illusion_moire_lines.png")
    moire_circles().save("illusion_moire_circles.png")
    bulge_checkerboard().save("illusion_bulge.png")


if __name__ == "__main__":
    main()
