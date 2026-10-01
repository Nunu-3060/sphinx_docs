// 13_mandelbulb.frag
// 第 13 章: マンデルバルブ。z <- z^8 + c を 3 次元の極座標で反復し、
// 距離推定関数 (DE) を SDF の代わりに使って描く。

const int   MAX_STEPS  = 200;
const float MAX_DIST   = 10.0;
const float SURF_DIST  = 0.0005;
const int   ITERATIONS = 8;
const float POWER      = 8.0;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));

// マンデルバルブの距離推定関数。trap には軌道が原点に最も近づいた距離を返す
float sdMandelbulb(vec3 c, out float trap)
{
    vec3 z = c;
    float dr = 1.0;   // |dz/dc| の近似
    float r = length(z);
    trap = r;
    for (int i = 0; i < ITERATIONS; i++) {
        if (r > 2.0) {
            break;        // 発散した
        }
        // 極座標で z を POWER 乗する
        float theta = acos(clamp(z.y / r, -1.0, 1.0)) * POWER;
        float phi = atan(z.z, z.x) * POWER;
        dr = POWER * pow(r, POWER - 1.0) * dr + 1.0;
        z = pow(r, POWER) *
            vec3(sin(theta) * cos(phi), cos(theta), sin(theta) * sin(phi)) + c;
        r = length(z);
        trap = min(trap, r);
    }
    return 0.5 * log(r) * r / dr;
}

float map(vec3 p, out float trap)
{
    // 外接球の外では球までの距離を返して反復を省く
    float bound = length(p) - 1.25;
    if (bound > 0.1) {
        trap = 1.0;
        return bound;
    }
    return sdMandelbulb(p, trap);
}

float map(vec3 p)
{
    float trap;
    return map(p, trap);
}

// 戻り値は (t, trap, 反復回数)。当たらなければ t は -1.0
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
    return vec3(-1.0, 0.0, float(MAX_STEPS));
}

vec3 calcNormal(vec3 p, float t)
{
    // 遠いほど差分の幅を大きくし、ノイズを抑える
    float h = 0.0005 * t;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h) +
                     k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) +
                     k.xxx * map(p + k.xxx * h));
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

    float angle = 0.8 + 0.15 * iTime;
    vec3 ro = vec3(2.6 * sin(angle), 1.2, 2.6 * cos(angle));
    vec3 ta = vec3(0.0, -0.1, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = vec3(0.05, 0.06, 0.09) + 0.05 * p.y;
    vec3 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos, hit.x);
        // 軌道トラップの値で色を付ける
        vec3 albedo = mix(vec3(0.9, 0.5, 0.2), vec3(0.2, 0.4, 0.8),
                          clamp(hit.y * 1.2 - 0.3, 0.0, 1.0));
        float diffuse = max(dot(n, LIGHT_DIR), 0.0);
        float back = max(dot(n, -LIGHT_DIR), 0.0);
        // 反復回数から求めた簡易 AO
        float occ = pow(1.0 - hit.z / float(MAX_STEPS), 2.0);
        col = albedo * (1.1 * diffuse + 0.15 * back + 0.35 * occ);
        col *= 0.4 + 0.6 * occ;
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
