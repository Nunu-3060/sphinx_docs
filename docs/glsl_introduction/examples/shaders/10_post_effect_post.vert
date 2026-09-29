#version 300 es

const vec2 POSITIONS[3] = vec2[3](vec2(-1.0, -1.0), vec2(3.0, -1.0), vec2(-1.0, 3.0));

out vec2 vTexCoord;

void main() {
    vec2 position = POSITIONS[gl_VertexID];
    vTexCoord = position * 0.5 + 0.5;  // クリップ座標 (-1〜1) をテクスチャ座標 (0〜1) に変換する
    gl_Position = vec4(position, 0.0, 1.0);
}
