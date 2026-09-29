#version 300 es
precision highp float;

in vec2 vTexCoord;
in vec2 vMaskCoord;

uniform sampler2D uTexture;  // テクスチャユニット 0 に割り当てる
uniform sampler2D uMask;     // テクスチャユニット 1 に割り当てる
uniform bool uUseMask;

out vec4 outColor;

void main() {
    // texture 関数：テクスチャ座標の位置の色を読み出す（サンプリング）
    vec4 color = texture(uTexture, vTexCoord);
    if (uUseMask) {
        // マスクは白黒の画像なので、赤成分だけを明るさとして使う
        float mask = texture(uMask, vMaskCoord).r;
        color.rgb *= mask;
    }
    outColor = color;
}
