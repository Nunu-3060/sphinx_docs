"""サンプルプロジェクトで使う画像と効果音を生成するスクリプト。

外部素材を使わずに済むよう、Pillow で単純な図形の画像を描き、
標準ライブラリの wave モジュールで短い効果音を作る。

使い方（examples フォルダーで実行する）::

    python tools/generate_assets.py

生成したファイルは examples/assets に保存される。
"""

from __future__ import annotations

import math
import struct
import wave
from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageDraw

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
SAMPLE_RATE = 22050

Rgba = tuple[int, int, int, int]


# ---------------------------------------------------------------------------
# 画像
# ---------------------------------------------------------------------------


def draw_player(leg_offset: int = 0) -> Image.Image:
    """青い丸型のキャラクターを描く。leg_offset で足の位置をずらす。"""
    image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    body: Rgba = (70, 130, 230, 255)
    outline: Rgba = (20, 40, 90, 255)
    # 足（歩行アニメーション用に左右の高さを変える）
    draw.rectangle((18, 48 - leg_offset, 26, 60 - leg_offset), fill=outline)
    draw.rectangle((38, 48 + leg_offset, 46, 60 + leg_offset), fill=outline)
    # 胴体と目
    draw.ellipse((8, 6, 56, 54), fill=body, outline=outline, width=3)
    draw.ellipse((22, 18, 30, 30), fill=(255, 255, 255, 255))
    draw.ellipse((36, 18, 44, 30), fill=(255, 255, 255, 255))
    draw.ellipse((25, 22, 29, 28), fill=(0, 0, 0, 255))
    draw.ellipse((39, 22, 43, 28), fill=(0, 0, 0, 255))
    return image


def draw_rock() -> Image.Image:
    """落下物（岩）を描く。"""
    image = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    points = [(24, 2), (42, 10), (46, 28), (36, 44), (14, 46), (3, 30), (6, 12)]
    draw.polygon(points, fill=(150, 110, 80, 255), outline=(70, 45, 30, 255), width=3)
    draw.line((14, 18, 22, 26), fill=(90, 60, 40, 255), width=3)
    draw.line((30, 30, 36, 22), fill=(90, 60, 40, 255), width=3)
    return image


def draw_coin() -> Image.Image:
    """コインを描く。"""
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 2, 30, 30), fill=(250, 200, 40, 255), outline=(170, 120, 0, 255), width=3)
    draw.rectangle((14, 9, 18, 23), fill=(255, 240, 150, 255))
    return image


def draw_tile(fill: Rgba, edge: Rgba) -> Image.Image:
    """32 x 32 ピクセルの地形タイルを描く。"""
    image = Image.new("RGBA", (32, 32), fill)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), outline=edge, width=2)
    return image


def draw_tileset() -> Image.Image:
    """タイルを横に 2 枚並べたタイルセット画像を作る（地面、レンガ）。"""
    image = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    image.paste(draw_tile((90, 160, 70, 255), (40, 90, 30, 255)), (0, 0))
    image.paste(draw_tile((170, 90, 60, 255), (100, 50, 30, 255)), (32, 0))
    return image


def draw_box() -> Image.Image:
    """物理演算のサンプルで使う木箱を描く。"""
    image = Image.new("RGBA", (40, 40), (190, 140, 80, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 39, 39), outline=(110, 70, 30, 255), width=3)
    draw.line((0, 0, 39, 39), fill=(110, 70, 30, 255), width=3)
    draw.line((39, 0, 0, 39), fill=(110, 70, 30, 255), width=3)
    return image


def save_images() -> None:
    """すべての画像を生成して保存する。"""
    draw_player().save(ASSETS_DIR / "player.png")
    for index, offset in enumerate([0, 3, 0, -3]):
        draw_player(offset).save(ASSETS_DIR / f"player_walk_{index}.png")
    draw_rock().save(ASSETS_DIR / "rock.png")
    draw_coin().save(ASSETS_DIR / "coin.png")
    draw_tileset().save(ASSETS_DIR / "tileset.png")
    draw_box().save(ASSETS_DIR / "box.png")


# ---------------------------------------------------------------------------
# 効果音
# ---------------------------------------------------------------------------


def square(phase: float) -> float:
    """周期 1 の矩形波を返す。"""
    return 1.0 if phase % 1.0 < 0.5 else -1.0


def synthesize(
    duration: float,
    frequency: Callable[[float], float],
    volume: float = 0.3,
) -> list[float]:
    """周波数が時間とともに変化する矩形波を生成する。

    frequency は経過時間の割合（0.0 から 1.0）を受け取り、周波数 [Hz] を返す関数。
    音の終わりは直線的に小さくして、ぶつ切りの雑音を防ぐ。
    """
    count = int(SAMPLE_RATE * duration)
    samples: list[float] = []
    phase = 0.0
    for i in range(count):
        ratio = i / count
        phase += frequency(ratio) / SAMPLE_RATE
        envelope = 1.0 - ratio
        samples.append(square(phase) * volume * envelope)
    return samples


def write_wav(path: Path, samples: list[float]) -> None:
    """モノラル 16 ビットの WAV ファイルとして保存する。"""
    frames = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(frames)


def constant_frequency(frequency: float) -> Callable[[float], float]:
    """常に同じ周波数を返す関数を作る。"""
    return lambda _ratio: frequency


def make_bgm() -> list[float]:
    """短い旋律を繰り返す BGM 用のループ素材を作る。"""
    notes = [262, 330, 392, 330, 294, 349, 440, 349]  # ド ミ ソ ミ レ ファ ラ ファ
    samples: list[float] = []
    for note in notes:
        samples.extend(synthesize(0.25, constant_frequency(float(note)), volume=0.15))
    return samples


def save_sounds() -> None:
    """すべての効果音を生成して保存する。"""
    write_wav(ASSETS_DIR / "jump.wav", synthesize(0.15, lambda r: 300.0 + 600.0 * r))
    write_wav(ASSETS_DIR / "coin.wav", synthesize(0.2, lambda r: 988.0 if r < 0.3 else 1319.0))
    write_wav(ASSETS_DIR / "hit.wav", synthesize(0.3, lambda r: 220.0 * math.exp(-3.0 * r)))
    write_wav(ASSETS_DIR / "bgm.wav", make_bgm())


def main() -> None:
    ASSETS_DIR.mkdir(exist_ok=True)
    save_images()
    save_sounds()
    print(f"素材を {ASSETS_DIR} に保存した。")


if __name__ == "__main__":
    main()
