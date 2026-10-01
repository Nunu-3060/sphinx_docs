// 07_orthographic.frag
// 第 7 章: 平行投影 (正射影) によるアイソメトリック表示。
// ORTHOGRAPHIC を 0 にすると、同じ向きのピンホールカメラ (透視投影) になる。

#define ORTHOGRAPHIC 1

const int   MAX_STEPS = 128;
const float MAX_DIST  = 200.0;
const float SURF_DIST = 0.001;

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));  // 光源の方向 (表面から光源へ)
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);             // 平行光源の放射輝度
const vec3 SKY_COLOR = vec3(0.3, 0.4, 0.55);            // 天空光 (環境光) の放射輝度

// ---- SDF ----------------------------------------------------------------

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float sdBox(vec3 p, vec3 b)
{
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

float sdPlane(vec3 p, float h)
{
    return p.y - h;
}

// ---- シーン --------------------------------------------------------------

// マテリアル ID
const float MAT_GROUND = 1.0;
const float MAT_SPHERE = 2.0;
const float MAT_TORUS  = 3.0;
const float MAT_BOX    = 4.0;

// (距離, マテリアル ID) の組のうち、距離が小さい方を返す
vec2 opU(vec2 a, vec2 b)
{
    return (a.x < b.x) ? a : b;
}

vec2 map(vec3 p)
{
    vec2 res = vec2(sdPlane(p, 0.0), MAT_GROUND);
    res = opU(res, vec2(sdSphere(p - vec3(-1.6, 1.0, 0.0), 1.0), MAT_SPHERE));
    res = opU(res, vec2(sdTorus(p - vec3(1.2, 0.3, 0.8), vec2(0.8, 0.3)),
                        MAT_TORUS));
    res = opU(res, vec2(sdBox(p - vec3(0.8, 0.6, -1.5), vec3(0.6)), MAT_BOX));
    return res;
}

// ---- レイマーチング ------------------------------------------------------

// 戻り値は (t, マテリアル ID)。当たらなければマテリアル ID は -1.0
vec2 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec2(t, h.y);
        }
        t += h.x;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec2(t, -1.0);
}

// 四面体の 4 頂点方向の差分から法線を求める
vec3 calcNormal(vec3 p)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h).x +
                     k.yyx * map(p + k.yyx * h).x +
                     k.yxy * map(p + k.yxy * h).x +
                     k.xxx * map(p + k.xxx * h).x);
}

// マテリアル ID から拡散反射率 (アルベド) を決める
vec3 albedoOf(float mat, vec3 p)
{
    if (mat == MAT_GROUND) {
        // 1 辺 1 の市松模様
        float checker = mod(floor(p.x) + floor(p.z), 2.0);
        return mix(vec3(0.25), vec3(0.45), checker);
    }
    if (mat == MAT_SPHERE) {
        return vec3(0.7, 0.15, 0.1);
    }
    if (mat == MAT_TORUS) {
        return vec3(0.15, 0.45, 0.7);
    }
    return vec3(0.7, 0.6, 0.2);
}

// ---- 影 ------------------------------------------------------------------

// ソフトシャドウ: レイが物体をかすめた度合い k * h / t から半影を近似する
float softShadow(vec3 ro, vec3 rd, float tmin, float tmax, float k)
{
    float res = 1.0;
    float t = tmin;
    for (int i = 0; i < 128 && t < tmax; i++) {
        float h = map(ro + t * rd).x;
        res = min(res, k * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.01, 0.5);
    }
    res = clamp(res, 0.0, 1.0);
    return res * res * (3.0 - 2.0 * res);  // smoothstep と同じ補間で滑らかにする
}

// ---- アンビエントオクルージョン ------------------------------------------

// 法線方向の 5 点で SDF を評価し、理想値 (サンプル点までの距離 h) より
// どれだけ小さいかで遮蔽の度合いを見積もる。1 は遮蔽なし、0 は完全な遮蔽
float calcAO(vec3 p, vec3 n)
{
    float occ = 0.0;
    float weight = 1.0;
    for (int i = 0; i < 5; i++) {
        float h = 0.02 + 0.1 * float(i);
        float d = map(p + h * n).x;
        occ += (h - d) * weight;
        weight *= 0.6;
    }
    return clamp(1.0 - 2.5 * occ, 0.0, 1.0);
}

// ---- 照明 ----------------------------------------------------------------

vec3 shade(vec3 p, vec3 rd, float mat)
{
    vec3 n = calcNormal(p);
    vec3 h = normalize(LIGHT_DIR - rd);
    float shadow = softShadow(p + n * 0.01, LIGHT_DIR, 0.01, 20.0, 8.0);
    float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
    float specular = pow(max(dot(n, h), 0.0), 32.0) * diffuse;
    float sky = (0.5 + 0.5 * n.y) * calcAO(p, n);
    vec3 col = albedoOf(mat, p) * (SUN_COLOR * diffuse + SKY_COLOR * sky);
    return col + SUN_COLOR * specular * 0.5;
}

// ---- カメラ --------------------------------------------------------------

// アイソメトリック表示の視線の方向: 3 つの軸が画面上で 120° ずつ離れて見える
const vec3 VIEW_DIR = -normalize(vec3(1.0, 1.0, 1.0));

// カメラの座標軸 (右、上、前) を求める
mat3 cameraBasis(vec3 forward)
{
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    return mat3(right, up, forward);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    vec3 target = vec3(0.0, 0.5, 0.0);     // 画面の中心に来る点
    mat3 cam = cameraBasis(VIEW_DIR);
    vec3 ro;
    vec3 rd;
#if ORTHOGRAPHIC
    // 平行投影: 方向はすべてのピクセルで同じで、始点をピクセルごとにずらす。
    // viewHeight は画面の高さに写るワールドの長さ
    const float viewHeight = 7.0;
    const float backOff = 50.0;            // 物体の手前まで始点を下げる距離
    ro = target - backOff * VIEW_DIR + cam * vec3(0.5 * viewHeight * p, 0.0);
    rd = VIEW_DIR;
#else
    // 透視投影: 始点は 1 点で、方向をピクセルごとに変える
    ro = target - 9.0 * VIEW_DIR;
    rd = cam * normalize(vec3(p, 2.0));
#endif

    vec3 col = SKY_COLOR;
    vec2 hit = raymarch(ro, rd);
    if (hit.y > 0.0) {
        col = shade(ro + hit.x * rd, rd, hit.y);
    }
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
