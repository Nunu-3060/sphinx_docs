// 10_texture.frag
// 第 10 章: 手続き的なテクスチャ。ノイズで作った 2 次元の模様を、
// トライプラナーマッピングで立体に貼り、バンプマッピングで凹凸の陰影を付ける。
// 左はテクスチャなし、右はテクスチャとバンプマッピングあり。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;
const float PI        = 3.14159265;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3 SKY_COLOR = vec3(0.3, 0.4, 0.55);

// ---- ノイズ (10_noise2d.frag と同じ) -------------------------------------

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

float fbm(vec2 p)
{
    float value = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < 4; i++) {
        value += amplitude * gradientNoise(p);
        p = 2.0 * OCTAVE_ROT * p;
        amplitude *= 0.5;
    }
    return value;
}

// ---- テクスチャ ----------------------------------------------------------

// 2 次元の模様: 大理石のような縞。値は 0〜1
float marble(vec2 uv)
{
    float n = fbm(2.0 * uv);
    return 0.5 + 0.5 * sin(6.0 * uv.x + 10.0 * n);
}

// トライプラナーマッピング: 3 つの座標平面に投影した模様を、
// 法線の向きに応じた重みで混ぜ合わせる
float triplanar(vec3 p, vec3 n)
{
    vec3 w = pow(abs(n), vec3(4.0));   // 指数が大きいほど境目がくっきりする
    w /= w.x + w.y + w.z;
    return w.x * marble(p.yz) + w.y * marble(p.zx) + w.z * marble(p.xy);
}

// ---- シーン --------------------------------------------------------------

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float sdRoundBox(vec3 p, vec3 b, float r)
{
    vec3 q = abs(p) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// 戻り値は (距離, マテリアル ID)。0: 地面、1: 物体
vec2 map(vec3 p)
{
    float objects = sdSphere(p - vec3(-1.6, 1.0, 0.0), 1.0);
    objects = min(objects, sdRoundBox(p - vec3(0.9, 0.8, -1.2), vec3(0.8),
                                      0.1));
    objects = min(objects, sdTorus(p - vec3(1.2, 0.3, 1.2), vec2(0.7, 0.3)));
    return (p.y < objects) ? vec2(p.y, 0.0) : vec2(objects, 1.0);
}

vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec2(t, h.y);
        }
        t += h.x;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(t, -1.0);
}

vec3 calcNormal(vec3 p)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h).x +
                     k.yyx * map(p + k.yyx * h).x +
                     k.yxy * map(p + k.yxy * h).x +
                     k.xxx * map(p + k.xxx * h).x);
}

// バンプマッピング: 模様の値を高さとみなし、その勾配で法線を傾ける。
// 形状 (SDF) は変えないので、レイマーチングの計算量は増えない
vec3 bumpNormal(vec3 p, vec3 n, float strength)
{
    const float e = 0.002;
    vec3 grad = vec3(triplanar(p + vec3(e, 0.0, 0.0), n) -
                     triplanar(p - vec3(e, 0.0, 0.0), n),
                     triplanar(p + vec3(0.0, e, 0.0), n) -
                     triplanar(p - vec3(0.0, e, 0.0), n),
                     triplanar(p + vec3(0.0, 0.0, e), n) -
                     triplanar(p - vec3(0.0, 0.0, e), n)) / (2.0 * e);
    // 勾配のうち、表面に沿った成分だけで法線を傾ける
    grad -= n * dot(n, grad);
    return normalize(n - strength * grad);
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 64 && t < 20.0; i++) {
        float h = map(ro + t * rd).x;
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.01, 0.5);
    }
    return clamp(res, 0.0, 1.0);
}

vec3 shade(vec3 p, vec3 rd, float mat, bool textured)
{
    vec3 n = calcNormal(p);
    vec3 albedo = vec3(0.35);
    if (mat > 0.5) {
        albedo = vec3(0.8, 0.78, 0.72);
        if (textured) {
            float m = triplanar(p, n);
            albedo = mix(vec3(0.25, 0.22, 0.2), vec3(0.85, 0.82, 0.75), m);
            n = bumpNormal(p, n, 0.02);
        }
    }
    vec3 h = normalize(LIGHT_DIR - rd);
    float shadow = softShadow(p + calcNormal(p) * 0.01, LIGHT_DIR);
    float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
    float specular = pow(max(dot(n, h), 0.0), 32.0) * diffuse;
    float sky = 0.5 + 0.5 * n.y;
    return albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky) +
           SUN_COLOR * specular * 0.3;
}

mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // 画面の左右に、同じ構図の画像を 1 つずつ並べる
    vec2 halfSize = vec2(0.5 * iResolution.x, iResolution.y);
    bool textured = fragCoord.x > halfSize.x;
    vec2 local = vec2(mod(fragCoord.x, halfSize.x), fragCoord.y);
    vec2 p = (2.0 * local - halfSize) / halfSize.y;

    vec3 ro = vec3(0.0, 3.5, 7.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.5));

    vec3 col = SKY_COLOR;
    vec2 hit = raymarch(ro, rd);
    if (hit.y >= 0.0) {
        col = shade(ro + hit.x * rd, rd, hit.y, textured);
    }
    col = pow(col, vec3(1.0 / 2.2));
    col = mix(col, vec3(1.0), step(abs(fragCoord.x - 0.5 * iResolution.x), 1.0));
    fragColor = vec4(col, 1.0);
}
