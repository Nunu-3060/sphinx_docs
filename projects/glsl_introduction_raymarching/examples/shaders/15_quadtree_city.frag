// 15_quadtree_city.frag
// 第 15 章: 手続き的な四分木による街並み。地面の区画を四分木で大小に分割し、
// 区画の大きさに応じたビルを建てる。レイが通過する葉のセル (区画) を順にたどり、
// 各セルの中だけでスフィアトレーシングを行う。

const float ROOT_SIZE  = 8.0;     // 分割前の区画の 1 辺
const int   MAX_DEPTH  = 3;       // 分割の最大の深さ (最小の区画の 1 辺は 1)
const int   MAX_CELLS  = 160;     // レイが通過するセルの最大数
const int   CELL_STEPS = 32;      // 1 セルの中でのスフィアトレーシングの最大反復回数
const float MAX_DIST   = 80.0;
const float SURF_DIST  = 0.001;
const float MAX_HEIGHT = 6.0;
const float CELL_EPS   = 0.001;   // 隣のセルに入るために、出口より少し先に進む距離

const vec3 LIGHT_DIR = normalize(vec3(-0.5, 0.6, -0.4));
const vec3 SUN_COLOR = vec3(1.4, 1.25, 1.05);
const vec3 SKY_COLOR = vec3(0.35, 0.45, 0.6);

// ---- ハッシュ (第 10 章) -------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float hash31(vec3 p)
{
    uvec3 q = uvec3(ivec3(p));
    return float(pcgHash(q.x + pcgHash(q.y + pcgHash(q.z)))) / 4294967296.0;
}

// ---- 四分木 --------------------------------------------------------------

// 点 p (xz) を含む葉のセル (区画) を求める (10_quadtree_pattern.frag と同じ方法)
void quadtreeLeaf(vec2 p, out vec2 cellMin, out float size)
{
    size = ROOT_SIZE;
    cellMin = floor(p / size) * size;
    for (int depth = 0; depth < MAX_DEPTH; depth++) {
        if (hash31(vec3(cellMin, float(depth))) > 0.7) {
            break;                                   // このセルは分割しない
        }
        size *= 0.5;
        cellMin += step(cellMin + size, p) * size;   // p を含む子に進む
    }
}

// ---- セルの中の形状 ------------------------------------------------------

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// 区画 (cellMin, size) のビルの大きさ (半分の長さ)。大きな区画ほど高いビルにする
vec3 buildingSize(vec2 cellMin, float size)
{
    float h = MAX_HEIGHT * (size / ROOT_SIZE) *
              (0.3 + 0.7 * hash31(vec3(cellMin, size + 17.0))) + 0.2;
    float w = 0.5 * size - 0.15;                     // 区画の縁に道路を残す
    return vec3(w, 0.5 * h, w);
}

// 区画の中の形状 (地面とビル) の SDF
float cellSDF(vec3 p, vec2 cellMin, float size)
{
    vec3 b = buildingSize(cellMin, size);
    vec3 center = vec3(cellMin.x + 0.5 * size, b.y, cellMin.y + 0.5 * size);
    return min(p.y, sdBox(p - center, b));
}

// ---- 大きさの異なるセルの走査 --------------------------------------------

// レイがセル (cellMin, size) の正方形から出ていく t を返す
float cellExit(vec3 ro, vec3 rd, vec2 cellMin, float size)
{
    vec2 dir = mix(rd.xz, vec2(1e-6), lessThan(abs(rd.xz), vec2(1e-6)));
    // 各軸について、進む向きにある辺 (正なら上側、負なら下側)
    vec2 edge = cellMin + step(0.0, dir) * size;
    vec2 t = (edge - ro.xz) / dir;
    return min(t.x, t.y);
}

// レイが最初に当たる点までの距離を返す。当たらなければ -1.0
float trace(vec3 ro, vec3 rd, out vec2 cellMinOut, out float sizeOut)
{
    float tEnter = 0.0;
    for (int i = 0; i < MAX_CELLS; i++) {
        // 現在の点を含む葉のセルを、根から求め直す
        vec3 p = ro + tEnter * rd;
        vec2 cellMin;
        float size;
        quadtreeLeaf(p.xz, cellMin, size);
        float tExit = cellExit(ro, rd, cellMin, size);

        // このセルの中 (tEnter〜tExit) だけでスフィアトレーシングを行う
        float t = tEnter;
        for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
            float d = cellSDF(ro + t * rd, cellMin, size);
            if (d < SURF_DIST) {
                cellMinOut = cellMin;
                sizeOut = size;
                return t;
            }
            t += d;
        }
        if ((rd.y > 0.0 && ro.y + tExit * rd.y > MAX_HEIGHT + 0.5) ||
            tExit > MAX_DIST) {
            break;
        }
        // 出口より少し先に進み、次のセルに入る
        tEnter = tExit + CELL_EPS;
    }
    return -1.0;
}

vec3 calcNormal(vec3 p, vec2 cellMin, float size)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * cellSDF(p + k.xyy * h, cellMin, size) +
                     k.yyx * cellSDF(p + k.yyx * h, cellMin, size) +
                     k.yxy * cellSDF(p + k.yxy * h, cellMin, size) +
                     k.xxx * cellSDF(p + k.xxx * h, cellMin, size));
}

// ---- メイン --------------------------------------------------------------

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

    vec3 ro = vec3(0.37 + 0.4 * iTime, 16.0, 0.21 + 0.8 * iTime);
    vec3 ta = ro + vec3(5.0, -11.0, 9.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.6));

    vec3 col = SKY_COLOR + 0.25 * (1.0 - max(rd.y, 0.0));
    vec2 cellMin;
    float size;
    float t = trace(ro, rd, cellMin, size);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos, cellMin, size);
        vec2 shadowCellMin;
        float shadowSize;
        float shadow = (trace(pos + n * 0.002, LIGHT_DIR, shadowCellMin,
                              shadowSize) > 0.0) ? 0.0 : 1.0;
        vec3 albedo;
        if (pos.y < 0.001) {
            albedo = vec3(0.22);                             // 道路
        } else {
            // 区画の大きさ (分割の深さ) でビルの色を変える
            float depth = log2(ROOT_SIZE / size);
            albedo = 0.45 + 0.3 * cos(6.2831853 *
                                      (0.2 * depth + vec3(0.0, 0.1, 0.2)));
        }
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.35 + 0.35 * n.y;
        col = albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR + 0.25, 1.0 - exp(-0.01 * t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
