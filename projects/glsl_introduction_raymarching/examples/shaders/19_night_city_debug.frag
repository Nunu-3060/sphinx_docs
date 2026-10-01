// 19_night_city_debug.frag
// 第 19 章: 19_night_city.frag のデバッグ版。DEBUG_MODE を -1 にして、
// 通常の描画、走査したセルの数、霧の散乱光、材質の色分けを 4 分割で表示する。
// DEBUG_MODE の行以外は 19_night_city.frag と同じである。
//
// 第 19 章: 実践: ボクセルの都市の夜景。第 15 章の街並みを夜にして、
// 窓の明かり、霧の中でにじむ街灯の光、雨に濡れた路面の映り込みを加える。

// DEBUG_MODE を変えると、デバッグ用の表示になる (第 9 章)。
//   0: 通常の描画  1: 走査したセルの数  2: 霧の散乱光だけ  3: 材質の色分け
//  -1: 画面を 4 分割して 0〜3 を同時に表示する
#define DEBUG_MODE -1

// ---- 品質の設定 ----------------------------------------------------------

const int   MAX_CELLS    = 120;   // 1 本のレイが通過するセルの最大数
const int   CELL_STEPS   = 32;    // 1 セルの中でのスフィアトレーシングの最大反復回数
const int   REFLECT_CELLS = 48;   // 映り込みのレイが通過するセルの最大数

const float MAX_DIST   = 80.0;
const float SURF_DIST  = 0.001;
const float MAX_HEIGHT = 5.0;     // ビルの高さの上限
const float PI         = 3.14159265;

// ---- 光と霧 --------------------------------------------------------------

const vec3  LAMP_COLOR   = vec3(1.0, 0.55, 0.2) * 0.6;  // 街灯の光の強さ
const float LAMP_HEIGHT  = 0.45;                         // 街灯の高さ
const float FOG_SIGMA    = 0.06;                         // 霧の消散係数
const float FOG_SCATTER  = 0.05;                         // 霧の散乱係数
const vec3  FOG_AMBIENT  = vec3(0.025, 0.03, 0.045);     // 霧に散乱された街全体の光
const vec3  MOON_DIR     = normalize(vec3(-0.4, 0.6, -0.5));
const vec3  MOON_COLOR   = vec3(0.05, 0.06, 0.09);

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

float valueNoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash21(i), hash21(i + vec2(1.0, 0.0)), u.x),
               mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), u.x),
               u.y);
}

// ---- 街の構成 ------------------------------------------------------------

// 4 セルごとに大通りを通す。大通りのセルにはビルを置かない
bool isAvenue(vec2 cell)
{
    return mod(cell.x, 4.0) == 0.0 || mod(cell.y, 4.0) == 0.0;
}

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

vec3 buildingSize(vec2 cell)
{
    float h = MAX_HEIGHT * pow(hash21(cell), 1.5) + 0.3;
    float w = 0.3 + 0.12 * hash21(cell + 17.0);
    return vec3(w, 0.5 * h, w);
}

// セル cell の中の形状 (路面とビル) の SDF (第 15 章)
float cellSDF(vec3 p, vec2 cell)
{
    float d = p.y;
    if (!isAvenue(cell)) {
        vec3 size = buildingSize(cell);
        vec3 center = vec3(cell.x + 0.5, size.y, cell.y + 0.5);
        d = min(d, sdBox(p - center, size));
    }
    return d;
}

// ---- 霧の中の街灯の光 (第 16 章) -----------------------------------------

// 点光源 lamp から、レイ ro + t rd の区間 [ta, tb] に散乱されて届く光の量。
// 光源までの距離の 2 乗に反比例する光を、区間について解析的に積分する:
//   ∫ dt / (d^2 + (t - tc)^2) = (atan((tb - tc) / d) - atan((ta - tc) / d)) / d
float lampInScatter(vec3 ro, vec3 rd, vec3 lamp, float ta, float tb)
{
    float tc = dot(lamp - ro, rd);                 // 光源に最も近づく t
    float d = max(length(ro + tc * rd - lamp), 0.02);
    return (atan((tb - tc) / d) - atan((ta - tc) / d)) / d;
}

// セル cell の 4 つの角にある街灯の位置 (大通りに面した角にだけ街灯がある)
vec3 lampPosition(vec2 corner)
{
    return vec3(corner.x, LAMP_HEIGHT, corner.y);
}

bool hasLamp(vec2 corner)
{
    // 大通りの交差点と、大通り沿いの 2 セルごとの角に街灯を置く
    bool onAvenueX = mod(corner.x, 4.0) == 0.0;
    bool onAvenueZ = mod(corner.y, 4.0) == 0.0;
    return (onAvenueX && mod(corner.y, 2.0) == 0.0) ||
           (onAvenueZ && mod(corner.x, 2.0) == 0.0);
}

// レイがセル cell を通過する区間 [ta, tb] で、周囲の街灯から散乱される光
vec3 fogInScatter(vec3 ro, vec3 rd, vec2 cell, float ta, float tb)
{
    float sum = 0.0;
    for (int j = 0; j <= 1; j++) {
        for (int i = 0; i <= 1; i++) {
            vec2 corner = cell + vec2(float(i), float(j));
            if (hasLamp(corner)) {
                sum += lampInScatter(ro, rd, lampPosition(corner), ta, tb);
            }
        }
    }
    // 区間の中央までの霧の透過率で減衰させる
    float transmittance = exp(-FOG_SIGMA * 0.5 * (ta + tb));
    return LAMP_COLOR * FOG_SCATTER / (4.0 * PI) * sum * transmittance;
}

// ---- 2D DDA とセル内のスフィアトレーシング (第 15 章) --------------------

struct Hit {
    float t;          // 当たった距離。当たらなければ -1
    vec2 cell;        // 当たったセル
    vec3 inScatter;   // 経路上で霧から散乱されて届いた光
    float cells;      // 走査したセルの数 (デバッグ用)
};

Hit trace(vec3 ro, vec3 rd, int maxCells, bool withFog)
{
    vec2 dir = mix(rd.xz, vec2(1e-6), lessThan(abs(rd.xz), vec2(1e-6)));
    vec2 cell = floor(ro.xz);
    vec2 stepDir = sign(dir);
    vec2 tDelta = abs(1.0 / dir);
    vec2 tMax = (stepDir * (cell - ro.xz) + 0.5 * stepDir + 0.5) * tDelta;
    float tEnter = 0.0;
    vec3 inScatter = vec3(0.0);

    for (int i = 0; i < maxCells; i++) {
        float tExit = min(min(tMax.x, tMax.y), MAX_DIST);
        float t = tEnter;
        for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
            float d = cellSDF(ro + t * rd, cell);
            if (d < SURF_DIST) {
                if (withFog) {
                    inScatter += fogInScatter(ro, rd, cell, tEnter, t);
                }
                return Hit(t, cell, inScatter, float(i + 1));
            }
            t += d;
        }
        if (withFog) {
            inScatter += fogInScatter(ro, rd, cell, tEnter, tExit);
        }
        if ((rd.y > 0.0 && ro.y + tExit * rd.y > MAX_HEIGHT + 0.5) ||
            tExit >= MAX_DIST) {
            return Hit(-1.0, cell, inScatter, float(i + 1));
        }
        vec2 mask = step(tMax, tMax.yx);
        tMax += mask * tDelta;
        cell += mask * stepDir;
        tEnter = tExit;
    }
    return Hit(-1.0, cell, inScatter, float(maxCells));
}

vec3 calcNormal(vec3 p, vec2 cell)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * cellSDF(p + k.xyy * h, cell) +
                     k.yyx * cellSDF(p + k.yyx * h, cell) +
                     k.yxy * cellSDF(p + k.yxy * h, cell) +
                     k.xxx * cellSDF(p + k.xxx * h, cell));
}

// ---- 材質と照明 ----------------------------------------------------------

const float MAT_ROAD   = 1.0;
const float MAT_WALL   = 2.0;
const float MAT_WINDOW = 3.0;
const float MAT_ROOF   = 4.0;

// 窓の明かり: 窓ごとにハッシュで点灯・消灯と色を決める
vec3 windowLight(vec3 p, vec3 n, vec2 cell, out bool isWindow)
{
    // 壁の上の座標 (横方向、高さ)
    float u = (abs(n.x) > 0.5) ? p.z : p.x;
    vec2 uv = vec2(u * 8.0, p.y * 7.0);
    vec2 id = floor(uv);
    vec2 f = fract(uv);
    isWindow = f.x > 0.25 && f.x < 0.8 && f.y > 0.3 && f.y < 0.8 && p.y > 0.12;
    if (!isWindow) {
        return vec3(0.0);
    }
    float h = hash31(vec3(id, cell.x * 31.0 + cell.y + n.x * 7.0 + n.z * 13.0));
    if (h < 0.55) {
        return vec3(0.0);                                  // 消灯
    }
    vec3 warm = vec3(1.0, 0.7, 0.35);
    vec3 cool = vec3(0.6, 0.75, 1.0);
    return mix(warm, cool, step(0.85, h)) * (0.6 + 0.8 * fract(h * 13.7));
}

// 路面の水たまり: ノイズの値が大きい場所ほど濡れている (0〜1)
float wetness(vec2 xz)
{
    float n = 0.6 * valueNoise(1.5 * xz) + 0.4 * valueNoise(4.0 * xz);
    return smoothstep(0.62, 0.7, n);
}

// 表面の点 p が受ける街灯の光 (周囲 4 つの角の街灯。影は省略する)
vec3 lampLighting(vec3 p, vec3 n)
{
    vec3 sum = vec3(0.0);
    vec2 base = floor(p.xz + 0.5) - 1.0;
    for (int j = 0; j <= 2; j++) {
        for (int i = 0; i <= 2; i++) {
            vec2 corner = base + vec2(float(i), float(j));
            if (!hasLamp(corner)) {
                continue;
            }
            vec3 toLamp = lampPosition(corner) - p;
            float dist2 = dot(toLamp, toLamp);
            float nl = max(dot(n, toLamp * inversesqrt(dist2)), 0.0);
            sum += LAMP_COLOR * nl / (dist2 + 0.01);
        }
    }
    return sum;
}

vec3 skyColor(vec3 rd)
{
    // 夜空: 地平線の近くは街の明かりで赤みを帯びる (光害)
    vec3 col = mix(vec3(0.06, 0.04, 0.035), vec3(0.004, 0.006, 0.015),
                   sqrt(clamp(rd.y, 0.0, 1.0)));
    // 星
    vec2 starCell = floor(rd.xz / max(rd.y, 0.05) * 60.0);
    float star = step(0.997, hash21(starCell)) * smoothstep(0.1, 0.4, rd.y);
    return col + vec3(star) * 0.5;
}

// 表面の色を求める。material には材質の番号を返す (デバッグ用)
vec3 shadeSurface(vec3 p, vec3 rd, vec2 cell, out float material)
{
    vec3 n = calcNormal(p, cell);
    vec3 lamps = lampLighting(p + n * 0.01, n);
    vec3 moon = MOON_COLOR * max(dot(n, MOON_DIR), 0.0);
    if (p.y < 0.002) {
        material = MAT_ROAD;
        vec3 asphalt = vec3(0.06);
        return asphalt * (lamps + moon + FOG_AMBIENT);
    }
    if (n.y > 0.5) {
        material = MAT_ROOF;
        return vec3(0.08) * (moon + FOG_AMBIENT);
    }
    bool isWindow;
    vec3 emission = windowLight(p, n, cell, isWindow);
    material = isWindow ? MAT_WINDOW : MAT_WALL;
    vec3 wall = mix(vec3(0.12, 0.11, 0.1), vec3(0.08, 0.09, 0.11),
                    hash21(cell + 5.0));
    return (isWindow ? vec3(0.02) : wall) * (lamps + moon + FOG_AMBIENT) +
           emission;
}

// 霧による減衰と散乱を、表面または空の色に加える
vec3 applyFog(vec3 col, float t, vec3 inScatter)
{
    float transmittance = exp(-FOG_SIGMA * t);
    return col * transmittance + FOG_AMBIENT * (1.0 - transmittance) + inScatter;
}

// ---- 1 ピクセルの描画 ----------------------------------------------------

vec3 heatmap(float x)
{
    return clamp(vec3(2.0 * x - 0.5, 1.0 - abs(2.0 * x - 1.0), 1.5 - 2.0 * x),
                 0.0, 1.0);
}

vec3 renderPixel(vec2 p, int mode)
{
    // カメラは大通りの上を、少し見上げながら進む
    vec3 ro = vec3(0.5, 0.35, 2.0 - 0.4 * iTime);
    vec3 forward = normalize(vec3(0.08, 0.12, -1.0));
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    vec3 rd = normalize(p.x * right + p.y * up + 1.4 * forward);

    Hit hit = trace(ro, rd, MAX_CELLS, true);
    if (mode == 1) {
        return heatmap(hit.cells / float(MAX_CELLS));
    }
    if (mode == 2) {
        return hit.inScatter;
    }

    if (hit.t < 0.0) {
        return (mode == 3) ? vec3(0.1, 0.1, 0.4)
                           : applyFog(skyColor(rd), MAX_DIST, hit.inScatter);
    }

    vec3 pos = ro + hit.t * rd;
    float material;
    vec3 col = shadeSurface(pos, rd, hit.cell, material);

    // 濡れた路面: フレネル反射で、窓や街灯の光を映り込ませる (第 11 章、第 12 章)
    float wet = (material == MAT_ROAD) ? wetness(pos.xz) : 0.0;
    if (mode == 3) {
        vec3 id = (material == MAT_ROAD) ? vec3(0.3) :
                  (material == MAT_WINDOW) ? vec3(1.0, 0.8, 0.3) :
                  (material == MAT_ROOF) ? vec3(0.5, 0.2, 0.2) : vec3(0.4, 0.5, 0.6);
        return mix(id, vec3(0.2, 0.5, 1.0), wet);
    }
    if (material == MAT_ROAD) {
        vec3 n = vec3(0.0, 1.0, 0.0);
        float cosTheta = max(dot(-rd, n), 0.0);
        // 乾いた路面は粗く、映り込みが弱い。水たまりは鏡に近い
        float f0 = mix(0.02, 0.04, wet);
        float fresnel = (f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0)) *
                        mix(0.05, 1.0, wet);
        vec3 reflDir = reflect(rd, n);
        Hit refl = trace(pos + n * 0.002, reflDir, REFLECT_CELLS, false);
        vec3 reflection;
        if (refl.t > 0.0) {
            float m;
            reflection = shadeSurface(pos + refl.t * reflDir, reflDir,
                                      refl.cell, m);
            reflection = applyFog(reflection, refl.t, vec3(0.0));
        } else {
            reflection = skyColor(reflDir);
        }
        col = mix(col, reflection, fresnel);
    }
    return applyFog(col, hit.t, hit.inScatter);
}

vec3 toneMapACES(vec3 x)
{
    x *= 0.6;
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;
    int mode = DEBUG_MODE;
    vec2 frag = fragCoord;
    if (mode < 0) {
        vec2 cell = floor(uv * 2.0);
        mode = int(cell.x) + 2 * int(1.0 - cell.y);   // 左上から 0, 1, 2, 3
        frag = fract(uv * 2.0) * iResolution.xy;
    }
    vec2 p = (2.0 * frag - iResolution.xy) / iResolution.y;
    vec3 col = renderPixel(p, mode);
    if (mode == 0 || mode == 2) {
        // 夜景は暗いので、露出を上げてからトーンマッピングする
        col = pow(toneMapACES(3.0 * col), vec3(1.0 / 2.2));
    }
    fragColor = vec4(col, 1.0);
}
