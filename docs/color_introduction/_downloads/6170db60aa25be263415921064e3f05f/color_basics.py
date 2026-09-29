"""「色の基礎」の章で使う図を作る。

1. 加法混色と減法混色
2. 色の三属性 (色相・彩度・明度) を HSV で 1 つずつ変化させた帯
3. 同時対比 (同じ色でも背景によって違って見える現象)
"""

import numpy as np

from color_utils import (FloatArray, gray, hex_to_rgb, hsv_to_rgb,
                         labeled_rows, save_image, save_rgb)


def circle_masks(size: int, radius: float,
                 offset: float) -> list[FloatArray]:
    """正三角形の頂点に中心を置いた、3 つの円のマスク (0.0 か 1.0) を作る。"""
    y, x = np.mgrid[0:size, 0:size].astype(float)
    center = size / 2.0
    masks = []
    for angle in (-90.0, 30.0, 150.0):
        cx = center + offset * np.cos(np.deg2rad(angle))
        cy = center + offset * np.sin(np.deg2rad(angle)) + offset * 0.25
        inside = (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2
        masks.append(inside.astype(float))
    return masks


def additive_mixing(size: int = 360) -> FloatArray:
    """黒地に光の三原色 (赤・緑・青) の円を重ね、成分を足し合わせる。"""
    masks = circle_masks(size, radius=size * 0.28, offset=size * 0.17)
    primaries = [hex_to_rgb("#ff0000"), hex_to_rgb("#00ff00"),
                 hex_to_rgb("#0000ff")]
    image = np.zeros((size, size, 3))
    for mask, color in zip(masks, primaries):
        image += mask[..., np.newaxis] * color
    return np.clip(image, 0.0, 1.0)


def subtractive_mixing(size: int = 360) -> FloatArray:
    """白地に色材の三原色 (シアン・マゼンタ・イエロー) の円を重ねる。

    色材は光の一部を吸収するので、重なった部分では反射率を掛け合わせる。
    """
    masks = circle_masks(size, radius=size * 0.28, offset=size * 0.17)
    primaries = [hex_to_rgb("#00ffff"), hex_to_rgb("#ff00ff"),
                 hex_to_rgb("#ffff00")]
    image = np.ones((size, size, 3))
    for mask, color in zip(masks, primaries):
        # マスクの外側では反射率 1.0 (何も吸収しない) として掛ける。
        image *= 1.0 - mask[..., np.newaxis] * (1.0 - color)
    return image


def attribute_strip(hue: FloatArray | float, saturation: FloatArray | float,
                    value: FloatArray | float, height: int = 48) -> FloatArray:
    """HSV の値 (幅方向の 1 次元配列を含む) から帯状の画像を作る。"""
    row = hsv_to_rgb(hue, saturation, value)
    return np.repeat(row[np.newaxis, :, :], height, axis=0)


def contrast_panel(target: FloatArray, background: FloatArray,
                   size: int = 200) -> FloatArray:
    """背景色の中央に、小さな正方形の色 ``target`` を置いた図。"""
    panel = np.tile(background, (size, size, 1))
    margin = size * 3 // 8
    panel[margin:size - margin, margin:size - margin] = target
    return panel


def simultaneous_contrast() -> FloatArray:
    """同じ灰色と同じ橙色を、明るさや色相の異なる背景に置いて並べる。"""
    spacer = np.ones((200, 16, 3))
    middle_gray = gray(0.5)
    orange = hex_to_rgb("#e08a3c")
    panels = [
        contrast_panel(middle_gray, gray(0.1)),
        spacer,
        contrast_panel(middle_gray, gray(0.9)),
        spacer, spacer,
        contrast_panel(orange, hex_to_rgb("#b22222")),
        spacer,
        contrast_panel(orange, hex_to_rgb("#2a5caa")),
    ]
    return np.concatenate(panels, axis=1)


def main() -> None:
    """本章の図を作り、保存する。"""
    spacer = np.ones((360, 24, 3))
    mixing = np.concatenate(
        [additive_mixing(), spacer, subtractive_mixing()], axis=1)
    save_rgb(mixing, "mixing.png")

    # 色相・彩度・明度のうち 1 つだけを左から右へ変化させる。
    ramp = np.linspace(0.0, 1.0, 720)
    attributes = labeled_rows([
        ("Hue", attribute_strip(ramp, 1.0, 1.0)),
        ("Saturation", attribute_strip(0.58, ramp, 1.0)),
        ("Value", attribute_strip(0.58, 1.0, ramp)),
    ], label_width=130)
    save_image(attributes, "hsv_attributes.png")

    save_rgb(simultaneous_contrast(), "simultaneous_contrast.png")


if __name__ == "__main__":
    main()
