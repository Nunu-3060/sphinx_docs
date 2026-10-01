// 01_uv.frag
// 第 1 章: ピクセル座標を 0〜1 に正規化し、そのまま色として出力する。

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // fragCoord はピクセル中心の座標 (左下が原点、単位はピクセル)
    vec2 uv = fragCoord / iResolution.xy;

    // R に x、G に y、B に時間とともに変化する値を割り当てる
    vec3 col = vec3(uv, 0.5 + 0.5 * sin(iTime));

    fragColor = vec4(col, 1.0);
}
