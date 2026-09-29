"""「実践: UI の配色設計」の章で使う図と数値を作る。

1. 基準の色から作ったカラースケール (50 から 900 までの 10 段階)
2. カラースケールから選んだ色で組み立てた、ライトテーマとダークテーマ
3. テーマの色の組み合わせのコントラスト比の確認 (標準出力に表示する)
4. 明るいブランドカラーをカラースケールに組み込む例
"""

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, contrast_ratio, font, hex_to_rgb,
                         oklab_lightness, rgb_to_hex, save_image, to_uint8)
from palette import oklch_scale

# カラースケールの段階の名前。数値が大きいほど暗い。
STEP_NAMES = ["50", "100", "200", "300", "400",
              "500", "600", "700", "800", "900"]

Theme = dict[str, FloatArray]


def make_scale(base_code: str) -> dict[str, FloatArray]:
    """基準の色から 10 段階のカラースケールを作り、段階の名前と対応させる。"""
    colors = oklch_scale(hex_to_rgb(base_code), len(STEP_NAMES),
                         lightest=0.97, darkest=0.22)
    return dict(zip(STEP_NAMES, colors))


# 役割ごとのカラースケール。
PRIMARY = make_scale("#2f6fb0")
NEUTRAL = make_scale("#6b7280")
SUCCESS = make_scale("#2e8540")
WARNING = make_scale("#b7791f")
DANGER = make_scale("#c53030")

# 役割 (トークン) に色を割り当てたテーマ。
LIGHT_THEME: Theme = {
    "background": NEUTRAL["50"],
    "surface": np.ones(3),
    "border": NEUTRAL["200"],
    "text": NEUTRAL["900"],
    "text-muted": NEUTRAL["600"],
    "primary": PRIMARY["600"],
    "on-primary": np.ones(3),
    "success": SUCCESS["600"],
    "warning": WARNING["600"],
    "danger": DANGER["600"],
}

DARK_THEME: Theme = {
    "background": NEUTRAL["900"],
    "surface": NEUTRAL["800"],
    "border": NEUTRAL["700"],
    "text": NEUTRAL["50"],
    "text-muted": NEUTRAL["300"],
    "primary": PRIMARY["300"],
    "on-primary": NEUTRAL["900"],
    "success": SUCCESS["300"],
    "warning": WARNING["300"],
    "danger": DANGER["300"],
}

# コントラスト比を確認する (前景, 背景) の組と、必要なコントラスト比。
CHECKS = [
    ("text", "background", 4.5),
    ("text", "surface", 4.5),
    ("text-muted", "surface", 4.5),
    ("on-primary", "primary", 4.5),
    ("primary", "surface", 3.0),
    ("success", "surface", 4.5),
    ("warning", "surface", 4.5),
    ("danger", "surface", 4.5),
]


def rgb_tuple(rgb: FloatArray) -> tuple[int, int, int]:
    """sRGB 値を、PIL の描画関数に渡す 0-255 の整数の組にする。"""
    r, g, b = (int(v) for v in to_uint8(rgb))
    return (r, g, b)


def scale_figure() -> Image.Image:
    """役割ごとのカラースケールを並べ、各段階に名前を書き込む。

    名前の文字色は、白と黒のうちコントラスト比が高い方を選ぶ。
    """
    scales = [("primary", PRIMARY), ("neutral", NEUTRAL),
              ("success", SUCCESS), ("warning", WARNING),
              ("danger", DANGER)]
    chip, label_width, gap = 64, 100, 8
    width = label_width + chip * len(STEP_NAMES) + gap
    height = gap + len(scales) * (chip + gap)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(16)
    white, black = np.ones(3), np.zeros(3)
    for row, (name, scale) in enumerate(scales):
        top = gap + row * (chip + gap)
        draw.text((gap, top + chip // 2), name, fill="black",
                  font=label_font, anchor="lm")
        for col, step in enumerate(STEP_NAMES):
            color = scale[step]
            left = label_width + col * chip
            draw.rectangle((left, top, left + chip - 1, top + chip - 1),
                           fill=rgb_tuple(color))
            text_color = (white if contrast_ratio(white, color)
                          >= contrast_ratio(black, color) else black)
            draw.text((left + chip // 2, top + chip // 2), step,
                      fill=rgb_tuple(text_color), font=label_font,
                      anchor="mm")
    return canvas


def mock_screen(theme: Theme, width: int = 400,
                height: int = 300) -> Image.Image:
    """テーマの色だけを使って、簡単な画面の見本を描く。"""
    canvas = Image.new("RGB", (width, height),
                       rgb_tuple(theme["background"]))
    draw = ImageDraw.Draw(canvas)
    title_font, body_font = font(20), font(15)

    # カード
    draw.rounded_rectangle((20, 20, width - 20, height - 20), radius=10,
                           fill=rgb_tuple(theme["surface"]),
                           outline=rgb_tuple(theme["border"]), width=2)
    draw.text((40, 44), "Project status", fill=rgb_tuple(theme["text"]),
              font=title_font)
    draw.text((40, 76), "Updated 5 minutes ago",
              fill=rgb_tuple(theme["text-muted"]), font=body_font)

    # 状態を表す行: 色に加えて記号でも区別する。
    statuses = [("success", "OK", "Build passed"),
                ("warning", "!", "2 tests are slow"),
                ("danger", "x", "Deploy failed")]
    for i, (token, symbol, message) in enumerate(statuses):
        y = 118 + i * 34
        draw.ellipse((40, y, 64, y + 24), outline=rgb_tuple(theme[token]),
                     width=2)
        draw.text((52, y + 12), symbol, fill=rgb_tuple(theme[token]),
                  font=font(12), anchor="mm")
        draw.text((76, y + 12), message, fill=rgb_tuple(theme[token]),
                  font=body_font, anchor="lm")

    # ボタン
    draw.rounded_rectangle((40, height - 76, 180, height - 40), radius=6,
                           fill=rgb_tuple(theme["primary"]))
    draw.text((110, height - 58), "Open report",
              fill=rgb_tuple(theme["on-primary"]), font=body_font,
              anchor="mm")
    return canvas


def mock_figure() -> Image.Image:
    """ライトテーマとダークテーマの画面の見本を横に並べる。"""
    light, dark = mock_screen(LIGHT_THEME), mock_screen(DARK_THEME)
    gap = 24
    canvas = Image.new("RGB", (light.width * 2 + gap, light.height),
                       "white")
    canvas.paste(light, (0, 0))
    canvas.paste(dark, (light.width + gap, 0))
    return canvas


def print_checks() -> None:
    """テーマごとに、色の組み合わせのコントラスト比を確認して表示する。"""
    for name, theme in (("ライト", LIGHT_THEME), ("ダーク", DARK_THEME)):
        print(f"{name}テーマ")
        for foreground, background, required in CHECKS:
            ratio = contrast_ratio(theme[foreground], theme[background])
            result = "OK" if ratio >= required else "NG"
            print(f"  {foreground:>10} / {background:<10} "
                  f"{ratio:5.2f} (基準 {required}) {result}")


# ブランドカラーの例。明るい橙なので、白い文字とのコントラスト比が低い。
BRAND_CODE = "#f39800"


def brand_scale(brand_code: str) -> tuple[dict[str, FloatArray], str]:
    """ブランドカラーからカラースケールを作り、明度が最も近い段を置き換える。

    戻り値は (カラースケール, ブランドカラーそのものを置いた段の名前)。
    """
    brand = hex_to_rgb(brand_code)
    scale = make_scale(brand_code)
    brand_lightness = float(oklab_lightness(brand))
    nearest = min(STEP_NAMES, key=lambda step: abs(
        float(oklab_lightness(scale[step])) - brand_lightness))
    scale[nearest] = brand
    return scale, nearest


def draw_button(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int],
                background: FloatArray, text_color: FloatArray) -> None:
    """ボタンを描き、その下に文字と背景のコントラスト比を書き添える。"""
    draw.rounded_rectangle(box, radius=6, fill=rgb_tuple(background))
    left, top, right, bottom = box
    draw.text(((left + right) // 2, (top + bottom) // 2), "Buy now",
              fill=rgb_tuple(text_color), font=font(18), anchor="mm")
    ratio = contrast_ratio(text_color, background)
    draw.text(((left + right) // 2, bottom + 16), f"{ratio:.2f} : 1",
              fill="black", font=font(16), anchor="mm")


def brand_figure() -> Image.Image:
    """ブランドカラーを組み込んだカラースケールと、ボタンの 3 つの例。"""
    scale, brand_step = brand_scale(BRAND_CODE)
    chip, gap = 64, 12
    width = chip * len(STEP_NAMES) + gap * 2
    canvas = Image.new("RGB", (width, 210), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(16)
    white, black = np.ones(3), np.zeros(3)
    for col, step in enumerate(STEP_NAMES):
        left = gap + col * chip
        color = scale[step]
        draw.rectangle((left, gap, left + chip - 1, gap + chip - 1),
                       fill=rgb_tuple(color))
        text_color = (white if contrast_ratio(white, color)
                      >= contrast_ratio(black, color) else black)
        draw.text((left + chip // 2, gap + chip // 2), step,
                  fill=rgb_tuple(text_color), font=label_font, anchor="mm")
        if step == brand_step:
            # ブランドカラーそのものを置いた段を太い枠で示す。
            draw.rectangle((left - 3, gap - 3, left + chip + 2,
                            gap + chip + 2), outline="black", width=3)
            draw.text((left + chip // 2, gap + chip + 14), "brand",
                      fill="black", font=label_font, anchor="mm")

    brand = scale[brand_step]
    buttons = [
        (brand, white),
        (brand, NEUTRAL["900"]),
        (scale["500"], white),
    ]
    for i, (background, text_color) in enumerate(buttons):
        left = gap + 40 + i * 210
        draw_button(draw, (left, 120, left + 150, 164), background,
                    text_color)
    return canvas


def print_brand_scale() -> None:
    """ブランドカラーのカラースケールと、文字色とのコントラスト比を表示する。"""
    scale, brand_step = brand_scale(BRAND_CODE)
    print(f"ブランドカラー {BRAND_CODE} は {brand_step} の段に置いた")
    print("段    色        明度 L  白の文字  neutral 900 の文字")
    for step in STEP_NAMES:
        color = scale[step]
        print(f"{step:>4}  {rgb_to_hex(color)}  "
              f"{float(oklab_lightness(color)):6.3f}  "
              f"{contrast_ratio(np.ones(3), color):8.2f}  "
              f"{contrast_ratio(NEUTRAL['900'], color):8.2f}")


def main() -> None:
    """本章の図を作って保存し、コントラスト比の確認結果を表示する。"""
    save_image(scale_figure(), "ui_scales.png")
    save_image(mock_figure(), "ui_mock.png")
    save_image(brand_figure(), "ui_brand.png")
    print_checks()
    print_brand_scale()


if __name__ == "__main__":
    main()
