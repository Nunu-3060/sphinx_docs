"""第 6 章: 24 × 24 のグリッドに沿って線画アイコンを描画する。

アイコンを「グリッド単位」の座標で定義し、任意の大きさで描画します。
次の画像を保存します。

* ch06_icon_keyline.png: グリッドとセーフエリアを重ねて拡大表示したもの
* ch06_icon_antialias.png: 直接描画と、拡大描画してから縮小したものの比較
* icon_<名前>_<大きさ>.png: 各アイコンの PNG (--export を指定したとき)

実行例::

    python ch06_icon_grid.py --outdir output --export
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FontType = ImageFont.FreeTypeFont | ImageFont.ImageFont
Point = tuple[float, float]

GRID = 24  # アイコンの基準となるグリッド数
PADDING = 2  # セーフエリアの外側の余白 (グリッド単位)
STROKE = 2  # 線の太さ (グリッド単位)
ICON_COLOR = "#222222"

FONT_CANDIDATES = [
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]


def load_font(size: int) -> FontType:
    """日本語フォントを読み込む。見つからなければ既定のフォントを返す。"""
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


class IconPen:
    """グリッド単位の座標をピクセルに変換して描画する。"""

    def __init__(self, draw: ImageDraw.ImageDraw, scale: float,
                 offset: Point = (0, 0)) -> None:
        self.draw = draw
        self.scale = scale  # 1 グリッド単位あたりのピクセル数
        self.offset = offset
        self.width = max(1, round(STROKE * scale))

    def px(self, point: Point) -> Point:
        """グリッド座標をピクセル座標に変換する。"""
        return (self.offset[0] + point[0] * self.scale,
                self.offset[1] + point[1] * self.scale)

    def lines(self, points: list[Point]) -> None:
        """折れ線を描く。角は丸める。"""
        self.draw.line([self.px(p) for p in points], fill=ICON_COLOR,
                       width=self.width, joint="curve")

    def rect(self, box: tuple[float, float, float, float],
             radius: float = 0) -> None:
        """四角形の輪郭を描く。radius は角の丸みの半径 (グリッド単位)。"""
        left, top = self.px((box[0], box[1]))
        right, bottom = self.px((box[2], box[3]))
        self.draw.rounded_rectangle((left, top, right, bottom),
                                    radius=radius * self.scale,
                                    outline=ICON_COLOR, width=self.width)

    def circle(self, center: Point, radius: float) -> None:
        """円の輪郭を描く。"""
        cx, cy = center
        self.ellipse((cx - radius, cy - radius, cx + radius, cy + radius))

    def ellipse(self, box: tuple[float, float, float, float]) -> None:
        """楕円の輪郭を描く。box はグリッド座標の (左, 上, 右, 下)。"""
        left, top = self.px((box[0], box[1]))
        right, bottom = self.px((box[2], box[3]))
        self.draw.ellipse((left, top, right, bottom), outline=ICON_COLOR,
                          width=self.width)

    def arc(self, box: tuple[float, float, float, float], start: float,
            end: float) -> None:
        """楕円の弧を描く。角度は 3 時の方向を 0 度とし、時計回り。"""
        left, top = self.px((box[0], box[1]))
        right, bottom = self.px((box[2], box[3]))
        self.draw.arc((left, top, right, bottom), start, end,
                      fill=ICON_COLOR, width=self.width)


# 各アイコンの形は、セーフエリア (2〜22) の中に収まるように定義する
def icon_home(pen: IconPen) -> None:
    """家 (ホーム) のアイコン。"""
    pen.lines([(3, 11), (12, 3), (21, 11)])
    pen.lines([(5.5, 9), (5.5, 21), (18.5, 21), (18.5, 9)])
    pen.lines([(10, 21), (10, 15), (14, 15), (14, 21)])


def icon_search(pen: IconPen) -> None:
    """虫眼鏡 (検索) のアイコン。"""
    pen.circle((10.5, 10.5), 6.5)
    pen.lines([(15.5, 15.5), (21, 21)])


def icon_mail(pen: IconPen) -> None:
    """封筒 (メール) のアイコン。"""
    pen.rect((2, 5, 22, 19), radius=2)
    pen.lines([(3, 6.5), (12, 13), (21, 6.5)])


def icon_user(pen: IconPen) -> None:
    """人物 (ユーザー) のアイコン。"""
    pen.circle((12, 8), 4.5)
    pen.arc((4, 15, 20, 29), 180, 360)


ICONS: dict[str, Callable[[IconPen], None]] = {
    "home": icon_home,
    "search": icon_search,
    "mail": icon_mail,
    "user": icon_user,
}


def render_icon(icon: Callable[[IconPen], None], size: int,
                supersample: int = 8) -> Image.Image:
    """アイコンを size × size ピクセルで描画する。

    supersample 倍の大きさで描画してから縮小し、輪郭を滑らかにする。
    supersample=1 のときは縮小せずにそのまま描画する。
    """
    large = size * supersample
    image = Image.new("RGBA", (large, large), (255, 255, 255, 0))
    icon(IconPen(ImageDraw.Draw(image), large / GRID))
    if supersample == 1:
        return image
    return image.resize((size, size), Image.Resampling.LANCZOS)


def on_white(image: Image.Image) -> Image.Image:
    """透過画像を白背景に合成する。"""
    background = Image.new("RGBA", image.size, "white")
    return Image.alpha_composite(background, image).convert("RGB")


def draw_keyline(scale: int = 10) -> Image.Image:
    """グリッド線とセーフエリアを重ねて、アイコンを拡大表示する。"""
    cell = GRID * scale
    gap, label_h = 24, 36
    width = len(ICONS) * cell + (len(ICONS) + 1) * gap
    sheet = Image.new("RGB", (width, cell + gap * 2 + label_h), "white")
    draw = ImageDraw.Draw(sheet)
    font = load_font(16)

    for i, (name, icon) in enumerate(ICONS.items()):
        left, top = gap + i * (cell + gap), gap
        for k in range(GRID + 1):  # 1 グリッド単位ごとの補助線
            pos = k * scale
            draw.line((left + pos, top, left + pos, top + cell),
                      fill="#e3e8f0")
            draw.line((left, top + pos, left + cell, top + pos),
                      fill="#e3e8f0")
        safe = (left + PADDING * scale, top + PADDING * scale,
                left + (GRID - PADDING) * scale,
                top + (GRID - PADDING) * scale)
        draw.rectangle(safe, outline="#ff6347")  # セーフエリア
        icon(IconPen(draw, scale, offset=(left, top)))
        draw.text((left + cell / 2, top + cell + 28), name, font=font,
                  fill="#555555", anchor="ms")
    return sheet


def draw_antialias_comparison(size: int = 24, zoom: int = 6) -> Image.Image:
    """直接描画と縮小描画を、ピクセルが見えるように拡大して比較する。"""
    font = load_font(16)
    label_w, gap = 260, 16
    cell = size * zoom
    width = label_w + len(ICONS) * (cell + gap)
    sheet = Image.new("RGB", (width, cell * 2 + gap * 3), "white")
    draw = ImageDraw.Draw(sheet)

    rows = [("直接描画 (1 倍)", 1), ("8 倍で描画して縮小", 8)]
    for row, (label, supersample) in enumerate(rows):
        top = gap + row * (cell + gap)
        draw.text((gap, top + cell / 2), label, font=font, fill="#222222",
                  anchor="lm")
        for i, icon in enumerate(ICONS.values()):
            small = on_white(render_icon(icon, size, supersample))
            # NEAREST で拡大すると、1 ピクセルがそのまま四角く見える
            enlarged = small.resize((cell, cell), Image.Resampling.NEAREST)
            sheet.paste(enlarged, (label_w + i * (cell + gap), top))
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--export", action="store_true",
                        help="各アイコンを 24, 48, 96 px の PNG で書き出す")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    draw_keyline().save(outdir / "ch06_icon_keyline.png")
    draw_antialias_comparison().save(outdir / "ch06_icon_antialias.png")
    if args.export:
        for name, icon in ICONS.items():
            for size in (24, 48, 96):
                path = outdir / f"icon_{name}_{size}.png"
                render_icon(icon, size).save(path)
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
