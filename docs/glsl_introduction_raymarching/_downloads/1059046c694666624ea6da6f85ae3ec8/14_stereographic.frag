// 14_stereographic.frag
// 第 14 章: 3 次元球面 S^3 上のクリフォードトーラスを、ステレオ投影で 3 次元に写して描く。
// トーラスは、ホップファイバーに沿ったリボンに切り分けてある。
// 4 次元の回転によって、投影された形が大きく変化する。

const int   MAX_STEPS  = 200;
const float MAX_DIST   = 40.0;
const float SURF_DIST  = 0.0005;
const float STEP_SCALE = 0.7;    // 距離の補正が近似なので、歩幅を小さくする
const float PI         = 3.14159265;

const float RIBBONS = 12.0;      // リボンの本数
const vec3  LIGHT_DIR = normalize(vec3(0.5, 0.8, 0.3));

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// 3 次元の点 p を、逆ステレオ投影で S^3 (4 次元の単位球面) 上の点に写す。
// 投影の中心は (0, 0, 0, 1)
vec4 inverseStereographic(vec3 p)
{
    float r2 = dot(p, p);
    return vec4(2.0 * p, r2 - 1.0) / (r2 + 1.0);
}

// S^3 上の点 q から、リボン状に切ったクリフォードトーラスまでの距離 (S^3 上の距離)。
// 戻り値の y にはリボンの番号を返す
vec2 sdRibbonTorus(vec4 q)
{
    // q = (cos α e^{iφ1}, sin α e^{iφ2}) と表したときの α、φ1、φ2
    float alpha = atan(length(q.zw), length(q.xy));
    float phi1 = atan(q.y, q.x);
    float phi2 = atan(q.w, q.z);

    // α = π / 4 のトーラス (クリフォードトーラス) からの距離。厚さは 0.03
    float shell = abs(alpha - 0.25 * PI) - 0.03;

    // φ1 - φ2 が一定の曲線はホップファイバー (S^3 上の大円) になる。
    // その方向に沿ったリボンに切り分ける (トーラス上の距離は角度の差の半分)
    float u = phi1 - phi2;
    float period = 2.0 * PI / RIBBONS;
    float id = round(u / period);
    float ribbon = 0.5 * abs(u - id * period) - 0.06;

    return vec2(max(shell, ribbon), mod(id, RIBBONS));
}

// 3 次元での距離の近似と、リボンの番号を返す
vec2 map(vec3 p)
{
    vec4 q = inverseStereographic(p);
    // 4 次元で回転させる (S^3 はどの回転でも自分自身に写る)
    q.xw = rot(0.3 * iTime) * q.xw;
    q.yz = rot(0.2 * iTime) * q.yz;
    vec2 res = sdRibbonTorus(q);
    // 逆ステレオ投影は局所的に 2 / (1 + |p|^2) 倍の拡大なので、
    // S^3 上の距離をその倍率で割って 3 次元の距離に直す
    res.x *= 0.5 * (1.0 + dot(p, p));
    return res;
}

vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST * max(t, 1.0)) {
            return vec2(t, h.y);
        }
        t += h.x * STEP_SCALE;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(-1.0, 0.0);
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

    vec3 ro = vec3(0.0, 3.0, 5.0);
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 1.6));

    vec3 col = vec3(0.06, 0.07, 0.1) * (1.0 - 0.3 * length(p));
    vec2 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos);
        // リボンごとに色を変える (第 7 章の余弦関数によるパレット)
        vec3 albedo = 0.5 + 0.45 * cos(6.2831853 * (hit.y / RIBBONS +
                                                   vec3(0.0, 0.33, 0.67)));
        float diffuse = max(dot(n, LIGHT_DIR), 0.0);
        float back = max(dot(n, -LIGHT_DIR), 0.0);
        col = albedo * (0.9 * diffuse + 0.2 * back + 0.15);
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
