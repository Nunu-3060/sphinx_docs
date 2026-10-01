// 13_kifs.frag
// 第 13 章: 折り返しによるフラクタル (KIFS: kaleidoscopic iterated function system)。
// 座標平面と対角面での折り返し、回転、拡大と平行移動を繰り返す。
// 回転の角度を時間とともに変えると、形が万華鏡のように変化する。

const int   MAX_STEPS  = 160;
const float MAX_DIST   = 20.0;
const float SURF_DIST  = 0.0005;
const int   ITERATIONS = 8;
const float SCALE      = 2.5;                   // 1 回の反復での拡大率
const vec3  OFFSET     = vec3(1.0, 1.0, 1.0);   // 拡大の中心

const vec3 LIGHT_DIR = normalize(vec3(0.5, 0.8, 0.4));

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// KIFS の距離推定関数
float sdKIFS(vec3 p, float angle)
{
    mat2 r1 = rot(angle);
    mat2 r2 = rot(0.7 * angle);
    float scale = 1.0;   // ここまでの拡大率の積
    for (int i = 0; i < ITERATIONS; i++) {
        // 3 つの座標平面で折り返す
        p = abs(p);
        // x >= y >= z となるように並べ替える。これは 3 つの対角面での折り返しに当たる
        if (p.x < p.y) p.xy = p.yx;
        if (p.x < p.z) p.xz = p.zx;
        if (p.y < p.z) p.yz = p.zy;
        // 回転させる
        p.xy = r1 * p.xy;
        p.yz = r2 * p.yz;
        // OFFSET を中心に拡大する
        p = SCALE * p - OFFSET * (SCALE - 1.0);
        scale *= SCALE;
    }
    // 最後に小さな箱を置き、拡大率の積で割って元の尺度の距離に戻す
    return sdBox(p, vec3(1.0)) / scale;
}

float map(vec3 p)
{
    return sdKIFS(p, 0.12 + 0.08 * sin(0.2 * iTime));
}

// 戻り値は (t, 反復回数)。当たらなければ t は -1
vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        if (d < SURF_DIST * t) {
            return vec2(t, float(i));
        }
        t += d;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(-1.0, float(MAX_STEPS));
}

vec3 calcNormal(vec3 p, float t)
{
    float h = 0.0005 * t;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
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

    float angle = 0.5 + 0.1 * iTime;
    vec3 ro = vec3(3.2 * sin(angle), 1.8, 3.2 * cos(angle));
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 1.8));

    vec3 col = vec3(0.06, 0.07, 0.09) * (1.0 - 0.3 * length(p));
    vec2 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos, hit.x);
        vec3 albedo = 0.55 + 0.4 * cos(vec3(0.0, 0.8, 1.6) + 2.0 * length(pos));
        float diffuse = max(dot(n, LIGHT_DIR), 0.0);
        float occ = pow(1.0 - hit.y / float(MAX_STEPS), 2.0);
        col = albedo * (1.0 * diffuse + 0.35 * occ * (0.6 + 0.4 * n.y));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
