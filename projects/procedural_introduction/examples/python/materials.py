"""第 4 章「パターンとマテリアル」: ノイズを組み合わせた素材の図を作る。

* materials.png: 木目・大理石・雲・錆
* marble_steps.png: 大理石を作る手順（縞 → 乱流で歪める → 色を付ける）
"""

from __future__ import annotations

import numpy as np

from color import gradient_map, hex_to_rgb
from common import FloatArray, grid, output_dir, setup_matplotlib
from noise import fbm, perlin2, turbulence, value2, worley2
from texture import mix, show_panels, smoothstep

SIZE = 320


def wood(x: FloatArray, y: FloatArray, rings: float = 7.0, distortion: float = 0.12, seed: int = 0) -> FloatArray:
    """木目。年輪（中心からの距離の縞）をノイズで歪め、細かな繊維の筋を加える。

    板は丸太を縦に切ったものなので、板の上に現れる年輪は、縦（木の伸びる向き）に長い山形の曲線になる。
    ここでは年輪の中心を板の上端の外 (1.0, -0.6) に置き、縦方向の距離を 0.35 倍に縮めて表す。
    """
    distance = np.hypot(x - 1.0, (y + 0.6) * 0.35)
    distance = distance + distortion * fbm(perlin2, x * 1.5, y * 0.5, octaves=4, seed=seed)
    ring = distance * rings - np.floor(distance * rings)  # fract: 0〜1 を繰り返す
    # 1 周期の中で、早材（明るい部分）から晩材（暗い部分）へ徐々に変わり、次の年輪で急に明るく戻る。
    late = smoothstep(0.55, 0.95, ring)
    grain = value2(x * 60.0, y * 3.0, seed=seed + 1) * 0.5 + 0.5  # 縦に伸びた細かい筋
    tone = np.clip(0.75 * late + 0.25 * grain, 0.0, 1.0)
    return mix(hex_to_rgb("#e3b77f"), hex_to_rgb("#9a5b2e"), tone)


def marble_value(x: FloatArray, y: FloatArray, frequency: float = 2.0, strength: float = 5.0,
                 seed: int = 0) -> FloatArray:
    """大理石の縞の値（-1〜1）。斜めの縞 sin を、乱流で位相をずらして歪める。"""
    return np.sin((x + 0.5 * y) * frequency * np.pi + strength * turbulence(perlin2, x, y, octaves=6, seed=seed))


def marble(x: FloatArray, y: FloatArray, seed: int = 0) -> FloatArray:
    """大理石。白地に、縞の値が 0 に近い所だけ細い灰色の脈を入れる。"""
    vein = 1.0 - np.abs(marble_value(x, y, seed=seed))  # 縞の中心線で 1
    return gradient_map(vein ** 4, [
        (0.0, hex_to_rgb("#f4f1ec")), (0.4, hex_to_rgb("#d9d4cc")), (0.8, hex_to_rgb("#7d7a76")),
        (1.0, hex_to_rgb("#3e3c3a")),
    ])


def clouds(x: FloatArray, y: FloatArray, cover: float = 0.45, seed: int = 0) -> FloatArray:
    """空の雲。fBm を雲の密度とし、しきい値 cover より上を雲にする。下側を少し暗くして厚みを出す。"""
    density = fbm(perlin2, x, y * 1.6, octaves=6, seed=seed) * 0.5 + 0.5
    below = fbm(perlin2, x, y * 1.6 + 0.08, octaves=6, seed=seed) * 0.5 + 0.5  # 少し下の点の密度
    amount = smoothstep(cover, cover + 0.25, density)
    shadow = np.clip((below - density) * 6.0 + 0.5, 0.0, 1.0)
    height = y / float(y.max())
    sky = mix(hex_to_rgb("#3f7cc4"), hex_to_rgb("#a8cdf0"), height)
    cloud = mix(hex_to_rgb("#ffffff"), hex_to_rgb("#9aa7b8"), shadow * 0.8)
    return mix(sky, cloud, amount)


def rust(x: FloatArray, y: FloatArray, amount: float = 0.5, seed: int = 0) -> tuple[FloatArray, FloatArray, FloatArray]:
    """錆びた金属。(色, 錆のマスク 0〜1, 高さ 0〜1) を返す。amount で錆の量を決める。"""
    # 金属の地: 細かいノイズと、一方向にこすった筋。
    brushed = value2(x * 3.0, y * 80.0, seed=seed) * 0.5 + 0.5
    metal = mix(hex_to_rgb("#7d8790"), hex_to_rgb("#b4bcc4"), 0.6 * brushed + 0.4)
    # 錆の分布: 大きな fBm をしきい値で切る。境界は細かな fBm で崩す。
    spread = fbm(perlin2, x * 1.2, y * 1.2, octaves=6, seed=seed + 1) * 0.5 + 0.5
    spread = spread + 0.12 * fbm(perlin2, x * 8.0, y * 8.0, octaves=3, seed=seed + 2)
    threshold = 1.0 - amount
    mask = smoothstep(threshold - 0.03, threshold + 0.03, spread)
    # 錆の色: 濃い茶から橙まで、別の fBm で変える。
    hue = fbm(perlin2, x * 4.0, y * 4.0, octaves=5, seed=seed + 3) * 0.5 + 0.5
    rust_color = gradient_map(hue, [(0.0, hex_to_rgb("#4a2412")), (0.5, hex_to_rgb("#8b3f1a")),
                                    (1.0, hex_to_rgb("#c8742f"))])
    # 錆の中の小さな穴（孔食）: セルラーノイズの F1 が小さい所。
    f1, _, _ = worley2(x * 6.0, y * 6.0, seed=seed + 4)
    pits = smoothstep(0.18, 0.08, f1) * mask
    color = mix(metal, rust_color, mask) * (1.0 - 0.5 * pits)[..., None]
    height = np.clip(0.5 + 0.35 * mask * (0.6 + 0.4 * hue) - 0.4 * pits, 0.0, 1.0)
    return color, mask, height


def draw_materials(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=2.0)
    rusty, _, _ = rust(x * 1.5, y * 1.5, seed=4)
    images = [wood(x, y, seed=1), marble(x, y, seed=2), clouds(x * 1.5, y * 1.5, seed=3), rusty]
    show_panels(images, ["木目", "大理石", "雲", "錆"], output_dir(__file__) / file_name)


def draw_marble_steps(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=2.0)
    straight = np.sin((x + 0.5 * y) * 2.0 * np.pi)
    images = [
        straight * 0.5 + 0.5,
        np.clip(turbulence(perlin2, x, y, octaves=6, seed=2) * 2.0, 0.0, 1.0),
        marble_value(x, y, seed=2) * 0.5 + 0.5,
        marble(x, y, seed=2),
    ]
    titles = ["斜めの縞 sin", "乱流", "乱流で縞の位相をずらす", "縞の中心を脈として色付け"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_materials("materials.png")
    draw_marble_steps("marble_steps.png")


if __name__ == "__main__":
    main()
