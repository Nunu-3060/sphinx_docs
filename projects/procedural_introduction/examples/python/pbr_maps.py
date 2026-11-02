"""第 4 章「パターンとマテリアル」: 1 つの手続きから PBR 用のテクスチャ一式を出力する。

錆びた金属の手続き（materials.py の rust）から、次の画像を同じ座標・同じシードで作る。
どれも周期を持たないので、繰り返して貼る場合は第 4 章の period を使った方法に置き換える。

* base_color.png: ベースカラー（表面の色）
* roughness.png: ラフネス（表面の粗さ。白いほど粗い）
* metallic.png: メタリック（金属かどうか。白が金属）
* normal.png: 法線マップ（OpenGL 方式。G が上向き）
* pbr_maps.png: 上の画像と、簡単な照明で陰影を付けた結果を並べた図
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, grid, output_dir, save_image, setup_matplotlib
from materials import rust
from noise import fbm, perlin2
from texture import encode_normal, height_to_normal, shade, show_panels

SIZE = 384


def pbr_maps(x: FloatArray, y: FloatArray, amount: float, seed: int) -> dict[str, FloatArray]:
    """錆びた金属の各マップを返す。どのマップも同じマスク（錆の分布）から作るので、互いに食い違わない。"""
    color, mask, height = rust(x, y, amount=amount, seed=seed)
    variation = fbm(perlin2, x * 6.0, y * 6.0, octaves=3, seed=seed + 9) * 0.5 + 0.5
    roughness = 0.3 + 0.1 * variation + (0.85 - 0.3) * mask  # 金属は滑らか、錆は粗い
    metallic = 1.0 - mask  # 錆は金属ではない（酸化物）
    normal = height_to_normal(height, strength=8.0)
    return {"base_color": color, "roughness": roughness, "metallic": metallic, "normal": normal, "height": height}


def preview(maps: dict[str, FloatArray], light: tuple[float, float, float] = (-0.5, 0.6, 0.6)) -> FloatArray:
    """拡散反射に、ラフネスで鋭さを変えたハイライトを足す簡単な陰影（物理的に厳密ではない）。"""
    normal = maps["normal"]
    diffuse = shade(normal, maps["base_color"] * (1.0 - 0.5 * maps["metallic"])[..., None], light=light)
    direction = np.asarray(light) / np.linalg.norm(light)
    half = direction + np.array([0.0, 0.0, 1.0])  # 光と視線（真上）の中間の向き
    half = half / np.linalg.norm(half)
    exponent = 2.0 / np.maximum(maps["roughness"], 0.05) ** 4  # 粗いほどハイライトが広く弱い
    specular = np.clip(normal @ half, 0.0, 1.0) ** exponent * (1.0 - maps["roughness"]) * 1.2
    tint = 0.04 + 0.96 * maps["metallic"][..., None] * maps["base_color"]  # 金属のハイライトは自分の色を帯びる
    result: FloatArray = np.clip(diffuse + specular[..., None] * (0.3 + tint), 0.0, 1.0)
    return result


def main() -> None:
    setup_matplotlib()
    directory = output_dir(__file__)
    x, y = grid(SIZE, SIZE, scale=3.0)
    maps = pbr_maps(x, y, amount=0.45, seed=4)
    save_image(maps["base_color"], directory / "base_color.png")
    save_image(maps["roughness"], directory / "roughness.png")
    save_image(maps["metallic"], directory / "metallic.png")
    save_image(encode_normal(maps["normal"]), directory / "normal.png")

    images = [maps["base_color"], maps["roughness"], maps["metallic"], encode_normal(maps["normal"]), preview(maps)]
    titles = ["ベースカラー", "ラフネス", "メタリック", "法線", "陰影を付けた例"]
    show_panels(images, titles, directory / "pbr_maps.png", size=2.6)


if __name__ == "__main__":
    main()
