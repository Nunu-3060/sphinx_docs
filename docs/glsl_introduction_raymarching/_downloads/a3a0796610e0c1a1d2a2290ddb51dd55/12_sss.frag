// 12_sss.frag
// 第 12 章: サブサーフェススキャッタリングの近似。翡翠のような半透明の物体を
// 後ろから照らす。左は通常の拡散反射だけ、右はラップライティングと透過光を加えたもの。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;

// 光源は物体の奥 (カメラから見て向こう側) の斜め上にある
const vec3 LIGHT_DIR = normalize(vec3(-0.4, 0.5, -1.0));
const vec3 SUN_COLOR = vec3(1.6, 1.45, 1.25);
const vec3 SKY_COLOR = vec3(0.25, 0.3, 0.4);

// 物体の中での光の減衰の強さ (消散係数、RGB ごと)。赤ほど減衰しやすい
const vec3 SIGMA_T = vec3(3.0, 1.2, 1.6);
const float WRAP   = 0.4;    // ラップライティングの回り込みの量

// ---- シーン --------------------------------------------------------------

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

// 楕円体の SDF の近似 (距離の下界)
float sdEllipsoid(vec3 p, vec3 r)
{
    float k0 = length(p / r);
    float k1 = length(p / (r * r));
    return k0 * (k0 - 1.0) / k1;
}

float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

// 半透明の物体だけの SDF。左から、厚い球、薄い葉、中くらいの太さの輪
float sdObjects(vec3 p)
{
    float d = sdSphere(p - vec3(-1.7, 0.9, 0.0), 0.9);
    d = min(d, sdEllipsoid(p - vec3(0.0, 1.0, 0.0), vec3(0.7, 1.0, 0.08)));
    vec3 q = p - vec3(1.7, 0.9, 0.0);
    d = min(d, sdTorus(q.xzy, vec2(0.65, 0.22)));   // 立てた輪
    return d;
}

// 戻り値は (距離, マテリアル ID)。0: 地面、1: 半透明の物体
vec2 map(vec3 p)
{
    float objects = sdObjects(p);
    return (p.y < objects) ? vec2(p.y, 0.0) : vec2(objects, 1.0);
}

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

vec3 calcNormal(vec3 p)
{
    const float h = 0.0005;
    const vec2 k = vec2(1.0, -1.0);
    return normalize(k.xyy * map(p + k.xyy * h).x +
                     k.yyx * map(p + k.yyx * h).x +
                     k.yxy * map(p + k.yxy * h).x +
                     k.xxx * map(p + k.xxx * h).x);
}

float softShadow(vec3 ro, vec3 rd)
{
    float res = 1.0;
    float t = 0.01;
    for (int i = 0; i < 64 && t < 20.0; i++) {
        float h = map(ro + t * rd).x;
        res = min(res, 8.0 * h / t);
        if (res < 0.001) {
            break;
        }
        t += clamp(h, 0.01, 0.5);
    }
    return clamp(res, 0.0, 1.0);
}

// ---- サブサーフェススキャッタリング --------------------------------------

// 物体の内部を光源の方向に進み、出口までの距離 (光が物体の中を通る長さ) を返す。
// 内部では -sdObjects(p) が表面までの距離になる (第 11 章)
float thicknessToLight(vec3 p, vec3 n)
{
    vec3 ro = p - n * 0.01;
    float t = 0.0;
    for (int i = 0; i < 64; i++) {
        float h = -sdObjects(ro + t * LIGHT_DIR);
        if (h < SURF_DIST || t > 4.0) {
            break;
        }
        t += max(h, 0.01);
    }
    return t;
}

vec3 shade(vec3 p, vec3 rd, float mat, bool sss)
{
    vec3 n = calcNormal(p);
    vec3 v = -rd;
    vec3 albedo = (mat > 0.5) ? vec3(0.35, 0.75, 0.5) : vec3(0.3);
    float shadow = softShadow(p + n * 0.01, LIGHT_DIR);
    float nl = dot(n, LIGHT_DIR);
    float sky = 0.5 + 0.5 * n.y;

    if (!sss || mat < 0.5) {
        // 通常の拡散反射 (第 5 章)
        float diffuse = max(nl, 0.0) * shadow;
        return albedo * (SUN_COLOR * diffuse + SKY_COLOR * sky);
    }

    // ラップライティング: 光の当たる範囲を裏側に少し回り込ませる
    float wrapped = max((nl + WRAP) / (1.0 + WRAP), 0.0);
    vec3 col = albedo * (SUN_COLOR * wrapped * mix(1.0, shadow, 0.5) +
                         SKY_COLOR * sky);

    // 透過光: 物体の中を光源まで通る長さで減衰させる (ランベルト・ベールの法則)
    vec3 transmittance = exp(-SIGMA_T * thicknessToLight(p, n));
    // 光源を正面から見る方向ほど強く見える (前方散乱)
    float forward = 0.3 + 0.7 * pow(max(dot(v, -LIGHT_DIR), 0.0), 4.0);
    col += albedo * SUN_COLOR * transmittance * forward;
    return col;
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
    // 画面の左右に、同じ構図の画像を 1 つずつ並べる
    vec2 halfSize = vec2(0.5 * iResolution.x, iResolution.y);
    bool sss = fragCoord.x > halfSize.x;
    vec2 local = vec2(mod(fragCoord.x, halfSize.x), fragCoord.y);
    vec2 p = (2.0 * local - halfSize) / halfSize.y;

    vec3 ro = vec3(0.0, 1.6, 6.5);
    vec3 ta = vec3(0.0, 0.8, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.3));

    vec3 col = SKY_COLOR;
    vec2 hit = raymarch(ro, rd);
    if (hit.y >= 0.0) {
        col = shade(ro + hit.x * rd, rd, hit.y, sss);
    }
    col = pow(col, vec3(1.0 / 2.2));
    col = mix(col, vec3(1.0), step(abs(fragCoord.x - halfSize.x), 1.0));
    fragColor = vec4(col, 1.0);
}
