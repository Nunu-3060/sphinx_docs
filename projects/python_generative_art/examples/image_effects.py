"""既存の画像を素材にした生成技法: ハーフトーン・ディザリング・ピクセルソート。

:doc:`../color` の ``extract_palette`` は、既存の画像から配色を
抜き出して別の作品の材料にする、という発想の例だった。ここでは
一歩進んで、既存の画像そのものを直接加工して新しい見た目を作る
3つの技法を扱う。いずれも「ゼロから座標や乱数で生成する」これまでの
章とは異なり、入力画像の明るさや色を単純な規則で変換するだけで、
元の画像には無かった質感が生まれる点が共通している。
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def halftone(
    image: Image.Image,
    cell_size: int,
    ink_color: tuple[int, int, int] = (20, 20, 20),
    background: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """新聞印刷の網点(ハーフトーン)のように、濃淡を点の大きさで表す。

    画像を ``cell_size`` 四方のセルに分割し、セルごとの平均輝度を
    求める。暗いセルほど大きな円を、明るいセルほど小さな円を中心に
    描くと、遠目には元の濃淡が、近づくと規則正しい点の並びが見える
    網点表現になる。
    """
    gray: np.ndarray = np.asarray(image.convert("L"), dtype=np.float64)
    height, width = gray.shape
    out: Image.Image = Image.new("RGB", (width, height), background)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(out)

    max_radius: float = cell_size / 2.0 * 0.95
    for y0 in range(0, height, cell_size):
        for x0 in range(0, width, cell_size):
            cell: np.ndarray = gray[y0:y0 + cell_size, x0:x0 + cell_size]
            darkness: float = 1.0 - float(cell.mean()) / 255.0
            radius: float = max_radius * darkness
            if radius < 0.5:
                continue
            cx: float = x0 + cell.shape[1] / 2.0
            cy: float = y0 + cell.shape[0] / 2.0
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                fill=ink_color,
            )

    return out


def floyd_steinberg_dither(
    image: Image.Image, levels: int = 2
) -> Image.Image:
    """誤差拡散法(Floyd-Steinberg)で階調数を減らす。

    各画素を最も近い ``levels`` 段階の輝度に丸め、丸めで生じた誤差を
    右・左下・下・右下の未処理画素へ ``7/16, 3/16, 5/16, 1/16`` の
    比率で配り歩く。単純な丸め(誤差を捨てる)と違い、誤差を周囲に
    伝播させることで、少ない階調数でも視覚的には元の濃淡が保たれた
    ように見える(誤差が近傍のドット密度の変化として表れるため)。
    行ごとに左から右へ処理する逐次アルゴリズムのため、ここでは
    NumPyでベクトル化せず、素直にPythonのループで実装している。
    """
    gray: np.ndarray = np.asarray(image.convert("L"), dtype=np.float64).copy()
    height, width = gray.shape
    step: float = 255.0 / (levels - 1)

    for y in range(height):
        for x in range(width):
            old_value: float = gray[y, x]
            new_value: float = round(old_value / step) * step
            gray[y, x] = new_value
            error: float = old_value - new_value

            if x + 1 < width:
                gray[y, x + 1] += error * 7 / 16
            if y + 1 < height:
                if x > 0:
                    gray[y + 1, x - 1] += error * 3 / 16
                gray[y + 1, x] += error * 5 / 16
                if x + 1 < width:
                    gray[y + 1, x + 1] += error * 1 / 16

    return Image.fromarray(np.clip(gray, 0, 255).astype(np.uint8), "L")


def pixel_sort(
    image: Image.Image, low: float = 90.0, high: float = 180.0
) -> Image.Image:
    """行ごとに、輝度が一定範囲内にある画素だけを明るさ順に並べ替える。

    各行について、輝度が ``[low, high]`` の範囲に収まる連続した区間を
    見つけ、その区間の中だけを画素の輝度順にソートする。範囲外の画素
    (非常に暗い/明るい部分)はソートの境界として手つかずのまま残すため、
    画像全体が縦縞状に流れたような、グリッチアート特有の見た目になる。
    """
    rgb: np.ndarray = np.asarray(image.convert("RGB"), dtype=np.uint8).copy()
    gray: np.ndarray = np.asarray(image.convert("L"), dtype=np.float64)
    height, width, _ = rgb.shape

    for y in range(height):
        mask: np.ndarray = (gray[y] >= low) & (gray[y] <= high)
        x: int = 0
        while x < width:
            if not mask[x]:
                x += 1
                continue
            start: int = x
            while x < width and mask[x]:
                x += 1
            end: int = x
            segment: np.ndarray = rgb[y, start:end]
            order: np.ndarray = np.argsort(gray[y, start:end])
            rgb[y, start:end] = segment[order]

    return Image.fromarray(rgb, "RGB")


def main() -> None:
    gallery: Path = Path("source/_static/gallery")

    noise_image: Image.Image = Image.open(gallery / "perlin_noise.png")
    halftone(noise_image, cell_size=8).save("halftone.png")

    dithered: Image.Image = floyd_steinberg_dither(noise_image, levels=2)
    dithered.save("dither_2level.png")

    coral_image: Image.Image = Image.open(
        gallery / "reaction_diffusion_coral.png"
    )
    pixel_sort(coral_image, low=75.0, high=200.0).save("pixel_sort.png")


if __name__ == "__main__":
    main()
