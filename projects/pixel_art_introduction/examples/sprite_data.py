"""本書のサンプルで共通に使うドット絵データ。

ドット絵は「文字 1 つ = 1 ピクセル」の文字列リストとして定義し、
パレット（文字から色への対応表）を使って Pillow の画像に変換する。
'.' は透明ピクセルを表す。

単体で実行すると、サンプル画像を output フォルダに保存する::

    python sprite_data.py
"""

from pathlib import Path

from PIL import Image

RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
Palette = dict[str, RGB]

TRANSPARENT: RGBA = (0, 0, 0, 0)

# スライム（16×16）。光源は左上。
SLIME_PALETTE: Palette = {
    "K": (34, 32, 52),     # 輪郭・目
    "d": (47, 122, 78),    # 陰
    "g": (79, 176, 90),    # 基本色
    "l": (158, 224, 106),  # 明部
    "w": (244, 255, 214),  # ハイライト
}

SLIME: list[str] = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "......KKKK......",
    "....KKwlggKK....",
    "...KwwlgggggK...",
    "..KlwlggggggdK..",
    "..KlggggggggdK..",
    ".KgggKggggKggdK.",
    ".KgggKggggKgddK.",
    ".KggggggggggddK.",
    ".KddgggggggdddK.",
    "..KKKKKKKKKKKK..",
    "................",
]

# 主人公（16×16、正面向き）。光源は左上。
HERO_PALETTE: Palette = {
    "K": (34, 32, 52),     # 輪郭
    "e": (34, 32, 52),     # 目
    "h": (143, 74, 43),    # 髪
    "H": (94, 47, 34),     # 髪の陰
    "s": (244, 199, 161),  # 肌
    "S": (217, 144, 107),  # 肌の陰
    "b": (59, 111, 209),   # 服
    "B": (38, 64, 143),    # 服の陰
    "y": (232, 179, 60),   # ベルト
    "p": (74, 85, 120),    # ズボン
    "P": (50, 58, 85),     # ズボンの陰
    "f": (107, 59, 38),    # 靴
}

_HERO_BODY: list[str] = [
    "................",
    "................",
    ".....KKKKKK.....",
    "....KhhhhhHK....",
    "...KhhhhhhhHK...",
    "...KhssssshHK...",
    "...KsesssseSK...",
    "...KssssssSSK...",
    "....KssssSSK....",
    "...KbbbbbbbBK...",
    "..KbbbbbbbbBBK..",
    "..KsKyyyyyyKsK..",
    "...KbbbbbbBBK...",
]

_LEGS_STAND: list[str] = [
    "....KpPKKpPK....",
    "....KffKKffK....",
    "....KKKKKKKK....",
]

_LEGS_LEFT_UP: list[str] = [
    "....KffKKpPK....",
    "....KKKKKffK....",
    "........KKKK....",
]

_LEGS_RIGHT_UP: list[str] = [
    "....KpPKKffK....",
    "....KffKKKKK....",
    "....KKKK........",
]

HERO: list[str] = _HERO_BODY + _LEGS_STAND

# 歩行アニメーション（4 フレーム）：直立 → 左足を上げる → 直立 → 右足を上げる
HERO_WALK: list[list[str]] = [
    _HERO_BODY + _LEGS_STAND,
    _HERO_BODY + _LEGS_LEFT_UP,
    _HERO_BODY + _LEGS_STAND,
    _HERO_BODY + _LEGS_RIGHT_UP,
]

# 草地のタイル（16×16）。上下左右をつなげても継ぎ目が出ないように描いてある。
GRASS_PALETTE: Palette = {
    "g": (90, 166, 70),    # 基本色
    "d": (61, 122, 58),    # 草の根元
    "l": (134, 201, 90),   # 草の先
}

GRASS_TILE: list[str] = [
    "gggggggggggggggg",
    "gglgggggggggglgg",
    "gdldggggggggdldg",
    "gggggggglggggggg",
    "gggggggdldgggggg",
    "gggggggggggggggg",
    "lggggggggggggggl",
    "ldgglgggggggggdl",
    "ggdldggggggggggg",
    "gggggggggggglggg",
    "gggggggggggdldgg",
    "ggggglgggggggggg",
    "ggggdldggggggggg",
    "gggggggggggggggg",
    "gggggggggglggggg",
    "gggggggggdldgggg",
]


def make_image(rows: list[str], palette: Palette) -> Image.Image:
    """文字列リストとパレットから RGBA 画像を作る。"""
    height = len(rows)
    width = len(rows[0])
    image = Image.new("RGBA", (width, height), TRANSPARENT)
    for y, row in enumerate(rows):
        if len(row) != width:
            raise ValueError(f"{y} 行目の長さが {len(row)} で、{width} と一致しない")
        for x, char in enumerate(row):
            if char != ".":
                image.putpixel((x, y), (*palette[char], 255))
    return image


def slime_image() -> Image.Image:
    """スライムの画像を返す。"""
    return make_image(SLIME, SLIME_PALETTE)


def hero_image() -> Image.Image:
    """主人公（直立）の画像を返す。"""
    return make_image(HERO, HERO_PALETTE)


def hero_walk_images() -> list[Image.Image]:
    """主人公の歩行アニメーションの各フレームを返す。"""
    return [make_image(rows, HERO_PALETTE) for rows in HERO_WALK]


def grass_tile_image() -> Image.Image:
    """草地のタイル画像を返す。"""
    return make_image(GRASS_TILE, GRASS_PALETTE)


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    slime_image().save(output_dir / "slime.png")
    hero_image().save(output_dir / "hero.png")
    grass_tile_image().save(output_dir / "grass.png")
    for index, frame in enumerate(hero_walk_images()):
        frame.save(output_dir / f"hero_walk_{index}.png")
    print(f"サンプル画像を {output_dir.resolve()} に保存した")


if __name__ == "__main__":
    main()
