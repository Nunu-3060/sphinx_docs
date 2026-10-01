// 04_hex_repeat.frag
// 第 4 章: 六角形の繰り返し。xz 平面を六角形のセルに分け、各セルに六角柱を置いて
// 蜂の巣のように敷き詰める。六角柱の高さは、セルの中心の位置に応じて波打たせる。

const int   MAX_STEPS  = 250;
const float MAX_DIST   = 60.0;
const float SURF_DIST  = 0.001;
const float STEP_SCALE = 0.5;    // 隣のセルとの高さの差による過大評価への対策

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3 SKY_COLOR = vec3(0.3, 0.4, 0.55);

// ---- 六角形の繰り返し ----------------------------------------------------

// 隣り合うセルの中心の間隔を 1 とする六角形の格子。
// セルの中心は、間隔 (1, √3) の長方形の格子と、それを (0.5, √3/2) ずらした格子の
// 2 つを合わせたものになる。点 p から近い方の中心を選ぶと、六角形のセルになる。
// 戻り値の xy はセルの中心を原点とする局所座標、zw はセルの中心の位置
vec4 hexCell(vec2 p)
{
    const vec2 s = vec2(1.0, 1.7320508);
    vec2 a = s * (floor(p / s) + 0.5);                        // 1 つ目の格子の中心
    vec2 b = s * (floor((p - 0.5 * s) / s) + 0.5) + 0.5 * s;  // 2 つ目の格子の中心
    vec2 da = p - a;
    vec2 db = p - b;
    return (dot(da, da) < dot(db, db)) ? vec4(da, a) : vec4(db, b);
}

// 六角柱の SDF (Quilez による)。xz 平面上の六角形 (内接円の半径 r) を、
// y 方向に高さの半分 h だけ押し出したもの。六角形の頂点は ±z の方向にある
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

// ---- シーン --------------------------------------------------------------

float columnHeight(vec2 center)
{
    return 0.6 + 0.35 * sin(0.8 * length(center) - 1.5 * iTime);
}

float map(vec3 p)
{
    vec4 hex = hexCell(p.xz);
    float h = columnHeight(hex.zw);
    // セルの局所座標で六角柱を評価する。隙間を空けるため内接円の半径を 0.46 にする
    float column = sdHexPrism(vec3(hex.x, p.y - 0.5 * h, hex.y), 0.46, 0.5 * h);
    return min(column, p.y);
}

// ---- レンダリング --------------------------------------------------------

float raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        if (d < SURF_DIST) {
            return t;
        }
        t += d * STEP_SCALE;
        if (t > MAX_DIST) {
            break;
        }
    }
    return -1.0;
}

vec3 calcNormal(vec3 p)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h) + k.yyx * map(p + k.yyx * h) +
                     k.yxy * map(p + k.yxy * h) + k.xxx * map(p + k.xxx * h));
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 64 && t < 10.0; i++) {
        float h = map(ro + t * rd);
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.01, 0.3);
    }
    return clamp(res, 0.0, 1.0);
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

    vec3 ro = vec3(5.0, 5.0, 7.0);
    vec3 ta = vec3(0.0, 0.3, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = SKY_COLOR;
    float t = raymarch(ro, rd);
    if (t > 0.0) {
        vec3 pos = ro + t * rd;
        vec3 n = calcNormal(pos);
        vec4 hex = hexCell(pos.xz);
        // 六角柱の上面は、高さに応じて色を変える
        vec3 albedo = (pos.y < 0.001) ? vec3(0.1)
                    : mix(vec3(0.85, 0.6, 0.15), vec3(0.95, 0.85, 0.5),
                          columnHeight(hex.zw) - 0.25);
        float diffuse = max(dot(n, LIGHT_DIR), 0.0) *
                        softShadow(pos + n * 0.01, LIGHT_DIR);
        float sky = 0.5 + 0.5 * n.y;
        col = albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
        col = mix(col, SKY_COLOR, 1.0 - exp(-0.02 * t));
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
