// 15_octree.frag
// 第 15 章: 手続き的な八分木。1 辺 8 の立方体の空間を、ハッシュ関数で選んだ場所だけ
// 8 つに分割することを繰り返し、葉のセルの一部に大小の立方体を浮かべる。
// 何も置かないセルは大きいまま残るので、レイは空の空間を一度に飛ばせる。

const float ROOT_HALF  = 4.0;     // 根のセル (立方体) の 1 辺の半分
const int   MAX_DEPTH  = 4;       // 分割の最大の深さ (最小のセルの 1 辺は 0.5)
const int   MAX_CELLS  = 200;
const int   CELL_STEPS = 24;
const float SURF_DIST  = 0.0005;
const float CELL_EPS   = 0.0005;

const vec3 LIGHT_DIR = normalize(vec3(0.5, 0.8, 0.3));

// ---- ハッシュ (第 10 章) -------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

// セルの位置 (最小のセルを単位とする整数) と深さから乱数を作る
float hashCell(vec3 cellMin, int depth, float salt)
{
    uvec3 q = uvec3(ivec3(cellMin * 2.0 + 16.0));
    uint h = pcgHash(q.x + pcgHash(q.y + pcgHash(q.z +
                                                 pcgHash(uint(depth) + uint(salt)))));
    return float(h) / 4294967296.0;
}

// ---- 八分木 --------------------------------------------------------------

// 点 p を含む葉のセルを求める。cellMin には最小の角、size には 1 辺、
// 戻り値には深さを返す
int octreeLeaf(vec3 p, out vec3 cellMin, out float size)
{
    size = 2.0 * ROOT_HALF;
    cellMin = vec3(-ROOT_HALF);
    int depth = 0;
    for (; depth < MAX_DEPTH; depth++) {
        if (hashCell(cellMin, depth, 0.0) > 0.75) {
            break;                                   // このセルは分割しない
        }
        size *= 0.5;
        cellMin += step(cellMin + size, p) * size;   // 8 つの子のうち p を含む子
    }
    return depth;
}

// 葉のセルに物体を置くか。深いセル (小さなセル) ほど置く確率を高くする
bool hasObject(vec3 cellMin, int depth)
{
    return hashCell(cellMin, depth, 7.0) < 0.15 + 0.12 * float(depth);
}

// ---- セルの中の形状 ------------------------------------------------------

float sdRoundBox(vec3 p, vec3 b, float r)
{
    vec3 q = abs(p) - b + r;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

// 葉のセルの中の立方体の SDF。物体の無いセルでは、セルの外まで届く大きな値を返す
float cellSDF(vec3 p, vec3 cellMin, float size, int depth)
{
    if (!hasObject(cellMin, depth)) {
        return 1e9;
    }
    vec3 center = cellMin + 0.5 * size;
    float half_ = 0.32 * size;
    return sdRoundBox(p - center, vec3(half_), 0.15 * half_);
}

// ---- 大きさの異なるセルの走査 --------------------------------------------

// 箱 [bmin, bmin + size] とレイの交差。戻り値は (入る t, 出る t)
vec2 boxInterval(vec3 ro, vec3 rd, vec3 bmin, float size)
{
    vec3 dir = mix(rd, vec3(1e-6), lessThan(abs(rd), vec3(1e-6)));
    vec3 t0 = (bmin - ro) / dir;
    vec3 t1 = (bmin + size - ro) / dir;
    vec3 tNear = min(t0, t1);
    vec3 tFar = max(t0, t1);
    return vec2(max(tNear.x, max(tNear.y, tNear.z)),
                min(tFar.x, min(tFar.y, tFar.z)));
}

// 戻り値は (t, 深さ, 通過したセルの数)。当たらなければ t は -1
vec3 trace(vec3 ro, vec3 rd)
{
    // まず根のセル全体との交差を調べ、外側の空間を飛ばす
    vec2 root = boxInterval(ro, rd, vec3(-ROOT_HALF), 2.0 * ROOT_HALF);
    if (root.x > root.y || root.y < 0.0) {
        return vec3(-1.0, 0.0, 0.0);
    }
    float tEnter = max(root.x, 0.0) + CELL_EPS;
    for (int i = 0; i < MAX_CELLS; i++) {
        if (tEnter > root.y) {
            break;                                   // 根のセルから出た
        }
        vec3 cellMin;
        float size;
        int depth = octreeLeaf(ro + tEnter * rd, cellMin, size);
        float tExit = boxInterval(ro, rd, cellMin, size).y;
        if (hasObject(cellMin, depth)) {
            float t = tEnter;
            for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
                float d = cellSDF(ro + t * rd, cellMin, size, depth);
                if (d < SURF_DIST) {
                    return vec3(t, float(depth), float(i + 1));
                }
                t += d;
            }
        }
        tEnter = tExit + CELL_EPS;
    }
    return vec3(-1.0, 0.0, 0.0);
}

vec3 calcNormal(vec3 p)
{
    vec3 cellMin;
    float size;
    int depth = octreeLeaf(p, cellMin, size);
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * cellSDF(p + k.xyy * h, cellMin, size, depth) +
                     k.yyx * cellSDF(p + k.yyx * h, cellMin, size, depth) +
                     k.yxy * cellSDF(p + k.yxy * h, cellMin, size, depth) +
                     k.xxx * cellSDF(p + k.xxx * h, cellMin, size, depth));
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

    float angle = 0.6 + 0.15 * iTime;
    vec3 ro = vec3(13.0 * sin(angle), 7.0, 13.0 * cos(angle));
    vec3 rd = setCamera(ro, vec3(0.0)) * normalize(vec3(p, 1.8));

    vec3 col = vec3(0.07, 0.08, 0.1) * (1.0 - 0.3 * length(p));
    vec3 hit = trace(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos);
        // 分割の深さ (立方体の大きさ) で色を変える
        vec3 albedo = 0.55 + 0.4 * cos(6.2831853 * (0.2 * hit.y +
                                                   vec3(0.0, 0.33, 0.67)));
        vec3 shadowHit = trace(pos + n * 0.002, LIGHT_DIR);
        float shadow = (shadowHit.x > 0.0) ? 0.3 : 1.0;
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        col = albedo * (1.0 * diffuse + 0.25 * (0.6 + 0.4 * n.y));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
