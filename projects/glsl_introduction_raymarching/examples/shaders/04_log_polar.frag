// 04_log_polar.frag
// 第 4 章: 対数極座標による拡大方向の繰り返し。
// 円の輪郭を一定の太さで描くには、距離に半径 r を掛けて補正する必要がある。
// 画面の左半分は補正なし、右半分は補正あり。時間とともに中心へ拡大し続ける。

const float PI = 3.14159265;
const float N  = 12.0;   // 1 周あたりの円の数

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;
    bool corrected = fragCoord.x > 0.5 * iResolution.x;

    // 対数極座標 (log r, θ) に変換する
    float r = length(p);
    vec2 w = vec2(log(r), atan(p.y, p.x));

    // 時間とともに log r の方向にずらすと、無限に拡大していくように見える
    w.x -= 0.3 * iTime;

    // 1 辺 2π / N の正方形で、log r と θ の両方向に繰り返す
    float cell = 2.0 * PI / N;
    vec2 id = floor(w / cell);
    // 列ごとに角度を半分ずらし、レンガのように互い違いに並べる
    w.y += 0.5 * cell * mod(id.x, 2.0);
    id.y = floor(w.y / cell);
    vec2 q = w - cell * (id + 0.5);

    // 対数極座標の中での円の SDF
    float dw = length(q) - 0.35 * cell;
    // 画面上での距離に直す。対数極座標は局所的に 1 / r 倍の拡大なので r を掛ける
    float d = corrected ? dw * r : dw * 0.3;

    // 円の内側を列ごとに色分けし、輪郭を白い線で描く
    vec3 inside = 0.5 + 0.4 * cos(vec3(0.0, 2.0, 4.0) + id.x);
    vec3 col = (d < 0.0) ? inside : vec3(0.08);
    col = mix(col, vec3(1.0), 1.0 - smoothstep(0.004, 0.008, abs(d)));

    // 中心付近は円が細かくなりすぎるので暗くする
    col *= smoothstep(0.0, 0.08, r);
    // 画面中央に境界線を引く
    col = mix(col, vec3(1.0), step(abs(fragCoord.x - 0.5 * iResolution.x), 1.0));

    fragColor = vec4(col, 1.0);
}
