// 18_landscape.frag
// 第 18 章: 実践: 夕暮れの風景を描く。夕日に照らされた山々と湖、空に浮かぶ雲。
// 発展編の技法 (ノイズ、反射と屈折、物理ベースの材質、大気の散乱、
// ボリュームレンダリング、複数パスの描画) を組み合わせる。
//
// パスの構成
//   Common  : 全パスで共有するコード (ノイズ、大気、雲、地形)
//   Buffer A: 雲を画面の 1/4 の解像度で描く。iChannel0 は使わない
//   Image   : 地形・湖面・空を描き、Buffer A の雲を合成する。iChannel0 は Buffer A
// Shadertoy では、各区切りの中身を Common・Buffer A・Image のタブに貼り付け、
// Image のタブの iChannel0 に Buffer A を設定する。

// ==== Common ====

// ---- 品質の設定 (重い場合は値を小さくする) -------------------------------

const int TERRAIN_STEPS    = 250;   // 地形のレイマーチングの最大反復回数
const int TERRAIN_OCTAVES  = 6;     // レイマーチングに使う地形のオクターブ数
const int NORMAL_OCTAVES   = 10;    // 法線に使う地形のオクターブ数
const int SHADOW_STEPS     = 40;    // 地形の影の反復回数
const int REFLECT_STEPS    = 100;   // 湖面の映り込みの反復回数
const int CLOUD_STEPS      = 32;    // 雲の視線方向の分割数
const int CLOUD_LIGHT_STEPS = 3;    // 雲の太陽方向の分割数
const int SKY_SAMPLES      = 12;    // 大気の散乱の視線方向の分割数
const int SKY_LIGHT_SAMPLES = 4;    // 大気の散乱の太陽方向の分割数

// ---- 単位と定数 ----------------------------------------------------------

// シーンの長さの単位は 100 m。大気の計算だけはメートルで行う
const float METERS_PER_UNIT = 100.0;
const float PI = 3.14159265;

// ---- ハッシュとノイズ (第 10 章) -----------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float hash21(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    return float(pcgHash(q.x + pcgHash(q.y))) / 4294967296.0;
}

float hash31(vec3 p)
{
    uvec3 q = uvec3(ivec3(p));
    return float(pcgHash(q.x + pcgHash(q.y + pcgHash(q.z)))) / 4294967296.0;
}

vec2 gradientAt(vec2 i)
{
    float angle = 2.0 * PI * hash21(i);
    return vec2(cos(angle), sin(angle));
}

float gradientNoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * f * (f * (f * 6.0 - 15.0) + 10.0);
    float a = dot(gradientAt(i), f);
    float b = dot(gradientAt(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0));
    float c = dot(gradientAt(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0));
    float d = dot(gradientAt(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0));
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

float valueNoise3(vec3 x)
{
    vec3 i = floor(x);
    vec3 f = fract(x);
    vec3 u = f * f * (3.0 - 2.0 * f);
    vec2 e = vec2(1.0, 0.0);
    return mix(mix(mix(hash31(i + e.yyy), hash31(i + e.xyy), u.x),
                   mix(hash31(i + e.yxy), hash31(i + e.xxy), u.x), u.y),
               mix(mix(hash31(i + e.yyx), hash31(i + e.xyx), u.x),
                   mix(hash31(i + e.yxx), hash31(i + e.xxx), u.x), u.y),
               u.z);
}

const mat2 OCTAVE_ROT = mat2(0.8, 0.6, -0.6, 0.8);

// ---- 太陽と大気 (第 16 章) -----------------------------------------------

const float EARTH_RADIUS = 6360e3;
const float ATMOSPHERE_RADIUS = 6420e3;
const vec3  BETA_RAYLEIGH = vec3(5.8e-6, 13.5e-6, 33.1e-6);
const float HEIGHT_RAYLEIGH = 8.0e3;
const float BETA_MIE = 21e-6;
const float HEIGHT_MIE = 1.2e3;
const float MIE_G = 0.76;
const float SUN_INTENSITY = 20.0;

// 太陽の方向。夕方の低い高度で、時間とともにわずかに沈んでいく
vec3 sunDirection(float time)
{
    float elevation = 0.09 - 0.0015 * time;
    return normalize(vec3(0.55, sin(elevation), -0.83));
}

vec2 raySphere(vec3 ro, vec3 rd, float r)
{
    float b = dot(ro, rd);
    float c = dot(ro, ro) - r * r;
    float disc = b * b - c;
    if (disc < 0.0) {
        return vec2(-1.0);
    }
    float s = sqrt(disc);
    return vec2(-b - s, -b + s);
}

vec2 densityAt(vec3 p)
{
    float h = length(p) - EARTH_RADIUS;
    return exp(-h / vec2(HEIGHT_RAYLEIGH, HEIGHT_MIE));
}

// 点 p から大気の上端まで、太陽の方向の光学的深さ
vec2 opticalDepthToSun(vec3 p, vec3 sunDir)
{
    float tEnd = raySphere(p, sunDir, ATMOSPHERE_RADIUS).y;
    float ds = tEnd / float(SKY_LIGHT_SAMPLES);
    vec2 depth = vec2(0.0);
    for (int i = 0; i < SKY_LIGHT_SAMPLES; i++) {
        depth += densityAt(p + (float(i) + 0.5) * ds * sunDir) * ds;
    }
    return depth;
}

// 地上の高さ heightMeters に届く太陽の光 (大気を通過して減衰した色)。
// この色を、地形・湖面・雲の照明に共通して使う
vec3 sunlightAt(float heightMeters, vec3 sunDir)
{
    vec3 p = vec3(0.0, EARTH_RADIUS + heightMeters, 0.0);
    vec2 depth = opticalDepthToSun(p, sunDir);
    vec3 tau = BETA_RAYLEIGH * depth.x + 1.1 * BETA_MIE * depth.y;
    return SUN_INTENSITY * exp(-tau);
}

// 高さ heightMeters から方向 rd を見たときの空の色 (単一散乱)
vec3 skyRadiance(float heightMeters, vec3 rd, vec3 sunDir)
{
    vec3 ro = vec3(0.0, EARTH_RADIUS + heightMeters, 0.0);
    float tEnd = raySphere(ro, rd, ATMOSPHERE_RADIUS).y;
    vec2 ground = raySphere(ro, rd, EARTH_RADIUS);
    if (ground.x > 0.0) {
        tEnd = ground.x;
    }
    float ds = tEnd / float(SKY_SAMPLES);
    vec3 sumRayleigh = vec3(0.0);
    vec3 sumMie = vec3(0.0);
    vec2 depthView = vec2(0.0);
    for (int i = 0; i < SKY_SAMPLES; i++) {
        vec3 p = ro + (float(i) + 0.5) * ds * rd;
        vec2 density = densityAt(p) * ds;
        depthView += density;
        if (raySphere(p, sunDir, EARTH_RADIUS).x > 0.0) {
            continue;
        }
        vec2 depth = depthView + opticalDepthToSun(p, sunDir);
        vec3 transmittance = exp(-(BETA_RAYLEIGH * depth.x +
                                   1.1 * BETA_MIE * depth.y));
        sumRayleigh += transmittance * density.x;
        sumMie += transmittance * density.y;
    }
    float mu = dot(rd, sunDir);
    float phaseRayleigh = 3.0 / (16.0 * PI) * (1.0 + mu * mu);
    float g2 = MIE_G * MIE_G;
    float phaseMie = 3.0 / (8.0 * PI) * ((1.0 - g2) * (1.0 + mu * mu)) /
                     ((2.0 + g2) * pow(1.0 + g2 - 2.0 * MIE_G * mu, 1.5));
    return SUN_INTENSITY * (sumRayleigh * BETA_RAYLEIGH * phaseRayleigh +
                            sumMie * BETA_MIE * phaseMie);
}

// 空気遠近法: 距離 t (シーンの単位) の物体の色を、大気の散乱でかすませる。
// 海面付近の消散係数で透過率を求め、失われた分を空の色で置き換える近似
vec3 aerialPerspective(vec3 col, float t, vec3 skyCol)
{
    float meters = t * METERS_PER_UNIT;
    vec3 transmittance = exp(-(BETA_RAYLEIGH + 1.1 * BETA_MIE) * meters);
    return col * transmittance + skyCol * (1.0 - transmittance);
}

// ---- 雲 (第 10 章、第 16 章) ---------------------------------------------

const float CLOUD_BOTTOM = 22.0;   // 雲の層の下端 (2.2 km)
const float CLOUD_TOP    = 32.0;   // 雲の層の上端 (3.2 km)
const float CLOUD_COVERAGE = 0.45; // 空のうち雲が覆う割合の目安
const float CLOUD_SIGMA = 0.6;     // 雲の消散係数 (密度 1、1 単位あたり)

// カールノイズ (第 10 章) で雲の流れを作る
vec2 curlField(vec2 p)
{
    const float e = 0.05;
    float dx = gradientNoise(p + vec2(e, 0.0)) - gradientNoise(p - vec2(e, 0.0));
    float dy = gradientNoise(p + vec2(0.0, e)) - gradientNoise(p - vec2(0.0, e));
    return vec2(dy, -dx) / (2.0 * e);
}

// 点 p での雲の密度 (0〜1)
float cloudDensity(vec3 p, float time)
{
    // 雲の層の中での高さに応じて、下端と上端で密度を 0 に近づける
    float h = (p.y - CLOUD_BOTTOM) / (CLOUD_TOP - CLOUD_BOTTOM);
    float profile = smoothstep(0.0, 0.2, h) * smoothstep(1.0, 0.6, h);
    if (profile <= 0.0) {
        return 0.0;
    }
    // 風で流しつつ、カールノイズの流れで形を変化させる
    vec3 q = p;
    q.xz += time * (vec2(1.5, 0.4) + 2.0 * curlField(0.01 * p.xz));
    q *= 0.03;
    float n = 0.5 * valueNoise3(q) + 0.25 * valueNoise3(2.03 * q) +
              0.125 * valueNoise3(4.01 * q) + 0.0625 * valueNoise3(8.02 * q);
    return clamp((n - (1.0 - CLOUD_COVERAGE)) * 3.0, 0.0, 1.0) * profile;
}

// レイ ro + t rd が雲の層を通過する区間 (入る t, 出る t)。通過しなければ (-1, -1)
vec2 cloudSlab(vec3 ro, vec3 rd)
{
    if (rd.y <= 0.01) {
        return vec2(-1.0);
    }
    float t0 = (CLOUD_BOTTOM - ro.y) / rd.y;
    float t1 = (CLOUD_TOP - ro.y) / rd.y;
    return vec2(max(t0, 0.0), min(t1, 600.0));
}

// 雲を描く。戻り値の rgb は雲から届く光、a は雲の透過率
vec4 renderClouds(vec3 ro, vec3 rd, vec3 sunDir, vec3 sunColor,
                  vec3 ambient, float jitter, float time)
{
    vec2 slab = cloudSlab(ro, rd);
    if (slab.x < 0.0 || slab.x >= slab.y) {
        return vec4(0.0, 0.0, 0.0, 1.0);
    }
    float dt = (slab.y - slab.x) / float(CLOUD_STEPS);
    float t = slab.x + jitter * dt;
    float mu = dot(rd, sunDir);
    // 前方散乱と後方散乱を混ぜた位相関数 (Henyey-Greenstein の和)
    float g = 0.6;
    float hgForward = (1.0 - g * g) /
                      (4.0 * PI * pow(1.0 + g * g - 2.0 * g * mu, 1.5));
    float hgBack = (1.0 - 0.09) / (4.0 * PI * pow(1.09 + 0.6 * mu, 1.5));
    float phase = mix(hgBack, hgForward, 0.7) * 4.0 * PI;

    vec3 col = vec3(0.0);
    float transmittance = 1.0;
    for (int i = 0; i < CLOUD_STEPS; i++) {
        vec3 p = ro + t * rd;
        float dens = cloudDensity(p, time);
        if (dens > 0.0) {
            // 太陽の方向の透過率
            float lightDepth = 0.0;
            for (int j = 1; j <= CLOUD_LIGHT_STEPS; j++) {
                lightDepth += cloudDensity(p + sunDir * 1.5 * float(j), time);
            }
            float lightT = exp(-CLOUD_SIGMA * lightDepth * 1.5);
            float absorbed = 1.0 - exp(-CLOUD_SIGMA * dens * dt);
            vec3 light = sunColor * lightT * phase * 0.05 + ambient;
            col += transmittance * absorbed * light;
            transmittance *= 1.0 - absorbed;
            if (transmittance < 0.02) {
                break;
            }
        }
        t += dt;
    }
    // 遠くの雲ほど空の色に溶け込ませる (空気遠近法)
    float fade = exp(-0.004 * slab.x);
    return vec4(col * fade, mix(1.0, transmittance, fade));
}

// ---- 地形 (第 10 章) -----------------------------------------------------

// 湖の中心 (xz)。湖の周囲を低く、遠くを高い山にする
const vec2 LAKE_CENTER = vec2(0.0, 12.0);

float terrainHeight(vec2 xz, int octaves)
{
    // リッジノイズで尾根のある山を作る
    vec2 p = 0.025 * xz;
    float ridges = 0.0;
    float amplitude = 0.5;
    for (int i = 0; i < octaves; i++) {
        float n = 1.0 - abs(1.4 * gradientNoise(p));
        ridges += amplitude * n * n;
        p = 2.0 * OCTAVE_ROT * p;
        amplitude *= 0.5;
    }
    // 湖からの距離に応じて、湖底から山の高さへ滑らかにつなぐ
    float distanceFromLake = length((xz - LAKE_CENTER) * vec2(0.7, 1.0));
    float mask = smoothstep(12.0, 38.0, distanceFromLake);
    float mountains = 14.0 * ridges - 2.0;
    float shore = 0.6 * ridges - 0.35;   // 湖の近くの低い起伏
    return mix(shore, mountains, mask);
}

// 遠いほど少ないオクターブで計算する (1 ピクセルより細かい起伏は見えない)
int octavesAt(float t, int maxOctaves)
{
    return clamp(maxOctaves - int(log2(1.0 + t / 20.0)), 3, maxOctaves);
}

float terrainSDF(vec3 p, int octaves)
{
    return p.y - terrainHeight(p.xz, octaves);
}

// ---- カメラ --------------------------------------------------------------

// 画面上の点 p (縦方向が -1〜1) を通るレイを作る。カメラは湖の上をゆっくり進む
void cameraRay(vec2 p, float time, out vec3 ro, out vec3 rd)
{
    ro = vec3(0.0, 0.8, 22.0 - 0.15 * time);
    vec3 forward = normalize(vec3(0.15, 0.07, -1.0));
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    rd = normalize(p.x * right + p.y * up + 1.6 * forward);
}

// ==== Buffer A ====
// 雲を 1/4 の解像度 (縦横それぞれ半分) で描く。
// 画面の左下の 1/4 の範囲だけを計算し、残りのピクセルは何もしない

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 halfRes = floor(0.5 * iResolution.xy);
    if (fragCoord.x >= halfRes.x || fragCoord.y >= halfRes.y) {
        fragColor = vec4(0.0, 0.0, 0.0, 1.0);
        return;
    }
    // 1/4 の画面の座標を、全画面の座標に対応させる
    vec2 p = (2.0 * fragCoord - halfRes) / halfRes.y;

    vec3 ro;
    vec3 rd;
    cameraRay(p, iTime, ro, rd);

    vec3 sunDir = sunDirection(iTime);
    vec3 sunColor = sunlightAt(CLOUD_BOTTOM * METERS_PER_UNIT, sunDir);
    vec3 ambient = 0.6 * skyRadiance(CLOUD_BOTTOM * METERS_PER_UNIT,
                                     vec3(0.0, 1.0, 0.0), sunDir);
    float jitter = hash31(vec3(fragCoord, float(iFrame)));
    fragColor = renderClouds(ro, rd, sunDir, sunColor, ambient, jitter, iTime);
}

// ==== Image ====
// 地形・湖面・空を描き、Buffer A の雲を合成する。iChannel0 は Buffer A

// DEBUG_MODE を変えると、デバッグ用の表示になる (第 9 章)。
//   0: 通常の描画  1: 地形の反復回数  2: 要素の色分け  3: 雲だけ
//  -1: 画面を 4 分割して 0〜3 を同時に表示する
#define DEBUG_MODE 0

const float SURF_DIST  = 0.0015;   // 距離に比例させる閾値の係数 (第 9 章)
const float STEP_SCALE = 0.5;      // 高さの関数なので歩幅を小さくする (第 10 章)
const float MAX_DIST   = 300.0;

const float MAT_ROCK  = 1.0;
const float MAT_GRASS = 2.0;
const float MAT_SNOW  = 3.0;
const float MAT_SAND  = 4.0;

// ---- 地形のレイマーチング ------------------------------------------------

// 戻り値は (t, 反復回数)。何にも当たらずに tMax を超えたら t は -1
vec2 marchTerrain(vec3 ro, vec3 rd, float tMax, int maxSteps)
{
    float t = 0.1;
    for (int i = 0; i < maxSteps; i++) {
        vec3 p = ro + t * rd;
        float d = terrainSDF(p, octavesAt(t, TERRAIN_OCTAVES));
        if (d < SURF_DIST * t) {
            return vec2(t, float(i));
        }
        t += d * STEP_SCALE;
        if (t > tMax) {
            return vec2(-1.0, float(i));
        }
    }
    // 反復回数の上限に達したレイは、地形すれすれを進んでいたとみなし、
    // 当たったものとして扱う (空として扱うと、山の映り込みに穴が空く)
    return vec2(t, float(maxSteps));
}

vec3 terrainNormal(vec3 p, float t)
{
    int octaves = octavesAt(t, NORMAL_OCTAVES);
    float e = 0.002 * t + 0.002;
    float hx = terrainHeight(p.xz + vec2(e, 0.0), octaves) -
               terrainHeight(p.xz - vec2(e, 0.0), octaves);
    float hz = terrainHeight(p.xz + vec2(0.0, e), octaves) -
               terrainHeight(p.xz - vec2(0.0, e), octaves);
    return normalize(vec3(-hx, 2.0 * e, -hz));
}

float terrainShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.05;
    for (int i = 0; i < SHADOW_STEPS && t < 80.0; i++) {
        float h = terrainSDF(ro + t * rd, 4);
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h * STEP_SCALE, 0.05, 4.0);
    }
    return clamp(res, 0.0, 1.0);
}

// ---- 材質 (第 12 章) -----------------------------------------------------

struct Material {
    float id;
    vec3 baseColor;
    float roughness;
};

// 高さと傾きで材質を割り当てる
Material terrainMaterial(vec3 p, vec3 n)
{
    float slope = n.y;                       // 1 が水平
    float detail = gradientNoise(0.8 * p.xz);
    if (p.y < 0.08 + 0.05 * detail) {
        return Material(MAT_SAND, vec3(0.32, 0.28, 0.22), 0.9);
    }
    if (p.y > 6.0 + 1.5 * detail && slope > 0.6) {
        return Material(MAT_SNOW, vec3(0.85, 0.88, 0.92), 0.5);
    }
    if (slope > 0.8 && p.y < 4.0 + detail) {
        return Material(MAT_GRASS, vec3(0.1, 0.17, 0.05), 0.9);
    }
    return Material(MAT_ROCK, vec3(0.22, 0.19, 0.17), 0.8);
}

float distributionGGX(float nh, float alpha)
{
    float a2 = alpha * alpha;
    float d = nh * nh * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}

float geometrySmith(float nv, float nl, float roughness)
{
    float k = (roughness + 1.0) * (roughness + 1.0) / 8.0;
    return (nv / (nv * (1.0 - k) + k)) * (nl / (nl * (1.0 - k) + k));
}

// 非金属の PBR (第 12 章)。雪にはラップライティングで SSS を近似する
vec3 shadeTerrain(vec3 p, vec3 n, vec3 v, Material m, vec3 sunDir,
                  vec3 sunColor, vec3 ambient, float shadow)
{
    vec3 h = normalize(sunDir + v);
    float nl = max(dot(n, sunDir), 0.0);
    float nv = max(dot(n, v), 1e-3);
    float f = 0.04 + 0.96 * pow(1.0 - max(dot(h, v), 0.0), 5.0);
    float alpha = m.roughness * m.roughness;
    float specular = distributionGGX(max(dot(n, h), 0.0), alpha) *
                     geometrySmith(nv, nl, m.roughness) * f /
                     (4.0 * nv * nl + 1e-4);
    float diffuseTerm = nl;
    if (m.id == MAT_SNOW) {
        // 雪の中で散乱した光が、影の側にわずかに回り込む (第 12 章)
        diffuseTerm = max((dot(n, sunDir) + 0.3) / 1.3, 0.0);
    }
    vec3 direct = ((1.0 - f) * m.baseColor / PI * diffuseTerm +
                   specular * nl) * sunColor * shadow;
    vec3 indirect = m.baseColor * ambient * (0.6 + 0.4 * n.y);
    return direct + indirect;
}

// ---- 湖面 (第 10 章、第 11 章) -------------------------------------------

// 波の高さ。2 つの勾配ノイズを逆向きに流す
float waveHeight(vec2 xz, float time)
{
    return 0.004 * gradientNoise(3.0 * xz + vec2(0.0, 0.4 * time)) +
           0.002 * gradientNoise(9.0 * xz - vec2(0.3 * time, 0.0));
}

// 波の法線。湖面の形は平面のまま、法線だけを傾ける (バンプマッピング)
vec3 waterNormal(vec2 xz, float time)
{
    const float e = 0.01;
    float hx = waveHeight(xz + vec2(e, 0.0), time) -
               waveHeight(xz - vec2(e, 0.0), time);
    float hz = waveHeight(xz + vec2(0.0, e), time) -
               waveHeight(xz - vec2(0.0, e), time);
    return normalize(vec3(-hx, 2.0 * e, -hz));
}

// 水の中での光の減衰 (消散係数、1 単位 = 100 m あたり)。赤ほど早く吸収される
const vec3 WATER_SIGMA = vec3(25.0, 6.0, 3.0);

vec3 shadeWater(vec3 p, vec3 rd, float t, vec3 sunDir, vec3 sunColor,
                vec3 ambient)
{
    // 遠くの波は 1 ピクセルより細かくなりちらつくので、距離に応じて平らにする
    vec3 n = normalize(mix(waterNormal(p.xz, iTime), vec3(0.0, 1.0, 0.0),
                           smoothstep(5.0, 40.0, t)));
    vec3 v = -rd;
    // フレネル反射率 (水の屈折率 1.33 では F0 = 0.02)
    float fresnel = 0.02 + 0.98 * pow(1.0 - max(dot(n, v), 0.0), 5.0);

    // 反射: 映り込む山と空
    vec3 reflDir = reflect(rd, n);
    reflDir.y = abs(reflDir.y);
    vec3 reflection;
    vec2 hit = marchTerrain(p + vec3(0.0, 0.01, 0.0), reflDir, MAX_DIST,
                            REFLECT_STEPS);
    if (hit.x > 0.0) {
        vec3 q = p + hit.x * reflDir;
        vec3 qn = terrainNormal(q, t + hit.x);
        reflection = shadeTerrain(q, qn, -reflDir, terrainMaterial(q, qn),
                                  sunDir, sunColor, ambient, 1.0);
        reflection = aerialPerspective(reflection, t + hit.x,
                                       skyRadiance(10.0, reflDir, sunDir));
    } else {
        reflection = skyRadiance(10.0, reflDir, sunDir);
    }
    // 太陽の映り込み (きらめき)
    reflection += sunColor * 15.0 * pow(max(dot(reflDir, sunDir), 0.0), 1200.0);

    // 屈折: 湖底の色を、水の中を通る距離で減衰させる (第 11 章、第 16 章)
    vec3 refrDir = refract(rd, n, 1.0 / 1.33);
    float depth = max(-terrainHeight(p.xz, 5), 0.0);
    float pathLength = depth / max(-refrDir.y, 0.05);
    vec3 transmittance = exp(-WATER_SIGMA * pathLength);
    vec3 bottom = vec3(0.3, 0.27, 0.2) * (sunColor * max(sunDir.y, 0.0) / PI +
                                          ambient);
    vec3 deepWater = vec3(0.01, 0.03, 0.035) * ambient;
    vec3 refraction = bottom * transmittance + deepWater * (1.0 - transmittance);

    return mix(refraction, reflection, fresnel);
}

// ---- 雲の合成 ------------------------------------------------------------

// Buffer A の 1/4 の解像度の雲を、双線形補間で拡大して読み出す
vec4 sampleClouds(vec2 fragCoord)
{
    vec2 halfRes = floor(0.5 * iResolution.xy);
    vec2 uv = 0.5 * fragCoord - 0.5;
    vec2 base = floor(uv);
    vec2 f = uv - base;
    ivec2 maxTexel = ivec2(halfRes) - 1;
    ivec2 i00 = clamp(ivec2(base), ivec2(0), maxTexel);
    ivec2 i11 = clamp(ivec2(base) + 1, ivec2(0), maxTexel);
    vec4 c00 = texelFetch(iChannel0, i00, 0);
    vec4 c10 = texelFetch(iChannel0, ivec2(i11.x, i00.y), 0);
    vec4 c01 = texelFetch(iChannel0, ivec2(i00.x, i11.y), 0);
    vec4 c11 = texelFetch(iChannel0, i11, 0);
    return mix(mix(c00, c10, f.x), mix(c01, c11, f.x), f.y);
}

// ---- 仕上げ (第 7 章) ----------------------------------------------------

vec3 toneMapACES(vec3 x)
{
    x *= 0.6;
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
}

vec3 colorGrade(vec3 col, vec2 uv)
{
    float luma = dot(col, vec3(0.2126, 0.7152, 0.0722));
    col = mix(vec3(luma), col, 1.15);
    col *= 0.6 + 0.4 * pow(16.0 * uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y),
                           0.15);
    return clamp(col, 0.0, 1.0);
}

vec3 heatmap(float x)
{
    return clamp(vec3(2.0 * x - 0.5, 1.0 - abs(2.0 * x - 1.0), 1.5 - 2.0 * x),
                 0.0, 1.0);
}

// ---- メイン --------------------------------------------------------------

// 1 ピクセルの色を求める。mode は DEBUG_MODE の値 (0〜3)。
// screenCoord は全画面での座標で、雲の読み出しに使う
vec3 renderPixel(vec2 p, vec2 screenCoord, int mode)
{
    vec3 ro;
    vec3 rd;
    cameraRay(p, iTime, ro, rd);

    // 太陽と空の光は 1 ピクセルにつき 1 回だけ求め、すべての照明に使う
    vec3 sunDir = sunDirection(iTime);
    vec3 sunColor = sunlightAt(ro.y * METERS_PER_UNIT, sunDir);
    vec3 ambient = 0.6 * skyRadiance(ro.y * METERS_PER_UNIT,
                                     vec3(0.0, 1.0, 0.0), sunDir);
    vec3 skyCol = skyRadiance(ro.y * METERS_PER_UNIT,
                              normalize(vec3(rd.x, max(rd.y, 0.0), rd.z)),
                              sunDir);
    vec4 clouds = sampleClouds(screenCoord);

    if (mode == 3) {
        return clouds.rgb + clouds.a * vec3(0.05, 0.07, 0.1);
    }

    // 湖面と地形のどちらに先に当たるか
    float tWater = (rd.y < 0.0) ? -ro.y / rd.y : -1.0;
    float tLimit = (tWater > 0.0) ? tWater : MAX_DIST;
    vec2 hit = marchTerrain(ro, rd, tLimit, TERRAIN_STEPS);

    if (mode == 1) {
        return heatmap(hit.y / float(TERRAIN_STEPS));
    }

    vec3 col;
    if (hit.x > 0.0) {
        // 地形
        vec3 pos = ro + hit.x * rd;
        vec3 n = terrainNormal(pos, hit.x);
        Material m = terrainMaterial(pos, n);
        if (mode == 2) {
            return (m.id == MAT_SNOW) ? vec3(1.0)
                 : (m.id == MAT_GRASS) ? vec3(0.2, 0.8, 0.2)
                 : (m.id == MAT_SAND) ? vec3(0.9, 0.8, 0.4) : vec3(0.5, 0.3, 0.2);
        }
        float shadow = terrainShadow(pos + n * 0.01, sunDir);
        col = shadeTerrain(pos, n, -rd, m, sunDir, sunColor, ambient, shadow);
        col = aerialPerspective(col, hit.x, skyCol);
    } else if (tWater > 0.0) {
        // 湖面
        if (mode == 2) {
            return vec3(0.1, 0.4, 0.9);
        }
        vec3 pos = ro + tWater * rd;
        col = shadeWater(pos, rd, tWater, sunDir, sunColor, ambient);
        col = aerialPerspective(col, tWater, skyCol);
    } else {
        // 空: 雲を手前に重ねる (雲の層は山より高いので、空が見える方向だけでよい)
        if (mode == 2) {
            return mix(vec3(0.5, 0.7, 1.0), vec3(1.0, 0.5, 0.8), 1.0 - clouds.a);
        }
        float sun = smoothstep(0.9996, 0.9999, dot(rd, sunDir));
        col = skyCol + sun * sunColor * 4.0;
        col = clouds.rgb + clouds.a * col;
    }
    return col;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;
    int mode = DEBUG_MODE;
    vec2 frag = fragCoord;
    if (mode < 0) {
        // 4 分割表示: 各領域に全画面と同じ構図を縮小して表示する
        vec2 cell = floor(uv * 2.0);
        int index = int(cell.x) + 2 * int(1.0 - cell.y);
        const int modes[4] = int[4](0, 1, 2, 3);
        mode = modes[index];
        frag = fract(uv * 2.0) * iResolution.xy;
    }
    vec2 p = (2.0 * frag - iResolution.xy) / iResolution.y;
    vec3 col = renderPixel(p, frag, mode);
    if (mode == 0) {
        col = colorGrade(pow(toneMapACES(col), vec3(1.0 / 2.2)),
                         frag / iResolution.xy);
    } else if (mode == 3) {
        col = pow(toneMapACES(col), vec3(1.0 / 2.2));
    }
    fragColor = vec4(col, 1.0);
}
