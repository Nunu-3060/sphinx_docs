// 04_polar.frag
// 第 4 章: 極座標による回転方向の繰り返し。
// 歯車の歯と、周囲に並ぶ柱は、それぞれ 1 つ分の SDF だけで作っている。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;
const float PI        = 3.14159265;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));

// ---- SDF ----------------------------------------------------------------

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdCylinder(vec3 p, float r, float h)
{
    vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

float sdPlane(vec3 p, float h)
{
    return p.y - h;
}

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// ---- 回転方向の繰り返し --------------------------------------------------

// 2 次元の点 p を、原点のまわりに n 等分した扇形の 1 つに折りたたむ。
// 折りたたんだ点は、角度 0 の方向 (+x 軸) を中心とする扇形の中にある
vec2 opRepeatAngle(vec2 p, float n)
{
    float sector = 2.0 * PI / n;
    float angle = atan(p.y, p.x);
    angle -= sector * round(angle / sector);
    return length(p) * vec2(cos(angle), sin(angle));
}

// ---- シーン --------------------------------------------------------------

// 歯車: 円柱の本体に 16 枚の歯を付け、中心に穴を空ける
float sdGear(vec3 p)
{
    float body = sdCylinder(p, 1.2, 0.2);
    vec3 q = p;
    q.xz = opRepeatAngle(p.xz, 16.0);
    float tooth = sdBox(q - vec3(1.3, 0.0, 0.0), vec3(0.18, 0.2, 0.1));
    float hole = sdCylinder(p, 0.35, 0.3);
    return max(min(body, tooth), -hole);
}

// 周囲に並ぶ 10 本の柱
float sdPillars(vec3 p)
{
    vec3 q = p;
    q.xz = opRepeatAngle(p.xz, 10.0);
    return sdCylinder(q - vec3(3.5, 1.0, 0.0), 0.25, 1.0);
}

float map(vec3 p)
{
    // 歯車は時間とともに回転させる
    vec3 g = p - vec3(0.0, 0.6, 0.0);
    g.xz = rot(0.5 * iTime) * g.xz;
    float d = sdGear(g);
    d = min(d, sdPillars(p));
    d = min(d, sdPlane(p, 0.0));
    return d;
}

// ---- レンダリング --------------------------------------------------------

float raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        if (d < SURF_DIST) {
            return t;
        }
        t += d;
        if (t > MAX_DIST) {
            break;
        }
    }
    return -1.0;
}

vec3 calcNormal(vec3 p)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 64 && t < 20.0; i++) {
        float h = map(ro + t * rd);
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.01, 0.5);
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

    vec3 ro = vec3(0.0, 4.5, 7.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = vec3(0.3, 0.4, 0.55);
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) *
                        softShadow(pos + n * 0.01, LIGHT_DIR);
        float sky = 0.5 + 0.5 * n.y;
        vec3 albedo = (pos.y < 0.01) ? vec3(0.35) : vec3(0.75, 0.6, 0.35);
        col = albedo * (1.2 * diffuse + vec3(0.3, 0.4, 0.55) * sky);
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
