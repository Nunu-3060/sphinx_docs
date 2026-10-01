// 16_atmosphere.frag
// 第 16 章: 大気の散乱。レイリー散乱とミー散乱の単一散乱を積分して、空の色を求める。
// 太陽の高度を時間とともに変え、昼の青空から夕焼けまでを表示する。
// 長さの単位はメートル。

const float PI = 3.14159265;

const float EARTH_RADIUS = 6360e3;        // 地球の半径
const float ATMOSPHERE_RADIUS = 6420e3;   // 大気の上端の半径

// レイリー散乱 (空気の分子による散乱)。波長の短い青ほど強く散乱する
const vec3  BETA_RAYLEIGH = vec3(5.8e-6, 13.5e-6, 33.1e-6);   // 海面での散乱係数 [1/m]
const float HEIGHT_RAYLEIGH = 8.0e3;                          // スケールハイト [m]

// ミー散乱 (エアロゾルによる散乱)。波長によらず、前方に強く散乱する
const float BETA_MIE = 21e-6;
const float HEIGHT_MIE = 1.2e3;
const float MIE_G = 0.76;                 // 前方散乱の強さ (位相関数の g)

const float SUN_INTENSITY = 20.0;
const int   VIEW_SAMPLES = 16;            // 視線方向の分割数
const int   LIGHT_SAMPLES = 8;            // 太陽の方向の分割数

// 原点を中心とする半径 r の球と、レイ ro + t * rd の交点の t (近い方, 遠い方)。
// 交わらなければ (-1, -1)
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

// 高さ h での、レイリー散乱とミー散乱の粒子の密度 (海面を 1 とする)
vec2 densityAt(vec3 p)
{
    float h = length(p) - EARTH_RADIUS;
    return exp(-h / vec2(HEIGHT_RAYLEIGH, HEIGHT_MIE));
}

// 点 p から太陽の方向に大気の上端まで進んだときの光学的深さ (密度 × 距離の積分)
vec2 opticalDepthToSun(vec3 p, vec3 sunDir)
{
    float tEnd = raySphere(p, sunDir, ATMOSPHERE_RADIUS).y;
    float ds = tEnd / float(LIGHT_SAMPLES);
    vec2 depth = vec2(0.0);
    for (int i = 0; i < LIGHT_SAMPLES; i++) {
        depth += densityAt(p + (float(i) + 0.5) * ds * sunDir) * ds;
    }
    return depth;
}

// 視点 ro から方向 rd を見たときに届く、散乱された太陽光
vec3 skyRadiance(vec3 ro, vec3 rd, vec3 sunDir)
{
    // 大気の中を進む区間を求める。地面に当たる場合は地面まで
    float tEnd = raySphere(ro, rd, ATMOSPHERE_RADIUS).y;
    vec2 ground = raySphere(ro, rd, EARTH_RADIUS);
    if (ground.x > 0.0) {
        tEnd = ground.x;
    }
    float ds = tEnd / float(VIEW_SAMPLES);

    vec3 sumRayleigh = vec3(0.0);
    vec3 sumMie = vec3(0.0);
    vec2 depthView = vec2(0.0);   // 視点からサンプル点までの光学的深さ
    for (int i = 0; i < VIEW_SAMPLES; i++) {
        vec3 p = ro + (float(i) + 0.5) * ds * rd;
        vec2 density = densityAt(p) * ds;
        depthView += density;
        // 太陽の光が地球に遮られる点は、散乱に寄与しない
        if (raySphere(p, sunDir, EARTH_RADIUS).x > 0.0) {
            continue;
        }
        vec2 depthSun = opticalDepthToSun(p, sunDir);
        // 太陽 → サンプル点 → 視点 の経路の透過率 (ランベルト・ベールの法則)
        vec2 depth = depthView + depthSun;
        vec3 tau = BETA_RAYLEIGH * depth.x + 1.1 * BETA_MIE * depth.y;
        vec3 transmittance = exp(-tau);
        sumRayleigh += transmittance * density.x;
        sumMie += transmittance * density.y;
    }

    // 位相関数: レイリー散乱は前後に対称、ミー散乱は前方に強い
    float mu = dot(rd, sunDir);
    float phaseRayleigh = 3.0 / (16.0 * PI) * (1.0 + mu * mu);
    float g2 = MIE_G * MIE_G;
    float phaseMie = 3.0 / (8.0 * PI) * ((1.0 - g2) * (1.0 + mu * mu)) /
                     ((2.0 + g2) * pow(1.0 + g2 - 2.0 * MIE_G * mu, 1.5));

    return SUN_INTENSITY * (sumRayleigh * BETA_RAYLEIGH * phaseRayleigh +
                            sumMie * BETA_MIE * phaseMie);
}

vec3 toneMapACES(vec3 x)
{
    x *= 0.6;
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    // 太陽の高度 [rad] を時間とともに変える。-0.05 (日没後)〜1.0 の範囲
    float elevation = 0.47 + 0.52 * cos(0.15 * iTime + 1.4);
    vec3 sunDir = normalize(vec3(0.0, sin(elevation), -cos(elevation)));

    // 地上 2 m から、太陽の方向 (-z) の地平線を少し見上げる
    vec3 ro = vec3(0.0, EARTH_RADIUS + 2.0, 0.0);
    vec3 forward = normalize(vec3(0.0, 0.25, -1.0));
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    vec3 rd = normalize(p.x * right + p.y * up + 1.2 * forward);

    vec3 col = skyRadiance(ro, rd, sunDir);
    // 太陽の円盤
    float sun = smoothstep(0.9995, 0.9998, dot(rd, sunDir));
    col += sun * 20.0 * exp(-BETA_RAYLEIGH * 8e4 / max(sunDir.y + 0.05, 0.05));

    col = pow(toneMapACES(col), vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
