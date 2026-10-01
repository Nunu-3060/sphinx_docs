// 14_julia.frag
// 第 14 章: 四元数ジュリア集合。z <- z^2 + c を四元数で反復してできる 4 次元の
// フラクタルを、w = 0 の 3 次元の断面で描く。c を時間とともに変化させる。

const int   MAX_STEPS  = 200;
const float MAX_DIST   = 10.0;
const float SURF_DIST  = 0.0005;
const int   ITERATIONS = 16;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));

// 四元数の 2 乗: (a, v)^2 = (a^2 - v・v, 2 a v)。ここでは x を実部とする
vec4 quatSquare(vec4 q)
{
    return vec4(q.x * q.x - dot(q.yzw, q.yzw), 2.0 * q.x * q.yzw);
}

// 四元数ジュリア集合の距離推定関数 (第 13 章のマンデルバルブと同じ形)。
// trap には軌道が原点に最も近づいた距離の 2 乗を返す
float sdJulia(vec3 p, vec4 c, out float trap)
{
    vec4 z = vec4(p, 0.0);
    float dz2 = 1.0;          // |dz/dz0|^2
    float z2 = dot(z, z);     // |z|^2
    trap = z2;
    for (int i = 0; i < ITERATIONS; i++) {
        dz2 *= 4.0 * z2;      // |z'| <- 2 |z| |z'|
        z = quatSquare(z) + c;
        z2 = dot(z, z);
        trap = min(trap, z2);
        if (z2 > 256.0) {
            break;
        }
    }
    // d = 0.5 |z| log|z| / |z'| を 2 乗の値から計算する
    return 0.25 * log(z2) * sqrt(z2 / dz2);
}

// 定数 c。形の面白い値の 1 つを選び、そのまわりで少しずつ変化させる
vec4 juliaConstant()
{
    vec4 base = vec4(-0.137, -0.630, -0.475, -0.046);
    return base + 0.05 * sin(0.5 * iTime * vec4(1.0, 1.3, 1.7, 2.1));
}

float map(vec3 p, out float trap)
{
    return sdJulia(p, juliaConstant(), trap);
}

float map(vec3 p)
{
    float trap;
    return map(p, trap);
}

vec3 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float trap;
        float d = map(ro + t * rd, trap);
        if (d < SURF_DIST * t) {
            return vec3(t, trap, float(i));
        }
        t += d;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec3(-1.0, 0.0, 0.0);
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

    float angle = 0.5 + 0.2 * iTime;
    vec3 ro = 3.2 * vec3(sin(angle), 0.5, cos(angle));
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 2.0));

    vec3 col = vec3(0.07, 0.08, 0.11) * (1.0 - 0.3 * length(p));
    vec3 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos, hit.x);
        vec3 albedo = mix(vec3(0.9, 0.35, 0.15), vec3(0.95, 0.85, 0.6),
                          clamp(sqrt(hit.y), 0.0, 1.0));
        float diffuse = max(dot(n, LIGHT_DIR), 0.0);
        float occ = 1.0 - hit.z / float(MAX_STEPS);
        col = albedo * (1.0 * diffuse + 0.3 * occ * (0.6 + 0.4 * n.y));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
