// 02_first_sphere.frag
// 第 2 章: スフィアトレーシングで球を 1 つ描く (シルエットのみ)。

const int   MAX_STEPS = 100;    // 最大反復回数
const float MAX_DIST  = 100.0;  // これより遠くに進んだら当たらなかったとみなす
const float SURF_DIST = 0.001;  // これより近づいたら表面に当たったとみなす

// 原点を中心とする半径 r の球の SDF
float sdSphere(vec3 p, float r)
{
    return length(p) - r;
}

// シーン全体の SDF
float map(vec3 p)
{
    return sdSphere(p, 1.0);
}

// レイ ro + t * rd を進め、表面に当たった t を返す。当たらなければ -1.0
float raymarch(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = map(ro + t * rd);
        if (d < SURF_DIST) {
            return t;
        }
        t += d;  // 最も近い表面までの距離だけ安全に進める
        if (t > MAX_DIST) {
            break;
        }
    }
    return -1.0;
}

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 p = (2.0 * fragCoord - iResolution.xy) / iResolution.y;

    // カメラは z = 3 に置き、-z 方向を向く。1.5 は焦点距離
    vec3 ro = vec3(0.0, 0.0, 3.0);
    vec3 rd = normalize(vec3(p, -1.5));

    float t = raymarch(ro, rd);

    vec3 col = vec3(0.1);        // 背景
    if (t > 0.0) {
        col = vec3(1.0);         // 球に当たったピクセルは白
    }
    fragColor = vec4(col, 1.0);
}
