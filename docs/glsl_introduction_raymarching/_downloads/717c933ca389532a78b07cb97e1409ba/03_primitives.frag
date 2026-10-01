// 03_primitives.frag
// 第 3 章: 基本形状の SDF を並べて表示する。
// 陰影の計算 (calcNormal と shade) の詳細は第 5 章で解説する。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;

// ---- 基本形状の SDF ------------------------------------------------------

// 球: 中心は原点、半径 r
float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

// 箱: 中心は原点、各軸方向の半分の長さ b
float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// 角丸の箱: 外形の半分の長さ b、角の丸みの半径 r
float sdRoundBox(vec3 p, vec3 b, float r)
{
    return sdBox(p, b - r) - r;
}

// トーラス: xz 平面上の半径 t.x の円のまわりの半径 t.y の管
float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// 円柱: y 軸が中心軸、半径 r、高さの半分 h
float sdCylinder(vec3 p, float r, float h)
{
    vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// カプセル: 線分 ab から半径 r 以内の領域
float sdCapsule(vec3 p, vec3 a, vec3 b, float r)
{
    vec3 pa = p - a;
    vec3 ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}

// 平面: y = h
float sdPlane(vec3 p, float h)
{
    return p.y - h;
}

// ---- シーン --------------------------------------------------------------

float map(vec3 p)
{
    float d = sdPlane(p, 0.0);
    // 奥の列
    d = min(d, sdSphere(p - vec3(-2.5, 0.8, -1.5), 0.8));
    d = min(d, sdBox(p - vec3(0.0, 0.7, -1.5), vec3(0.7)));
    d = min(d, sdRoundBox(p - vec3(2.5, 0.7, -1.5), vec3(0.7), 0.2));
    // 手前の列
    d = min(d, sdTorus(p - vec3(-2.5, 0.25, 1.5), vec2(0.7, 0.25)));
    d = min(d, sdCylinder(p - vec3(0.0, 0.7, 1.5), 0.6, 0.7));
    d = min(d, sdCapsule(p, vec3(2.0, 0.4, 1.5), vec3(3.0, 1.2, 1.5), 0.4));
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

// SDF の勾配から法線を求める (第 5 章)
vec3 calcNormal(vec3 p)
{
    const vec2 e = vec2(0.001, 0.0);
    return normalize(vec3(map(p + e.xyy) - map(p - e.xyy),
                          map(p + e.yxy) - map(p - e.yxy),
                          map(p + e.yyx) - map(p - e.yyx)));
}

// 簡単な拡散反射の陰影 (第 5 章)
vec3 shade(vec3 p)
{
    vec3 n = calcNormal(p);
    vec3 lightDir = normalize(vec3(0.6, 0.8, 0.4));
    float diffuse = max(dot(n, lightDir), 0.0);
    // 地面 (y = 0) は暗めの灰色、それ以外は明るい灰色にする
    vec3 albedo = (p.y < 0.01) ? vec3(0.45) : vec3(0.9);
    return albedo * (0.15 + 0.85 * diffuse);
}

// カメラ位置 ro から注視点 ta を向くカメラ行列 (第 2 章)
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

    vec3 ro = vec3(0.0, 6.0, 7.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.5));

    vec3 col = vec3(0.1);
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        col = shade(ro + t * rd);
    }
    fragColor = vec4(col, 1.0);
}
