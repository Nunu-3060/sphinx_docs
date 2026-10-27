"""色相をずらしたカラーランプ（明度順に並べた色の列）を作る。

暗い色ほど色相を寒色側（青）へ、明るい色ほど暖色側（黄）へずらす。
色見本の PNG と、GIMP や Aseprite で読み込める GPL 形式のパレットを保存する。

使い方::

    python make_palette.py                    # 緑（色相 120 度）の 5 段階
    python make_palette.py --hue 0 --steps 7  # 赤の 7 段階
    python make_palette.py --shift 0          # 色相をずらさない場合
"""

import argparse
import colorsys
from pathlib import Path

from PIL import Image, ImageDraw

RGB = tuple[int, int, int]


def shift_hue_toward(hue: float, target: float, amount: float) -> float:
    """色相 hue（度）を target（度）に向かって最大 amount 度だけ近づける。"""
    diff = (target - hue + 180.0) % 360.0 - 180.0  # -180 から 180 の範囲の差
    if abs(diff) <= amount:
        return target % 360.0
    return (hue + amount * (1 if diff > 0 else -1)) % 360.0


def make_ramp(hue: float, steps: int, shift: float = 20.0,
              value_range: tuple[float, float] = (0.25, 0.95),
              saturation_range: tuple[float, float] = (0.35, 0.75)) -> list[RGB]:
    """暗い色から明るい色へ並んだカラーランプを返す。

    Args:
        hue: 中央の色の色相（度）
        steps: 色数（2 以上）
        shift: 両端の色で色相をずらす量（度）。0 にすると色相は一定になる。
        value_range: 明度の最小値と最大値（0.0 から 1.0）
        saturation_range: 彩度の最小値と最大値（0.0 から 1.0）
    """
    if steps < 2:
        raise ValueError("色数は 2 以上にする")
    colors: list[RGB] = []
    for i in range(steps):
        t = i / (steps - 1)  # 0.0（最も暗い）から 1.0（最も明るい）
        # 中央からの距離に比例して、暗い側は青（240 度）、明るい側は黄（60 度）へ近づける
        if t < 0.5:
            h = shift_hue_toward(hue, 240.0, shift * (0.5 - t) * 2)
        else:
            h = shift_hue_toward(hue, 60.0, shift * (t - 0.5) * 2)
        # 彩度は中央で最大、両端で低くする
        s_min, s_max = saturation_range
        s = s_max - (s_max - s_min) * abs(t - 0.5) * 2
        v_min, v_max = value_range
        v = v_min + (v_max - v_min) * t
        r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
        colors.append((round(r * 255), round(g * 255), round(b * 255)))
    return colors


def to_hex(color: RGB) -> str:
    """色を #rrggbb 形式の文字列にする。"""
    return "#{:02x}{:02x}{:02x}".format(*color)


def save_swatch(colors: list[RGB], path: Path, cell: int = 32) -> None:
    """色見本の画像を保存する。"""
    image = Image.new("RGB", (cell * len(colors), cell))
    draw = ImageDraw.Draw(image)
    for i, color in enumerate(colors):
        draw.rectangle((i * cell, 0, (i + 1) * cell - 1, cell - 1), fill=color)
    image.save(path)


def save_gpl(colors: list[RGB], path: Path, name: str) -> None:
    """GIMP パレット形式（.gpl）で保存する。"""
    lines = ["GIMP Palette", f"Name: {name}", "Columns: 0", "#"]
    lines += [f"{r:3d} {g:3d} {b:3d}\t{to_hex((r, g, b))}" for r, g, b in colors]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="色相をずらしたカラーランプを作る")
    parser.add_argument("--hue", type=float, default=120.0, help="中央の色の色相（度、既定値: 120）")
    parser.add_argument("--steps", type=int, default=5, help="色数（既定値: 5）")
    parser.add_argument("--shift", type=float, default=20.0, help="色相をずらす量（度、既定値: 20）")
    args = parser.parse_args()

    colors = make_ramp(args.hue, args.steps, args.shift)
    for color in colors:
        print(to_hex(color), color)

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    save_swatch(colors, output_dir / "ramp.png")
    save_gpl(colors, output_dir / "ramp.gpl", "ramp")
    print(f"保存した: {output_dir / 'ramp.png'}, {output_dir / 'ramp.gpl'}")


if __name__ == "__main__":
    main()
