"""色相(Hue)を軸にした配色パレットの生成と、画像からの配色抽出。

HSB(HSV)色空間では色相を環状の値として扱えるため、基準の色相に
オフセットを加えるだけで「類似色」「補色」「トライアド」
「スプリットコンプリメンタリー」といった配色パターンを機械的に
生成できる。標準ライブラリの ``colorsys`` には頼らず、HSV->RGB変換
そのものをNumPyでベクトル化して自前実装した上で、次の3つを実装する。

1. 色相スキームに基づくパレット生成とスウォッチ画像の描画
2. 2色間をHSB空間で滑らかに補間するグラデーションの生成
   （色相環の短い弧を通るように補間する）
3. 既存の画像から ``Image.quantize`` で支配的な色を抽出し、
   パレットとして描画する
"""

from collections.abc import Sequence
from typing import cast

import numpy as np
from PIL import Image

SWATCH_SIZE: int = 128


def hsv_to_rgb(
    hue: np.ndarray | float,
    saturation: np.ndarray | float,
    value: np.ndarray | float,
) -> np.ndarray:
    """HSV(色相・彩度・明度)を六角錐モデルに基づきRGBへ変換する。

    hue・saturation・value はいずれもスカラーか、互いにブロード
    キャスト可能なNumPy配列で、すべて 0.0-1.0 の範囲（色相は1周=1.0の
    環状の値）として扱う。戻り値は入力の形状の末尾にRGB用の軸
    (長さ3、値は0.0-1.0)を追加した形状の配列になる。
    """
    h: np.ndarray
    s: np.ndarray
    v: np.ndarray
    h, s, v = np.broadcast_arrays(
        np.asarray(hue, dtype=float) % 1.0,
        np.asarray(saturation, dtype=float),
        np.asarray(value, dtype=float),
    )

    chroma: np.ndarray = v * s
    h_prime: np.ndarray = h * 6.0
    x: np.ndarray = chroma * (1.0 - np.abs(h_prime % 2.0 - 1.0))
    m: np.ndarray = v - chroma
    zero: np.ndarray = np.zeros_like(chroma)

    # h_prime の整数部が 0-5 のどの区間(60度ごとの6区間)に
    # 入るかで、(chroma, x, 0) をどの成分に割り当てるかが変わる。
    sector: np.ndarray = np.floor(h_prime).astype(np.int64) % 6
    conditions: list[np.ndarray] = [sector == i for i in range(6)]

    r: np.ndarray = np.select(
        conditions, [chroma, x, zero, zero, x, chroma]
    )
    g: np.ndarray = np.select(
        conditions, [x, chroma, chroma, x, zero, zero]
    )
    b: np.ndarray = np.select(
        conditions, [zero, zero, x, chroma, chroma, x]
    )

    return np.stack([r, g, b], axis=-1) + m[..., np.newaxis]


def _hsv_to_rgb255(
    hue: float, saturation: float, value: float
) -> tuple[int, int, int]:
    """0.0-1.0のHSV値を0-255のRGBタプルに変換する。"""
    rgb: np.ndarray = (hsv_to_rgb(hue, saturation, value) * 255).round()
    r, g, b = rgb.astype(int)
    return (int(r), int(g), int(b))


def hue_scheme(
    base_hue: float,
    offsets: Sequence[float],
    saturation: float = 0.75,
    value: float = 0.9,
) -> list[tuple[int, int, int]]:
    """基準色相 base_hue に offsets を加えた色相群をRGBパレットとして返す。

    base_hue と offsets はすべて 0.0-1.0 (1周=1.0) で表す。offsets の
    与え方を変えるだけで、類似色・補色・トライアドなど任意の配色
    パターンを表現できる。
    """
    return [
        _hsv_to_rgb255(base_hue + offset, saturation, value)
        for offset in offsets
    ]


def analogous_palette(
    base_hue: float, count: int = 5, spread: float = 0.12
) -> list[tuple[int, int, int]]:
    """base_hue を中心に ±spread の範囲へ均等割りした類似色パレット。"""
    offsets: np.ndarray = np.linspace(-spread, spread, count)
    return hue_scheme(base_hue, offsets.tolist())


def complementary_palette(base_hue: float) -> list[tuple[int, int, int]]:
    """base_hue とその補色(色相環上で180度反対)の2色パレット。"""
    return hue_scheme(base_hue, [0.0, 0.5])


def split_complementary_palette(
    base_hue: float, split: float = 1 / 12
) -> list[tuple[int, int, int]]:
    """base_hue と、その補色の両隣2色から成る3色パレット。

    補色そのものを使うより穏やかな対比になる。
    """
    return hue_scheme(base_hue, [0.0, 0.5 - split, 0.5 + split])


def triadic_palette(base_hue: float) -> list[tuple[int, int, int]]:
    """色相環を三等分した3色パレット(トライアド配色)。"""
    return hue_scheme(base_hue, [0.0, 1 / 3, 2 / 3])


# PCCS(日本色彩研究所の実用配色体系)が定義する12のトーン。
# それぞれ「鮮やかさ・明るさの印象」を彩度・明度の組み合わせとして
# 代表させたもので、PCCSの図版と同じく4列3行のグリッドで
# 並べられる順に定義している(vivid〜deepが上段、light〜darkが
# 中段、pale〜dark_grayishが下段)。
PCCS_TONES: dict[str, tuple[float, float]] = {
    "vivid": (1.00, 0.90),
    "bright": (0.75, 0.95),
    "strong": (0.85, 0.75),
    "deep": (0.90, 0.55),
    "light": (0.55, 0.95),
    "soft": (0.50, 0.75),
    "dull": (0.45, 0.60),
    "dark": (0.60, 0.35),
    "pale": (0.25, 0.95),
    "light_grayish": (0.15, 0.80),
    "grayish": (0.15, 0.55),
    "dark_grayish": (0.15, 0.30),
}


def tone_on_tone_palette(
    base_hue: float, tones: Sequence[str] = tuple(PCCS_TONES)
) -> list[tuple[int, int, int]]:
    """base_hue を固定し、PCCSのトーンを変えた配色パレット(トーンオントーン)。

    色相をそろえたまま彩度・明度だけを変化させるため、統一感の
    ある濃淡・調子のバリエーションになる。
    """
    return [
        _hsv_to_rgb255(base_hue, *PCCS_TONES[tone]) for tone in tones
    ]


def tone_in_tone_palette(
    tone: str, hues: Sequence[float]
) -> list[tuple[int, int, int]]:
    """PCCSのトーン(彩度・明度)を固定し、色相を変えた配色パレット
    (トーンイントーン)。

    色相はばらばらでも、彩度・明度の組み合わせ(トーン)がそろって
    いるため、「淡い」「くすんだ」といった印象は統一される。
    """
    saturation, value = PCCS_TONES[tone]
    return [_hsv_to_rgb255(hue, saturation, value) for hue in hues]


def render_swatches(
    palette: Sequence[tuple[int, int, int]], swatch_size: int = SWATCH_SIZE
) -> Image.Image:
    """パレットを横並びの正方形として描画したスウォッチ画像を返す。"""
    width: int = swatch_size * len(palette)
    pixels: np.ndarray = np.zeros((swatch_size, width, 3), dtype=np.uint8)
    for i, color in enumerate(palette):
        left: int = i * swatch_size
        right: int = left + swatch_size
        pixels[:, left:right] = color
    return Image.fromarray(pixels)


def render_grid(
    palette: Sequence[tuple[int, int, int]],
    columns: int,
    swatch_size: int = SWATCH_SIZE,
) -> Image.Image:
    """パレットを指定した列数のグリッドとして描画したスウォッチ画像を返す。

    PCCSのトーン一覧のように、行と列に意味がある配色を並べる用途を
    想定している。
    """
    rows: int = -(-len(palette) // columns)  # 切り上げ除算
    width: int = swatch_size * columns
    height: int = swatch_size * rows
    pixels: np.ndarray = np.full((height, width, 3), 255, dtype=np.uint8)
    for i, color in enumerate(palette):
        row, col = divmod(i, columns)
        top: int = row * swatch_size
        left: int = col * swatch_size
        pixels[top:top + swatch_size, left:left + swatch_size] = color
    return Image.fromarray(pixels)


def _stack_vertically(
    images: Sequence[Image.Image],
    gap: int = 8,
    background: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """複数の画像を、左端をそろえて縦に並べた1枚の画像にまとめる。"""
    max_width: int = max(image.width for image in images)
    total_height: int = (
        sum(image.height for image in images) + gap * (len(images) - 1)
    )
    canvas: Image.Image = Image.new(
        "RGB", (max_width, total_height), background
    )
    y: int = 0
    for image in images:
        canvas.paste(image, (0, y))
        y += image.height + gap
    return canvas


def hsb_gradient(
    start_hue: float,
    end_hue: float,
    saturation: float = 0.75,
    value: float = 0.9,
    steps: int = 256,
    shortest_path: bool = True,
) -> np.ndarray:
    """start_hue から end_hue へ色相を補間したグラデーションを返す。

    ``shortest_path=True`` (既定) では、色相環上で近い側(短い弧)を
    通るように差分を [-0.5, 0.5) に正規化してから補間する。False に
    すると 0.0-1.0 の数値としてそのまま線形補間するため、例えば
    赤(0.98)から橙(0.05)へは、本来はすぐ隣の色なのに色相環を
    ほぼ一周する遠回りのグラデーションになってしまう。

    戻り値は形状 (steps, 3) の uint8 配列。
    """
    t: np.ndarray = np.linspace(0.0, 1.0, steps)
    hues: np.ndarray
    if shortest_path:
        delta: float = (end_hue - start_hue + 0.5) % 1.0 - 0.5
        hues = (start_hue + delta * t) % 1.0
    else:
        hues = start_hue + (end_hue - start_hue) * t

    rgb: np.ndarray = hsv_to_rgb(hues, saturation, value)
    return (rgb * 255).round().astype(np.uint8)


def render_gradient(gradient: np.ndarray, height: int = 80) -> Image.Image:
    """(steps, 3) のグラデーション配列を横方向の帯画像として描画する。"""
    band: np.ndarray = np.tile(gradient[np.newaxis, :, :], (height, 1, 1))
    return Image.fromarray(band, mode="RGB")


def extract_palette(
    image_path: str, count: int = 8
) -> list[tuple[int, int, int]]:
    """画像を count 色に量子化し、支配的な色を出現頻度順に返す。

    PIL の適応パレット量子化 (median cut) で画像全体を count 色に
    減色し、実際に使われているピクセル数が多い色から順に並べる。
    """
    source: Image.Image = Image.open(image_path).convert("RGB")
    quantized: Image.Image = source.quantize(
        colors=count, method=Image.Quantize.MEDIANCUT
    )

    # パレットモード("P")の画像は必ず自身のパレットと出現数を持ち、
    # 色ごとの識別子は常にパレット内の整数インデックスになる。
    palette_raw: list[int] | None = quantized.getpalette()
    counts_raw = quantized.getcolors(maxcolors=count)
    assert palette_raw is not None
    assert counts_raw is not None
    palette: list[int] = palette_raw
    counts: list[tuple[int, int]] = cast(
        list[tuple[int, int]], counts_raw
    )
    counts.sort(key=lambda item: item[0], reverse=True)

    colors: list[tuple[int, int, int]] = []
    for _, index in counts:
        r, g, b = palette[index * 3:index * 3 + 3]
        colors.append((r, g, b))
    return colors


def main() -> None:
    base_hue: float = 0.55  # 水色寄りの青を基準色相にする

    scheme_image: Image.Image = _stack_vertically(
        [
            render_swatches(analogous_palette(base_hue)),
            render_swatches(complementary_palette(base_hue)),
            render_swatches(split_complementary_palette(base_hue)),
            render_swatches(triadic_palette(base_hue)),
        ]
    )
    scheme_image.save("hsb_palette.png")

    gradient_image: Image.Image = _stack_vertically(
        [
            render_gradient(
                hsb_gradient(0.98, 0.08, shortest_path=False)
            ),
            render_gradient(
                hsb_gradient(0.98, 0.08, shortest_path=True)
            ),
        ],
        gap=4,
    )
    gradient_image.save("gradient.png")

    tone_on_tone_image: Image.Image = render_grid(
        tone_on_tone_palette(base_hue), columns=4
    )
    tone_on_tone_image.save("tone_on_tone.png")

    tone_in_tone_hues: list[float] = np.linspace(
        0.0, 1.0, 6, endpoint=False
    ).tolist()
    tone_in_tone_image: Image.Image = render_swatches(
        tone_in_tone_palette("soft", tone_in_tone_hues)
    )
    tone_in_tone_image.save("tone_in_tone.png")

    extracted: list[tuple[int, int, int]] = extract_palette(
        "source/_static/gallery/julia.png", count=8
    )
    render_swatches(extracted).save("extracted_palette.png")


if __name__ == "__main__":
    main()
