#version 300 es

// 画面全体を覆う大きな三角形の 3 頂点。頂点バッファーを使わず、gl_VertexID で選ぶ
const vec2 POSITIONS[3] = vec2[3](
    vec2(-1.0, -1.0),
    vec2( 3.0, -1.0),
    vec2(-1.0,  3.0)
);

void main() {
    gl_Position = vec4(POSITIONS[gl_VertexID], 0.0, 1.0);
}
