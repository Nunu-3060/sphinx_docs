// 14_slice.frag
// 第 14 章: 4 次元の超立方体 (テッセラクト) を 4 次元で回転させ、
// w = 0 の 3 次元の断面を描く。回転に伴って断面の形が変わっていく。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 50.0;
const float SURF_DIST = 0.001;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// 4 次元の角丸の箱。3 次元の箱 (第 3 章) の式が、そのまま 4 次元でも成り立つ
float sdBox4(vec4 p, vec4 b, float r)
{
    vec4 q = abs(p) - b + r;
    return length(max(q, 0.0)) +
           min(max(max(q.x, q.y), max(q.z, q.w)), 0.0) - r;
}

// 4 次元の点を回転させる。xw 平面と zw 平面の回転は、3 次元には無い回転である
vec4 rotate4(vec4 p, float time)
{
    p.xw = rot(0.7 * time) * p.xw;
    p.zw = rot(0.45 * time) * p.zw;
    p.xy = rot(0.3) * p.xy;
    return p;
}

// 3 次元の点 p を 4 次元の点 (p, 0) とみなし、回転させた超立方体の SDF を評価する。
// 4 次元の距離は、断面の中での距離以下なので、距離の下界として使える
float map(vec3 p)
{
    vec4 q = rotate4(vec4(p, 0.0), iTime);
    return sdBox4(q, vec4(1.0), 0.05);
}

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

    vec3 ro = vec3(3.5, 2.5, 4.5);
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 2.0));

    vec3 col = vec3(0.08, 0.09, 0.12) * (1.0 - 0.3 * length(p));
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos);
        // 4 次元の空間での位置によって色を変える
        vec4 q = rotate4(vec4(pos, 0.0), iTime);
        vec3 albedo = 0.55 + 0.45 * cos(vec3(0.0, 2.0, 4.0) + 1.5 * q.w);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0);
        float sky = 0.5 + 0.5 * n.y;
        col = albedo * (0.9 * diffuse + 0.25 * sky);
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
