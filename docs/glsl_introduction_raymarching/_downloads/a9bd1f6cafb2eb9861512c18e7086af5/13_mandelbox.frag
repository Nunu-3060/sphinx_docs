// 13_mandelbox.frag
// 第 13 章: マンデルボックス。ボックスフォールド、スフィアフォールド、拡大と平行移動を
// 繰り返してできるフラクタル。拡大率を時間とともにゆっくり変え、形の変化を見せる。

const int   MAX_STEPS  = 200;
const float MAX_DIST   = 30.0;
const float SURF_DIST  = 0.0004;
const int   ITERATIONS = 12;

const float MIN_RADIUS2   = 0.25;   // スフィアフォールドの内側の球の半径の 2 乗
const float FIXED_RADIUS2 = 1.0;    // スフィアフォールドの外側の球の半径の 2 乗

const vec3 LIGHT_DIR = normalize(vec3(0.5, 0.8, 0.4));

// 拡大率。2 から 3 の間でゆっくり変える
float scaleAt(float time)
{
    return 2.5 + 0.3 * sin(0.15 * time);
}

// ボックスフォールド: 範囲 [-1, 1] の外に出た座標を、境界で折り返す
vec3 boxFold(vec3 z)
{
    return clamp(z, -1.0, 1.0) * 2.0 - z;
}

// スフィアフォールド: 原点に近い点を外側へ、ある範囲の点を球面について反転させる。
// 点を k 倍するので、距離推定のための導関数の大きさ dr も k 倍する
void sphereFold(inout vec3 z, inout float dr)
{
    float r2 = dot(z, z);
    if (r2 < MIN_RADIUS2) {
        float k = FIXED_RADIUS2 / MIN_RADIUS2;   // 内側の球の中は一定の倍率で拡大
        z *= k;
        dr *= k;
    } else if (r2 < FIXED_RADIUS2) {
        float k = FIXED_RADIUS2 / r2;            // 球面についての反転
        z *= k;
        dr *= k;
    }
}

// マンデルボックスの距離推定関数。trap には軌道が原点に最も近づいた距離の 2 乗を返す
float sdMandelbox(vec3 p, float scale, out float trap)
{
    vec3 z = p;
    float dr = 1.0;     // 導関数の大きさの近似
    trap = 1e10;
    for (int i = 0; i < ITERATIONS; i++) {
        z = boxFold(z);
        sphereFold(z, dr);
        z = scale * z + p;               // 拡大と平行移動
        dr = dr * abs(scale) + 1.0;
        trap = min(trap, dot(z, z));
    }
    return length(z) / abs(dr);
}

float map(vec3 p, out float trap)
{
    return sdMandelbox(p, scaleAt(iTime), trap);
}

float map(vec3 p)
{
    float trap;
    return map(p, trap);
}

// 戻り値は (t, trap, 反復回数)。当たらなければ t は -1
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
    float h = 0.0005 * t;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 48 && t < 5.0; i++) {
        float h = map(ro + t * rd);
        res = min(res, 8.0 * h / t);
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

    float angle = 0.7 + 0.08 * iTime;
    vec3 ro = vec3(12.0 * sin(angle), 6.5, 12.0 * cos(angle));
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 1.8));

    vec3 col = vec3(0.07, 0.08, 0.1) * (1.0 - 0.3 * length(p));
    vec3 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos, hit.x);
        // 軌道トラップの値で色を付ける (第 7 章の余弦関数によるパレット)
        float m = clamp(0.25 * log(hit.y + 1.0), 0.0, 1.0);
        vec3 albedo = 0.55 + 0.4 * cos(6.2831853 * (m + vec3(0.1, 0.25, 0.4)));
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) *
                        softShadow(pos + n * 0.002 * hit.x, LIGHT_DIR);
        float occ = pow(1.0 - hit.z / float(MAX_STEPS), 2.0);   // 簡易 AO
        col = albedo * (1.1 * diffuse + 0.35 * occ * (0.6 + 0.4 * n.y));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
