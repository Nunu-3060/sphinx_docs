// 15_hex_columns.frag
// 第 15 章: 六角形の格子の走査。六角形のセルごとに高さの異なる六角柱を立て、
// 玄武岩の柱状節理のような風景を描く。レイが通過するセルを、各セルから
// 出ていく辺を求めて順にたどり、各セルの中だけでスフィアトレーシングを行う。

const int   MAX_CELLS  = 160;    // レイが通過するセルの最大数
const int   CELL_STEPS = 24;     // 1 セルの中でのスフィアトレーシングの最大反復回数
const float MAX_DIST   = 60.0;
const float SURF_DIST  = 0.001;
const float MAX_HEIGHT = 3.0;    // 六角柱の高さの上限

const vec3 LIGHT_DIR = normalize(vec3(-0.5, 0.55, -0.6));
const vec3 SUN_COLOR = vec3(1.4, 1.25, 1.05);
const vec3 SKY_COLOR = vec3(0.35, 0.45, 0.6);

// ---- ハッシュとノイズ (第 10 章) -----------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

float hash21(vec2 p)
{
    uvec2 q = uvec2(ivec2(floor(p * 2.0 + 0.5)));   // 半整数の座標も区別する
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

// ---- 六角形の格子 --------------------------------------------------------

// 隣り合うセルの中心の間隔を 1 とする六角形の格子 (第 4 章の 04_hex_repeat.frag と同じ)。
// 点 p を含むセルの中心を返す
vec2 hexCenter(vec2 p)
{
    const vec2 s = vec2(1.0, 1.7320508);
    vec2 a = s * (floor(p / s) + 0.5);
    vec2 b = s * (floor((p - 0.5 * s) / s) + 0.5) + 0.5 * s;
    return (dot(p - a, p - a) < dot(p - b, p - b)) ? a : b;
}

// 六角形のセルの 3 組の辺の法線。隣のセルの中心は、この方向に ±1 だけ離れている
const vec2 HEX_NORMALS[3] = vec2[3](vec2(1.0, 0.0),
                                    vec2(0.5, 0.8660254),
                                    vec2(-0.5, 0.8660254));

// ---- セルの中の形状 ------------------------------------------------------

float sdHexPrism(vec3 p, float r, float h)
{
    const vec3 k = vec3(-0.8660254, 0.5, 0.57735);
    vec2 q = abs(p.zx);
    q -= 2.0 * min(dot(k.xy, q), 0.0) * k.xy;
    vec2 d = vec2(length(q - vec2(clamp(q.x, -k.z * r, k.z * r), r)) *
                  sign(q.y - r),
                  abs(p.y) - h);
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

// セルの中心 center に立てる六角柱の高さ。海岸から内陸に向かって高くなり、
// セルごとにランダムな段差を付ける。0 以下のセルには六角柱を立てない (海)
float columnHeight(vec2 center)
{
    float base = smoothstep(-6.0, 10.0, center.y + 4.0 * valueNoise(0.15 * center));
    return (MAX_HEIGHT - 0.2) * base - 0.25 + 0.35 * hash21(center);
}

// セル center の中の形状 (海面と六角柱) の SDF
float cellSDF(vec3 p, vec2 center)
{
    float h = columnHeight(center);
    if (h <= 0.0) {
        return p.y;
    }
    float column = sdHexPrism(vec3(p.x - center.x, p.y - 0.5 * h,
                                   p.z - center.y), 0.48, 0.5 * h);
    return min(column, p.y);
}

// ---- 六角形の格子の走査 --------------------------------------------------

// レイが最初に当たる点までの距離を返す。当たらなければ -1.0。
// cellOut には当たったセルの中心を返す
float trace(vec3 ro, vec3 rd, out vec2 cellOut)
{
    vec2 center = hexCenter(ro.xz);
    float tEnter = 0.0;
    for (int i = 0; i < MAX_CELLS; i++) {
        // このセルから出ていく辺: 3 組の辺のそれぞれについて、
        // レイが進む向きにある辺に達する t を求め、最小のものを選ぶ
        float tExit = 1e9;
        vec2 nextCenter = center;
        for (int k = 0; k < 3; k++) {
            vec2 n = HEX_NORMALS[k];
            float dn = dot(rd.xz, n);
            if (abs(dn) < 1e-6) {
                continue;
            }
            float side = sign(dn);   // 正の側と負の側のどちらの辺に向かうか
            // 辺は、セルの中心から法線方向に ±0.5 の位置にある
            float t = (side * 0.5 - dot(ro.xz - center, n)) / dn;
            if (t < tExit) {
                tExit = t;
                nextCenter = center + side * n;   // 辺の向こう側のセル
            }
        }

        // このセルの中 (tEnter〜tExit) だけでスフィアトレーシングを行う
        float t = tEnter;
        for (int j = 0; j < CELL_STEPS && t < tExit; j++) {
            float d = cellSDF(ro + t * rd, center);
            if (d < SURF_DIST) {
                cellOut = center;
                return t;
            }
            t += d;
        }
        if ((rd.y > 0.0 && ro.y + tExit * rd.y > MAX_HEIGHT + 0.5) ||
            tExit > MAX_DIST) {
            break;
        }
        center = nextCenter;
        tEnter = tExit;
    }
    cellOut = center;
    return -1.0;
}

vec3 calcNormal(vec3 p, vec2 center)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * cellSDF(p + k.xyy * h, center) +
                     k.yyx * cellSDF(p + k.yyx * h, center) +
                     k.yxy * cellSDF(p + k.yxy * h, center) +
                     k.xxx * cellSDF(p + k.xxx * h, center));
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

    float angle = 0.3 + 0.1 * iTime;
    vec3 ta = vec3(0.0, 0.3, -1.0);
    vec3 ro = ta + vec3(7.0 * sin(angle), 3.5, 7.0 * cos(angle));
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.8));

    vec3 col = SKY_COLOR + 0.3 * (1.0 - max(rd.y, 0.0));
    vec2 cell;
    float t = trace(ro, rd, cell);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos, cell);
        vec2 shadowCell;
        float shadow = (trace(pos + n * 0.002, LIGHT_DIR, shadowCell) > 0.0)
                       ? 0.0 : 1.0;
        vec3 albedo;
        if (pos.y < 0.001) {
            albedo = vec3(0.05, 0.12, 0.15);                         // 海
        } else {
            albedo = vec3(0.11, 0.105, 0.1) * (0.8 + 0.4 * hash21(cell));  // 玄武岩
        }
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.5 + 0.5 * n.y;
        col = albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR + 0.3, 1.0 - exp(-0.01 * t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
