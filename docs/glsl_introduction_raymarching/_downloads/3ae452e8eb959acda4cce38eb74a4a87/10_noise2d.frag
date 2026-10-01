// 10_noise2d.frag
// 第 10 章: ハッシュとノイズの比較。画面を 6 つに分け、次の順に表示する。
//   上段: ハッシュ (格子ごとの乱数)、値ノイズ、勾配ノイズ
//   下段: fBm、ドメインワーピング、リッジノイズ

const float PI = 3.14159265;

// ---- ハッシュ ------------------------------------------------------------

// PCG ハッシュ (Jarzynski and Olano, 2020)。32 ビット整数を攪拌する
uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// 整数の格子点 p に 0 以上 1 未満の乱数を割り当てる
float hash21(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));  // 負の座標も 32 ビットの整数として扱う
    return float(pcgHash(q.x + pcgHash(q.y))) / 4294967296.0;
}

// ---- 値ノイズ ------------------------------------------------------------

// 格子点の乱数を 3 次のエルミート補間でつなぐ。値の範囲は 0〜1
float valueNoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    float a = hash21(i);
    float b = hash21(i + vec2(1.0, 0.0));
    float c = hash21(i + vec2(0.0, 1.0));
    float d = hash21(i + vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// ---- 勾配ノイズ ----------------------------------------------------------

// 格子点 i に割り当てる単位ベクトル (勾配)
vec2 gradientAt(vec2 i)
{
    float angle = 2.0 * PI * hash21(i);
    return vec2(cos(angle), sin(angle));
}

// 格子点の勾配と、格子点から p へのベクトルの内積を 5 次の補間でつなぐ。
// 格子点での値は 0 で、値の範囲はおよそ -0.7〜0.7
float gradientNoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    float a = dot(gradientAt(i), f);
    float b = dot(gradientAt(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(gradientAt(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(gradientAt(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// ---- fBm とその応用 ------------------------------------------------------

// オクターブごとに座標を回転させ、格子の方向が揃って見えるのを防ぐ
const mat2 OCTAVE_ROT = mat2(0.8, 0.6, -0.6, 0.8);

// フラクタルブラウン運動: 周波数を 2 倍、振幅を半分にしながら 6 層重ねる
float fbm(vec2 p)
{
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 6; i++) {
        value += amplitude * gradientNoise(p);
        p = 2.0 * OCTAVE_ROT * p;
        amplitude *= 0.5;
    }
    return value;
}

// ドメインワーピング: fBm でゆがめた座標で、もう一度 fBm を評価する
float warpedFbm(vec2 p)
{
    vec2 q = vec2(fbm(p + vec2(0.0, 0.0)), fbm(p + vec2(5.2, 1.3)));
    return fbm(p + 4.0 * q + 0.1 * iTime);
}

// リッジノイズ: 勾配ノイズの絶対値を反転させ、尾根のような鋭い線を作る
float ridgedFbm(vec2 p)
{
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 6; i++) {
        float n = 1.0 - abs(gradientNoise(p) * 1.4);
        value += amplitude * n * n;
        p = 2.0 * OCTAVE_ROT * p;
        amplitude *= 0.5;
    }
    return value;
}

// ---- メイン --------------------------------------------------------------

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // 画面を横 3 × 縦 2 の領域に分ける
    vec2 grid = vec2(3.0, 2.0);
    vec2 uv = fragCoord / iResolution.xy;
    vec2 cell = floor(uv * grid);
    int index = int(cell.x) + 3 * int(1.0 - cell.y);  // 左上から 0, 1, 2, ...

    // 各領域の縦方向に格子 8 個分が入る座標
    vec2 local = fract(uv * grid);
    float aspect = (iResolution.x / grid.x) / (iResolution.y / grid.y);
    vec2 p = 8.0 * local * vec2(aspect, 1.0);

    float v;
    if (index == 0) {
        v = hash21(floor(p));                     // ハッシュ
    } else if (index == 1) {
        v = valueNoise(p);                        // 値ノイズ
    } else if (index == 2) {
        v = 0.5 + gradientNoise(p);               // 勾配ノイズ
    } else if (index == 3) {
        v = 0.5 + fbm(0.5 * p);                   // fBm
    } else if (index == 4) {
        v = 0.5 + warpedFbm(0.3 * p);             // ドメインワーピング
    } else {
        v = ridgedFbm(0.3 * p);                   // リッジノイズ
    }
    vec3 col = vec3(clamp(v, 0.0, 1.0));

    // 領域の境界線
    vec2 border = step(vec2(0.005), local) * step(local, vec2(0.995));
    col *= border.x * border.y;

    fragColor = vec4(col, 1.0);
}
