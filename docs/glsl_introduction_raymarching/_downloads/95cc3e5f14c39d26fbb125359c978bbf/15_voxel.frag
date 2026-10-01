// 15_voxel.frag
// 第 15 章: 3D DDA によるボクセルの描画。1 辺 1 の立方体 (ボクセル) を格子状に並べ、
// 各ボクセルが埋まっているかどうかを第 10 章のノイズで決めて地形を作る。

const int   MAX_STEPS = 256;      // レイが通過するボクセルの最大数
const vec3  LIGHT_DIR = normalize(vec3(0.5, 0.8, 0.3));
const vec3  SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3  SKY_COLOR = vec3(0.35, 0.45, 0.6);

// ---- ノイズ (第 10 章) ---------------------------------------------------

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

float valueNoise(vec2 p)
{
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash21(i), hash21(i + vec2(1.0, 0.0)), u.x),
               mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), u.x),
               u.y);
}

// ---- ボクセルの世界 ------------------------------------------------------

// 列 (x, z) の地面の高さ (整数)
float groundHeight(vec2 xz)
{
    float h = 8.0 * valueNoise(0.06 * xz) + 3.0 * valueNoise(0.2 * xz);
    return floor(h);
}

// 格子の番号 cell のボクセルが埋まっていれば true
bool isFilled(vec3 cell)
{
    return cell.y < groundHeight(cell.xz);
}

// ---- 3D DDA --------------------------------------------------------------

struct Hit {
    bool found;
    float t;        // 当たった面までの距離
    vec3 cell;      // 当たったボクセルの番号
    vec3 normal;    // 当たった面の法線
};

// レイが通過するボクセルを、始点に近い順に 1 つずつたどる (Amanatides and Woo, 1987)
Hit traverse(vec3 ro, vec3 rd, int maxSteps)
{
    // 0 による割り算を避ける
    rd = mix(rd, vec3(1e-6), lessThan(abs(rd), vec3(1e-6)));
    vec3 cell = floor(ro);
    vec3 stepDir = sign(rd);
    // 1 セル進むのに必要な t の増分
    vec3 tDelta = abs(1.0 / rd);
    // 各軸について、次のセルの境界に達する t
    vec3 tMax = (stepDir * (cell - ro) + 0.5 * stepDir + 0.5) * tDelta;
    vec3 mask = vec3(0.0);

    for (int i = 0; i < maxSteps; i++) {
        if (isFilled(cell)) {
            // 最後に越えた境界 (mask の軸) が、当たった面である
            float t = (i == 0) ? 0.0 : dot(tMax - tDelta, mask);
            return Hit(true, t, cell, -stepDir * mask);
        }
        // 最も近い境界の軸を選び、その方向に 1 セル進む
        mask = step(tMax, min(tMax.yzx, tMax.zxy));
        tMax += mask * tDelta;
        cell += mask * stepDir;
    }
    return Hit(false, 0.0, cell, vec3(0.0));
}

// ---- 色 ------------------------------------------------------------------

vec3 voxelColor(vec3 cell, vec3 normal)
{
    float top = groundHeight(cell.xz) - 1.0;
    vec3 grass = vec3(0.25, 0.5, 0.15);
    vec3 dirt = vec3(0.45, 0.32, 0.2);
    vec3 stone = vec3(0.45);
    vec3 col = (cell.y < top - 2.0) ? stone : dirt;
    // 一番上のボクセルの上面は草にする
    if (cell.y == top && normal.y > 0.5) {
        col = grass;
    }
    // ボクセルごとに明るさを少しばらつかせる
    return col * (0.85 + 0.3 * hash21(cell.xz + 37.0 * cell.y));
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

    vec3 ta = vec3(2.0 * iTime, 6.0, 0.0);
    vec3 ro = ta + vec3(-14.0, 12.0, 18.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = SKY_COLOR + 0.3 * (1.0 - rd.y);
    Hit hit = traverse(ro, rd, MAX_STEPS);
    if (hit.found) {
        vec3 pos = ro + hit.t * rd;
        // 影: 当たった面から光源の方向に、もう一度 DDA でたどる
        Hit shadowHit = traverse(pos + hit.normal * 0.001, LIGHT_DIR, 64);
        float shadow = shadowHit.found ? 0.0 : 1.0;
        float diffuse = max(dot(hit.normal, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.35 + 0.35 * hit.normal.y;
        col = voxelColor(hit.cell, hit.normal) *
              (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR + 0.3, 1.0 - exp(-0.006 * hit.t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
