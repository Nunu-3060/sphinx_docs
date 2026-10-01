// 15_city.frag
// 第 15 章: グリッドの走査とスフィアトレーシングの組み合わせ。
// xz 平面の各セルに、高さと幅がランダムなビルを 1 棟ずつ置く。
// レイが通るセルを 2D DDA で順にたどり、各セルの中だけでスフィアトレーシングを行う。

const int   MAX_CELLS  = 96;      // レイが通過するセルの最大数
const int   CELL_STEPS = 32;      // 1 セルの中でのスフィアトレーシングの最大反復回数
const float MAX_DIST   = 80.0;
const float SURF_DIST  = 0.001;
const float MAX_HEIGHT = 4.0;     // ビルの高さの上限

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

float hash21(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    return float(pcgHash(q.x + pcgHash(q.y))) / 4294967296.0;
}

// ---- セルの中の形状 ------------------------------------------------------

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// セル cell に置くビルの大きさ (半分の長さ)。セルごとに幅と高さが異なる
vec3 buildingSize(vec2 cell)
{
    float h = MAX_HEIGHT * pow(hash21(cell), 2.0) + 0.2;
    float w = 0.25 + 0.15 * hash21(cell + 17.0);
    return vec3(w, 0.5 * h, w);
}

// セル cell の中にある形状 (地面とビル) の SDF。
// ほかのセルのビルは考えないので、セルの外では正しい距離にならない
float cellSDF(vec3 p, vec2 cell)
{
    vec3 size = buildingSize(cell);
    vec3 center = vec3(cell.x + 0.5, size.y, cell.y + 0.5);
    return min(p.y, sdBox(p - center, size));
}

// ---- 2D DDA とスフィアトレーシング ---------------------------------------

// レイが最初に当たる点までの距離を返す。当たらなければ -1.0。
// cellOut には当たったセルの番号を返す
float trace(vec3 ro, vec3 rd, out vec2 cellOut)
{
    vec2 dir = mix(rd.xz, vec2(1e-6), lessThan(abs(rd.xz), vec2(1e-6)));
    vec2 cell = floor(ro.xz);
    vec2 stepDir = sign(dir);
    vec2 tDelta = abs(1.0 / dir);
    vec2 tMax = (stepDir * (cell - ro.xz) + 0.5 * stepDir + 0.5) * tDelta;
    float tEnter = 0.0;

    for (int i = 0; i < MAX_CELLS; i++) {
        float tExit = min(tMax.x, tMax.y);
        // このセルの中 (tEnter〜tExit) だけでスフィアトレーシングを行う
        float t = tEnter;
        for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
            float d = cellSDF(ro + t * rd, cell);
            if (d < SURF_DIST) {
                cellOut = cell;
                return t;
            }
            t += d;
        }
        // 上に向かうレイが、ビルより高い所まで上がったら、もう何にも当たらない
        if (rd.y > 0.0 && ro.y + tExit * rd.y > MAX_HEIGHT + 0.5) {
            break;
        }
        // 次のセルに進む
        vec2 mask = step(tMax, tMax.yx);
        tMax += mask * tDelta;
        cell += mask * stepDir;
        tEnter = tExit;
        if (tEnter > MAX_DIST) {
            break;
        }
    }
    cellOut = cell;
    return -1.0;
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

// ---- 色 ------------------------------------------------------------------

vec3 albedoOf(vec3 p, vec3 n, vec2 cell)
{
    if (p.y < 0.001) {
        return vec3(0.25);                               // 道路
    }
    vec3 base = mix(vec3(0.55, 0.52, 0.48), vec3(0.35, 0.4, 0.5),
                    hash21(cell + 5.0));
    // 側面に窓の並びを描く
    if (abs(n.y) < 0.5) {
        vec2 uv = vec2(p.x + p.z, p.y) * vec2(6.0, 5.0);
        vec2 f = fract(uv);
        float window = step(0.3, f.x) * step(f.x, 0.8) * step(0.35, f.y) *
                       step(f.y, 0.75);
        base = mix(base, vec3(0.1, 0.12, 0.15), window);
    }
    return base;
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

    // カメラは街の上空を斜めに進む
    vec3 ro = vec3(0.3 * iTime + 0.37, 5.5, 0.6 * iTime + 0.21);
    vec3 ta = ro + vec3(3.0, -2.5, 6.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.6));

    vec3 col = SKY_COLOR + 0.25 * (1.0 - rd.y);
    vec2 cell;
    float t = trace(ro, rd, cell);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos, cell);
        // 影も同じ走査で求める
        vec2 shadowCell;
        float shadow = trace(pos + n * 0.002, LIGHT_DIR, shadowCell) > 0.0
                       ? 0.0 : 1.0;
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.35 + 0.35 * n.y;
        col = albedoOf(pos, n, cell) * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR + 0.25, 1.0 - exp(-0.01 * t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
