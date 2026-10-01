// 11_reflection_refraction.frag
// 第 11 章: 反射と屈折。左の球は鏡面、右の球はガラス。
// GLSL は再帰呼び出しができないため、ループと「スループット」で光の経路を追跡する。

const int   MAX_STEPS   = 128;
const float MAX_DIST    = 100.0;
const float SURF_DIST   = 0.001;
const int   MAX_BOUNCES = 6;     // 反射・屈折を追跡する最大回数
const float IOR         = 1.5;   // ガラスの屈折率

const vec3 LIGHT_DIR = normalize(vec3(0.6, 0.7, 0.4));
const vec3 SUN_COLOR = vec3(1.3, 1.2, 1.0);
const vec3 SKY_COLOR = vec3(0.3, 0.4, 0.55);

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

const float MAT_GROUND = 1.0;
const float MAT_MIRROR = 2.0;
const float MAT_GLASS  = 3.0;
const float MAT_TORUS  = 4.0;
const float MAT_BOX    = 5.0;

vec2 opU(vec2 a, vec2 b)
{
    return (a.x < b.x) ? a : b;
}

// ガラスの物体だけの SDF (内部を進むときに使う)
float sdGlass(vec3 p)
{
    return sdSphere(p - vec3(1.2, 1.0, 0.5), 1.0);
}

vec2 map(vec3 p)
{
    vec2 res = vec2(sdPlane(p, 0.0), MAT_GROUND);
    res = opU(res, vec2(sdSphere(p - vec3(-1.2, 1.0, 0.0), 1.0), MAT_MIRROR));
    res = opU(res, vec2(sdGlass(p), MAT_GLASS));
    res = opU(res, vec2(sdTorus(p - vec3(0.3, 0.3, -2.2), vec2(0.8, 0.3)),
                        MAT_TORUS));
    res = opU(res, vec2(sdBox(p - vec3(2.8, 0.5, -1.5), vec3(0.5)), MAT_BOX));
    return res;
}

// ---- レイマーチング ------------------------------------------------------

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

// ガラスの内部をレイマーチングし、出口までの距離を返す。
// 内部では -sdGlass(p) が表面までの距離になる
float marchInside(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float h = -sdGlass(ro + t * rd);
        if (h < SURF_DIST) {
            break;
        }
        t += h;
    }
    return t;
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
    return res * res * (3.0 - 2.0 * res);
}

// ---- 照明 ----------------------------------------------------------------

vec3 skyColor(vec3 rd)
{
    vec3 col = mix(vec3(0.65, 0.75, 0.85), vec3(0.2, 0.35, 0.65),
                   sqrt(clamp(rd.y, 0.0, 1.0)));
    float sun = max(dot(rd, LIGHT_DIR), 0.0);
    col += SUN_COLOR * (pow(sun, 512.0) * 4.0 + pow(sun, 16.0) * 0.15);
    return col;
}

vec3 albedoOf(float mat, vec3 p)
{
    if (mat == MAT_GROUND) {
        float checker = mod(floor(p.x) + floor(p.z), 2.0);
        return mix(vec3(0.25), vec3(0.45), checker);
    }
    if (mat == MAT_TORUS) {
        return vec3(0.15, 0.45, 0.7);
    }
    return vec3(0.7, 0.6, 0.2);
}

// 拡散反射面の色 (第 5 章・第 6 章と同じ)
vec3 shadeDiffuse(vec3 p, vec3 n, vec3 rd, float mat)
{
    vec3 h = normalize(LIGHT_DIR - rd);
    float shadow = softShadow(p + n * 0.01, LIGHT_DIR, 0.01, 20.0, 8.0);
    float diffuse = max(dot(n, LIGHT_DIR), 0.0) * shadow;
    float specular = pow(max(dot(n, h), 0.0), 32.0) * diffuse;
    float sky = 0.5 + 0.5 * n.y;
    vec3 col = albedoOf(mat, p) * (SUN_COLOR * diffuse + SKY_COLOR * sky);
    return col + SUN_COLOR * specular * 0.3;
}

// Schlick の近似によるフレネル反射率。cosTheta は入射角の余弦
float fresnelSchlick(float cosTheta, float f0)
{
    return f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0);
}

// 反射・屈折を追跡してレイの色を求める
vec3 render(vec3 ro, vec3 rd)
{
    vec3 col = vec3(0.0);
    vec3 throughput = vec3(1.0);  // ここまでの経路で光が減衰する割合

    for (int bounce = 0; bounce < MAX_BOUNCES; bounce++) {
        vec2 hit = raymarch(ro, rd);
        if (hit.y < 0.0) {
            col += throughput * skyColor(rd);
            break;
        }
        vec3 p = ro + hit.x * rd;
        vec3 n = calcNormal(p);

        if (hit.y == MAT_MIRROR) {
            // 鏡面: 反射方向へ進み直す
            throughput *= vec3(0.9, 0.9, 0.95);
            ro = p + n * 0.01;
            rd = reflect(rd, n);
        } else if (hit.y == MAT_GLASS) {
            // 入射面で反射する割合 (フレネル項)
            float f0 = pow((IOR - 1.0) / (IOR + 1.0), 2.0);
            float f = fresnelSchlick(max(dot(-rd, n), 0.0), f0);
            // 反射成分は空の色で近似して加え、残りの (1 - f) で屈折を追跡する
            col += throughput * f * skyColor(reflect(rd, n));
            throughput *= 1.0 - f;

            // 空気からガラスへ屈折して内部を進む
            vec3 rdIn = refract(rd, n, 1.0 / IOR);
            vec3 pIn = p - n * 0.01;
            vec3 pOut = pIn + marchInside(pIn, rdIn) * rdIn;
            vec3 nOut = calcNormal(pOut);

            // ガラスから空気へ屈折して外に出る。全反射になる場合は反射方向で近似する
            vec3 rdOut = refract(rdIn, -nOut, IOR);
            if (dot(rdOut, rdOut) == 0.0) {
                rdOut = reflect(rdIn, -nOut);
            }
            throughput *= vec3(0.95, 0.98, 1.0);  // わずかに青みを付ける
            ro = pOut + nOut * 0.01;
            rd = rdOut;
        } else {
            // 拡散反射面: 直接光で色を決めて終了する
            col += throughput * shadeDiffuse(p, n, rd, hit.y);
            break;
        }
    }
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
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    float angle = 0.2 * iTime;
    vec3 ta = vec3(0.0, 0.8, 0.0);
    vec3 ro = ta + vec3(6.0 * sin(angle), 1.8, 6.0 * cos(angle));
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.0));

    vec3 col = render(ro, rd);
    col = pow(col, vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
