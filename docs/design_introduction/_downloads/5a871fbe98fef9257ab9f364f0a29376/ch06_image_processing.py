"""第 6 章: 資料や UI に写真を載せるときの基本的な加工を行う。

次の画像を保存します。

* ch06_crop.png: 中央で切り抜いた場合と、主題の位置を指定した場合の比較
* ch06_resample.png: 縮小時の補間方法 (NEAREST と LANCZOS) の比較
* ch06_overlay.png: 写真に文字を重ねるときの、スクリムの有無の比較

入力画像を指定しない場合は、matplotlib に同梱されているサンプル画像
(grace_hopper.jpg) を使います。

実行例::

    python ch06_image_processing.py --outdir output
    python ch06_image_processing.py --input photo.jpg --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from matplotlib import cbook
from PIL import Image, ImageDraw, ImageFont, ImageOps

FontType = ImageFont.FreeTypeFont | ImageFont.ImageFont

BOLD_FONTS = [
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/meiryob.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]


def load_font(size: int) -> FontType:
    """日本語の太字フォントを読み込む。見つからなければ既定のフォントを返す。"""
    for path in BOLD_FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def load_sample_image() -> Image.Image:
    """matplotlib に同梱されているサンプル画像を読み込む。"""
    path = cbook.get_sample_data("grace_hopper.jpg", asfileobj=False)
    return Image.open(str(path)).convert("RGB")


def add_caption(image: Image.Image, text: str) -> Image.Image:
    """画像の下に説明文の帯を追加する。"""
    band = 40
    result = Image.new("RGB", (image.width, image.height + band), "white")
    result.paste(image, (0, 0))
    draw = ImageDraw.Draw(result)
    draw.text((image.width / 2, image.height + band / 2), text,
              font=load_font(16), fill="#222222", anchor="mm")
    return result


def hstack(images: list[Image.Image], gap: int = 16) -> Image.Image:
    """画像を上端を揃えて横に並べる。"""
    width = sum(im.width for im in images) + gap * (len(images) - 1)
    height = max(im.height for im in images)
    result = Image.new("RGB", (width, height), "white")
    x = 0
    for im in images:
        result.paste(im, (x, 0))
        x += im.width + gap
    return result


def crop_comparison(photo: Image.Image) -> Image.Image:
    """16:9 に切り抜くとき、centering の指定で結果がどう変わるかを示す。

    ImageOps.fit の centering は、切り抜く位置を (横, 縦) の比率
    (0〜1) で指定する。(0.5, 0.5) は中央、縦 0.0 は上端に寄せる。
    """
    size = (384, 216)
    center = ImageOps.fit(photo, size, centering=(0.5, 0.5))
    upper = ImageOps.fit(photo, size, centering=(0.5, 0.2))
    return hstack([add_caption(center, "centering=(0.5, 0.5)"),
                   add_caption(upper, "centering=(0.5, 0.2)")])


def zone_plate(size: int = 512) -> Image.Image:
    """中心から外側へ向かうほど縞が細かくなる同心円の画像を作る。

    縮小時の折り返しひずみ (エイリアシング) を確認するための図形。
    """
    y, x = np.mgrid[-1:1:size * 1j, -1:1:size * 1j]
    values = 0.5 + 0.5 * np.cos(np.pi * size / 4 * (x ** 2 + y ** 2))
    return Image.fromarray((values * 255).astype(np.uint8))


def resample_comparison() -> Image.Image:
    """1/4 に縮小したときの、補間方法による違いを示す。"""
    source = zone_plate()
    small = (source.width // 4, source.height // 4)
    results = []
    for name, method in [("NEAREST", Image.Resampling.NEAREST),
                         ("LANCZOS", Image.Resampling.LANCZOS)]:
        reduced = source.resize(small, method)
        # 違いが見えるように、縮小した結果を 2 倍に拡大して表示する
        shown = reduced.resize((small[0] * 2, small[1] * 2),
                               Image.Resampling.NEAREST)
        results.append(add_caption(shown.convert("RGB"), name))
    return hstack(results)


def add_scrim(image: Image.Image, height_ratio: float = 0.5,
              max_alpha: int = 200) -> Image.Image:
    """画像の下側に、下へ向かって濃くなる黒のグラデーションを重ねる。"""
    width, height = image.size
    start = int(height * (1 - height_ratio))
    alpha = np.zeros((height, width), dtype=np.uint8)
    ramp = np.linspace(0, max_alpha, height - start).astype(np.uint8)
    alpha[start:, :] = ramp[:, np.newaxis]
    scrim = Image.new("RGBA", image.size, (0, 0, 0, 0))
    scrim.putalpha(Image.fromarray(alpha))
    return Image.alpha_composite(image.convert("RGBA"), scrim).convert("RGB")


def overlay_comparison(photo: Image.Image) -> Image.Image:
    """写真の上に白い文字を重ねる。スクリムの有無で読みやすさを比べる。"""
    base = ImageOps.fit(photo, (384, 216), centering=(0.5, 0.5))
    font = load_font(26)
    results = []
    for label, use_scrim in [("文字を直接重ねる", False),
                             ("スクリムを重ねる", True)]:
        image = add_scrim(base) if use_scrim else base.copy()
        draw = ImageDraw.Draw(image)
        draw.text((20, image.height - 20), "プログラミングの先駆者",
                  font=font, fill="white", anchor="ls")
        results.append(add_caption(image, label))
    return hstack(results)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--input", type=Path, default=None,
                        help="加工する画像ファイル (省略時はサンプル画像)")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    if args.input is None:
        photo = load_sample_image()
    else:
        photo = Image.open(args.input).convert("RGB")
    crop_comparison(photo).save(outdir / "ch06_crop.png")
    resample_comparison().save(outdir / "ch06_resample.png")
    overlay_comparison(photo).save(outdir / "ch06_overlay.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
