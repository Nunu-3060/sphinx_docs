// 10_curl.frag
// 第 10 章: カールノイズ。同じノイズ ψ から作った 2 つのベクトル場に沿って、
// 市松模様を流す (移流させる)。
//   左: 勾配の場 v = ∇ψ。湧き出しと吸い込みがあり、模様が集まったり広がったりする
//   右: カールの場 v = (∂ψ/∂y, -∂ψ/∂x)。発散が 0 で、模様の面積が保たれる
// 流す時間は、時間とともに増減させている。

const float PI = 3.14159265;
const int   ADVECT_STEPS = 40;   // 移流の計算の分割数

// ---- ノイズ (第 10 章) ---------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float hash21(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    return float(pcgHash(q.x + pcgHash(q.y))) / 4294967296.0;
}

vec2 gradientAt(vec2 i)
{
    float angle = 2.0 * PI * hash21(i);
    return vec2(cos(angle), sin(angle));
}

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

// ポテンシャル ψ: 2 オクターブの勾配ノイズ
float potential(vec2 p)
{
    return gradientNoise(1.5 * p) + 0.5 * gradientNoise(3.0 * p + 7.3);
}

// ---- ベクトル場 ----------------------------------------------------------

// ψ の勾配を中心差分で求める
vec2 potentialGradient(vec2 p)
{
    const float e = 0.01;
    return vec2(potential(p + vec2(e, 0.0)) - potential(p - vec2(e, 0.0)),
                potential(p + vec2(0.0, e)) - potential(p - vec2(0.0, e))) /
           (2.0 * e);
}

// 勾配の場: ψ の大きくなる方向に流れる。発散は 0 ではない
vec2 gradientField(vec2 p)
{
    return potentialGradient(p);
}

// カールの場: 勾配を 90° 回転させたもの。ψ の等高線に沿って流れ、発散が 0 になる
vec2 curlField(vec2 p)
{
    vec2 g = potentialGradient(p);
    return vec2(g.y, -g.x);
}

// 点 p の色が、時間 duration の間にどこから流れてきたかを、流れを逆にたどって求める
vec2 traceBack(vec2 p, float duration, bool curl)
{
    float dt = duration / float(ADVECT_STEPS);
    for (int i = 0; i < ADVECT_STEPS; i++) {
        vec2 v = curl ? curlField(p) : gradientField(p);
        p -= dt * v;
    }
    return p;
}

// ---- メイン --------------------------------------------------------------

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // 画面の左右に、同じ範囲の画像を 1 つずつ並べる
    vec2 halfSize = vec2(0.5 * iResolution.x, iResolution.y);
    bool curl = fragCoord.x > halfSize.x;
    vec2 local = vec2(mod(fragCoord.x, halfSize.x), fragCoord.y);
    vec2 p = 2.0 * (2.0 * local - halfSize) / halfSize.y;

    // 流す時間を 0〜0.12 の間で増減させる
    float duration = 0.06 - 0.06 * cos(0.5 * iTime);
    vec2 q = traceBack(p, duration, curl);

    // 元の位置 q での市松模様と、細い格子線
    vec2 cell = floor(4.0 * q);
    float checker = mod(cell.x + cell.y, 2.0);
    vec3 col = mix(vec3(0.15, 0.3, 0.55), vec3(0.9, 0.85, 0.7), checker);
    vec2 f = abs(fract(4.0 * q) - 0.5);
    col = mix(col, vec3(0.05), smoothstep(0.44, 0.47, max(f.x, f.y)));

    col = mix(col, vec3(1.0), step(abs(fragCoord.x - halfSize.x), 1.0));
    fragColor = vec4(col, 1.0);
}
