// 04_repetition.frag
// 第 4 章: 空間の繰り返し・回転・折り返しを組み合わせる。
// 1 つの形状の SDF だけで、無数の回転する箱を描く。

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

// ---- 変形 ----------------------------------------------------------------

// 2 次元の回転行列 (角度 a [rad])
mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// xz 平面を間隔 s の格子で無限に繰り返す。id には格子の番号を返す
vec3 opRepeatXZ(vec3 p, float s, out vec2 id)
{
    id = round(p.xz / s);
    p.xz -= s * id;
    return p;
}

// ---- シーン --------------------------------------------------------------

float map(vec3 p)
{
    float d = sdPlane(p, 0.0);

    vec2 id;
    vec3 q = opRepeatXZ(p, 2.0, id);
    q.y -= 0.6;
    // 格子ごとに位相をずらして y 軸まわりに回転させる
    q.xz = rot(iTime + 0.7 * (id.x + id.y)) * q.xz;
    // x 方向を折り返し、左右対称な形にする
    q.x = abs(q.x);
    float box = sdBox(q - vec3(0.25, 0.0, 0.0), vec3(0.2, 0.4, 0.4));
    d = min(d, box);
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

    vec3 ro = vec3(0.0, 3.0, 8.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.5));

    vec3 col = vec3(0.1);
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        col = shade(ro + t * rd);
    }
    fragColor = vec4(col, 1.0);
}
