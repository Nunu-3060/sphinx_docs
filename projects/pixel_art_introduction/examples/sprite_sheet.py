"""アニメーションのフレームをスプライトシートにまとめ、GIF アニメーションも書き出す。

使い方::

    python sprite_sheet.py                   # サンプルの歩行アニメーションを使う
    python sprite_sheet.py --duration 250    # 1 フレームの表示時間を 250 ミリ秒にする
"""

import argparse
from pathlib import Path

from PIL import Image

from scale_nearest import scale_nearest
from sprite_data import hero_walk_images

RGBA = tuple[int, int, int, int]


def make_sheet(frames: list[Image.Image], columns: int) -> Image.Image:
    """同じ大きさのフレームを columns 列で並べたスプライトシートを作る。"""
    width, height = frames[0].size
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new("RGBA", (width * columns, height * rows), (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        if frame.size != (width, height):
            raise ValueError("すべてのフレームを同じ大きさにする")
        sheet.paste(frame, ((index % columns) * width, (index // columns) * height))
    return sheet


def split_sheet(sheet: Image.Image, width: int, height: int) -> list[Image.Image]:
    """スプライトシートを左上から右へ、上から下へ順に切り出す。"""
    frames: list[Image.Image] = []
    for top in range(0, sheet.height, height):
        for left in range(0, sheet.width, width):
            frames.append(sheet.crop((left, top, left + width, top + height)))
    return frames


def save_gif(frames: list[Image.Image], path: Path, duration: int, scale: int,
             background: RGBA = (232, 236, 240, 255)) -> None:
    """フレームを背景色の上に重ね、拡大して GIF アニメーションとして保存する。

    GIF は半透明を扱えないため、ここでは背景色と合成してから保存する。
    """
    images: list[Image.Image] = []
    for frame in frames:
        canvas = Image.new("RGBA", frame.size, background)
        canvas.alpha_composite(frame.convert("RGBA"))
        images.append(scale_nearest(canvas, scale).convert("RGB"))
    images[0].save(path, save_all=True, append_images=images[1:], duration=duration, loop=0)


def main() -> None:
    parser = argparse.ArgumentParser(description="スプライトシートと GIF アニメーションを作る")
    parser.add_argument("--duration", type=int, default=150, help="1 フレームの表示時間（ミリ秒、既定値: 150）")
    parser.add_argument("--scale", type=int, default=6, help="GIF の倍率（既定値: 6）")
    args = parser.parse_args()

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    frames = hero_walk_images()
    sheet = make_sheet(frames, columns=len(frames))
    sheet.save(output_dir / "hero_walk_sheet.png")

    # 保存したシートを読み直して切り出し、GIF にする
    loaded = Image.open(output_dir / "hero_walk_sheet.png")
    width, height = frames[0].size
    save_gif(split_sheet(loaded, width, height), output_dir / "hero_walk.gif", args.duration, args.scale)
    print(f"保存した: {output_dir / 'hero_walk_sheet.png'}, {output_dir / 'hero_walk.gif'}")


if __name__ == "__main__":
    main()
