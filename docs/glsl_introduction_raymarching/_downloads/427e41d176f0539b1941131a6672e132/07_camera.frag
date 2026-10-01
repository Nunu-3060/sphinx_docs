// 07_camera.frag
// 第 7 章: 周回するカメラとマウス操作、空の描画、フォグ、トーンマッピング、
// スーパーサンプリングによるアンチエイリアス。

#define AA 2  // 1 ピクセルあたり AA x AA 本のレイを飛ばす (1 で無効)

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

// ---- 背景とフォグ --------------------------------------------------------

// レイの方向に応じた空の色。地平線は明るく、天頂は濃い青にし、太陽を描く
vec3 skyColor(vec3 rd)
{
    vec3 horizon = vec3(0.65, 0.75, 0.85);
    vec3 zenith = vec3(0.2, 0.35, 0.65);
    vec3 col = mix(horizon, zenith, sqrt(clamp(rd.y, 0.0, 1.0)));
    float sun = max(dot(rd, LIGHT_DIR), 0.0);
    col += SUN_COLOR * (pow(sun, 512.0) * 4.0 + pow(sun, 16.0) * 0.15);
    return col;
}

// 距離 t に応じて色 col を空の色に近づける (指数フォグ)
vec3 applyFog(vec3 col, vec3 rd, float t)
{
    const float density = 0.015;
    float fog = 1.0 - exp(-density * t);
    return mix(col, skyColor(vec3(rd.x, 0.0, rd.z)), fog);
}

// ---- トーンマッピング ----------------------------------------------------

// ACES Filmic の近似式 (Narkowicz, 2015)。0〜∞ の値を 0〜1 に収める
vec3 toneMapACES(vec3 x)
{
    x *= 0.6;  // 露出の調整 (元の近似式の係数)
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
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

// ---- メイン --------------------------------------------------------------

// カメラ位置 ro から注視点 ta を向くカメラ行列
mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

// 1 本のレイの色を求める (トーンマッピング前の線形な値)
vec3 render(vec3 ro, vec3 rd)
{
    vec2 hit = raymarch(ro, rd);
    if (hit.y < 0.0) {
        return skyColor(rd);
    }
    vec3 col = shade(ro + hit.x * rd, rd, hit.y);
    return applyFog(col, rd, hit.x);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    // カメラは注視点のまわりを周回する。マウスでドラッグすると視点を操作できる
    float angle = 0.3 * iTime;
    float height = 2.5;
    if (iMouse.z > 0.0) {
        angle = 6.2832 * iMouse.x / iResolution.x;
        height = 0.5 + 6.0 * iMouse.y / iResolution.y;
    }
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 ro = ta + vec3(6.0 * sin(angle), height, 6.0 * cos(angle));
    mat3 cam = setCamera(ro, ta);

    // AA x AA 個のサブピクセルで色を求めて平均する (スーパーサンプリング)
    vec3 col = vec3(0.0);
    for (int m = 0; m < AA; m++) {
        for (int n = 0; n < AA; n++) {
            vec2 offset = (vec2(m, n) + 0.5) / float(AA) - 0.5;
            vec2 p = (2.0 * (fragCoord + offset) - iResolution.xy) /
                     iResolution.y;
            vec3 rd = cam * normalize(vec3(p, 2.0));
            col += toneMapACES(render(ro, rd));
        }
    }
    col /= float(AA * AA);

    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
