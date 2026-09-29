#version 300 es

// フラグメントシェーダーでは float の精度を必ず指定する
precision highp float;

// 出力変数：このフラグメントの色 (R, G, B, A)。各成分は 0.0 から 1.0
out vec4 outColor;

void main() {
    outColor = vec4(1.0, 0.5, 0.2, 1.0);  // オレンジ色
}
