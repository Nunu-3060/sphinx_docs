#version 300 es
precision highp float;

// 頂点シェーダーの出力と同じ名前・型で宣言する
in vec3 vColor;
flat in vec3 vFlatColor;

// uniform 変数：1 回の描画の間、すべてのフラグメントで同じ値
uniform float uBrightness;  // 明るさの倍率
uniform bool uUseFlat;      // true のとき補間しない色を使う

out vec4 outColor;

void main() {
    vec3 color = uUseFlat ? vFlatColor : vColor;
    outColor = vec4(color * uBrightness, 1.0);
}
