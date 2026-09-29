#version 300 es
precision highp float;

uniform vec2 uResolution;
uniform float uTime;
uniform int uMode;      // 表示内容
uniform int uHash;      // 0：sin、1：Xorshift、2：PCG
uniform int uNoise;     // fBm、大理石、雲に使うノイズ（0：バリューノイズ、1：パーリンノイズ）
uniform float uOffset;  // 格子の番号に足す値（表示内容 0 のみ）
uniform float uScale;   // 格子の細かさ（画面の高さに入る格子の数）
uniform int uOctaves;   // fBm で重ねるノイズの数

out vec4 outColor;

// ---- ハッシュ関数 ----
// どれも、格子の番号（整数の値を持つ vec2）から 0 以上 1 未満の擬似乱数を作る。
// 同じ番号からは必ず同じ値が得られる。

// sin を使うハッシュ関数：短いが、入力が大きいと精度が不足して規則的な模様が現れる
float hashSin(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Xorshift（32 ビット）：シフトと XOR を組み合わせて、ビットをかき混ぜる
uint xorshift32(uint x) {
    x ^= x << 13u;
    x ^= x >> 17u;
    x ^= x << 5u;
    return x;
}

float hashXorshift(vec2 p) {
    uvec2 q = uvec2(ivec2(p));                       // 負の番号もそのまま uint にできる
    uint x = (q.x * 0x8da6b343u) ^ (q.y * 0xd8163841u); // 乗算で x と y を混ぜる
    x = xorshift32(x + 0x9e3779b9u);                 // 0 にならないように定数を足す
    x *= 0x2c1b3c6du;
    x = xorshift32(x);
    return float(x >> 8u) / 16777216.0;              // 上位 24 ビットを 0〜1 の float にする
}

// PCG ハッシュ：線形合同法で状態を進め、その状態を並べ替えて出力する
uint pcg(uint v) {
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float hashPcg(vec2 p) {
    uvec2 q = uvec2(ivec2(p));
    return float(pcg(q.x + pcg(q.y)) >> 8u) / 16777216.0;
}

// uHash で選んだハッシュ関数を呼び出す
float hash(vec2 p) {
    if (uHash == 1) {
        return hashXorshift(p);
    } else if (uHash == 2) {
        return hashPcg(p);
    }
    return hashSin(p);
}
// ---- ハッシュ関数ここまで ----

// ---- ノイズ関数 ----
// バリューノイズ：格子点に乱数を置き、その間をなめらかに補間する（結果は 0〜1）
float valueNoise(vec2 p) {
    vec2 i = floor(p);  // 格子の番号
    vec2 f = fract(p);  // 格子の中での位置（0 から 1）

    // 周囲 4 つの格子点の乱数
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));

    // 補間の重みを 3 次曲線で滑らかにする（smoothstep と同じ式）
    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// 格子点ごとの勾配：ハッシュ関数で決めた角度の単位ベクトル
vec2 gradient(vec2 cell) {
    float angle = 6.28318530718 * hash(cell);
    return vec2(cos(angle), sin(angle));
}

// パーリンノイズ（グラディエントノイズ）：結果はおおよそ -0.7〜0.7
float perlinNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    // 各格子点の勾配と、格子点から p へのベクトルの内積
    float a = dot(gradient(i), f);
    float b = dot(gradient(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(gradient(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(gradient(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));

    // 補間の重みを 5 次曲線 6t^5 - 15t^4 + 10t^3 で滑らかにする
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);

    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

// uNoise で選んだノイズを、0〜1 の範囲で返す
float noise(vec2 p) {
    if (uNoise == 1) {
        return 0.5 + perlinNoise(p);
    }
    return valueNoise(p);
}

// fBm（フラクショナルブラウン運動）：周波数を 2 倍、振幅を 1/2 にしながらノイズを重ねる
const int MAX_OCTAVES = 8;

float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < MAX_OCTAVES; i++) {
        if (i >= uOctaves) {
            break;
        }
        value += amplitude * noise(p);
        p *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}
// ---- ノイズ関数ここまで ----

void main() {
    // 画面の高さを基準にした座標（縦横比を保つ）
    vec2 p = gl_FragCoord.xy / uResolution.y * uScale;

    vec3 color;
    if (uMode == 0) {
        // 格子ごとに異なる乱数（隣の格子との間に連続性はない）
        color = vec3(hash(floor(p) + uOffset));
    } else if (uMode == 1) {
        color = vec3(valueNoise(p));
    } else if (uMode == 2) {
        color = vec3(0.5 + perlinNoise(p));
    } else if (uMode == 3) {
        color = vec3(fbm(p));
    } else if (uMode == 4) {
        // 大理石：縞模様（sin）の位相を fBm でずらす
        float stripes = sin(p.x * 2.0 + 8.0 * fbm(p));
        float v = 0.5 + 0.5 * stripes;
        color = mix(vec3(0.25, 0.28, 0.35), vec3(0.95, 0.94, 0.90), v);
    } else {
        // 雲：fBm の結果で座標をずらしてから、もう一度 fBm を計算する（ドメインワーピング）
        vec2 q = vec2(fbm(p + vec2(0.0, 0.1 * uTime)),
                      fbm(p + vec2(5.2, 1.3) - vec2(0.05 * uTime, 0.0)));
        float f = fbm(p + 2.0 * q);
        vec3 sky = vec3(0.25, 0.5, 0.9);
        color = mix(sky, vec3(1.0), smoothstep(0.3, 0.8, f));
    }

    outColor = vec4(color, 1.0);
}
