// 15_tri_grid.frag
// 第 15 章: 三角形の格子の走査。正三角形のセルごとに高さの異なる三角柱を立てる。
// 三角形の格子は 3 組の平行な直線でできているので、15_voxel.frag の DDA を
// 3 組の直線に広げるだけで走査できる。

const int   MAX_CELLS  = 200;
const int   CELL_STEPS = 24;
const float MAX_DIST   = 60.0;
const float SURF_DIST  = 0.001;
const float MAX_HEIGHT = 2.0;
const float SPACING    = 0.8;    // 平行な直線の間隔 (三角形の高さ)

const vec3 LIGHT_DIR = normalize(vec3(0.5, 0.7, 0.3));
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3 SKY_COLOR = vec3(0.3, 0.4, 0.55);

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

// ---- 三角形の格子 --------------------------------------------------------

// 3 組の直線の法線。互いに 120° ずつ離れた単位ベクトルで、和は 0 になる
const vec2 TRI_NORMALS[3] = vec2[3](vec2(0.0, 1.0),
                                    vec2(-0.8660254, -0.5),
                                    vec2(0.8660254, -0.5));

// 点 p (xz) について、3 組の直線のそれぞれで何本目の直線の間にあるか (セルの番号)
vec3 triCell(vec2 p)
{
    return floor(vec3(dot(p, TRI_NORMALS[0]), dot(p, TRI_NORMALS[1]),
                      dot(p, TRI_NORMALS[2])) / SPACING);
}

// ---- セルの中の形状 ------------------------------------------------------

// セルの番号の和は -1 か -2 になり、それによって三角形の向きが決まる。
// 和が -1 の三角形は「各直線の下側の境界」、-2 の三角形は「上側の境界」で囲まれる
float sdTriangleCell(vec2 p, vec3 cell, float inset)
{
    vec3 dots = vec3(dot(p, TRI_NORMALS[0]), dot(p, TRI_NORMALS[1]),
                     dot(p, TRI_NORMALS[2]));
    if (cell.x + cell.y + cell.z > -1.5) {
        // 和が -1: 3 本の下側の境界から内側にある
        vec3 d = cell * SPACING + inset - dots;
        return max(d.x, max(d.y, d.z));
    }
    // 和が -2: 3 本の上側の境界から内側にある
    vec3 d = dots - (cell + 1.0) * SPACING + inset;
    return max(d.x, max(d.y, d.z));
}

float prismHeight(vec3 cell)
{
    return 0.15 + MAX_HEIGHT * pow(hash31(cell + 100.0), 3.0);
}

// セル cell の中の形状 (地面と三角柱) の SDF。凸多角形の各辺の平面までの
// 距離の最大値なので、厳密な距離ではなく距離の下界になる
float cellSDF(vec3 p, vec3 cell)
{
    float h = prismHeight(cell);
    float prism = max(sdTriangleCell(p.xz, cell, 0.04), p.y - h);
    return min(prism, p.y);
}

// ---- 三角形の格子の走査 (3 組の直線の DDA) -------------------------------

float trace(vec3 ro, vec3 rd, out vec3 cellOut)
{
    vec3 cell = triCell(ro.xz);
    // 各組の直線について、レイの進行方向の成分と、1 本進むのに必要な t の増分
    vec3 dirDots = vec3(dot(rd.xz, TRI_NORMALS[0]), dot(rd.xz, TRI_NORMALS[1]),
                        dot(rd.xz, TRI_NORMALS[2]));
    dirDots = mix(dirDots, vec3(1e-6), lessThan(abs(dirDots), vec3(1e-6)));
    vec3 stepDir = sign(dirDots);
    vec3 tDelta = SPACING / abs(dirDots);
    vec3 originDots = vec3(dot(ro.xz, TRI_NORMALS[0]),
                           dot(ro.xz, TRI_NORMALS[1]),
                           dot(ro.xz, TRI_NORMALS[2]));
    // 各組の次の直線に達する t (15_voxel.frag の 3D DDA と同じ式)
    vec3 tMax = ((cell + 0.5 + 0.5 * stepDir) * SPACING - originDots) / dirDots;
    float tEnter = 0.0;

    for (int i = 0; i < MAX_CELLS; i++) {
        float tExit = min(tMax.x, min(tMax.y, tMax.z));
        float t = tEnter;
        for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
            float d = cellSDF(ro + t * rd, cell);
            if (d < SURF_DIST) {
                cellOut = cell;
                return t;
            }
            t += d;
        }
        if ((rd.y > 0.0 && ro.y + tExit * rd.y > MAX_HEIGHT + 0.5) ||
            tExit > MAX_DIST) {
            break;
        }
        // 最も近い直線を越え、その組の番号だけを 1 つ進める
        vec3 mask = step(tMax, min(tMax.yzx, tMax.zxy));
        tMax += mask * tDelta;
        cell += mask * stepDir;
        tEnter = tExit;
    }
    cellOut = cell;
    return -1.0;
}

vec3 calcNormal(vec3 p, vec3 cell)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * cellSDF(p + k.xyy * h, cell) +
                     k.yyx * cellSDF(p + k.yyx * h, cell) +
                     k.yxy * cellSDF(p + k.yxy * h, cell) +
                     k.xxx * cellSDF(p + k.xxx * h, cell));
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

    float angle = 0.6 + 0.1 * iTime;
    vec3 ro = vec3(7.0 * sin(angle), 5.0, 7.0 * cos(angle));
    vec3 ta = vec3(0.0, 0.3, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.8));

    vec3 col = SKY_COLOR;
    vec3 cell;
    float t = trace(ro, rd, cell);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos, cell);
        vec3 shadowCell;
        float shadow = (trace(pos + n * 0.002, LIGHT_DIR, shadowCell) > 0.0)
                       ? 0.0 : 1.0;
        // 三角形の向き (セルの番号の和) で色を変える
        bool upward = cell.x + cell.y + cell.z > -1.5;
        vec3 albedo = (pos.y < 0.001) ? vec3(0.12)
                    : upward ? vec3(0.8, 0.35, 0.25) : vec3(0.25, 0.5, 0.75);
        albedo *= 0.8 + 0.4 * hash31(cell);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.5 + 0.5 * n.y;
        col = albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR, 1.0 - exp(-0.02 * t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
