// 09_debug.frag
// 第 9 章: デバッグ用の可視化。DEBUG_MODE を書き換えて表示を切り替える。
//   0: 通常の描画    1: 法線    2: 反復回数    3: 距離 (深度)
//  -1: 画面を 4 分割し、左上から時計回りに 0, 1, 2, 3 を表示する

#define DEBUG_MODE -1

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
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

// 戻り値は (t, マテリアル ID, 反復回数)。当たらなければマテリアル ID は -1.0
vec3 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec2 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec3(t, h.y, float(i));
        }
        t += h.x;
        if (t > MAX_DIST) {
            return vec3(t, -1.0, float(i));
        }
    }
    return vec3(t, -1.0, float(MAX_STEPS));
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
    vec3 v = -rd;
    vec3 h = normalize(LIGHT_DIR + v);
    vec3 albedo = albedoOf(mat, p);

    float shadow = softShadow(p + n * 0.01, LIGHT_DIR, 0.01, 20.0, 8.0);
    float occ = calcAO(p, n);

    float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
    float specular = pow(max(dot(n, h), 0.0), 32.0) * diffuse;
    float sky = (0.5 + 0.5 * n.y) * occ;

    vec3 col = albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
    col += SUN_COLOR * specular * 0.5;
    return col;
}

// ---- デバッグ表示 --------------------------------------------------------

vec3 heatmap(float x)
{
    return clamp(vec3(2.0 * x - 0.5, 1.0 - abs(2.0 * x - 1.0), 1.5 - 2.0 * x),
                 0.0, 1.0);
}

// mode に応じた色を返す。戻り値はガンマ補正前の値なので、表示したい値は
// あらかじめ 2.2 乗しておく
vec3 debugColor(int mode, vec3 ro, vec3 rd)
{
    vec3 hit = raymarch(ro, rd);
    vec3 p = ro + hit.x * rd;
    bool isHit = hit.y > 0.0;

    if (mode == 1) {
        // 法線 [-1, 1] を色 [0, 1] に変換する
        return isHit ? pow(0.5 + 0.5 * calcNormal(p), vec3(2.2)) : vec3(0.0);
    }
    if (mode == 2) {
        return pow(heatmap(hit.z / float(MAX_STEPS)), vec3(2.2));
    }
    if (mode == 3) {
        // 近いほど白、遠いほど黒 (距離 20 で 0)
        float depth = isHit ? 1.0 - clamp(hit.x / 20.0, 0.0, 1.0) : 0.0;
        return vec3(pow(depth, 2.2));
    }
    return isHit ? shade(p, rd, hit.y) : SKY_COLOR;
}

// ---- メイン --------------------------------------------------------------

// カメラ位置 ro から注視点 ta を向くカメラ行列
mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;
    int mode = DEBUG_MODE;
    vec2 frag = fragCoord;
    if (mode < 0) {
        // 4 分割表示: 各領域を全画面と同じ構図で縮小表示する
        vec2 cell = floor(uv * 2.0);             // (0, 0) が左下
        int index = int(cell.x) + 2 * int(1.0 - cell.y);
        const int modes[4] = int[4](0, 1, 3, 2); // 左上, 右上, 左下, 右下
        mode = modes[index];
        frag = fract(uv * 2.0) * iResolution.xy;
    }

    vec2 p = (2.0 * frag - iResolution.xy) / iResolution.y;
    vec3 ro = vec3(0.0, 3.0, 6.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = debugColor(mode, ro, rd);
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
