// 20_still_life.frag
// 第 20 章: 実践: パストレーシングによる静物画。大理石の台の上に、金の器、ガラスの球、
// 翡翠の置物、メンガーのスポンジの置物を並べ、第 17 章のパストレーシングで描く。
// 第 11 章・第 12 章で近似した反射・屈折・サブサーフェススキャッタリングを、
// 経路の追跡で物理的に計算する。
//
// パスの構成
//   Common  : シーン、材質、サンプリングの関数
//   Buffer A: 経路を追跡し、前のフレームまでの結果に足し合わせる。iChannel0 は Buffer A
//   Image   : 蓄積した結果を平均して表示する。iChannel0 は Buffer A
// Shadertoy では、各区切りの中身を Common・Buffer A・Image のタブに貼り付け、
// Buffer A と Image の iChannel0 に Buffer A を設定する。

// ==== Common ====

// DEBUG_MODE を変えると、デバッグ用の表示になる (第 9 章)。
//   0: パストレーシング  1: ベースカラー  2: 法線  3: 材質の色分け
//  -1: 画面を 4 分割して 0〜3 を同時に表示する
#define DEBUG_MODE 0

// ---- 品質の設定 ----------------------------------------------------------

const int   SAMPLES   = 2;       // 1 フレーム、1 ピクセルあたりの経路の数
const int   MAX_DEPTH = 8;       // 1 経路あたりの最大反射回数
const int   MAX_STEPS = 160;
const float MAX_DIST  = 30.0;
const float SURF_DIST = 0.0005;
const float PI        = 3.14159265;

// ---- 乱数 (第 10 章、第 17 章) -------------------------------------------

uint seed;

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float random()
{
    seed = pcgHash(seed);
    return float(seed) / 4294967296.0;
}

vec2 hash22(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    uint h = pcgHash(q.x + pcgHash(q.y));
    return vec2(float(h), float(pcgHash(h))) / 4294967296.0;
}

// 法線 n に直交する 2 つの単位ベクトルを作る
void basis(vec3 n, out vec3 t, out vec3 b)
{
    vec3 a = abs(n.x) > 0.5 ? vec3(0.0, 1.0, 0.0) : vec3(1.0, 0.0, 0.0);
    t = normalize(cross(a, n));
    b = cross(n, t);
}

vec3 cosineSampleHemisphere(vec3 n)
{
    float u1 = random();
    float phi = 2.0 * PI * random();
    float r = sqrt(u1);
    vec3 t;
    vec3 b;
    basis(n, t, b);
    return normalize(r * cos(phi) * t + r * sin(phi) * b + sqrt(1.0 - u1) * n);
}

vec3 uniformSampleSphere()
{
    float z = 2.0 * random() - 1.0;
    float phi = 2.0 * PI * random();
    float r = sqrt(max(1.0 - z * z, 0.0));
    return vec3(r * cos(phi), r * sin(phi), z);
}

// ---- SDF -----------------------------------------------------------------

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float smin(float a, float b, float k)
{
    float h = max(k - abs(a - b), 0.0) / k;
    return min(a, b) - h * h * k * 0.25;
}

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// メンガーのスポンジ (第 13 章)。3 段階
float sdMenger(vec3 p)
{
    float d = sdBox(p, vec3(1.0));
    float scale = 1.0;
    for (int i = 0; i < 3; i++) {
        vec3 a = mod(p * scale, 2.0) - 1.0;
        scale *= 3.0;
        vec3 r = abs(1.0 - 3.0 * abs(a));
        float c = (min(max(r.x, r.y), min(max(r.y, r.z), max(r.z, r.x))) - 1.0) /
                  scale;
        d = max(d, c);
    }
    return d;
}

// ---- シーン --------------------------------------------------------------

const float MAT_LIGHT  = 1.0;   // 照明 (発光体)
const float MAT_WALL   = 2.0;   // 背景の壁 (拡散反射)
const float MAT_MARBLE = 3.0;   // 大理石の台 (拡散反射 + つや)
const float MAT_GOLD   = 4.0;   // 金の器 (金属)
const float MAT_GLASS  = 5.0;   // ガラスの球 (誘電体)
const float MAT_JADE   = 6.0;   // 翡翠の置物 (内部で散乱する)
const float MAT_CERAMIC = 7.0;  // メンガーのスポンジの置物 (拡散反射)

// 照明: y = LIGHT_Y の平面上の長方形で、下向きに発光する
const float LIGHT_Y      = 4.0;
const vec2  LIGHT_CENTER = vec2(-1.5, 1.0);   // xz
const vec2  LIGHT_HALF   = vec2(1.0, 0.8);    // xz の半分の大きさ
const vec3  LIGHT_EMIT   = vec3(14.0, 13.0, 11.8);
const vec3  ENVIRONMENT  = vec3(0.02, 0.024, 0.03);   // 部屋の外から届く光

// 各物体の SDF。内部を進むときに個別に使う
float sdGlass(vec3 p)
{
    return length(p - vec3(0.05, 0.5, 0.75)) - 0.5;
}

float sdJade(vec3 p)
{
    // 球を滑らかにつないだ、座った小動物のような形
    vec3 q = p - vec3(1.35, 0.0, -0.1);
    float body = length((q - vec3(0.0, 0.42, 0.0)) * vec3(1.0, 1.15, 1.0)) - 0.42;
    float head = length(q - vec3(0.05, 0.98, 0.05)) - 0.27;
    float ear1 = length(q - vec3(-0.12, 1.25, 0.0)) - 0.08;
    float ear2 = length(q - vec3(0.2, 1.24, 0.05)) - 0.08;
    float d = smin(body, head, 0.15);
    d = smin(d, min(ear1, ear2), 0.08);
    return d;
}

float sdBowl(vec3 p)
{
    // 球の殻を上で切り取った器
    vec3 q = p - vec3(-1.35, 0.62, 0.15);
    float shell = abs(length(q) - 0.62) - 0.035;
    return max(shell, q.y - 0.2);
}

float sdOrnament(vec3 p)
{
    vec3 q = p - vec3(0.6, 0.33, -1.15);
    q.xz = rot(0.6) * q.xz;
    return sdMenger(q / 0.33) * 0.33;
}

vec2 opU(vec2 a, vec2 b)
{
    return (a.x < b.x) ? a : b;
}

// 戻り値は (距離, 材質)
vec2 map(vec3 p)
{
    // 台 (上面が y = 0)
    vec2 res = vec2(sdBox(p - vec3(0.0, -0.15, 0.0), vec3(3.0, 0.15, 2.0)),
                    MAT_MARBLE);
    // 背景: 奥の壁と床
    res = opU(res, vec2(min(p.z + 2.6, p.y + 1.5), MAT_WALL));
    // 照明
    vec3 lp = p - vec3(LIGHT_CENTER.x, LIGHT_Y, LIGHT_CENTER.y);
    res = opU(res, vec2(sdBox(lp, vec3(LIGHT_HALF.x, 0.02, LIGHT_HALF.y)),
                        MAT_LIGHT));
    res = opU(res, vec2(sdBowl(p), MAT_GOLD));
    res = opU(res, vec2(sdGlass(p), MAT_GLASS));
    res = opU(res, vec2(sdJade(p), MAT_JADE));
    res = opU(res, vec2(sdOrnament(p), MAT_CERAMIC));
    return res;
}

vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec2(t, h.y);
        }
        t += h.x;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(t, -1.0);
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

// 物体 mat の内部を、方向 rd に表面まで進んだ距離を返す (第 11 章)
float marchInside(vec3 ro, vec3 rd, float mat)
{
    float t = 0.0;
    for (int i = 0; i < 96; i++) {
        vec3 p = ro + t * rd;
        float h = -((mat == MAT_GLASS) ? sdGlass(p) : sdJade(p));
        if (h < SURF_DIST) {
            break;
        }
        t += h;
    }
    return t;
}

// 物体 mat だけの SDF の勾配 (内部から外に出るときの法線)
vec3 objectNormal(vec3 p, float mat)
{
    const vec2 e = vec2(0.0005, 0.0);
    if (mat == MAT_GLASS) {
        return normalize(vec3(sdGlass(p + e.xyy) - sdGlass(p - e.xyy),
                              sdGlass(p + e.yxy) - sdGlass(p - e.yxy),
                              sdGlass(p + e.yyx) - sdGlass(p - e.yyx)));
    }
    return normalize(vec3(sdJade(p + e.xyy) - sdJade(p - e.xyy),
                          sdJade(p + e.yxy) - sdJade(p - e.yxy),
                          sdJade(p + e.yyx) - sdJade(p - e.yyx)));
}

// ---- 材質のパラメーター --------------------------------------------------

// 大理石の模様: ボロノイの境界 (第 10 章) を細い脈として描く
float marbleVeins(vec2 xz)
{
    vec2 x = 1.2 * xz + 0.3 * vec2(sin(3.0 * xz.y), cos(2.0 * xz.x));
    vec2 n = floor(x);
    vec2 f = fract(x);
    float f1 = 8.0;
    float f2 = 8.0;
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            float d = length(g + hash22(n + g) - f);
            if (d < f1) {
                f2 = f1;
                f1 = d;
            } else if (d < f2) {
                f2 = d;
            }
        }
    }
    return 1.0 - smoothstep(0.0, 0.05, f2 - f1);
}

vec3 baseColorOf(float mat, vec3 p)
{
    if (mat == MAT_WALL) {
        return vec3(0.35, 0.33, 0.3);
    }
    if (mat == MAT_MARBLE) {
        return mix(vec3(0.8, 0.78, 0.74), vec3(0.35, 0.33, 0.32),
                   0.8 * marbleVeins(p.xz));
    }
    if (mat == MAT_GOLD) {
        return vec3(1.0, 0.78, 0.34);
    }
    if (mat == MAT_JADE) {
        return vec3(0.55, 0.85, 0.6);
    }
    if (mat == MAT_CERAMIC) {
        return vec3(0.75, 0.72, 0.68);
    }
    return vec3(1.0);
}

// ---- BRDF とサンプリング (第 12 章) --------------------------------------

float distributionGGX(float nh, float alpha)
{
    float a2 = alpha * alpha;
    float d = nh * nh * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}

float geometrySmith(float nv, float nl, float roughness)
{
    // 間接光にも使うので、Karis の画像ベースの照明用の係数 k = α / 2 を使う
    float k = roughness * roughness / 2.0;
    return (nv / (nv * (1.0 - k) + k)) * (nl / (nl * (1.0 - k) + k));
}

vec3 fresnelSchlick(float cosTheta, vec3 f0)
{
    return f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0);
}

// GGX の分布に従ってマイクロファセットの法線 h を選ぶ (重点サンプリング)
vec3 sampleGGX(vec3 n, float alpha)
{
    float u1 = random();
    float phi = 2.0 * PI * random();
    float cosTheta = sqrt((1.0 - u1) / (1.0 + (alpha * alpha - 1.0) * u1));
    float sinTheta = sqrt(max(1.0 - cosTheta * cosTheta, 0.0));
    vec3 t;
    vec3 b;
    basis(n, t, b);
    return normalize(sinTheta * cos(phi) * t + sinTheta * sin(phi) * b +
                     cosTheta * n);
}

// 鏡面反射の BRDF × cos の値 (光源の直接サンプリングで使う)
vec3 specularBRDF(vec3 n, vec3 v, vec3 l, vec3 f0, float roughness)
{
    vec3 h = normalize(v + l);
    float nl = max(dot(n, l), 0.0);
    float nv = max(dot(n, v), 1e-4);
    float alpha = roughness * roughness;
    return distributionGGX(max(dot(n, h), 0.0), alpha) *
           geometrySmith(nv, nl, roughness) *
           fresnelSchlick(max(dot(h, v), 0.0), f0) / (4.0 * nv + 1e-4);
}

// ---- 光源の直接サンプリング (第 17 章) -----------------------------------

// 照明上の 1 点を一様に選び、その点から点 p に届く光を返す (面積測度での推定。
// 表面側の cos と BRDF は含まない)。toLight には照明への方向を返す
vec3 sampleLight(vec3 p, vec3 n, out vec3 toLight)
{
    vec2 xz = LIGHT_CENTER + (2.0 * vec2(random(), random()) - 1.0) * LIGHT_HALF;
    vec3 lp = vec3(xz.x, LIGHT_Y - 0.02, xz.y);
    vec3 d = lp - p;
    float dist2 = dot(d, d);
    toLight = d * inversesqrt(dist2);
    float cosLight = toLight.y;           // 照明の法線 (0, -1, 0) と -toLight の内積
    if (dot(n, toLight) <= 0.0 || cosLight <= 0.0) {
        return vec3(0.0);
    }
    vec2 hit = raymarch(p, toLight);
    if (hit.y != MAT_LIGHT) {
        return vec3(0.0);
    }
    float area = 4.0 * LIGHT_HALF.x * LIGHT_HALF.y;
    return LIGHT_EMIT * cosLight / dist2 * area;
}

// ---- 経路の追跡 ----------------------------------------------------------

// 翡翠の内部での散乱 (ランダムウォーク法)。単位は 1 長さあたり
const vec3  JADE_SIGMA_T = vec3(9.0);                 // 消散係数
const vec3  JADE_ALBEDO  = vec3(0.92, 0.985, 0.94);   // 散乱アルベド (散乱 / 消散)
const float GLASS_IOR    = 1.5;
const float JADE_IOR     = 1.45;

vec3 tracePath(vec3 ro, vec3 rd)
{
    vec3 radiance = vec3(0.0);
    vec3 throughput = vec3(1.0);
    // 直前の反射で光源の直接サンプリングを行っていなければ、
    // 照明に当たったときにその光を加える (二重に数えないため)
    bool countEmission = true;

    for (int depth = 0; depth < MAX_DEPTH; depth++) {
        vec2 hit = raymarch(ro, rd);
        if (hit.y < 0.0) {
            radiance += throughput * ENVIRONMENT;
            break;
        }
        if (hit.y == MAT_LIGHT) {
            if (countEmission) {
                radiance += throughput * LIGHT_EMIT;
            }
            break;
        }
        vec3 p = ro + hit.x * rd;
        vec3 n = calcNormal(p);
        vec3 v = -rd;
        vec3 base = baseColorOf(hit.y, p);

        if (hit.y == MAT_GLASS) {
            // ---- ガラス: 反射と屈折をフレネル反射率で確率的に選ぶ ----
            float f = fresnelSchlick(max(dot(n, v), 0.0), vec3(0.04)).x;
            if (random() < f) {
                ro = p + n * 0.002;
                rd = reflect(rd, n);
            } else {
                // 内部に入り、全反射を繰り返しながら出口を探す
                vec3 dir = refract(rd, n, 1.0 / GLASS_IOR);
                vec3 q = p - n * 0.002;
                for (int k = 0; k < 4; k++) {
                    q += marchInside(q, dir, MAT_GLASS) * dir;
                    vec3 nOut = objectNormal(q, MAT_GLASS);
                    vec3 out_ = refract(dir, -nOut, GLASS_IOR);
                    float fi = fresnelSchlick(max(dot(-dir, -nOut), 0.0),
                                              vec3(0.04)).x;
                    if (dot(out_, out_) > 0.0 && random() > fi) {
                        dir = out_;
                        q += nOut * 0.004;
                        break;
                    }
                    dir = reflect(dir, -nOut);   // 内部での反射
                    q -= nOut * 0.002;
                }
                ro = q;
                rd = dir;
            }
            countEmission = true;
            continue;
        }

        if (hit.y == MAT_JADE) {
            // ---- 翡翠: 表面での反射か、内部に入ってランダムウォーク ----
            float f = fresnelSchlick(max(dot(n, v), 0.0), vec3(0.035)).x;
            if (random() < f) {
                ro = p + n * 0.002;
                rd = reflect(rd, n);
                countEmission = true;
                continue;
            }
            vec3 dir = refract(rd, n, 1.0 / JADE_IOR);
            vec3 q = p - n * 0.002;
            bool escaped = false;
            for (int k = 0; k < 64; k++) {
                // 次の散乱までの距離を、指数分布からランダムに選ぶ
                float s = -log(max(random(), 1e-6)) / JADE_SIGMA_T.x;
                float exitDist = marchInside(q, dir, MAT_JADE);
                if (s < exitDist) {
                    q += s * dir;
                    throughput *= JADE_ALBEDO;          // 散乱のたびに少し吸収される
                    dir = uniformSampleSphere();        // 等方散乱
                } else {
                    q += exitDist * dir;
                    escaped = true;
                    break;
                }
            }
            if (!escaped) {
                break;                                  // 内部で吸収された
            }
            // 出口からは拡散的に (ランバート反射と同じ分布で) 出ていくとみなす。
            // そのため、拡散反射と同じく光源の直接サンプリングを使える
            vec3 nOut = objectNormal(q, MAT_JADE);
            ro = q + nOut * 0.004;
            vec3 toLight;
            vec3 light = sampleLight(ro, nOut, toLight);
            radiance += throughput * light * max(dot(nOut, toLight), 0.0) / PI;
            rd = cosineSampleHemisphere(nOut);
            countEmission = false;
            continue;
        }

        if (hit.y == MAT_GOLD) {
            // ---- 金属: GGX の重点サンプリングと光源の直接サンプリング ----
            const float roughness = 0.3;
            vec3 toLight;
            vec3 light = sampleLight(p + n * 0.002, n, toLight);
            radiance += throughput * light *
                        specularBRDF(n, v, toLight, base, roughness);
            vec3 h = sampleGGX(n, roughness * roughness);
            vec3 l = reflect(rd, h);
            float nl = dot(n, l);
            if (nl <= 0.0) {
                break;
            }
            float nv = max(dot(n, v), 1e-4);
            float vh = max(dot(v, h), 0.0);
            float nh = max(dot(n, h), 1e-4);
            // BRDF × cos / pdf = F × G × (v・h) / ((n・v)(n・h))
            throughput *= fresnelSchlick(vh, base) *
                          geometrySmith(nv, nl, roughness) * vh / (nv * nh);
            ro = p + n * 0.002;
            rd = l;
            countEmission = false;
        } else if (hit.y == MAT_MARBLE && random() < 0.2) {
            // ---- 大理石のつや: 確率 0.2 で鏡面反射の成分を選ぶ ----
            const float roughness = 0.15;
            vec3 h = sampleGGX(n, roughness * roughness);
            vec3 l = reflect(rd, h);
            float nl = dot(n, l);
            if (nl <= 0.0) {
                break;
            }
            float nv = max(dot(n, v), 1e-4);
            float vh = max(dot(v, h), 0.0);
            float nh = max(dot(n, h), 1e-4);
            throughput *= fresnelSchlick(vh, vec3(0.04)) *
                          geometrySmith(nv, nl, roughness) * vh /
                          (nv * nh) / 0.2;
            ro = p + n * 0.002;
            rd = l;
            countEmission = true;   // この成分は直接サンプリングで数えていない
        } else {
            // ---- 拡散反射: 光源の直接サンプリングとコサイン重み付きの方向選択 ----
            float diffuseProb = (hit.y == MAT_MARBLE) ? 0.8 : 1.0;
            vec3 toLight;
            vec3 light = sampleLight(p + n * 0.002, n, toLight);
            radiance += throughput * light * base / PI *
                        max(dot(n, toLight), 0.0) / diffuseProb;
            throughput *= base / diffuseProb;
            ro = p + n * 0.002;
            rd = cosineSampleHemisphere(n);
            countEmission = false;
        }

        // ロシアンルーレット: 寄与の小さい経路を確率的に打ち切る (第 17 章)
        if (depth >= 3) {
            float survive = clamp(max(throughput.r, max(throughput.g,
                                                        throughput.b)),
                                  0.05, 0.95);
            if (random() > survive) {
                break;
            }
            throughput /= survive;
        }
    }
    return radiance;
}

// ---- カメラ (第 17 章の薄レンズモデル) -----------------------------------

const float FOCAL          = 2.4;
const float FOCUS_DISTANCE = 4.3;     // ガラスの球のあたりにピントを合わせる
const float APERTURE       = 0.05;

void cameraRay(vec2 p, out vec3 ro, out vec3 rd)
{
    vec3 eye = vec3(0.0, 1.5, 4.8);
    vec3 target = vec3(0.0, 0.45, 0.0);
    vec3 forward = normalize(target - eye);
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    vec3 dir = normalize(p.x * right + p.y * up + FOCAL * forward);
    vec3 focusPoint = eye + dir * (FOCUS_DISTANCE / dot(dir, forward));
    float r = APERTURE * sqrt(random());
    float phi = 2.0 * PI * random();
    ro = eye + r * (cos(phi) * right + sin(phi) * up);
    rd = normalize(focusPoint - ro);
}

// デバッグ用の表示 (mode 1〜3)。経路の追跡はせず、最初に当たった点の情報を返す
vec3 debugColor(int mode, vec3 ro, vec3 rd)
{
    vec2 hit = raymarch(ro, rd);
    if (hit.y < 0.0) {
        return vec3(0.0);
    }
    vec3 p = ro + hit.x * rd;
    if (mode == 1) {
        return baseColorOf(hit.y, p);
    }
    if (mode == 2) {
        return 0.5 + 0.5 * calcNormal(p);
    }
    return 0.5 + 0.45 * cos(6.2831853 * (hit.y / 7.0 + vec3(0.0, 0.33, 0.67)));
}

// ==== Buffer A ====
// 経路を追跡し、前のフレームまでの合計に足し合わせる。
// rgb に放射輝度の合計、a に経路の数の合計を保存する

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    seed = pcgHash(uint(fragCoord.x) + uint(fragCoord.y) * 4096u +
                   uint(iFrame) * 16777216u);

    vec2 uv = fragCoord / iResolution.xy;
    int mode = DEBUG_MODE;
    vec2 frag = fragCoord;
    if (mode < 0) {
        vec2 cell = floor(uv * 2.0);
        mode = int(cell.x) + 2 * int(1.0 - cell.y);   // 左上から 0, 1, 2, 3
        frag = fract(uv * 2.0) * iResolution.xy;
    }

    vec3 sum = vec3(0.0);
    for (int i = 0; i < SAMPLES; i++) {
        vec2 jitter = vec2(random(), random()) - 0.5;
        vec2 p = (2.0 * (frag + jitter) - iResolution.xy) / iResolution.y;
        vec3 ro;
        vec3 rd;
        cameraRay(p, ro, rd);
        sum += (mode == 0) ? tracePath(ro, rd)
                           : pow(debugColor(mode, ro, rd), vec3(2.2));
    }
    vec4 previous = (iFrame == 0) ? vec4(0.0)
                                  : texelFetch(iChannel0, ivec2(fragCoord), 0);
    fragColor = previous + vec4(sum, float(SAMPLES));
}

// ==== Image ====
// 蓄積した合計を経路の数で割って平均し、トーンマッピングして表示する

vec3 toneMapACES(vec3 x)
{
    x *= 0.6;
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec4 data = texelFetch(iChannel0, ivec2(fragCoord), 0);
    vec3 col = data.rgb / max(data.a, 1.0);
    // デバッグ表示 (mode 1〜3) の領域はトーンマッピングしない
    bool debugArea = DEBUG_MODE > 0 ||
                     (DEBUG_MODE < 0 && (fragCoord.x >= 0.5 * iResolution.x ||
                                         fragCoord.y < 0.5 * iResolution.y));
    col = debugArea ? col : toneMapACES(col);
    fragColor = vec4(pow(col, vec3(1.0 / 2.2)), 1.0);
}
