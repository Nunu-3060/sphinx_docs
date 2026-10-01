// 01_circle2d.frag
// 第 1 章: 2 次元の距離関数で円を描き、距離の値を縞模様で可視化する。

// 原点を中心とする半径 r の円までの符号付き距離
float sdCircle(vec2 p, float r)
{
    return length(p) - r;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // 画面中央を原点とし、縦方向が -1〜1 になる座標に変換する
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    float d = sdCircle(p, 0.5);

    // 外側 (d > 0) を橙、内側 (d < 0) を青で塗る
    vec3 col = (d > 0.0) ? vec3(0.9, 0.6, 0.3) : vec3(0.4, 0.7, 0.85);
    // 境界から離れるほど明るくし、距離に比例した縞を重ねる
    col *= 1.0 - exp(-4.0 * abs(d));
    col *= 0.8 + 0.2 * cos(100.0 * d);
    // 境界 (d = 0) を白い線で描く
    col = mix(col, vec3(1.0), 1.0 - smoothstep(0.0, 0.01, abs(d)));

    fragColor = vec4(col, 1.0);
}
