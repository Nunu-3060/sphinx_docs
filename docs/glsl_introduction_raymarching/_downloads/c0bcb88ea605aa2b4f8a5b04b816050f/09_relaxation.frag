// 09_relaxation.frag
// 第 9 章: 過緩和 (over-relaxation) によるスフィアトレーシングの高速化。
// 反復回数をヒートマップで表示する。左は通常の方法、右は過緩和。
// 青いほど少ない反復で、赤いほど多くの反復で結果が確定したことを表す。

const int   MAX_STEPS = 128;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;
const float OMEGA     = 1.2;     // 過緩和の係数 (1 以上 2 未満)

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

float sdTorus(vec3 p, vec2 t)
{
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

float map(vec3 p)
{
    float d = p.y;
    d = min(d, sdSphere(p - vec3(-1.6, 1.0, 0.0), 1.0));
    d = min(d, sdTorus(p - vec3(1.2, 0.3, 0.8), vec2(0.8, 0.3)));
    return d;
}

// 通常のスフィアトレーシング。反復回数を返す
int raymarchSteps(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        if (d < SURF_DIST || t > MAX_DIST) {
            return i;
        }
        t += d;
    }
    return MAX_STEPS;
}

// 過緩和を使うスフィアトレーシング (Keinert et al., 2014)。反復回数を返す
int relaxedRaymarchSteps(vec3 ro, vec3 rd)
{
    float omega = OMEGA;
    float t = 0.0;
    float previousD = 0.0;    // 前の点での SDF の値
    float stepLength = 0.0;   // 前の点から進んだ距離
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        // 前の点と今の点を中心とする 2 つの安全な球が重ならなければ、
        // その隙間で表面を通り越した可能性がある
        if (omega > 1.0 && stepLength > previousD + d) {
            t -= stepLength - previousD;   // 通常の歩幅で進んだ位置まで戻る
            stepLength = 0.0;
            omega = 1.0;                   // 以降は通常の方法で進む
            continue;
        }
        if (d < SURF_DIST || t > MAX_DIST) {
            return i;
        }
        stepLength = omega * d;
        previousD = d;
        t += stepLength;
    }
    return MAX_STEPS;
}

vec3 heatmap(float x)
{
    return clamp(vec3(2.0 * x - 0.5, 1.0 - abs(2.0 * x - 1.0), 1.5 - 2.0 * x),
                 0.0, 1.0);
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
    // 画面の左右に、同じ構図の画像を 1 つずつ並べる
    vec2 halfSize = vec2(0.5 * iResolution.x, iResolution.y);
    bool relaxed = fragCoord.x > halfSize.x;
    vec2 local = vec2(mod(fragCoord.x, halfSize.x), fragCoord.y);
    vec2 p = (2.0 * local - halfSize) / halfSize.y;

    vec3 ro = vec3(0.0, 3.5, 7.0);
    vec3 ta = vec3(0.0, 0.5, 0.0);
    vec3 rd = setCamera(ro, ta) * normalize(vec3(p, 1.5));

    int steps = relaxed ? relaxedRaymarchSteps(ro, rd) : raymarchSteps(ro, rd);
    vec3 col = heatmap(float(steps) / 64.0);

    col = mix(col, vec3(1.0), step(abs(fragCoord.x - 0.5 * iResolution.x), 1.0));
    fragColor = vec4(col, 1.0);
}
