// 10_terrain.frag
// 第 10 章: fBm で作った高さの関数を SDF の代わりに使い、地形をレイマーチングで描く。
// 高さの関数は厳密な距離ではないので、歩幅を小さくして進む。

const int   MAX_STEPS  = 300;
const float MAX_DIST   = 80.0;
const float SURF_DIST  = 0.001;
const float STEP_SCALE = 0.5;    // 歩幅の係数 (距離の過大評価への対策)

const vec3 LIGHT_DIR = normalize(vec3(0.8, 0.4, 0.2));
const vec3 SUN_COLOR = vec3(1.4, 1.25, 1.0);
const vec3 SKY_COLOR = vec3(0.35, 0.45, 0.6);

// ---- ノイズ (10_noise2d.frag と同じ) -------------------------------------

const float PI = 3.14159265;

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

const mat2 OCTAVE_ROT = mat2(0.8, 0.6, -0.6, 0.8);

// ---- 地形 ----------------------------------------------------------------

// 水平位置 xz での地形の高さ。octaves はノイズを重ねる層の数
float terrainHeight(vec2 xz, int octaves)
{
    vec2 p = 0.25 * xz;
    float value = 0.0;
    float amplitude = 1.0;
    for (int i = 0; i < octaves; i++) {
        value += amplitude * gradientNoise(p);
        p = 2.0 * OCTAVE_ROT * p;
        amplitude *= 0.5;
    }
    return 3.0 * value;
}

// 高さの関数から作った「SDF の代わり」の関数。
// 真の距離ではないが、表面 (値が 0) の外側で正、内側で負になる
float map(vec3 p, int octaves)
{
    return p.y - terrainHeight(p.xz, octaves);
}

float raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 p = ro + t * rd;
        // レイマーチングでは粗い地形 (5 層) で十分
        float d = map(p, 5);
        if (d < SURF_DIST * t) {
            return t;
        }
        t += d * STEP_SCALE;
        if (t > MAX_DIST) {
            break;
        }
    }
    return -1.0;
}

// 高さの関数の勾配から法線を求める。陰影には細かい地形 (9 層) を使う
vec3 calcNormal(vec3 p, float t)
{
    float e = 0.001 * t + 0.001;
    float hx = terrainHeight(p.xz + vec2(e, 0.0), 9) -
               terrainHeight(p.xz - vec2(e, 0.0), 9);
    float hz = terrainHeight(p.xz + vec2(0.0, e), 9) -
               terrainHeight(p.xz - vec2(0.0, e), 9);
    return normalize(vec3(-hx, 2.0 * e, -hz));
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.05;
    for (int i = 0; i < 48 && t < 20.0; i++) {
        float h = map(ro + t * rd, 5);
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h * STEP_SCALE, 0.05, 1.0);
    }
    return clamp(res, 0.0, 1.0);
}

// ---- 色 ------------------------------------------------------------------

vec3 skyColor(vec3 rd)
{
    vec3 col = mix(vec3(0.7, 0.75, 0.8), vec3(0.25, 0.4, 0.7),
                   sqrt(clamp(rd.y, 0.0, 1.0)));
    float sun = max(dot(rd, LIGHT_DIR), 0.0);
    col += SUN_COLOR * (pow(sun, 512.0) * 4.0 + pow(sun, 16.0) * 0.15);
    return col;
}

// 高さと傾きで地面の色を決める
vec3 terrainAlbedo(vec3 p, vec3 n)
{
    vec3 rock = vec3(0.3, 0.26, 0.22);
    vec3 grass = vec3(0.12, 0.25, 0.06);
    vec3 snow = vec3(0.9);
    // 平らな場所 (n.y が 1 に近い) ほど草に覆われる
    vec3 col = mix(rock, grass, smoothstep(0.65, 0.85, n.y));
    // 高く平らな場所ほど雪が積もる
    float snowAmount = smoothstep(1.5, 2.5, p.y + 0.5 * n.y);
    return mix(col, snow, snowAmount * smoothstep(0.5, 0.8, n.y));
}

vec3 render(vec3 ro, vec3 rd)
{
    float t = raymarch(ro, rd);
    if (t < 0.0) {
        return skyColor(rd);
    }
    vec3 p = ro + t * rd;
    vec3 n = calcNormal(p, t);

    float shadow = softShadow(p + n * 0.01, LIGHT_DIR);
    float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
    float sky = 0.5 + 0.5 * n.y;
    vec3 col = terrainAlbedo(p, n) * (SUN_COLOR * diffuse + SKY_COLOR * sky);

    // 遠くほど空の色に近づける (第 7 章のフォグ)
    float fog = 1.0 - exp(-0.015 * t);
    return mix(col, skyColor(vec3(rd.x, 0.0, rd.z)), fog);
}

// ---- メイン --------------------------------------------------------------

mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    // カメラは地形の上を -z 方向に進む。高さは真下の地形から決める
    float z = -0.8 * iTime;
    vec3 ro = vec3(1.0, 0.0, z);
    ro.y = terrainHeight(ro.xz, 5) + 1.2;
    vec3 ta = vec3(0.0, ro.y - 0.6, z - 4.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.8));

    vec3 col = render(ro, rd);
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
