#version 300 es

layout(location = 0) in vec3 aPosition;  // モデル座標での位置
layout(location = 1) in vec3 aNormal;    // モデル座標での法線

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;  // 法線をワールド座標へ変換する行列

out vec3 vWorldPosition;  // ワールド座標での位置
out vec3 vNormal;         // ワールド座標での法線

void main() {
    vec4 worldPosition = uModel * vec4(aPosition, 1.0);
    vWorldPosition = worldPosition.xyz;
    vNormal = uNormalMatrix * aNormal;
    gl_Position = uProjection * uView * worldPosition;
}
