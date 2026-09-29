#version 300 es

// 頂点属性：頂点ごとに異なる値
layout(location = 0) in vec2 aPosition;  // 頂点の位置
layout(location = 1) in vec3 aColor;     // 頂点の色

// ステージ間変数：フラグメントシェーダーへ渡す値
out vec3 vColor;           // 三角形の内部で補間される（smooth は既定なので省略している）
flat out vec3 vFlatColor;  // 補間されず、プロボーキング頂点（最後の頂点）の値が使われる

void main() {
    vColor = aColor;
    vFlatColor = aColor;
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
