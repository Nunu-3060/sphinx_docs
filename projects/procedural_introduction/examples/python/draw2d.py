"""2 次元のアニメーションを描くための簡単な描画ライブラリ（Pillow を使う）。

第 12〜14 章の動画は、各フレームをこの Canvas で描き、配列にして VideoWriter に渡す。
座標は「ワールド座標」（x は右、y は上が正）で指定する。内部では 2 倍の解像度で描いてから
縮小し、線や円の縁のギザギザ（エイリアス）を目立たなくする。
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import lru_cache

import numpy as np
from numpy.typing import ArrayLike
from PIL import Image, ImageDraw, ImageFont

from common import ByteArray, FloatArray

Color = tuple[int, int, int] | tuple[int, int, int, int]


def rgb(values: Sequence[float], alpha: float | None = None) -> Color:
    """0〜1 の RGB（と不透明度）を Pillow の 0〜255 の色にする。"""
    r, g, b = (int(np.clip(v, 0.0, 1.0) * 255.0 + 0.5) for v in values[:3])
    if alpha is None:
        return (r, g, b)
    return (r, g, b, int(np.clip(alpha, 0.0, 1.0) * 255.0 + 0.5))


@lru_cache(maxsize=16)
def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """日本語を表示できるフォントを探して読み込む。見つからなければ Pillow の既定のフォントを使う。"""
    from matplotlib import font_manager

    installed = {font.name: font.fname for font in font_manager.fontManager.ttflist}
    for name in ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "IPAexGothic", "Hiragino Sans", "DejaVu Sans"]:
        if name in installed:
            return ImageFont.truetype(installed[name], size)
    return ImageFont.load_default()


class Canvas:
    """ワールド座標で図形を描くキャンバス。

    center はキャンバスの中心に来るワールド座標、scale は 1 単位あたりの画素数。
    """

    def __init__(
        self,
        width: int,
        height: int,
        background: Sequence[float] = (1.0, 1.0, 1.0),
        center: tuple[float, float] = (0.0, 0.0),
        scale: float = 100.0,
        supersample: int = 2,
    ) -> None:
        self.width = width
        self.height = height
        self.center = center
        self.scale = scale
        self.supersample = supersample
        self.image = Image.new("RGB", (width * supersample, height * supersample), rgb(background))
        self.draw = ImageDraw.Draw(self.image, "RGBA")

    def to_pixels(self, points: ArrayLike) -> FloatArray:
        """ワールド座標の点列 (N, 2) を、内部の画像の画素座標に変換する。"""
        p = np.asarray(points, dtype=np.float64).reshape(-1, 2)
        k = self.scale * self.supersample
        x = (p[:, 0] - self.center[0]) * k + self.width * self.supersample / 2
        y = (self.center[1] - p[:, 1]) * k + self.height * self.supersample / 2
        return np.stack([x, y], axis=1)

    def _flat(self, points: ArrayLike) -> list[float]:
        result: list[float] = self.to_pixels(points).ravel().tolist()
        return result

    def polyline(self, points: ArrayLike, width: float, color: Color) -> None:
        """折れ線を描く。width は画面上の画素数。"""
        self.draw.line(self._flat(points), fill=color, width=max(1, round(width * self.supersample)), joint="curve")

    def polygon(self, points: ArrayLike, fill: Color, outline: Color | None = None, width: float = 1.0) -> None:
        """多角形を塗る。"""
        self.draw.polygon(self._flat(points), fill=fill, outline=outline, width=max(1, round(width * self.supersample)))

    def circle(self, center: ArrayLike, radius: float, fill: Color | None, outline: Color | None = None,
               width: float = 1.0) -> None:
        """円を描く。radius はワールド座標の長さ。"""
        cx, cy = self.to_pixels(center)[0]
        r = radius * self.scale * self.supersample
        self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline,
                          width=max(1, round(width * self.supersample)))

    def dot(self, center: ArrayLike, radius_px: float, fill: Color) -> None:
        """画面上の大きさ radius_px（画素）の点を描く。"""
        cx, cy = self.to_pixels(center)[0]
        r = radius_px * self.supersample
        self.draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)

    def text(self, position_px: tuple[float, float], text: str, size: int, color: Color,
             anchor: str = "la") -> None:
        """画面の左上を原点とする画素座標 position_px に文字を書く（ワールド座標ではない）。"""
        x, y = position_px
        font = load_font(size * self.supersample)
        self.draw.text((x * self.supersample, y * self.supersample), text, fill=color, font=font, anchor=anchor)

    def to_array(self) -> ByteArray:
        """縮小して (height, width, 3) の 8 bit の配列にする。"""
        image = self.image.reduce(self.supersample) if self.supersample > 1 else self.image
        return np.asarray(image, dtype=np.uint8)
