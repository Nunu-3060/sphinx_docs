// 13_menger.frag
// 第 13 章: メンガーのスポンジ。箱から十字の穴を繰り返しくり抜いて作る。
// 空間の繰り返し (第 4 章) を縮尺を変えながら何度も適用する。

const int   MAX_STEPS  = 160;
const float MAX_DIST   = 20.0;
const float SURF_DIST  = 0.0005;
const int   ITERATIONS = 4;      // くり抜く回数 (フラクタルの深さ)

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// メンガーのスポンジの SDF。戻り値は (距離, 最後にくり抜いた階層)
vec2 sdMenger(vec3 p)
{
    float d = sdBox(p, vec3(1.0));
    float scale = 1.0;
    float level = 0.0;
    for (int i = 0; i < ITERATIONS; i++) {
        // 1 辺 2 / scale の立方体で空間を繰り返す
        vec3 a = mod(p * scale, 2.0) - 1.0;
        scale *= 3.0;
        // 3 方向に貫通する十字形の穴までの距離
        vec3 r = abs(1.0 - 3.0 * abs(a));
        float da = max(r.x, r.y);
        float db = max(r.y, r.z);
        float dc = max(r.z, r.x);
        float c = (min(da, min(db, dc)) - 1.0) / scale;
        if (c > d) {
            d = c;               // 穴の方が表面を決めている
            level = float(i + 1);
        }
    }
    return vec2(d, level);
}

vec2 map(vec3 p)
{
    return sdMenger(p);
}

// 戻り値は (t, 階層, 反復回数)。当たらなければ t は -1.0
vec3 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        // 遠いほど閾値を大きくする (1 ピクセルより細かい構造は見えない)
        if (h.x < SURF_DIST * t) {
            return vec3(t, h.y, float(i));
        }
        t += h.x;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec3(-1.0, 0.0, float(MAX_STEPS));
}

vec3 calcNormal(vec3 p)
{
    const float h = 0.0002;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h).x +
                     k.yyx * map(p + k.yyx * h).x +
                     k.yxy * map(p + k.yxy * h).x +
                     k.xxx * map(p + k.xxx * h).x);
}

float softShadow(vec3 ro, vec3 rd, float k)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 64 && t < 5.0; i++) {
        float h = map(ro + t * rd).x;
        res = min(res, k * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.005, 0.2);
    }
    return clamp(res, 0.0, 1.0);
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
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    float angle = 0.6 + 0.2 * iTime;
    vec3 ro = vec3(3.2 * sin(angle), 2.0, 3.2 * cos(angle));
    vec3 ta = vec3(0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 bg = vec3(0.12, 0.13, 0.16) * (1.0 - 0.3 * length(p));
    vec3 col = bg;
    vec3 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos);
        // 階層ごとに色を変える
        vec3 albedo = 0.5 + 0.35 * cos(vec3(0.0, 0.6, 1.2) + 0.9 * hit.y);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) *
                        softShadow(pos + n * 0.002, LIGHT_DIR, 16.0);
        // 反復回数が多い場所は細かい隙間に近いとみなし、暗くする (簡易 AO)
        float occ = 1.0 - hit.z / float(MAX_STEPS);
        col = albedo * (1.2 * diffuse + 0.3 * occ * (0.6 + 0.4 * n.y));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
