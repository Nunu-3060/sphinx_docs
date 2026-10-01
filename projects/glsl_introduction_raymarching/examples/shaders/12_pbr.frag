// 12_pbr.frag
// 第 12 章: 物理ベースの材質。GGX による鏡面反射と、金属度・粗さによる材質の指定。
// 球の列は、上が金属 (金属度 1)、下が非金属 (金属度 0)。左から右へ粗さを大きくする。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;
const float PI        = 3.14159265;

const vec3 LIGHT_DIR      = normalize(vec3(0.5, 0.6, 0.6));
const vec3 SUN_IRRADIANCE = vec3(3.8, 3.5, 3.1);   // 平行光源の放射照度

// ---- シーン --------------------------------------------------------------

const float COLUMNS = 6.0;
const float SPACING = 1.1;

// 戻り値は (距離, 列の番号, 行の番号)。行: 0 が非金属、1 が金属。地面は行 -1
vec3 map(vec3 p)
{
    // 球を 6 列 × 2 行に並べる (第 4 章の有限回の繰り返し)
    float center = 0.5 * (COLUMNS - 1.0);
    float column = clamp(round(p.x / SPACING + center), 0.0, COLUMNS - 1.0);
    float row = clamp(round((p.y - 0.5) / SPACING), 0.0, 1.0);
    vec3 c = vec3((column - center) * SPACING, 0.5 + row * SPACING, 0.0);
    float sphere = length(p - c) - 0.45;
    float ground = p.y + 0.05;
    return (sphere < ground) ? vec3(sphere, column, row)
                             : vec3(ground, 0.0, -1.0);
}

vec3 raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        vec3 h = map(ro + t * rd);
        if (h.x < SURF_DIST) {
            return vec3(t, h.yz);
        }
        t += h.x;
        if (t > MAX_DIST) {
            break;
        }
    }
    return vec3(-1.0, 0.0, 0.0);
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

// ---- 環境 ----------------------------------------------------------------

vec3 skyColor(vec3 rd)
{
    vec3 col = mix(vec3(0.55, 0.6, 0.65), vec3(0.15, 0.3, 0.6),
                   sqrt(clamp(rd.y, 0.0, 1.0)));
    // 地平線より下は地面の色
    col = mix(vec3(0.3, 0.29, 0.27), col, smoothstep(-0.02, 0.02, rd.y));
    float sun = max(dot(rd, LIGHT_DIR), 0.0);
    return col + vec3(8.0, 7.5, 6.5) * pow(sun, 800.0);
}

// 粗さに応じてぼかした環境の色の近似。粗い表面ほど、多くの方向の平均に近づく
vec3 environment(vec3 dir, float roughness)
{
    vec3 average = vec3(0.3, 0.35, 0.4);
    vec3 sharp = skyColor(dir);
    return mix(sharp, average, roughness * roughness);
}

// ---- マイクロファセット BRDF ---------------------------------------------

// GGX の法線分布関数。alpha は粗さの 2 乗
float distributionGGX(float nh, float alpha)
{
    float a2 = alpha * alpha;
    float d = nh * nh * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}

// 幾何減衰項: Smith の方法を Schlick-GGX の式で近似したもの
float geometrySmith(float nv, float nl, float roughness)
{
    float k = (roughness + 1.0) * (roughness + 1.0) / 8.0;
    float gv = nv / (nv * (1.0 - k) + k);
    float gl = nl / (nl * (1.0 - k) + k);
    return gv * gl;
}

// Schlick の近似によるフレネル反射率 (第 11 章)。f0 は RGB ごとの値
vec3 fresnelSchlick(float cosTheta, vec3 f0)
{
    return f0 + (1.0 - f0) * pow(1.0 - cosTheta, 5.0);
}

// 材質 (色、金属度、粗さ) を持つ表面の色を求める
vec3 shadePBR(vec3 p, vec3 n, vec3 v, vec3 baseColor, float metallic,
              float roughness)
{
    vec3 l = LIGHT_DIR;
    vec3 h = normalize(l + v);
    float nl = max(dot(n, l), 0.0);
    float nv = max(dot(n, v), 1e-4);
    float nh = max(dot(n, h), 0.0);

    // 垂直入射での反射率: 非金属は 0.04、金属は色そのもの
    vec3 f0 = mix(vec3(0.04), baseColor, metallic);
    vec3 f = fresnelSchlick(max(dot(h, v), 0.0), f0);

    // 鏡面反射: Cook-Torrance のマイクロファセット BRDF
    float alpha = roughness * roughness;
    vec3 specular = distributionGGX(nh, alpha) *
                    geometrySmith(nv, nl, roughness) * f / (4.0 * nv * nl + 1e-4);
    // 拡散反射: 鏡面反射されなかった光のうち、非金属の部分だけが拡散反射する
    vec3 kd = (1.0 - f) * (1.0 - metallic);
    vec3 diffuse = kd * baseColor / PI;

    float shadow = softShadow(p + n * 0.01, l);
    vec3 direct = (diffuse + specular) * SUN_IRRADIANCE * nl * shadow;

    // 環境光: 拡散反射は法線方向、鏡面反射は反射方向の環境の色で近似する
    vec3 fAmbient = fresnelSchlick(nv, f0);
    vec3 ambientDiffuse = (1.0 - fAmbient) * (1.0 - metallic) * baseColor *
                          environment(n, 1.0);
    vec3 ambientSpecular = fAmbient * environment(reflect(-v, n), roughness);
    return direct + ambientDiffuse + ambientSpecular;
}

// ---- メイン --------------------------------------------------------------

mat3 setCamera(vec3 ro, vec3 ta)
{
    vec3 cw = normalize(ta - ro);
    vec3 cu = normalize(cross(cw, vec3(0.0, 1.0, 0.0)));
    vec3 cv = cross(cu, cw);
    return mat3(cu, cv, cw);
}

vec3 toneMapACES(vec3 x)
{
    x *= 0.6;
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14),
                 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    vec3 ro = vec3(0.0, 1.6, 6.5);
    vec3 ta = vec3(0.0, 1.0, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 2.2));

    vec3 col = skyColor(rd);
    vec3 hit = raymarch(ro, rd);
    if (hit.x > 0.0) {
        vec3 pos = ro + hit.x * rd;
        vec3 n = calcNormal(pos);
        vec3 v = -rd;
        if (hit.z < 0.0) {
            // 地面: 粗い非金属
            col = shadePBR(pos, n, v, vec3(0.3), 0.0, 0.9);
        } else {
            float roughness = mix(0.05, 1.0, hit.y / (COLUMNS - 1.0));
            float metallic = hit.z;
            vec3 baseColor = (metallic > 0.5) ? vec3(1.0, 0.78, 0.34)  // 金
                                              : vec3(0.7, 0.1, 0.08);  // 赤
            col = shadePBR(pos, n, v, baseColor, metallic, roughness);
        }
    }
    col = pow(toneMapACES(col), vec3(1.0 / 2.2));
    fragColor = vec4(col, 1.0);
}
