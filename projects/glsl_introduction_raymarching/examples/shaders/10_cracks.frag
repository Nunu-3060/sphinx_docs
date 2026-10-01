// 10_cracks.frag
// 第 10 章: セルラーノイズの 3 次元の応用。地面をボロノイのセルで区切って石畳にし、
// 岩の表面を 3 次元のセルラーノイズでひび割れさせる。
// どちらもノイズで SDF を変形させているので、歩幅を小さくして進む。

const int   MAX_STEPS  = 200;
const float MAX_DIST   = 40.0;
const float SURF_DIST  = 0.001;
const float STEP_SCALE = 0.6;    // ノイズによる距離の過大評価への対策

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.6, 0.3));
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3 SKY_COLOR = vec3(0.3, 0.38, 0.5);

// ---- ハッシュ (第 10 章) -------------------------------------------------

uint pcgHash(uint v)
{
    uint state = v * 747796405u + 2891336453u;
    uint word = ((state >> ((state >> 28u) + 4u)) ^ state) * 277803737u;
    return (word >> 22u) ^ word;
}

vec2 hash22(vec2 p)
{
    uvec2 q = uvec2(ivec2(p));
    uint h = pcgHash(q.x + pcgHash(q.y));
    return vec2(float(h), float(pcgHash(h))) / 4294967296.0;
}

vec3 hash33(vec3 p)
{
    uvec3 q = uvec3(ivec3(p));
    uint h = pcgHash(q.x + pcgHash(q.y + pcgHash(q.z)));
    uint h2 = pcgHash(h);
    return vec3(float(h), float(h2), float(pcgHash(h2))) / 4294967296.0;
}

// ---- セルラーノイズ ------------------------------------------------------

// 2 次元のボロノイの境界までの距離 (10_cellular.frag と同じ方法)。
// cellId には、点 x が属するセルの番号を返す
float voronoiBorder(vec2 x, out vec2 cellId)
{
    vec2 n = floor(x);
    vec2 f = fract(x);
    vec2 nearestCell = vec2(0.0);
    vec2 nearest = vec2(0.0);
    float best = 8.0;
    for (int j = -1; j <= 1; j++) {
        for (int i = -1; i <= 1; i++) {
            vec2 g = vec2(float(i), float(j));
            vec2 r = g + 0.1 + 0.8 * hash22(n + g) - f;
            float d = dot(r, r);
            if (d < best) {
                best = d;
                nearest = r;
                nearestCell = g;
            }
        }
    }
    float border = 8.0;
    for (int j = -2; j <= 2; j++) {
        for (int i = -2; i <= 2; i++) {
            vec2 g = nearestCell + vec2(float(i), float(j));
            vec2 r = g + 0.1 + 0.8 * hash22(n + g) - f;
            vec2 diff = r - nearest;
            if (dot(diff, diff) > 1e-6) {
                border = min(border, dot(0.5 * (nearest + r), normalize(diff)));
            }
        }
    }
    cellId = n + nearestCell;
    return border;
}

// 3 次元のセルラーノイズの F2 - F1 (3 × 3 × 3 のセルを調べる)。
// 値が 0 に近い場所がボロノイの境界 (ひび割れ) になる
float cellularEdge3(vec3 x)
{
    vec3 n = floor(x);
    vec3 f = fract(x);
    float f1 = 8.0;
    float f2 = 8.0;
    for (int k = -1; k <= 1; k++) {
        for (int j = -1; j <= 1; j++) {
            for (int i = -1; i <= 1; i++) {
                vec3 g = vec3(float(i), float(j), float(k));
                vec3 r = g + hash33(n + g) - f;
                float d = length(r);
                if (d < f1) {
                    f2 = f1;
                    f1 = d;
                } else if (d < f2) {
                    f2 = d;
                }
            }
        }
    }
    return f2 - f1;
}

// ---- シーン --------------------------------------------------------------

const float MAT_STONE = 1.0;
const float MAT_JOINT = 2.0;
const float MAT_ROCK  = 3.0;

// 石畳: セルごとに高さの異なる石を並べ、境界 (目地) を低くする
vec2 sdPaving(vec3 p)
{
    vec2 cellId;
    float border = voronoiBorder(1.5 * p.xz, cellId) / 1.5;
    float top = 0.06 + 0.03 * hash22(cellId + 7.0).x;       // 石の高さ
    // 目地から離れるにつれて、角を丸めながら石の高さまで上げる
    float height = top * smoothstep(0.015, 0.06, border);
    float mat = (border < 0.03) ? MAT_JOINT : MAT_STONE;
    return vec2(p.y - height, mat);
}

// 岩: 球の表面を、3 次元のセルラーノイズの境界に沿ってくぼませる
vec2 sdRock(vec3 p)
{
    vec3 q = p - vec3(0.0, 0.8, 0.0);
    float d = length(q) - 0.9;
    // 岩の近くだけでノイズを評価する (第 9 章のバウンディングボリューム)
    if (d < 0.1) {
        float edge = cellularEdge3(3.0 * q);
        d += 0.04 * (1.0 - smoothstep(0.0, 0.12, edge));
    }
    return vec2(d, MAT_ROCK);
}

vec2 map(vec3 p)
{
    vec2 paving = sdPaving(p);
    vec2 rock = sdRock(p);
    return (rock.x < paving.x) ? rock : paving;
}

vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec2(t, h.y);
        }
        t += h.x * STEP_SCALE;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(-1.0, 0.0);
}

vec3 calcNormal(vec3 p)
{
    const float h = 0.001;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h).x +
                     k.yyx * map(p + k.yyx * h).x +
                     k.yxy * map(p + k.yxy * h).x +
                     k.xxx * map(p + k.xxx * h).x);
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.02;
    for (int i = 0; i < 48 && t < 6.0; i++) {
        float h = map(ro + t * rd).x;
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.02, 0.3);
    }
    return clamp(res, 0.0, 1.0);
}

vec3 albedoOf(float mat, vec3 p)
{
    if (mat == MAT_JOINT) {
        return vec3(0.15, 0.13, 0.11);
    }
    if (mat == MAT_ROCK) {
        return vec3(0.45, 0.42, 0.38);
    }
    vec2 cellId;
    voronoiBorder(1.5 * p.xz, cellId);
    return vec3(0.5, 0.45, 0.4) * (0.75 + 0.5 * hash22(cellId).y);
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

    float angle = 0.5 + 0.1 * iTime;
    vec3 ro = vec3(4.0 * sin(angle), 2.6, 4.0 * cos(angle));
    vec3 ta = vec3(0.0, 0.4, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.8));

    vec3 col = SKY_COLOR;
    vec2 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos);
        float shadow = softShadow(pos + n * 0.01, LIGHT_DIR);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
        float sky = 0.5 + 0.5 * n.y;
        col = albedoOf(hit.y, pos) * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR, 1.0 - exp(-0.02 * hit.x));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
