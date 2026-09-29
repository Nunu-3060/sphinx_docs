#version 300 es

layout(location = 0) in vec2 aGrid;  // 格子点の位置 (x, z)。-1 から 1 の範囲

uniform mat4 uViewProjection;  // 射影行列 × ビュー行列
uniform float uTime;           // 経過時間（秒）
uniform float uAmplitude;      // 波の高さ

out float vHeight;  // 高さ（-1 から 1 に正規化した値）

const float WAVE_NUMBER = 12.0;  // 波数：大きいほど波の間隔が狭い
const float ANGULAR_SPEED = 3.0; // 角速度：大きいほど速く進む

void main() {
    // 中心からの距離に応じて高さを変え、同心円状に広がる波を作る
    float r = length(aGrid);
    float wave = sin(WAVE_NUMBER * r - ANGULAR_SPEED * uTime);
    vHeight = wave;
    vec3 position = vec3(aGrid.x, uAmplitude * wave, aGrid.y);
    gl_Position = uViewProjection * vec4(position, 1.0);
}
