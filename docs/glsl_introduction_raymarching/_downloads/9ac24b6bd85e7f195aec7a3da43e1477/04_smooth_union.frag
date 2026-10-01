// 04_smooth_union.frag
// 第 4 章: スムース合成。2 つの球が近づくと滑らかにつながる。
// 左は min による通常の和、右は smin による滑らかな和。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdPlane(vec3 p, float h)
{
    return p.y - h;
}

// ---- 合成 ----------------------------------------------------------------

// 多項式による smooth min。k は滑らかにつなぐ範囲の幅
float smin(float a, float b, float k)
{
    float h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h * h * k * 0.25;
}

// ---- シーン --------------------------------------------------------------

// 中心 c のまわりで 2 つの球を左右に往復させる
float twoSpheres(vec3 p, vec3 c, bool smoothBlend)
{
    float s = 0.9 * sin(iTime);
    float a = sdSphere(p - c - vec3(-s, 0.0, 0.0), 0.6);
    float b = sdSphere(p - c - vec3( s, 0.0, 0.0), 0.6);
    return smoothBlend ? smin(a, b, 0.5) : min(a, b);
}

float map(vec3 p)
{
    float d = sdPlane(p, 0.0);
    d = min(d, twoSpheres(p, vec3(-1.8, 0.8, 0.0), false));
    d = min(d, twoSpheres(p, vec3( 1.8, 0.8, 0.0), true));
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

    vec3 ro = vec3(0.0, 3.0, 7.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.5));

    vec3 col = vec3(0.1);
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        col = shade(ro + t * rd);
    }
    fragColor = vec4(col, 1.0);
}
