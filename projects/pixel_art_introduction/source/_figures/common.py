"""図の生成で共通に使う関数。"""

from pathlib import Path

from PIL import Image, ImageDraw

RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]

WHITE: RGBA = (255, 255, 255, 255)
PANEL: RGBA = (232, 236, 240, 255)
INK: RGB = (34, 32, 52)
PAPER: RGB = (240, 240, 232)


def scale(image: Image.Image, factor: int) -> Image.Image:
    """最近傍補間で整数倍に拡大する。"""
    return image.resize((image.width * factor, image.height * factor), Image.Resampling.NEAREST)


def checker(width: int, height: int, cell: int = 4,
            colors: tuple[RGBA, RGBA] = ((255, 255, 255, 255), (214, 218, 224, 255))) -> Image.Image:
    """透明部分を表す市松模様の画像を作る。"""
    image = Image.new("RGBA", (width, height), colors[0])
    draw = ImageDraw.Draw(image)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            if (x // cell + y // cell) % 2:
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=colors[1])
    return image


def flatten(image: Image.Image, background: RGBA = PANEL) -> Image.Image:
    """透明部分を背景色で塗りつぶした画像を返す。"""
    base = Image.new("RGBA", image.size, background)
    base.alpha_composite(image.convert("RGBA"))
    return base


def on_checker(image: Image.Image, factor: int) -> Image.Image:
    """拡大した画像を市松模様の上に重ねる。"""
    big = scale(image.convert("RGBA"), factor)
    base = checker(big.width, big.height, cell=factor)
    base.alpha_composite(big)
    return base


def with_grid(image: Image.Image, factor: int, color: RGBA = (0, 0, 0, 48)) -> Image.Image:
    """拡大した画像にピクセルの境界線を重ねる。"""
    big = scale(image.convert("RGBA"), factor)
    overlay = Image.new("RGBA", big.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(0, big.width + 1, factor):
        draw.line((min(x, big.width - 1), 0, min(x, big.width - 1), big.height - 1), fill=color)
    for y in range(0, big.height + 1, factor):
        draw.line((0, min(y, big.height - 1), big.width - 1, min(y, big.height - 1)), fill=color)
    big.alpha_composite(overlay)
    return big


def hstack(images: list[Image.Image], gap: int = 24, background: RGBA = WHITE) -> Image.Image:
    """画像を横に並べる（下端をそろえる）。"""
    width = sum(image.width for image in images) + gap * (len(images) - 1)
    height = max(image.height for image in images)
    result = Image.new("RGBA", (width, height), background)
    x = 0
    for image in images:
        result.alpha_composite(image.convert("RGBA"), (x, height - image.height))
        x += image.width + gap
    return result


def vstack(images: list[Image.Image], gap: int = 24, background: RGBA = WHITE) -> Image.Image:
    """画像を縦に並べる（左端をそろえる）。"""
    width = max(image.width for image in images)
    height = sum(image.height for image in images) + gap * (len(images) - 1)
    result = Image.new("RGBA", (width, height), background)
    y = 0
    for image in images:
        result.alpha_composite(image.convert("RGBA"), (0, y))
        y += image.height + gap
    return result


def pad(image: Image.Image, margin: int, background: RGBA) -> Image.Image:
    """周囲に余白を付ける。"""
    result = Image.new("RGBA", (image.width + margin * 2, image.height + margin * 2), background)
    result.alpha_composite(image.convert("RGBA"), (margin, margin))
    return result


def points_image(points: list[tuple[int, int]], margin: int = 1,
                 ink: RGB = INK, paper: RGB = PAPER) -> Image.Image:
    """座標の集合を描いた画像を作る（座標は左下原点、上向きが正）。"""
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    width = max(xs) - min(xs) + 1 + margin * 2
    height = max(ys) - min(ys) + 1 + margin * 2
    image = Image.new("RGBA", (width, height), (*paper, 255))
    for x, y in points:
        image.putpixel((x - min(xs) + margin, max(ys) - y + margin), (*ink, 255))
    return image


def mix(a: RGB, b: RGB, t: float) -> RGB:
    """色 a と色 b を t（0.0 で a、1.0 で b）の割合で混ぜる。"""
    return (round(a[0] + (b[0] - a[0]) * t), round(a[1] + (b[1] - a[1]) * t), round(a[2] + (b[2] - a[2]) * t))


def save(image: Image.Image, out_dir: Path, name: str) -> None:
    """PNG として保存する。"""
    image.save(out_dir / name)
