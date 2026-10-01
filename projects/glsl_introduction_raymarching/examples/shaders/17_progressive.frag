// 17_progressive.frag
// 第 17 章: 複数パスによるパストレーシング。Buffer A で毎フレーム少数の経路を追跡し、
// 前のフレームまでの結果に足し合わせていく (フレーム間の蓄積)。
// 薄レンズによる被写界深度と、動く球のモーションブラーも加えている。
//
// Shadertoy で実行する場合は、「// ==== Buffer A ====」から「// ==== Image ====」
// の前までを Buffer A のタブに、それ以降を Image のタブに貼り付け、
// 両方のタブの iChannel0 に Buffer A を設定する。

// ==== Buffer A ====
// iChannel0: Buffer A (自分自身の前のフレームの結果)
// 出力: rgb に放射輝度の合計、a に経路の数の合計

const int   MAX_STEPS = 128;
const float MAX_DIST  = 20.0;
const float SURF_DIST = 0.0005;
const int   SAMPLES   = 4;      // 1 フレーム、1 ピクセルあたりの経路の数
const int   MAX_DEPTH = 4;
const float PI        = 3.14159265;

const float FOCAL          = 2.0;    // 焦点距離 (画面の高さを 2 とする)
const float FOCUS_DISTANCE = 3.7;    // ピントが合う距離 (奥の箱のあたり)
const float APERTURE       = 0.08;   // レンズの半径 (大きいほどぼける)

// ---- 乱数 ----------------------------------------------------------------

uint seed;

// PCG ハッシュ (Jarzynski and Olano, 2020)
uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// 0 以上 1 未満の一様乱数
float random()
{
    seed = pcgHash(seed);
    return float(seed) / 4294967296.0;
}

// 法線 n のまわりの半球から、cos に比例する確率密度で方向を選ぶ
vec3 cosineSampleHemisphere(vec3 n)
{
    float u1 = random();
    float u2 = random();
    float r = sqrt(u1);
    float phi = 2.0 * PI * u2;
    // n に直交する 2 つの単位ベクトル
    vec3 a = abs(n.x) > 0.5 ? vec3(0.0, 1.0, 0.0) : vec3(1.0, 0.0, 0.0);
    vec3 tangent = normalize(cross(a, n));
    vec3 bitangent = cross(n, tangent);
    return normalize(r * cos(phi) * tangent + r * sin(phi) * bitangent +
                     sqrt(1.0 - u1) * n);
}

// ---- シーン --------------------------------------------------------------

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

mat2 rot(float a)
{
    float c = cos(a);
    float s = sin(a);
    return mat2(c, s, -s, c);
}

// 露光時間の中の時刻 (0〜1)。経路ごとに乱数で決める
float shutterTime = 0.0;

const float MAT_WHITE = 1.0;
const float MAT_RED   = 2.0;
const float MAT_GREEN = 3.0;
const float MAT_LIGHT = 4.0;

vec2 opU(vec2 a, vec2 b)
{
    return (a.x < b.x) ? a : b;
}

// 厚さ 0.1 の板で作った部屋 (内側は x: -1〜1, y: 0〜2, z: -1〜1)。
// 手前 (z = 1 側) は開いている
vec2 map(vec3 p)
{
    const vec3 wallX = vec3(0.05, 1.1, 1.1);   // 左右の壁の大きさ (半分)
    const vec3 wallY = vec3(1.1, 0.05, 1.1);   // 床と天井
    const vec3 wallZ = vec3(1.1, 1.1, 0.05);   // 奥の壁
    vec2 res = vec2(sdBox(p - vec3(0.0, -0.05, 0.0), wallY), MAT_WHITE);
    res = opU(res, vec2(sdBox(p - vec3(0.0, 2.05, 0.0), wallY), MAT_WHITE));
    res = opU(res, vec2(sdBox(p - vec3(0.0, 1.0, -1.05), wallZ), MAT_WHITE));
    res = opU(res, vec2(sdBox(p - vec3(-1.05, 1.0, 0.0), wallX), MAT_RED));
    res = opU(res, vec2(sdBox(p - vec3(1.05, 1.0, 0.0), wallX), MAT_GREEN));
    // 天井の照明
    res = opU(res, vec2(sdBox(p - vec3(0.0, 2.0, 0.0), vec3(0.4, 0.02, 0.4)),
                        MAT_LIGHT));
    // 回転した背の高い箱と球
    vec3 q = p - vec3(-0.35, 0.6, -0.3);
    q.xz = rot(0.4) * q.xz;
    res = opU(res, vec2(sdBox(q, vec3(0.3, 0.6, 0.3)), MAT_WHITE));
    // 球は露光時間の間に左へ動く (モーションブラー)
    vec3 center = vec3(0.45 - 0.25 * shutterTime, 0.35, 0.25);
    res = opU(res, vec2(sdSphere(p - center, 0.35), MAT_WHITE));
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

vec3 albedoOf(float mat)
{
    if (mat == MAT_RED) {
        return vec3(0.63, 0.07, 0.05);
    }
    if (mat == MAT_GREEN) {
        return vec3(0.12, 0.45, 0.09);
    }
    return vec3(0.73);
}

// ---- パストレーシング ----------------------------------------------------

// 天井の照明: y = LIGHT_Y の平面上の正方形 (下向きに発光する)
const float LIGHT_Y     = 1.98;
const float LIGHT_HALF  = 0.4;                          // 1 辺の半分
const float LIGHT_AREA  = 4.0 * LIGHT_HALF * LIGHT_HALF;
const vec3  LIGHT_EMIT  = vec3(15.0);                   // 放射輝度

// 点 p (法線 n、アルベド albedo) が照明から直接受ける光を、照明上の 1 点を
// 選んで推定する (Next Event Estimation)
vec3 sampleDirectLight(vec3 p, vec3 n, vec3 albedo)
{
    vec3 lp = vec3((2.0 * random() - 1.0) * LIGHT_HALF, LIGHT_Y,
                   (2.0 * random() - 1.0) * LIGHT_HALF);
    vec3 toLight = lp - p;
    float dist2 = dot(toLight, toLight);
    vec3 l = toLight / sqrt(dist2);
    float cosSurface = dot(n, l);
    float cosLight = l.y;            // 照明の法線 (0, -1, 0) と -l の内積
    if (cosSurface <= 0.0 || cosLight <= 0.0) {
        return vec3(0.0);
    }
    // 照明に向かうレイが最初に照明に当たれば、途中に遮るものは無い
    vec2 hit = raymarch(p, l);
    if (hit.y != MAT_LIGHT) {
        return vec3(0.0);
    }
    // 面積測度での推定: BRDF * Le * cos * cos' / r^2 / pdf (pdf = 1 / 面積)
    vec3 brdf = albedo / PI;
    return brdf * LIGHT_EMIT * cosSurface * cosLight / dist2 * LIGHT_AREA;
}

// 1 本の経路をたどり、視点に届く放射輝度の推定値を返す
vec3 tracePath(vec3 ro, vec3 rd)
{
    vec3 radiance = vec3(0.0);
    vec3 throughput = vec3(1.0);
    for (int depth = 0; depth < MAX_DEPTH; depth++) {
        vec2 hit = raymarch(ro, rd);
        if (hit.y < 0.0) {
            break;                           // 部屋の外に出た
        }
        if (hit.y == MAT_LIGHT) {
            // 直接光は sampleDirectLight で数えているので、
            // 視点から照明が直接見える場合だけ加える
            if (depth == 0) {
                radiance += LIGHT_EMIT;
            }
            break;
        }
        vec3 p = ro + hit.x * rd;
        vec3 n = calcNormal(p);
        vec3 albedo = albedoOf(hit.y);
        vec3 origin = p + n * 0.002;

        // 直接光
        radiance += throughput * sampleDirectLight(origin, n, albedo);

        // 間接光: 次の方向を選ぶ。cos 比例の重点サンプリングでは
        // BRDF * cos / pdf = (albedo / PI) * cos / (cos / PI) = albedo になる
        throughput *= albedo;
        ro = origin;
        rd = cosineSampleHemisphere(n);
    }
    return radiance;
}

// 半径 1 の円板の中から一様に点を選ぶ
vec2 sampleDisk()
{
    float r = sqrt(random());
    float phi = 2.0 * PI * random();
    return r * vec2(cos(phi), sin(phi));
}

// 薄レンズのカメラ: レンズ上の点から、ピント面上の点に向かうレイを作る
void cameraRay(vec2 p, out vec3 ro, out vec3 rd)
{
    vec3 eye = vec3(0.0, 1.0, 3.4);
    vec3 dir = normalize(vec3(p, -FOCAL));
    // レイがピント面 (カメラから FOCUS_DISTANCE の平面) と交わる点
    vec3 focusPoint = eye + dir * (FOCUS_DISTANCE / -dir.z);
    vec2 lens = APERTURE * sampleDisk();
    ro = eye + vec3(lens, 0.0);
    rd = normalize(focusPoint - ro);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    seed = pcgHash(uint(fragCoord.x) + uint(fragCoord.y) * 4096u +
                   uint(iFrame) * 16777216u);

    vec3 sum = vec3(0.0);
    for (int i = 0; i < SAMPLES; i++) {
        vec2 jitter = vec2(random(), random()) - 0.5;
        vec2 p = (2.0 * (fragCoord + jitter) - iResolution.xy) / iResolution.y;
        shutterTime = random();          // 露光時間の中の時刻を選ぶ
        vec3 ro;
        vec3 rd;
        cameraRay(p, ro, rd);
        sum += tracePath(ro, rd);
    }

    // 前のフレームまでの合計に加える。最初のフレームでは 0 から始める
    vec4 previous = (iFrame == 0) ? vec4(0.0)
                                  : texelFetch(iChannel0, ivec2(fragCoord), 0);
    fragColor = previous + vec4(sum, float(SAMPLES));
}

// ==== Image ====
// iChannel0: Buffer A
// 蓄積した合計を経路の数で割って平均し、表示用の値に変換する

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec4 data = texelFetch(iChannel0, ivec2(fragCoord), 0);
    vec3 col = data.rgb / max(data.a, 1.0);
    col = col / (1.0 + col);           // Reinhard のトーンマッピング
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
