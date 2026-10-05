"""「デジタル画像」の章の図を作るスクリプト。

次の図を作る。

* resolution.png: 同じ円を異なる解像度で表した画像
* channels.png: カラー画像と、その R、G、B のチャンネル
* gamma_blend.png: sRGB の値と線形な値で補間したグラデーション
* alpha_over.png: アルファ値を使った半透明の合成
"""

import numpy as np

from cg_utils import (BoolArray, FloatArray, WHITE, enlarge, hstack,
                      linear_to_srgb, output_dir, save_image,
                      srgb_to_linear)


def pixel_centers(width: int, height: int) -> tuple[FloatArray, FloatArray]:
    """各画素の中心の座標 (x, y) を返す。

    画素 (i, j) の中心は (i + 0.5, j + 0.5) とする。y 軸は下向きである。
    """
    xs, ys = np.meshgrid(np.arange(width) + 0.5, np.arange(height) + 0.5)
    return xs, ys


def disk_mask(size: int, cx: float, cy: float, radius: float) -> BoolArray:
    """画素の中心が円の内側にあれば True となる配列を返す。

    座標は 0.0 から 1.0 に正規化した値で指定する。
    """
    xs, ys = pixel_centers(size, size)
    return np.asarray((xs / size - cx) ** 2 + (ys / size - cy) ** 2
                      <= radius ** 2)


def add_grid(image: FloatArray, scale: int) -> FloatArray:
    """enlarge() で拡大した画像に、画素の境界を示す灰色の線を引く。"""
    result = image.copy()
    result[::scale, :, :] = 0.75
    result[:, ::scale, :] = 0.75
    return result


def resolution_figure() -> FloatArray:
    """同じ円を 8、16、64 画素四方で表した画像を、同じ大きさに拡大して並べる。"""
    display = 256
    panels = []
    for size in (8, 16, 64):
        mask = disk_mask(size, 0.5, 0.5, 0.38)
        image = np.where(mask[..., None], np.array([0.15, 0.35, 0.7]), WHITE)
        scale = display // size
        image = enlarge(image, scale)
        if scale >= 8:
            image = add_grid(image, scale)
        panels.append(image)
    return hstack(panels)


def test_image(width: int, height: int) -> FloatArray:
    """横方向に色相、縦方向に明るさが変わるカラー画像を作る。"""
    xs, ys = pixel_centers(width, height)
    hue = xs / width * 6.0
    # 色相環を 6 つの区間に分け、R、G、B それぞれの値を折れ線で作る。
    r = np.clip(np.abs(hue - 3.0) - 1.0, 0.0, 1.0)
    g = np.clip(2.0 - np.abs(hue - 2.0), 0.0, 1.0)
    b = np.clip(2.0 - np.abs(hue - 4.0), 0.0, 1.0)
    brightness = 1.0 - ys / height
    return np.stack([r, g, b], axis=-1) * brightness[..., None]


def channels_figure() -> FloatArray:
    """カラー画像と、その R、G、B のチャンネルを灰色で表した画像を並べる。"""
    image = test_image(192, 128)
    panels = [image]
    for channel in range(3):
        gray = np.repeat(image[..., channel:channel + 1], 3, axis=-1)
        panels.append(gray)
    return hstack(panels)


def lerp(a: FloatArray, b: FloatArray, t: FloatArray) -> FloatArray:
    """a と b を t : (1 - t) に内分した値を返す(線形補間)。"""
    return np.asarray(a * (1.0 - t) + b * t, dtype=np.float64)


def gamma_blend_figure() -> FloatArray:
    """赤から緑へのグラデーションを、sRGB の値と線形な値で補間して比べる。

    上の帯は sRGB の値をそのまま補間したもの、下の帯は線形な値に変換して
    から補間し、sRGB の値に戻したものである。
    """
    width, height = 512, 64
    red = np.array([1.0, 0.0, 0.0])
    green = np.array([0.0, 1.0, 0.0])
    t = (np.arange(width) + 0.5) / width
    t = t[None, :, None]

    srgb_band = lerp(red, green, t)
    linear_band = linear_to_srgb(
        lerp(srgb_to_linear(red), srgb_to_linear(green), t))

    srgb_band = np.repeat(srgb_band, height, axis=0)
    linear_band = np.repeat(linear_band, height, axis=0)
    gap = np.ones((12, width, 3))
    return np.concatenate([srgb_band, gap, linear_band], axis=0)


def over(fg: FloatArray, alpha: FloatArray, bg: FloatArray) -> FloatArray:
    """前景の色 fg を、アルファ値 alpha で背景 bg の上に重ねる。

    Porter と Duff の over 演算子(前景のアルファ値が乗算済みでない場合)。
    色は線形な値で渡す。
    """
    return np.asarray(fg * alpha + bg * (1.0 - alpha), dtype=np.float64)


def checkerboard(width: int, height: int, cell: int) -> FloatArray:
    """白と灰色の市松模様の画像を作る(線形な値)。"""
    xs, ys = np.meshgrid(np.arange(width) // cell, np.arange(height) // cell)
    light = (xs + ys) % 2 == 0
    value = np.where(light, 0.9, 0.55)
    return np.asarray(srgb_to_linear(np.repeat(value[..., None], 3, axis=-1)))


def alpha_figure() -> FloatArray:
    """市松模様の背景に、アルファ値 0.6 の赤、緑、青の円を順に重ねる。"""
    size = 256
    image = checkerboard(size, size, 16)
    circles = [
        ((0.38, 0.38), np.array([0.9, 0.1, 0.1])),
        ((0.62, 0.38), np.array([0.1, 0.75, 0.2])),
        ((0.5, 0.6), np.array([0.1, 0.25, 0.9])),
    ]
    for (cx, cy), color in circles:
        mask = disk_mask(size, cx, cy, 0.25)
        alpha = np.where(mask, 0.6, 0.0)[..., None]
        image = over(srgb_to_linear(color), alpha, image)
    return linear_to_srgb(image)


def main() -> None:
    out = output_dir()
    save_image(resolution_figure(), out / "resolution.png")
    save_image(channels_figure(), out / "channels.png")
    save_image(gamma_blend_figure(), out / "gamma_blend.png")
    save_image(alpha_figure(), out / "alpha_over.png")


if __name__ == "__main__":
    main()
