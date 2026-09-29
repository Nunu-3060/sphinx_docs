#version 300 es

layout(location = 0) in vec2 aPosition;  // 頂点の位置
layout(location = 1) in vec2 aTexCoord;  // テクスチャ座標（左下 (0, 0)、右上 (1, 1)）

uniform float uScale;  // テクスチャ座標の倍率（中心を基準に拡大縮小する）

out vec2 vTexCoord;    // 1 枚目のテクスチャ用の座標
out vec2 vMaskCoord;   // マスク用の座標（倍率を掛けない）

void main() {
    vTexCoord = (aTexCoord - 0.5) * uScale + 0.5;
    vMaskCoord = aTexCoord;
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
