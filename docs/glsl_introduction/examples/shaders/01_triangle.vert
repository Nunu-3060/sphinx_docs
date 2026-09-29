#version 300 es

// 頂点属性：JavaScript から渡される頂点の位置 (x, y)
layout(location = 0) in vec2 aPosition;

void main() {
    // 頂点の位置をクリップ座標として出力する（z = 0.0、w = 1.0）
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
