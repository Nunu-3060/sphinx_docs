#version 300 es

layout(location = 0) in vec3 aPosition;  // モデル座標での頂点の位置
layout(location = 1) in vec3 aColor;     // 頂点の色

uniform mat4 uModel;       // モデル行列：モデル座標 → ワールド座標
uniform mat4 uView;        // ビュー行列：ワールド座標 → ビュー座標
uniform mat4 uProjection;  // 射影行列：ビュー座標 → クリップ座標

out vec3 vColor;

void main() {
    vColor = aColor;
    // 位置は w = 1.0 の同次座標にし、右側の行列から順に掛けてクリップ座標へ変換する
    gl_Position = uProjection * uView * uModel * vec4(aPosition, 1.0);
}
