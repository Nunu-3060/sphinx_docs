// 02_step_count.frag
// 第 2 章: レイマーチングの反復回数を色で可視化する。
// 青いほど少ない反復で、赤いほど多くの反復で結果が確定したことを表す。

const int   MAX_STEPS = 100;
const float MAX_DIST  = 100.0;
const float SURF_DIST = 0.001;

float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

// y = h の水平な平面
float sdPlane(vec3 p, float h)
{
    return p.y - h;
}

float map(vec3 p)
{
    return min(sdSphere(p, 1.0), sdPlane(p, -1.0));
}

// 反復回数を返す
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

// 0〜1 の値を青 → 緑 → 赤の色に変換する
vec3 heatmap(float x)
{
    return clamp(vec3(2.0 * x - 0.5, 1.0 - abs(2.0 * x - 1.0), 1.5 - 2.0 * x),
                 0.0, 1.0);
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    vec3 ro = vec3(0.0, 0.0, 3.0);
    vec3 rd = normalize(vec3(p, -1.5));

    int steps = raymarchSteps(ro, rd);
    vec3 col = heatmap(float(steps) / float(MAX_STEPS));

    fragColor = vec4(col, 1.0);
}
